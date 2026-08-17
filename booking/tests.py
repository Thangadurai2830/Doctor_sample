from django.test import TestCase
from django.contrib.auth.models import User
from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment, Treatment
import datetime

class AppointmentModelTest(TestCase):
    def setUp(self):
        user_doc = User.objects.create_user(username='doc', password='pass')
        user_pat = User.objects.create_user(username='pat', password='pass')
        doctor = Doctor.objects.create(profile=user_doc.profile, specialty='Cardiology', qualification='MD', experience=5, available_slots='[]')
        patient = Patient.objects.create(profile=user_pat.profile)
        self.appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=datetime.date.today(),
            appointment_time=datetime.datetime.now().time(),
            status='pending'
        )

    def test_appointment_str(self):
        self.assertIn(self.appointment.doctor.profile.user.username, str(self.appointment))
        self.assertIn(self.appointment.patient.profile.user.username, str(self.appointment))

class TreatmentModelTest(TestCase):
    def setUp(self):
        user_doc = User.objects.create_user(username='doc2', password='pass')
        user_pat = User.objects.create_user(username='pat2', password='pass')
        doctor = Doctor.objects.create(profile=user_doc.profile, specialty='Dermatology', qualification='MD', experience=10, available_slots='[]')
        patient = Patient.objects.create(profile=user_pat.profile)
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=datetime.date.today(),
            appointment_time=datetime.datetime.now().time(),
            status='completed'
        )
        self.treatment = Treatment.objects.create(
            appointment=appointment,
            diagnosis='Test Diagnosis',
            prescription='Test Prescription',
            notes='Test Notes'
        )

    def test_treatment_str(self):
        self.assertIn('Treatment for', str(self.treatment))