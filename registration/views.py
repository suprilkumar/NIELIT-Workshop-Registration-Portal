from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Student
from .forms import StudentRegistrationForm, CertificateCheckForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Registration successful! Your Registration ID: {student.id}')
            return redirect('registration:registration_success', student_id=student.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'registration/registration_success.html', {'student': student})

def download_certificate(request):
    form = CertificateCheckForm()
    student = None
    error_message = None
    
    if request.method == 'POST':
        form = CertificateCheckForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            try:
                student = Student.objects.get(mobile_number=mobile_number)
                if student.is_approved:
                    return generate_certificate_pdf(student)
                else:
                    error_message = "Your certificate is not approved yet. Please contact the administration."
            except Student.DoesNotExist:
                error_message = "No registration found with this mobile number."
    
    return render(request, 'registration/certificate_download.html', {
        'form': form,
        'error_message': error_message
    })

def generate_certificate_pdf(student):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Add border
    p.setStrokeColorRGB(0.2, 0.5, 0.8)
    p.setLineWidth(5)
    p.rect(50, 50, width - 100, height - 100)
    
    # Add title
    p.setFont("Helvetica-Bold", 24)
    p.setFillColorRGB(0.2, 0.5, 0.8)
    p.drawCentredString(width/2, height - 100, "CERTIFICATE OF COMPLETION")
    
    # Add content
    p.setFont("Helvetica", 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawCentredString(width/2, height - 150, "This is to certify that")
    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height - 190, student.name)
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 230, f"has successfully completed the course")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 270, student.course_enrolled.course_name)
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 310, f"at {student.preferred_centre.centre_name}")
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, height - 370, f"Certificate ID: {student.id}")
    p.drawCentredString(width/2, height - 390, f"Date of Issue: {datetime.now().strftime('%B %d, %Y')}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{student.mobile_number}.pdf"'
    return response