from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Doctor
from .forms import DoctorForm, DoctorSearchForm, AppointmentFilterForm, PatientSearchForm
from booking.models import Appointment, Treatment
from patients.models import Patient
from core.models import Profile


@login_required
def dashboard(request):
    """Doctor dashboard"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied. Doctor privileges required.')
        return redirect('home')
    
    try:
        doctor = request.user.profile.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')
    
    # Get today's appointments
    from django.utils import timezone
    today = timezone.now().date()
    
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today
    ).order_by('appointment_time')
    
    # Get statistics
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    pending_appointments = Appointment.objects.filter(
        doctor=doctor, 
        status='pending'
    ).count()
    completed_appointments = Appointment.objects.filter(
        doctor=doctor, 
        status='completed'
    ).count()
    
    context = {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'appointments_count': total_appointments,
        'slots_count': 10,  # Placeholder for slots count
        'patients_count': 25,  # Placeholder for patients count
    }
    
    return render(request, 'doctors/dashboard.html', context)


@login_required
def appointments(request):
    """View all appointments for doctor"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        doctor = request.user.profile.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')
    
    appointments_list = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
    
    # Apply filters
    filter_form = AppointmentFilterForm(request.GET)
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
        'doctor': doctor,
    }
    
    return render(request, 'doctors/appointments.html', context)


@login_required
def patient_search(request):
    """Search patients"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patients = Patient.objects.none()
    search_form = PatientSearchForm()
    
    if request.GET.get('search_query'):
        search_form = PatientSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['search_query']
            patients = Patient.objects.filter(
                Q(profile__user__first_name__icontains=query) |
                Q(profile__user__last_name__icontains=query) |
                Q(profile__user__username__icontains=query) |
                Q(profile__user__email__icontains=query) |
                Q(id__icontains=query)
            )
    
    context = {
        'patients': patients,
        'search_form': search_form,
    }
    
    return render(request, 'doctors/patient_search.html', context)


@login_required
def patient_detail(request, patient_id):
    """View patient details and history"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Get patient's appointment history with this doctor
    try:
        doctor = request.user.profile.doctor
        appointments = Appointment.objects.filter(
            patient=patient,
            doctor=doctor
        ).order_by('-appointment_date')
    except Doctor.DoesNotExist:
        appointments = []
    
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    
    return render(request, 'doctors/patient_detail.html', context)


@login_required
def profile_edit(request):
    """Edit doctor profile"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        doctor = request.user.profile.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor, user_instance=request.user)
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
            
            # Save doctor fields
            form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctors:dashboard')
    else:
        form = DoctorForm(instance=doctor, user_instance=request.user)
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    
    return render(request, 'doctors/profile.html', context)


def doctor_list(request):
    """Public doctor listing"""
    doctors = Doctor.objects.all()
    search_form = DoctorSearchForm()
    
    if request.GET:
        search_form = DoctorSearchForm(request.GET)
        if search_form.is_valid():
            if search_form.cleaned_data['name']:
                name_query = search_form.cleaned_data['name']
                doctors = doctors.filter(
                    Q(profile__user__first_name__icontains=name_query) |
                    Q(profile__user__last_name__icontains=name_query)
                )
            if search_form.cleaned_data['specialty']:
                doctors = doctors.filter(
                    specialty__icontains=search_form.cleaned_data['specialty']
                )
            if search_form.cleaned_data['location']:
                doctors = doctors.filter(
                    profile__address__icontains=search_form.cleaned_data['location']
                )
    
    # Pagination
    paginator = Paginator(doctors, 12)
    page_number = request.GET.get('page')
    doctors_page = paginator.get_page(page_number)
    
    context = {
        'doctors': doctors_page,
        'search_form': search_form,
    }
    
    return render(request, 'doctors/doctor_list.html', context)


def doctor_detail(request, doctor_id):
    """Public doctor detail view"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    context = {
        'doctor': doctor,
    }
    
    return render(request, 'doctors/doctor_detail.html', context)


# Legacy admin views (keeping for backward compatibility)
@login_required
def doctor_dashboard(request):
    return dashboard(request)


@login_required
def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.profile = request.user.profile
            doctor.save()
            messages.success(request, "Doctor profile added successfully!")
            return redirect('doctors:doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile updated!")
            return redirect('doctors:doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, "Doctor profile deleted.")
        return redirect('doctors:doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})


@login_required
def doctor_profile(request):
    try:
        doctor = request.user.profile.doctor
    except Doctor.DoesNotExist:
        doctor = None
    return render(request, 'doctors/doctor_profile.html', {'doctor': doctor})


@login_required
def slots(request):
    """Manage doctor slots/availability"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'doctor':
        messages.error(request, 'Access denied. Doctor privileges required.')
        return redirect('home')
    
    try:
        doctor = request.user.profile.doctor
    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('home')
    
    # Simple slots management view
    context = {
        'doctor': doctor,
        'slots_count': 10,  # Placeholder
    }
    
    return render(request, 'doctors/slots.html', context)