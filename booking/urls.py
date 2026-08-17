from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_dashboard, name='booking_dashboard'),  # Root booking URL
    path('book/', views.book_appointment, name='book_appointment'),
    path('slots/<int:doctor_id>/<str:date>/', views.available_slots, name='available_slots'),
    path('detail/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('confirm/<int:pk>/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('add-treatment/<int:pk>/', views.add_treatment, name='add_treatment'),
]