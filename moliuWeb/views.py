from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from .models import Posture, Patient, Activity, Game, Model
from .forms import ImportGame, ClassifyPosture, LoginForm
from .utils import importGame, addScoredPosturesToDataFile, createDataFile
import random


class LoginView(auth_views.LoginView):
    template_name = "moliuWeb/login.html"
    form_class = LoginForm


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = "moliuWeb:login"


@login_required
def index(request):
    return render(request, "moliuWeb/index.html")


class PatientsView(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = "moliuWeb/patients.html"

    def get_context_data(self):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        qs = Patient.objects.all().exclude(name="paciente0")
        return qs


class PatientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Patient
    fields = ["name", "surnames", "nickname"]
    template_name = "moliuWeb/addPatient.html"
    success_url = reverse_lazy("moliuWeb:patients")


class PatientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Patient
    fields = ["name", "surnames", "nickname"]
    template_name = "moliuWeb/updatePatient.html"
    success_url = reverse_lazy("moliuWeb:patients")


class PatientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Patient
    template_name = "moliuWeb/deletePatient.html"
    success_url = reverse_lazy("moliuWeb:patients")


class ActivitiesView(LoginRequiredMixin, generic.ListView):
    model = Activity
    template_name = "moliuWeb/activities.html"

    def get_context_data(self):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        qs = Activity.objects.all().exclude(name="actividad0")
        return qs


class GamesView(LoginRequiredMixin, generic.ListView):
    model = Game
    importGameForm = ImportGame
    template_name = "moliuWeb/games.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["form"] = self.importGameForm()
        return context


class GameImportView(LoginRequiredMixin, generic.base.TemplateView):
    template_name: str = "moliuWeb/importGame.html"
    importGameForm = ImportGame

    def get_context_data(self):
        context = super().get_context_data()
        context["form"] = self.importGameForm()
        return context

    def post(self, request):
        importGameForm = self.importGameForm(request.POST, request.FILES)

        if importGameForm.is_valid():
            video = importGameForm.cleaned_data["video"]
            joints = importGameForm.cleaned_data["joints"]
            importGame(video, joints)
            return HttpResponseRedirect(reverse("moliuWeb:games"))
        else:
            context = {"form": importGameForm}
            return render(request, self.template_name, context=context)


@login_required
def exportGameData(request, gameId):
    game = Game.objects.get(pk=gameId)

    if not Posture.objects.filter(game=game, isScored=True):
        messages.info(request, "Debe clasificar al menos una postura antes de exportar datos")
        return redirect("moliuWeb:games")

    dataFile = createDataFile(game)
    addScoredPosturesToDataFile(game, dataFile)

    messages.success(request, "Datos exportados correctamente y guardados en el servidor")

    return redirect("moliuWeb:games")


class GameDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Game
    template_name = "moliuWeb/deleteGame.html"
    success_url = reverse_lazy("moliuWeb:games")


class ClassifyPostures(LoginRequiredMixin, View):
    def get(self, request, gameId):
        game = get_object_or_404(Game, pk=gameId)
        postures = Posture.objects.filter(game=game, isScored=False)

        if not postures:
            messages.info(
                request, "Todas las posturas de la partida seleccionada han sido ya puntuadas"
            )
            return redirect("moliuWeb:games")

        posture = random.choice(postures)
        classifyPostureForm = ClassifyPosture

        return render(
            request,
            "moliuWeb/classifyPostures.html",
            {"posture": posture, "form": classifyPostureForm(instance=posture)},
        )

    def post(self, request, gameId):
        posture = Posture.objects.get(image=request.POST["image"])
        classifyPostureForm = ClassifyPosture(request.POST, instance=posture)

        if classifyPostureForm.is_valid():
            classifyPostureForm.save()
        else:
            print(classifyPostureForm.errors)

        return HttpResponseRedirect(
            reverse("moliuWeb:classifyPostures", kwargs={"gameId": gameId}),
        )


class ModelsView(LoginRequiredMixin, generic.ListView):
    model = Model
    template_name = "moliuWeb/models.html"

    def get_queryset(self):
        pass
