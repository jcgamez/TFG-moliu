from rest_framework import serializers
from moliuWeb.models import Patient, Activity


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ["id"]


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ["id"]
