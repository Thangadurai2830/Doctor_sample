from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Appointment, Treatment
from .forms import AppointmentForm, TreatmentForm, AppointmentSearchForm, SlotSelectionForm
from doctors.models import Doctor
from patients.models import Patient


@login_required
def booking_dashboard(request):
    """Booking dashboard - shows different content based on user type"""
    user_type = getattr(request.user.profile, 'user_type', None)
    
    if user_type == 'patient':
        # Patient view - show their appointments and doctors
        try:
            patient = request.user.profile.patient
            appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:5]
        except:
            appointments = []
        
        doctors = Doctor.objects.all()[:6]  # Show some available doctors
        
        context = {
            'user_type': user_type,
            'appointments': appointments,
            'doctors': doctors,
        }
        return render(request, 'booking/dashboard.html', context)
        
    elif user_type == 'doctor':
        # Doctor view - show their appointments
        try:
            doctor = request.user.profile.doctor
            appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')[:10]
        except:
            appointments = []
            
        context = {
            'user_type': user_type,
            'appointments': appointments,
        }
        return render(request, 'booking/dashboard.html', context)
        
    else:
        # Admin or other users
        appointments = Appointment.objects.all().order_by('-appointment_date')[:10]
        doctors = Doctor.objects.all()[:6]
        patients = Patient.objects.all()[:6]
        
        context = {
            'user_type': user_type,
            'appointments': appointments,
            'doctors': doctors,
            'patients': patients,
        }
        return render(request, 'booking/dashboard.html', context)


@login_required
def book_appointment(request):
    """Book new appointment"""
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('home')
    
    try:
        patient = request.user.profile.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(profile=request.user.profile)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('booking:appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'booking/appointment_book.html', context)


@login_required
def available_slots(request, doctor_id, date):
    """Get available slots for a doctor on a specific date"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get booked slots for the date
    booked_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date,
        status__in=['pending', 'confirmed']
    ).values_list('appointment_time', flat=True)
    
    # Available time slots
    all_slots = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00'
    ]
    
    available_slots = []
    for slot in all_slots:
        if slot not in [str(time) for time in booked_appointments]:
            available_slots.append({
                'time': slot,
                'display': slot.replace(':', ':') + (' AM' if int(slot[:2]) < 12 else ' PM')
            })
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({'slots': available_slots})
    
    context = {
        'doctor': doctor,
        'date': date,
        'available_slots': available_slots,
    }
    return render(request, 'booking/slot_list.html', context)


@login_required
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Allow access if user is the patient, doctor, or admin
    can_view = (
        (user_profile.user_type == 'patient' and hasattr(user_profile, 'patient') and appointment.patient == user_profile.patient) or
        (user_profile.user_type == 'doctor' and hasattr(user_profile, 'doctor') and appointment.doctor == user_profile.doctor) or
        (user_profile.user_type == 'admin')
    )
    
    if not can_view:
        messages.error(request, 'You do not have permission to view this appointment.')
        return redirect('home')
    
    context = {
        'appointment': appointment,
        'can_modify': user_profile.user_type in ['doctor', 'admin'],
    }
    return render(request, 'booking/appointment_detail.html', context)


@login_required
def appointment_history(request):
    """View appointment history"""
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, 'Profile not found.')
        return redirect('home')
    
    appointments = Appointment.objects.none()
    
    if user_profile.user_type == 'patient' and hasattr(user_profile, 'patient'):
        appointments = Appointment.objects.filter(patient=user_profile.patient)
    elif user_profile.user_type == 'doctor' and hasattr(user_profile, 'doctor'):
        appointments = Appointment.objects.filter(doctor=user_profile.doctor)
    elif user_profile.user_type == 'admin':
        appointments = Appointment.objects.all()
    
    appointments = appointments.order_by('-appointment_date', '-appointment_time')
    
    # Apply search filters
    search_form = AppointmentSearchForm(request.GET)
    if search_form.is_valid():
        if search_form.cleaned_data.get('date_from'):
            appointments = appointments.filter(
                appointment_date__gte=search_form.cleaned_data['date_from']
            )
        if search_form.cleaned_data.get('date_to'):
            appointments = appointments.filter(
                appointment_date__lte=search_form.cleaned_data['date_to']
            )
        if search_form.cleaned_data.get('status'):
            appointments = appointments.filter(
                status=search_form.cleaned_data['status']
            )
        if search_form.cleaned_data.get('doctor'):
            appointments = appointments.filter(
                doctor=search_form.cleaned_data['doctor']
            )
    
    # Pagination
    paginator = Paginator(appointments, 15)
    page_number = request.GET.get('page')
    appointments_page = paginator.get_page(page_number)
    
    context = {
        'appointments': appointments_page,
        'search_form': search_form,
        'user_type': user_profile.user_type,
    }
    return render(request, 'booking/appointment_history.html', context)


@login_required
def confirm_appointment(request, pk):
    """Confirm an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Only doctors and admins can confirm appointments
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile or user_profile.user_type not in ['doctor', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if user_profile.user_type == 'doctor':
        if not hasattr(user_profile, 'doctor') or appointment.doctor != user_profile.doctor:
            messages.error(request, 'You can only confirm your own appointments.')
            return redirect('home')
    
    appointment.status = 'confirmed'
    appointment.save()
    messages.success(request, "Appointment confirmed successfully!")
    return redirect('booking:appointment_detail', pk=appointment.pk)


@login_required
def cancel_appointment(request, pk):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Allow cancellation by patient (own appointments), doctor (own appointments), or admin (any)
    can_cancel = (
        (user_profile.user_type == 'patient' and hasattr(user_profile, 'patient') and appointment.patient == user_profile.patient) or
        (user_profile.user_type == 'doctor' and hasattr(user_profile, 'doctor') and appointment.doctor == user_profile.doctor) or
        (user_profile.user_type == 'admin')
    )
    
    if not can_cancel:
        messages.error(request, 'You do not have permission to cancel this appointment.')
        return redirect('home')
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.info(request, "Appointment cancelled successfully.")
        return redirect('booking:appointment_detail', pk=appointment.pk)
    
    return render(request, 'booking/appointment_cancel.html', {'appointment': appointment})


@login_required
def add_treatment(request, pk):
    """Add treatment details to appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Only doctors can add treatments
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile or user_profile.user_type != 'doctor':
        messages.error(request, 'Only doctors can add treatment details.')
        return redirect('home')
    
    if not hasattr(user_profile, 'doctor') or appointment.doctor != user_profile.doctor:
        messages.error(request, 'You can only add treatments to your own appointments.')
        return redirect('home')
    
    # Check if treatment already exists
    treatment = getattr(appointment, 'treatment', None)
    
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.appointment = appointment
            treatment.save()
            
            # Mark appointment as completed
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(request, "Treatment details added successfully!")
            return redirect('booking:appointment_detail', pk=appointment.pk)
    else:
        form = TreatmentForm(instance=treatment)
    
    context = {
        'form': form,
        'appointment': appointment,
        'treatment': treatment,
    }
    return render(request, 'booking/treatment_add.html', context)