import uuid
from django.db import models
from course.models import Course, Centre

class Student(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('ews', 'EWS'),
        ('obc', 'OBC'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    email_id = models.EmailField()
    father_name = models.CharField(max_length=200)
    course_enrolled = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    preferred_centre = models.ForeignKey(Centre, on_delete=models.CASCADE, related_name='students')
    is_approved = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.mobile_number}"
    
    class Meta:
        ordering = ['-registration_date']