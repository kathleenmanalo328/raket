from rest_framework import viewsets
from .models import JobApplication, SavedJob
from .serializers import JobApplicationSerializer, SavedJobSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class SavedJobViewSet(viewsets.ModelViewSet):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)