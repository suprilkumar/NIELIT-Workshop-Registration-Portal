from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<uuid:pk>/edit/', views.course_edit, name='course_edit'),
    path('<uuid:pk>/delete/', views.course_delete, name='course_delete'),
    path('centres/', views.centre_list, name='centre_list'),
    path('centres/create/', views.centre_create, name='centre_create'),
    path('centres/<uuid:pk>/edit/', views.centre_edit, name='centre_edit'),
    path('centres/<uuid:pk>/delete/', views.centre_delete, name='centre_delete'),
]