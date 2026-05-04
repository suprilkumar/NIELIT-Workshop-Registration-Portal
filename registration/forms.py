from django import forms
from .models import Student
from course.models import Course, Centre

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'mobile_number', 'date_of_birth', 'category', 'email_id', 'father_name', 'course_enrolled', 'preferred_centre']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile Number', 'maxlength': '10'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
            'course_enrolled': forms.Select(attrs={'class': 'form-control'}),
            'preferred_centre': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_enrolled'].queryset = Course.objects.filter(course_status__in=['active', 'open', 'ongoing'])
        self.fields['preferred_centre'].queryset = Centre.objects.all()
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits')
        return mobile

class CertificateCheckForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 10-digit Mobile Number',
            'maxlength': '10'
        })
    )
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits')
        return mobile