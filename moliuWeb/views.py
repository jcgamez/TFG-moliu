from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Posture, Patient, Activity, Game, Model
from .forms import ImportGame, ClassifyPosture
from .utils import importGame
import random


def index(request):
    return render(request, "moliuWeb/index.html")


class PatientsView(generic.ListView):
    model = Patient
    template_name = "moliuWeb/patients.html"

    def get_queryset(self):
        pass


class ActivitiesView(generic.ListView):
    model = Activity
    template_name = "moliuWeb/activities.html"

    def get_queryset(self):
        pass


class GamesView(generic.ListView):
    model = Game
    importGameForm = ImportGame
    template_name = "moliuWeb/games.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["form"] = self.importGameForm()
        return context

    def post(self, request):
        importGameForm = self.importGameForm(request.POST, request.FILES)

        if importGameForm.is_valid():
            video = importGameForm.cleaned_data["video"]
            importGame(video)
            return HttpResponseRedirect(reverse("moliuWeb:games"))

        return render(request, self.template_name, {"form": importGameForm})


def classifyPostures(request, gameId):
    game = get_object_or_404(Game, pk=gameId)

    if request.method == "GET":
        postures = Posture.objects.filter(game=game, score=Posture.Scores.NON_SCORED)
        posture = random.choice(postures)
        classifyPostureForm = ClassifyPosture
        return render(
            request,
            "moliuWeb/classifyPostures.html",
            {"posture": posture, "form": classifyPostureForm(instance=posture)},
        )

    if request.method == "POST":
        posture = Posture.objects.get(image=request.POST["image"])
        classifyPostureForm = ClassifyPosture(request.POST, instance=posture)

        if classifyPostureForm.is_valid():
            classifyPostureForm.save()
        else:
            print(classifyPostureForm.errors)

        return HttpResponseRedirect(
            reverse("moliuWeb:classifyPostures", kwargs={"gameId": gameId}),
        )


class ModelsView(generic.ListView):
    model = Model
    template_name = "moliuWeb/models.html"

    def get_queryset(self):
        pass
