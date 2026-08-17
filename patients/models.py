from django.db import models
from core.models import Profile

class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.profile.user.get_full_name() if self.profile.user else str(self.pk)