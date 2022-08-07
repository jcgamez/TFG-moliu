from django.http import JsonResponse
from rest_framework.views import APIView

from moliuWeb.models import Patient
from .serializers import PatientSerializer


class Patients(APIView):
    def get(self, request, format=None):
        patients = Patient.objects.all()

        patients_serializer = PatientSerializer(patients, many=True)
        return JsonResponse(patients_serializer.data, safe=False)
