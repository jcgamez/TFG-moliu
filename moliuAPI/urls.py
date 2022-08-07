from django.urls import path
from . import views

app_name = "moliuAPI"

urlpatterns = [
    path("patients", views.Patients.as_view(), name="patients"),
]
