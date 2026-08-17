from django.contrib import admin
from .models import Appointment, Treatment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__profile__user__username', 'doctor__profile__user__username')
    
    def get_patient_name(self, obj):
        return obj.patient.profile.user.get_full_name() or obj.patient.profile.user.username
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.profile.user.get_full_name() or obj.doctor.profile.user.username
    get_doctor_name.short_description = 'Doctor'

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis')
    search_fields = ('diagnosis', 'prescription')
