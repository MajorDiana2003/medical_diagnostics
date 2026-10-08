from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PatientRegistrationForm, PatientLoginForm
from appointments.models import Appointment


def register_view(request):
    """Контроллер регистрации нового пациента."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PatientRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Контроллер входа в систему."""
    if request.user.is_authenticated:
        return redirect('home')

    error_message = None
    if request.method == 'POST':
        form = PatientLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            error_message = "Неверный email или пароль. Пожалуйста, проверьте данные."
    else:
        form = PatientLoginForm()

    return render(request, 'users/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    """Контроллер выхода из учетной записи."""
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    """Контроллер Личного кабинета пациента."""
    # Вытягиваем из базы данных все записи текущего пользователя
    # select_related помогает загрузить данные о враче и услуге одним быстрым запросом
    user_appointments = Appointment.objects.filter(user=request.user).select_related('doctor', 'service')

    context = {
        'user': request.user,
        'appointments': user_appointments,
    }
    return render(request, 'users/profile.html', context)
