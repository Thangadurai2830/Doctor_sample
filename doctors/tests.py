from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile
from .models import Doctor

class DoctorModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='doc', password='pass')
        # Profile is automatically created by signal, just update it
        profile = user.profile
        profile.user_type = 'doctor'
        profile.save()
        self.doctor = Doctor.objects.create(
            profile=profile,
            specialty='Cardiology',
            qualification='MD',
            experience=10,
            available_slots='[]'
        )

    def test_doctor_str(self):
        self.assertIn('Cardiology', str(self.doctor))
        self.assertIn(self.doctor.profile.user.get_full_name(), str(self.doctor))