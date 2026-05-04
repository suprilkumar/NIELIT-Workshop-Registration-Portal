from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Course, Centre
from .forms import CourseForm, CentreForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    courses = Course.objects.filter(course_status__in=['active', 'open', 'ongoing'])
    centres = Centre.objects.all()
    return render(request, 'course/course_list.html', {
        'courses': courses,
        'centres': centres
    })

@user_passes_test(is_admin)
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list_admin.html', {'courses': courses})

@user_passes_test(is_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course:course_list')
    else:
        form = CourseForm()
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Create Course'})

@user_passes_test(is_admin)
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Edit Course'})

@user_passes_test(is_admin)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course:course_list')
    return render(request, 'course/course_confirm_delete.html', {'object': course})

@user_passes_test(is_admin)
def centre_list(request):
    centres = Centre.objects.all()
    return render(request, 'course/centre_list.html', {'centres': centres})

@user_passes_test(is_admin)
def centre_create(request):
    if request.method == 'POST':
        form = CentreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Centre created successfully!')
            return redirect('course:centre_list')
    else:
        form = CentreForm()
    return render(request, 'course/centre_form.html', {'form': form, 'title': 'Create Centre'})

@user_passes_test(is_admin)
def centre_edit(request, pk):
    centre = get_object_or_404(Centre, pk=pk)
    if request.method == 'POST':
        form = CentreForm(request.POST, instance=centre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Centre updated successfully!')
            return redirect('course:centre_list')
    else:
        form = CentreForm(instance=centre)
    return render(request, 'course/centre_form.html', {'form': form, 'title': 'Edit Centre'})

@user_passes_test(is_admin)
def centre_delete(request, pk):
    centre = get_object_or_404(Centre, pk=pk)
    if request.method == 'POST':
        centre.delete()
        messages.success(request, 'Centre deleted successfully!')
        return redirect('course:centre_list')
    return render(request, 'course/centre_confirm_delete.html', {'object': centre})


def public_courses(request):
    courses = Course.objects.filter(course_status__in=['active', 'open', 'ongoing'])
    return render(request, 'courses_public.html', {'courses': courses})

def public_centres(request):
    centres = Centre.objects.all()
    return render(request, 'centres_public.html', {'centres': centres})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Add email sending logic here
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'contact.html')