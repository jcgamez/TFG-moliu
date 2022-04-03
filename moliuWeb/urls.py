from django.urls import path

from . import views

app_name = "moliuWeb"

urlpatterns = [
    path("", views.index, name="index"),
    path("patients", views.PatientsView.as_view(), name="patients"),
    path("activities", views.ActivitiesView.as_view(), name="activities"),
    path("games", views.GamesView.as_view(), name="games"),
    path("models", views.ModelsView.as_view(), name="models"),
]
