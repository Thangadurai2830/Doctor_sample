from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Treatment
from doctors.models import Doctor
from patients.models import Patient


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': '2024-01-01'
                }
            ),
            'appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'doctor': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['doctor'].empty_label = "Select a Doctor"


class TreatmentForm(forms.ModelForm):
    """Form for adding treatment details"""
    
    class Meta:
        model = Treatment
        fields = ['diagnosis', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter diagnosis details...'
                }
            ),
            'prescription': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    'rows': 6,
                    'placeholder': 'Enter prescription details...'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Additional notes (optional)...'
                }
            )
        }


class AppointmentSearchForm(forms.Form):
    """Form for searching appointments"""
    
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
        choices=[('', 'All Status')] + list(Appointment.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        required=False,
        empty_label="All Doctors",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SlotSelectionForm(forms.Form):
    """Form for selecting available time slots"""
    
    SLOT_CHOICES = [
        ('09:00', '09:00 AM'),
        ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('14:00', '02:00 PM'),
        ('14:30', '02:30 PM'),
        ('15:00', '03:00 PM'),
        ('15:30', '03:30 PM'),
        ('16:00', '04:00 PM'),
        ('16:30', '04:30 PM'),
        ('17:00', '05:00 PM'),
    ]
    
    selected_slot = forms.ChoiceField(
        choices=SLOT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'slot-radio'}),
        label="Available Time Slots"
    )
