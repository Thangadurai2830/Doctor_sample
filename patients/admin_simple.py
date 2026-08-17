from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_user_email', 'dob')
    search_fields = ('profile__user__username', 'profile__user__first_name', 'profile__user__last_name')
    
    def get_patient_name(self, obj):
        return obj.profile.user.get_full_name() or obj.profile.user.username
    get_patient_name.short_description = 'Patient Name'
    
    def get_user_email(self, obj):
        return obj.profile.user.email
    get_user_email.short_description = 'Email'
