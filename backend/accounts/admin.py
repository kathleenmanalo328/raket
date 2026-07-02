from django.contrib import admin
from .models import Profile, Resume, ResumeEducation, ResumeExperience, Follow

admin.site.register(Profile)
admin.site.register(Resume)
admin.site.register(ResumeEducation)
admin.site.register(ResumeExperience)
admin.site.register(Follow)
