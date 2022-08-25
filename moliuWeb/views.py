from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.core.files import File
from django.conf import settings
from pathlib import Path
from .models import Posture, Patient, Activity, Game, Model
from .forms import ImportGame, ClassifyPosture, LoginForm, CreateTrainingSet, AddActivity
from .utils import importGame, addScoredPosturesToDataFile, createDataFile, createTrainingFile
import random
import os


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

    def get_queryset(self):
        qs = Activity.objects.all().exclude(name="actividad0")
        return qs


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    model = Activity
    template_name = "moliuWeb/addActivity.html"
    form_class = AddActivity
    success_url = reverse_lazy("moliuWeb:activities")

    def get_context_data(self):
        context = super().get_context_data()
        backgroundDir = os.path.join(settings.BASE_DIR, "media/activities/backgrounds")
        shapeDir = os.path.join(settings.BASE_DIR, "media/activities/shapes")
        musicDir = os.path.join(settings.BASE_DIR, "media/activities/music")

        os.system(f"mkdir -p {backgroundDir}")
        os.system(f"mkdir -p {shapeDir}")
        os.system(f"mkdir -p {musicDir}")

        context["shapes"] = sorted(os.listdir(shapeDir))
        context["backgrounds"] = sorted(os.listdir(backgroundDir))
        context["music"] = sorted(os.listdir(musicDir))

        return context

    def post(self, request):
        addActivityForm = self.form_class(request.POST, request.FILES)

        if addActivityForm.is_valid():
            cleanedData = addActivityForm.cleaned_data
            background = cleanedData["background"][1:]
            backgroundPath = Path(os.path.join(settings.BASE_DIR, background))

            with backgroundPath.open(mode="rb") as f:
                activity = Activity(
                    name=cleanedData["name"],
                    description=cleanedData["description"],
                    background=File(f, name=backgroundPath.name),
                    points=cleanedData["points"],
                )
                activity.save()

            return HttpResponseRedirect(reverse("moliuWeb:activities"))
        else:
            context = {"form": addActivityForm}
            return render(request, self.template_name, context=context)


class ActivityDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Activity
    template_name = "moliuWeb/deleteActivity.html"
    success_url = reverse_lazy("moliuWeb:activities")


class GamesView(LoginRequiredMixin, generic.ListView):
    model = Game
    template_name = "moliuWeb/games.html"


class GameImportView(LoginRequiredMixin, generic.base.TemplateView):
    template_name = "moliuWeb/importGame.html"
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


class CreateTrainingSetView(LoginRequiredMixin, generic.FormView):
    template_name = "moliuWeb/createTrainingSet.html"
    form_class = CreateTrainingSet

    def get(self, request):
        games = Game.objects.all()

        for game in games:
            exportedDataDir = os.path.join(
                settings.MEDIA_ROOT, "games", game.directoryName, "exportedData"
            )
            if os.path.isdir(exportedDataDir) and os.listdir(exportedDataDir):
                break
        else:
            messages.error(
                request, "Al menos debe haber un fichero de datos exportados en el servidor"
            )
            return redirect("moliuWeb:models")

        return self.render_to_response(self.get_context_data())

    def post(self, request):
        createTrainingSetForm = CreateTrainingSet(request.POST)

        if createTrainingSetForm.is_valid():
            createTrainingFile(createTrainingSetForm.cleaned_data)
        else:
            print(createTrainingSetForm.errors)

        return HttpResponseRedirect(reverse("moliuWeb:models"))
