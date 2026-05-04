from django import forms
from .models import Course, Centre

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_desc', 'course_duration', 'course_status', 'course_fees']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'course_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Course Description'}),
            'course_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3 months'}),
            'course_status': forms.Select(attrs={'class': 'form-control'}),
            'course_fees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Course Fees'}),
        }

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ['centre_name', 'centre_address', 'centre_contact', 'centre_email', 'centre_desc']
        widgets = {
            'centre_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Centre Name'}),
            'centre_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Centre Address'}),
            'centre_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'centre_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'centre_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Centre Description'}),
        }