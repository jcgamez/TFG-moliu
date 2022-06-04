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

    if os.name == "nt":
        gameName = game.video.path.split("\\")[-2]
    elif os.name == "posix":
        gameName = game.video.path.split("/")[-2]

    for frame in sorted(os.listdir(framesDir)):
        frameImage = "games/" + gameName + "/frames/" + frame
        p = Posture(game=game, image=frameImage)
        p.save()


def createDataFile(game):
    gameDate = game.date.strftime("%Y_%m_%d--%H_%M_%S")
    exportedDataDir = os.path.join(settings.MEDIA_ROOT, "games", gameDate, "exportedData")

    filename = datetime.datetime.now().strftime("%Y_%m_%d--%H_%M_%S") + ".txt"
    dataFile = os.path.join(exportedDataDir, filename)

    os.system(f"mkdir -p {exportedDataDir} && cp {game.joints.path} {dataFile}")

    return dataFile


def addScoredPosturesToDataFile(game, dataFile):
    postures = Posture.objects.filter(game=game, isScored=True)
    scoredPostures = {}

    for posture in postures:
        frameNumber = int(posture.image.split("/")[-1].split(".")[0])
        scoredPostures[frameNumber] = posture.score

    with open(dataFile, "r+") as f:
        frames = f.readlines()
        f.seek(0)
        f.write(frames[0].strip() + "; 26 --> [Class]\n")
        for frame in range(1, len(frames)):
            if frame - 1 in scoredPostures.keys():
                f.write(frames[frame].strip() + f" {scoredPostures[frame-1]}\n")
        f.truncate()
