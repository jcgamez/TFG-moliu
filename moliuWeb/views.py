from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Patient, Activity, Game, Model
from .forms import UploadGame


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
    template_name = "moliuWeb/games.html"
    form = UploadGame

    def get_context_data(self):
        form = self.form()
        context = super().get_context_data()
        context["form"] = form
        return context

    def post(self, request):
        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            video = form.cleaned_data["video"]
            activity0 = Activity.objects.get(name="actividad0")
            patient0 = Patient.objects.get(name="paciente0")
            game = Game(activity=activity0, patient=patient0, video=video)
            game.save()
            return HttpResponseRedirect(reverse("moliuWeb:games"))

        return render(request, self.template_name, {"form": form})


class ModelsView(generic.ListView):
    model = Model
    template_name = "moliuWeb/models.html"

    def get_queryset(self):
        pass
