from .models import Patient, Activity, Game, Frame
import os
import ffmpeg


def importGame(gameVideo) -> None:
    activity0 = Activity.objects.get(name="actividad0")
    patient0 = Patient.objects.get(name="paciente0")
    game = Game(activity=activity0, patient=patient0, video=gameVideo)
    game.save()
    extractFramesFromVideo(game)
    createFrames(game)


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


def createFrames(game: Game):
    framesDir = os.path.join(os.path.dirname(game.video.path), "frames")
    gameName = game.video.path.split("\\")[-2]

    for frame in os.listdir(framesDir):
        frameImage = "gamesVideos/" + gameName + "/frames/" + frame
        f = Frame(game=game, frameImage=frameImage)
        f.save()
