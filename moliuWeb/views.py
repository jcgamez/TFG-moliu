from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Patient, Activity, Game, Model
from .forms import ImportGame
from .utils import importGame


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


class ModelsView(generic.ListView):
    model = Model
    template_name = "moliuWeb/models.html"

    def get_queryset(self):
        pass
