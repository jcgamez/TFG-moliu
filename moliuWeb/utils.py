from math import sqrt, acos, degrees
from django.conf import settings
from .models import Patient, Activity, Game, Posture
import os
import ffmpeg
import datetime


def importGame(gameVideo, jointsFile) -> None:
    activity0 = Activity.objects.get(name="actividad0")
    patient0 = Patient.objects.get(name="paciente0")
    game = Game(activity=activity0, patient=patient0, video=gameVideo, joints=jointsFile)
    game.save()
    extractFramesFromVideo(game)
    createPostures(game)


def extractFramesFromVideo(game: Game) -> None:
    try:
        videoInfo = ffmpeg.probe(game.video.path)
    except ffmpeg.Error as e:
        print("stdout:", e.stdout.decode("utf8"))
        print("stderr:", e.stderr.decode("utf8"))
        raise e

    frameRate = [int(value) for value in videoInfo["streams"][0]["avg_frame_rate"].split("/")]
    framesPerSecond = round(frameRate[0] / frameRate[1])
    framesDir = os.path.join(os.path.dirname(game.video.path), "frames")
    os.mkdir(framesDir)

    try:
        (
            ffmpeg.input(game.video.path)
            .filter("fps", fps=framesPerSecond)
            .output(f"{framesDir}/%04d.png", start_number=0)
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
    except ffmpeg.Error as e:
        print("stdout:", e.stdout.decode("utf8"))
        print("stderr:", e.stderr.decode("utf8"))
        raise e


def createPostures(game: Game):
    framesDir = os.path.join(os.path.dirname(game.video.path), "frames")

    for frame in sorted(os.listdir(framesDir)):
        frameImage = "games/" + game.directoryName + "/frames/" + frame
        p = Posture(game=game, image=frameImage)
        p.save()


def createDataFile(game):
    exportedDataDir = os.path.join(settings.MEDIA_ROOT, "games", game.directoryName, "exportedData")
    now = datetime.datetime.now().strftime(settings.DATETIME_FORMAT) + ".txt"
    dataFile = os.path.join(exportedDataDir, now)

    os.system(f"mkdir -p {exportedDataDir} && cp {game.joints.path} {dataFile}")

    return dataFile


def addScoredPosturesToDataFile(game, dataFile):
    postures = Posture.objects.filter(game=game, isScored=True)
    scoredPostures = {}

    for posture in postures:
        frameNumber = int(posture.image.split("/")[-1].split(".")[0])
        scoredPostures[frameNumber] = posture.score

        if posture.score is None:
            scoredPostures[frameNumber] = -1

    with open(dataFile, "r+") as dataFileWithScores:
        frames = dataFileWithScores.readlines()
        dataFileWithScores.seek(0)
        dataFileWithScores.write(frames[0].strip() + "; 26 --> [Class]\n")
        for frame in range(1, len(frames)):
            if frame - 1 in scoredPostures.keys():
                dataFileWithScores.write(frames[frame].strip() + f" {scoredPostures[frame-1]}\n")
        dataFileWithScores.truncate()


def createTrainingFile(dataFiles):
    trainingDataDir = os.path.join(settings.MEDIA_ROOT, "datasets")
    os.system(f"mkdir -p {trainingDataDir}")
    now = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
    filename = os.path.join(settings.MEDIA_ROOT, "datasets", now) + ".arff"

    bodyParts = [
        "SpineBase",
        "SpineMid",
        "Neck",
        "Head",
        "ShoulderLeft",
        "ElbowLeft",
        "WristLeft",
        "HandLeft",
        "ShoulderRight",
        "ElbowRight",
        "WristRight",
        "HandRight",
        "HipLeft",
        "KneeLeft",
        "AnkleLeft",
        "FootLeft",
        "HipRight",
        "KneeRight",
        "AnkleRight",
        "FootRight",
        "SpineShoulder",
        "HandTipLeft",
        "ThumbLeft",
        "HandTipRight",
        "ThumbRight",
    ]

    with open(filename, "w+") as trainingFile:
        trainingFile.write("@relation posturasClasificadas--" + now + "\n\n")

        for bodyPart in bodyParts:
            trainingFile.write("@attribute " + bodyPart + "X real\n")
            trainingFile.write("@attribute " + bodyPart + "Y real\n")
            trainingFile.write("@attribute " + bodyPart + "Z real\n\n")

        for part1 in bodyParts:
            if part1 == "SpineBase":
                continue

            for part2 in bodyParts:
                if part2 in [part1, "SpineBase"]:
                    continue

                trainingFile.write("@attribute Angle[" + part1 + "-" + part2 + "]XY real\n")
                trainingFile.write("@attribute Angle[" + part1 + "-" + part2 + "]XZ real\n")
                trainingFile.write("@attribute Angle[" + part1 + "-" + part2 + "]YZ real\n\n")

        trainingFile.write("@attribute class real\n\n")
        trainingFile.write("@data\n")

        for game, dataFilename in dataFiles.items():
            if dataFilename == "No usar":
                continue

            dataFilePath = os.path.join(
                settings.MEDIA_ROOT, "games", game, "exportedData", dataFilename
            )
            with open(dataFilePath, "r") as dataFile:
                for line in dataFile.readlines()[1:]:
                    attributes = line.split(" ")
                    angles = obtainAngles(bodyParts, attributes[1:])
                    addAnglesToAttributes(attributes, angles)
                    attributesWithoutFrame = ",".join(attributes[1:])
                    trainingFile.write(attributesWithoutFrame)


def obtainAngles(bodyParts, coordinatesInSpace):
    joints = {}
    angles = {}
    i = 0

    for bodyPart in bodyParts:
        joints[bodyPart] = {
            "X": float(coordinatesInSpace[i]),
            "Y": float(coordinatesInSpace[i + 1]),
            "Z": float(coordinatesInSpace[i + 2]),
        }
        i += 3

    for part1 in bodyParts:
        if part1 == "SpineBase":
            continue

        for part2 in bodyParts:
            if part2 in [part1, "SpineBase"]:
                continue

            anglesByPlane = getAnglesByPlane(joints[part1], joints[part2], joints["SpineBase"])
            angles[part1 + "-" + part2] = anglesByPlane

    return angles


def getAnglesByPlane(part1, part2, spineBase):
    anglesByPlane = {
        "XY": 0,
        "XZ": 0,
        "YZ": 0,
    }

    # XY Plane
    sideA = sqrt((part1["X"] - part2["X"]) ** 2 + (part1["Y"] - part2["Y"]) ** 2)
    sideB = sqrt((part1["X"] - spineBase["X"]) ** 2 + (part1["Y"] - spineBase["Y"]) ** 2)
    sideC = sqrt((part2["X"] - spineBase["X"]) ** 2 + (part2["Y"] - spineBase["Y"]) ** 2)

    if sideA != 0 and sideB != 0 and sideC != 0:
        cosine = -(sideA**2 - sideB**2 - sideC**2) / (2 * sideB * sideC)
        angleXY = degrees(acos(round(cosine, 12)))
        anglesByPlane["XY"] = round(angleXY, 4)

    # XZ Plane
    sideA = sqrt((part1["X"] - part2["X"]) ** 2 + (part1["Z"] - part2["Z"]) ** 2)
    sideB = sqrt((part1["X"] - spineBase["X"]) ** 2 + (part1["Z"] - spineBase["Z"]) ** 2)
    sideC = sqrt((part2["X"] - spineBase["X"]) ** 2 + (part2["Z"] - spineBase["Z"]) ** 2)

    if sideA != 0 and sideB != 0 and sideC != 0:
        cosine = -(sideA**2 - sideB**2 - sideC**2) / (2 * sideB * sideC)
        angleXZ = degrees(acos(round(cosine, 12)))
        anglesByPlane["XZ"] = round(angleXZ, 4)

    # YZ Plane
    sideA = sqrt((part1["Y"] - part2["Y"]) ** 2 + (part1["Z"] - part2["Z"]) ** 2)
    sideB = sqrt((part1["Y"] - spineBase["Y"]) ** 2 + (part1["Z"] - spineBase["Z"]) ** 2)
    sideC = sqrt((part2["Y"] - spineBase["Y"]) ** 2 + (part2["Z"] - spineBase["Z"]) ** 2)

    if sideA != 0 and sideB != 0 and sideC != 0:
        cosine = -(sideA**2 - sideB**2 - sideC**2) / (2 * sideB * sideC)
        angleYZ = degrees(acos(round(cosine, 12)))
        anglesByPlane["YZ"] = round(angleYZ, 4)

    return anglesByPlane


def addAnglesToAttributes(attributes, angles):
    classValue = attributes[-1]
    del attributes[-1]

    for anglesByPart in angles.values():
        attributes.append(str(anglesByPart["XY"]))
        attributes.append(str(anglesByPart["XZ"]))
        attributes.append(str(anglesByPart["YZ"]))

    attributes.append(classValue)
