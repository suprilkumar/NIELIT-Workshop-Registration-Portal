
#account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, CreateAdminForm, CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView

def is_admin(user):
    return user.is_authenticated and user.is_staff

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard:index')
        messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')

@login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            messages.success(request, f'Admin user {user.username} created successfully!')
            return redirect('dashboard:index')
    else:
        form = CreateAdminForm()
    
    return render(request, 'account/create_admin.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'account/password_reset.html'
    success_url = '/account/login/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Password reset email sent successfully!')
        return super().form_valid(form)