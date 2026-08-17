from django import forms
from django.contrib.auth.models import User
from .models import Patient


class PatientForm(forms.ModelForm):
    """Form for creating/updating patient profiles"""
    
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
        model = Patient
        fields = ['dob', 'medical_history']
        widgets = {
            'dob': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'medical_history': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Medical history (optional)...'
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


class AppointmentHistoryFilterForm(forms.Form):
    """Form for filtering appointment history"""
    
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