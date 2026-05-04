from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from registration.models import Student
from course.models import Course, Centre
from datetime import datetime, timedelta
import json
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def dashboard_index(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_centres = Centre.objects.count()
    approved_students = Student.objects.filter(is_approved=True).count()
    pending_approvals = Student.objects.filter(is_approved=False).count()
    
    recent_registrations = Student.objects.all().select_related('course_enrolled', 'preferred_centre')[:10]
    
    course_enrollment_stats = Course.objects.annotate(
        student_count=Count('students')
    ).order_by('-student_count')[:5]
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_centres': total_centres,
        'approved_students': approved_students,
        'pending_approvals': pending_approvals,
        'recent_registrations': recent_registrations,
        'course_enrollment_stats': course_enrollment_stats,
        'now': datetime.now(),
    }
    return render(request, 'dashboard/index.html', context)

@user_passes_test(is_admin)
def students_list(request):
    # Get all students with related data
    students = Student.objects.select_related('course_enrolled', 'preferred_centre').all()
    
    # Get filter parameters
    course_filter = request.GET.get('course')
    center_filter = request.GET.get('center')
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Apply filters
    if course_filter and course_filter != '':
        students = students.filter(course_enrolled_id=course_filter)
    
    if center_filter and center_filter != '':
        students = students.filter(preferred_centre_id=center_filter)
    
    if status_filter and status_filter != '':
        if status_filter == 'approved':
            students = students.filter(is_approved=True)
        elif status_filter == 'pending':
            students = students.filter(is_approved=False)
    
    if category_filter and category_filter != '':
        students = students.filter(category=category_filter)
    
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(mobile_number__icontains=search_query) |
            Q(email_id__icontains=search_query) |
            Q(father_name__icontains=search_query)
        )
    
    # Get all courses and centers for filter dropdowns
    courses = Course.objects.all()
    centres = Centre.objects.all()
    
    context = {
        'students': students,
        'courses': courses,
        'centres': centres,
        'selected_course': course_filter,
        'selected_center': center_filter,
        'selected_status': status_filter,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'dashboard/students_list.html', context)

@user_passes_test(is_admin)
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'dashboard/student_detail.html', {'student': student})

@user_passes_test(is_admin)
def approve_certificate(request):
    students = Student.objects.filter(is_approved=False).select_related('course_enrolled', 'preferred_centre')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            student = get_object_or_404(Student, id=student_id)
            student.is_approved = True
            student.save()
            messages.success(request, f'Student {student.name} has been approved for certification!')
            return redirect('dashboard:approve_certificate')
    
    return render(request, 'dashboard/approve_certificate.html', {'students': students})

@user_passes_test(is_admin)
def approve_multiple(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        if student_ids:
            count = Student.objects.filter(id__in=student_ids).update(is_approved=True)
            messages.success(request, f'{count} students have been approved for certification!')
        return redirect('dashboard:approve_certificate')

@user_passes_test(is_admin)
def approve_single(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            student.is_approved = True
            student.save()
            return JsonResponse({'success': True, 'message': 'Student approved successfully!'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found!'})
    return JsonResponse({'success': False, 'message': 'Invalid request!'})

@user_passes_test(is_admin)
def reports(request):
    # Get last 30 days registration data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    dates = []
    counts = []
    current_date = start_date
    while current_date <= end_date:
        count = Student.objects.filter(registration_date__date=current_date).count()
        dates.append(current_date.strftime('%Y-%m-%d'))
        counts.append(count)
        current_date += timedelta(days=1)
    
    # Category distribution
    categories = Student.objects.values('category').annotate(count=Count('id'))
    category_labels = []
    category_data = []
    category_map = dict(Student.CATEGORY_CHOICES)
    for c in categories:
        category_labels.append(category_map.get(c['category'], c['category']))
        category_data.append(c['count'])
    
    # Course enrollment distribution
    course_stats = Course.objects.annotate(student_count=Count('students')).filter(student_count__gt=0)
    course_labels = [course.course_name for course in course_stats]
    course_data = [course.student_count for course in course_stats]
    
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'course_labels': json.dumps(course_labels),
        'course_data': json.dumps(course_data),
        'total_students': Student.objects.count(),
        'approved_count': Student.objects.filter(is_approved=True).count(),
        'pending_count': Student.objects.filter(is_approved=False).count(),
    }
    return render(request, 'dashboard/reports.html', context)

@user_passes_test(is_admin)
def generate_full_report(request):
    # Generate Excel report
    students = Student.objects.select_related('course_enrolled', 'preferred_centre').all().values(
        'name', 'mobile_number', 'email_id', 'date_of_birth', 'category', 
        'father_name', 'course_enrolled__course_name', 'preferred_centre__centre_name',
        'is_approved', 'registration_date'
    )
    
    df = pd.DataFrame(list(students))
    df.columns = ['Name', 'Mobile Number', 'Email', 'Date of Birth', 'Category', 
                  'Father Name', 'Course Enrolled', 'Preferred Centre', 'Certificate Status', 'Registration Date']
    
    # Create Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Students Report', index=False)
    
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=students_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    return response

@user_passes_test(is_admin)
def export_students_pdf(request):
    students = Student.objects.select_related('course_enrolled', 'preferred_centre').all()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=students_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, alignment=1, spaceAfter=30)
    
    # Title
    elements.append(Paragraph("Students Registration Report", title_style))
    elements.append(Spacer(1, 20))
    
    # Table data
    data = [['Name', 'Mobile', 'Email', 'Course', 'Center', 'Status', 'Date']]
    for student in students:
        data.append([
            student.name,
            student.mobile_number,
            student.email_id,
            student.course_enrolled.course_name,
            student.preferred_centre.centre_name,
            'Approved' if student.is_approved else 'Pending',
            student.registration_date.strftime('%Y-%m-%d')
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response