from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('students/', views.students_list, name='students_list'),
    path('students/<uuid:pk>/', views.student_detail, name='student_detail'),
    path('approve/', views.approve_certificate, name='approve_certificate'),
    path('approve-multiple/', views.approve_multiple, name='approve_multiple'),
    path('approve-single/', views.approve_single, name='approve_single'),
    path('reports/', views.reports, name='reports'),
    path('generate-report/', views.generate_full_report, name='generate_full_report'),
    path('export-pdf/', views.export_students_pdf, name='export_pdf'),
]