from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('register/', views.register_student, name='register'),
    path('success/<uuid:student_id>/', views.registration_success, name='registration_success'),
    path('certificate/', views.download_certificate, name='certificate'),
]