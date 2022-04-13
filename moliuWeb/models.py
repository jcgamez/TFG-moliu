from django.db import models
import shortuuid


class Patient(models.Model):
    name = models.CharField(max_length=30)
    surnames = models.CharField(max_length=70, null=True)
    nickname = models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return self.name + " " + self.surnames if self.surnames else self.name


def getSentinelPatient():
    return Patient.objects.filter(name="paciente0")


class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


def getSentinelActivity():
    return Activity.objects.filter(name="actividad0")


class Model(models.Model):
    filename = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    learningTechnique = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.filename


def videoUploadPath(instance, filename):
    videoUuid = shortuuid.uuid()
    return "gamesVideos/" + videoUuid + "/" + videoUuid + ".avi"


class Game(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.SET(getSentinelActivity))
    patient = models.ForeignKey(Patient, on_delete=models.SET(getSentinelPatient))
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to=videoUploadPath)

    def __str__(self) -> str:
        activity = self.activity.__str__()
        patient = self.patient.__str__()
        date = self.date.__str__()
        return activity + "-" + patient + "-" + date


class Frame(models.Model):
    class Scores(models.IntegerChoices):
        NON_SCORED = -1
        VERY_BAD = 0
        BAD = 25
        REGULAR = 50
        GOOD = 75
        VERY_GOOD = 100

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(choices=Scores.choices, default=Scores.NON_SCORED)
    frameImage = models.CharField(max_length=250)
