from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Doctor dashboard and main views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/', views.appointments, name='appointments'),
    path('slots/', views.slots, name='slots'),
    path('patients/search/', views.patient_search, name='patient_search'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Public doctor views
    path('', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    
    # Admin views for managing doctors
    path('add/', views.doctor_add, name='doctor_add'),
    path('update/<int:pk>/', views.doctor_update, name='doctor_update'),
    path('delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),
    
    # Legacy URLs
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor-profile/', views.doctor_profile, name='doctor_profile'),
]