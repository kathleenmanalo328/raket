from django.db import models
from django.contrib.auth.models import User
from core.models import PrefixedIDModel

class Profile(PrefixedIDModel):
    id_prefix = "rpr-"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    headline = models.CharField(max_length=150, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    portfolio_url = models.URLField(blank=True)
    raket_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Resume(PrefixedIDModel):
    id_prefix = "rres-"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    label = models.CharField(max_length=120)
    summary = models.TextField(max_length=3000, blank=True)
    skills = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_published:
            Resume.objects.filter(user=self.user).exclude(pk=self.pk).update(is_published=False)
    def __str__(self):
        return f"{self.user.username} - {self.label}"

class ResumeExperience(PrefixedIDModel):
    id_prefix = "rexp-"
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

class ResumeEducation(PrefixedIDModel):
    id_prefix = "redu-"
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} — {self.school}"

class Follow(PrefixedIDModel):
    id_prefix = "rfol-"
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"