from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from course.models import Course
from .models import Student, Certificate
from .forms import StudentRegistrationForm, UserLookupForm



def register_course(request, course_id=None):
    """Course registration page with pre-selected course"""
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Registration successful! Your Registration Number is: {student.registration_number}')
            return redirect('registration:registration_success', reg_number=student.registration_number)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if course_id:
            course = get_object_or_404(Course, id=course_id, is_active=True)
            if not course.is_available_for_registration():
                messages.error(request, f'Sorry, {course.course_name} is no longer available for registration.')
                return redirect('course:public_courses')
            initial['course_enrolled'] = course
        
        form = StudentRegistrationForm(initial=initial)
    
    context = {
        'form': form,
        'course_readonly': course_id is not None,
        'pre_selected_course': get_object_or_404(Course, id=course_id) if course_id else None
    }
    return render(request, 'registration/register.html', context)

def registration_success(request, reg_number):
    """Registration success page"""
    student = get_object_or_404(Student, registration_number=reg_number)
    return render(request, 'registration/registration_success.html', {'student': student})


def user_profile(request):
    """User profile lookup page - no authentication required"""
    students = None
    lookup_done = False
    
    if request.method == 'POST':
        form = UserLookupForm(request.POST)
        if form.is_valid():
            lookup_by = form.cleaned_data['lookup_by']
            email_id = form.cleaned_data.get('email_id')
            mobile_number = form.cleaned_data.get('mobile_number')
            
            if lookup_by == 'email' and email_id:
                students = Student.objects.filter(email_id=email_id).exclude(status='cancelled')
                lookup_done = True
                if not students.exists():
                    messages.info(request, 'No registrations found with this email address.')
            elif lookup_by == 'mobile' and mobile_number:
                students = Student.objects.filter(mobile_number=mobile_number).exclude(status='cancelled')
                lookup_done = True
                if not students.exists():
                    messages.info(request, 'No registrations found with this mobile number.')
    else:
        form = UserLookupForm()
    
    context = {
        'form': form,
        'students': students,
        'lookup_done': lookup_done,
    }
    return render(request, 'registration/user_profile.html', context)

def download_certificate(request, reg_number):
    try:
        student = Student.objects.get(registration_number=reg_number)
        if student.status != 'completed':
            messages.error(request, 'Certificate is only available for completed courses.')
            return redirect('registration:user_profile')
        
        certificate, created = Certificate.objects.get_or_create(student=student)
        
        return render(request, 'registration/certificate_view.html', {
            'student': student,
            'certificate': certificate
        })
    except Student.DoesNotExist:
        messages.error(request, 'Registration not found.')
        return redirect('registration:user_profile')

def verify_certificate(request, cert_number):
    """Public certificate verification"""
    certificate = get_object_or_404(Certificate, certificate_number=cert_number)
    return render(request, 'registration/verify_certificate.html', {'certificate': certificate})