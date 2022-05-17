from django.urls import path
from . import views

app_name = "moliuWeb"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("patients", views.PatientsView.as_view(), name="patients"),
    path("patients/add/", views.PatientCreateView.as_view(), name="addPatient"),
    path("patients/update/<int:pk>", views.PatientUpdateView.as_view(), name="updatePatient"),
    path("patients/delete/<int:pk>", views.PatientDeleteView.as_view(), name="deletePatient"),
    path("activities", views.ActivitiesView.as_view(), name="activities"),
    path("games", views.GamesView.as_view(), name="games"),
    path("games/classify/<int:gameId>", views.ClassifyPostures.as_view(), name="classifyPostures"),
    path("models", views.ModelsView.as_view(), name="models"),
]
