from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from moliuWeb.models import Patient, Activity
from .serializers import PatientSerializer, ActivitySerializer


class Patients(APIView):
    def get(self, request, format=None):
        patients = Patient.objects.all().exclude(name="paciente0")

        patientsSerializer = PatientSerializer(patients, many=True)

        processedData = {"players": patientsSerializer.data}

        return JsonResponse(processedData, safe=True)

    def post(self, request, format=None):
        patientSerializer = PatientSerializer(data=request.data)
        if patientSerializer.is_valid():
            patientSerializer.save()
            return JsonResponse(patientSerializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(patientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activities(APIView):
    def get(self, request, format=None):
        activities = Activity.objects.all().exclude(name="actividad0")

        activitiesSerializer = ActivitySerializer(activities, many=True)

        processedData = {"activities": activitiesSerializer.data}

        return JsonResponse(processedData, safe=True)
