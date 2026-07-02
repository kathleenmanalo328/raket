from rest_framework import serializers
from .models import JobApplication, SavedJob


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "job", "applicant", "resume", "cover_letter", "status", "created_at"]
        read_only_fields = ["id", "applicant", "status", "created_at"]


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ["id", "job", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]