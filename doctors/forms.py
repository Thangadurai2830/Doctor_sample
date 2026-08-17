from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class DoctorForm(forms.ModelForm):
    """Form for creating/updating doctor profiles"""
    
    # User fields
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        )
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}
        )
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
        )
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Address'
            }
        )
    )
    
    class Meta:
        model = Doctor
        fields = ['specialty', 'qualification', 'experience', 'available_slots']
        widgets = {
            'specialty': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Specialty (e.g., Cardiology)'}
            ),
            'qualification': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Qualification (e.g., MBBS, MD)'}
            ),
            'experience': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}
            ),
            'available_slots': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Available time slots (e.g., Monday 9-12, Tuesday 2-6)'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        # Extract user instance if updating
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        
        # Populate user fields if updating
        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            if hasattr(self.user_instance, 'profile'):
                self.fields['phone'].initial = self.user_instance.profile.phone
                self.fields['address'].initial = self.user_instance.profile.address


class DoctorSearchForm(forms.Form):
    """Form for searching doctors"""
    
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Doctor name...'
            }
        )
    )
    specialty = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Specialty...'
            }
        )
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Location...'
            }
        )
    )


class AppointmentFilterForm(forms.Form):
    """Form for filtering appointments in doctor dashboard"""
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + [
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class PatientSearchForm(forms.Form):
    """Form for searching patients in doctor dashboard"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Patient name or ID...'
            }
        )
    )