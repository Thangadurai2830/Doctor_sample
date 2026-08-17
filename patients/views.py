from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Patient
from .forms import PatientForm, AppointmentHistoryFilterForm
from doctors.models import Doctor
from booking.models import Appointment
from core.models import Profile


@login_required
def dashboard(request):
    """Patient dashboard"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patient privileges required.')
        return redirect('home')
    
    try:
        patient = request.user.profile.patient
    except Patient.DoesNotExist:
        # Create patient profile if it doesn't exist
        patient = Patient.objects.create(profile=request.user.profile)
    
    # Get upcoming appointments
    from django.utils import timezone
    today = timezone.now().date()
    
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=today
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    # Get recent appointments
    recent_appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-appointment_date', '-appointment_time')[:5]
    
    # Get statistics
    total_appointments = Appointment.objects.filter(patient=patient).count()
    completed_appointments = Appointment.objects.filter(
        patient=patient,
        status='completed'
    ).count()
    
    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'recent_appointments': recent_appointments,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
    }
    
    return render(request, 'patients/dashboard.html', context)


@login_required
def appointment_history(request):
    """View appointment history"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        patient = request.user.profile.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(profile=request.user.profile)
    
    appointments_list = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
    
    # Apply filters
    filter_form = AppointmentHistoryFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['date_from']:
            appointments_list = appointments_list.filter(
                appointment_date__gte=filter_form.cleaned_data['date_from']
            )
        if filter_form.cleaned_data['date_to']:
            appointments_list = appointments_list.filter(
                appointment_date__lte=filter_form.cleaned_data['date_to']
            )
        if filter_form.cleaned_data['status']:
            appointments_list = appointments_list.filter(
                status=filter_form.cleaned_data['status']
            )
    
    # Pagination
    paginator = Paginator(appointments_list, 10)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)
    
    context = {
        'appointments': appointments,
        'filter_form': filter_form,
        'patient': patient,
    }
    
    return render(request, 'patients/appointment_history.html', context)


@login_required
def doctor_search(request):
    """Search for doctors"""
    doctors = Doctor.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    specialty = request.GET.get('specialty', '')
    location = request.GET.get('location', '')
    
    if search_query:
        doctors = doctors.filter(
            Q(profile__user__first_name__icontains=search_query) |
            Q(profile__user__last_name__icontains=search_query) |
            Q(specialty__icontains=search_query)
        )
    
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)
    
    if location:
        doctors = doctors.filter(profile__address__icontains=location)
    
    # Pagination
    paginator = Paginator(doctors, 12)
    page_number = request.GET.get('page')
    doctors_page = paginator.get_page(page_number)
    
    context = {
        'doctors': doctors_page,
        'search_query': search_query,
        'specialty': specialty,
        'location': location,
    }
    
    return render(request, 'patients/doctor_search.html', context)


@login_required
def doctor_detail(request, doctor_id):
    """View doctor details"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Check if user can book appointment (is patient)
    can_book = (
        request.user.is_authenticated and 
        hasattr(request.user, 'profile') and 
        request.user.profile.user_type == 'patient'
    )
    
    context = {
        'doctor': doctor,
        'can_book': can_book,
    }
    
    return render(request, 'patients/doctor_detail.html', context)


@login_required
def profile_edit(request):
    """Edit patient profile"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        patient = request.user.profile.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(profile=request.user.profile)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient, user_instance=request.user)
        if form.is_valid():
            # Update user fields
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            
            # Update profile fields
            profile = user.profile
            profile.phone = form.cleaned_data.get('phone', '')
            profile.address = form.cleaned_data.get('address', '')
            profile.save()
            
            # Save patient fields
            form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('patients:dashboard')
    else:
        form = PatientForm(instance=patient, user_instance=request.user)
    
    context = {
        'form': form,
        'patient': patient,
    }
    
    return render(request, 'patients/profile.html', context)


# Legacy views for backward compatibility
@login_required
def patient_dashboard(request):
    return dashboard(request)


@login_required
def patient_profile(request):
    return profile_edit(request)


def register(request):
    """Patient registration view"""
    if request.method == 'POST':
        # Handle registration logic here
        pass
    return render(request, 'patient/register.html')