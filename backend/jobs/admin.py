from django.contrib import admin
from .models import JobPost, JobApplication, SavedJob

admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(SavedJob)

