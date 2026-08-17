from django.db import models
from core.models import Profile

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    available_slots = models.TextField(blank=True, help_text="JSON or text for available slots")

    def __str__(self):
        return f"{self.profile.user.get_full_name()} ({self.specialty})"