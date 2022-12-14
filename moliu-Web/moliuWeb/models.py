from django.db import models
from django.conf import settings


class Patient(models.Model):
    name = models.CharField(max_length=30)
    surnames = models.CharField(max_length=70, null=True)
    nickname = models.CharField(max_length=30, null=True, unique=True)

    def __str__(self) -> str:
        return self.name + " " + self.surnames if self.surnames else self.name


def getSentinelPatient():
    return Patient.objects.filter(name="paciente0")


class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    background = models.CharField(max_length=255, null=True, blank=False)
    music = models.CharField(max_length=255, null=True, blank=True)
    points = models.JSONField(null=True, blank=False)

    def __str__(self) -> str:
        return self.name


def getSentinelActivity():
    return Activity.objects.filter(name="actividad0")


class Model(models.Model):
    name = models.CharField(max_length=255, default="Un modelo", unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    learningTechnique = models.CharField(max_length=255)
    filename = models.FileField(upload_to="models/")

    def __str__(self) -> str:
        return str(self.filename)


def videoUploadPath(instance, filename):
    return "games/" + instance.directoryName + "/" + instance.directoryName + ".avi"


def jointsUploadPath(instance, filename):
    return "games/" + instance.directoryName + "/" + instance.directoryName + ".txt"


class Game(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.SET(getSentinelActivity))
    patient = models.ForeignKey(Patient, on_delete=models.SET(getSentinelPatient))
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to=videoUploadPath)
    joints = models.FileField(upload_to=jointsUploadPath)

    @property
    def directoryName(self):
        return self.date.strftime(settings.DATETIME_FORMAT)

    def __str__(self) -> str:
        activity = self.activity.__str__()
        patient = self.patient.__str__()
        date = self.date.strftime("%Y/%m/%d - %H:%M:%S")
        return activity + " - " + patient + " - " + date


class Posture(models.Model):
    class Scores(models.IntegerChoices):
        VERY_BAD = 0
        BAD = 25
        REGULAR = 50
        GOOD = 75
        VERY_GOOD = 100

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(choices=Scores.choices, default=None, null=True, blank=True)
    isScored = models.BooleanField(default=False)
    image = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.image + " - " + self.score.__str__()
