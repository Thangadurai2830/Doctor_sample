from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Patient dashboard and main views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/history/', views.appointment_history, name='appointment_history'),
    path('doctors/search/', views.doctor_search, name='doctor_search'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('register/', views.register, name='register'),
    
    # Legacy URLs for backward compatibility
    path('', views.patient_dashboard, name='patient_dashboard'),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('history/', views.appointment_history, name='appointment_history'),
]