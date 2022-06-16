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
                    splittedLine = line.split(" ")
                    lineWithoutFrame = ",".join(splittedLine[1:])
                    trainingFile.write(lineWithoutFrame)
