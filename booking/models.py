from django.db import models
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(blank=True, help_text="Patient symptoms or reason for appointment")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.profile.user.username} with {self.doctor.profile.user.username} on {self.appointment_date} at {self.appointment_time}"

class Treatment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Treatment for {self.appointment}"