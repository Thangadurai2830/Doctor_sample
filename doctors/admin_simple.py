from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_doctor_name', 'get_user_email', 'specialty', 'qualification', 'experience')
    list_filter = ('specialty',)
    search_fields = ('profile__user__username', 'profile__user__first_name', 'profile__user__last_name', 'specialty', 'qualification')
    
    def get_doctor_name(self, obj):
        return obj.profile.user.get_full_name() or obj.profile.user.username
    get_doctor_name.short_description = 'Doctor Name'
    
    def get_user_email(self, obj):
        return obj.profile.user.email
    get_user_email.short_description = 'Email'
