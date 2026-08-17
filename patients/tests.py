from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile
from .models import Patient
import datetime

class PatientModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='pat', password='pass')
        # Profile is automatically created by signal, just update it
        profile = user.profile
        profile.user_type = 'patient'
        profile.save()
        self.patient = Patient.objects.create(profile=profile, dob=datetime.date(2000, 1, 1), medical_history='None')

    def test_patient_str(self):
        self.assertEqual(str(self.patient), self.patient.profile.user.get_full_name())