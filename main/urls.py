from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from course.views import home, public_courses, public_centres, about, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('courses/', public_courses, name='public_courses'),
    path('centres/', public_centres, name='public_centres'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('account/', include('account.urls')),
    path('course/', include('course.urls')),
    path('registration/', include('registration.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)