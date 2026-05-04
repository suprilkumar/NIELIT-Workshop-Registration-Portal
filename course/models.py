import uuid
from django.db import models

class Centre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    centre_name = models.CharField(max_length=200)
    centre_address = models.TextField()
    centre_contact = models.CharField(max_length=15)
    centre_email = models.EmailField()
    centre_desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.centre_name
    
    class Meta:
        ordering = ['-created_at']

class Course(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('ongoing', 'Ongoing'),
        ('open', 'Open for Registration'),
        ('closed', 'Registration Closed'),
        ('completed', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_name = models.CharField(max_length=200)
    course_desc = models.TextField()
    course_duration = models.CharField(max_length=100)
    course_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    course_fees = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course_name
    
    class Meta:
        ordering = ['-created_at']