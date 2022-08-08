from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from moliuWeb.models import Patient, Activity
from .serializers import PatientSerializer, ActivitySerializer


class Patients(APIView):
    def get(self, request, format=None):
        patients = Patient.objects.all()

        patients_serializer = PatientSerializer(patients, many=True)
        return JsonResponse(patients_serializer.data, safe=False)

    def post(self, request, format=None):
        patientSerializer = PatientSerializer(data=request.data)
        if patientSerializer.is_valid():
            patientSerializer.save()
            return JsonResponse(patientSerializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(patientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activities(APIView):
    def get(self, request, format=None):
        patients = Activity.objects.all().exclude(name="actividad0")

        patients_serializer = ActivitySerializer(patients, many=True)
        return JsonResponse(patients_serializer.data, safe=False)
