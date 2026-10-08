from django.shortcuts import render
from .models import MedicalService, Doctor, Feedback


def index_view(request):
    success_message = False

    # Если пользователь заполнил форму и нажал кнопку "Отправить заявку"
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Сохраняем данные в таблицу Feedback базы данных PostgreSQL
        Feedback.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        success_message = True

    # Снова вытягиваем услуги и врачей для отображения на странице
    services = MedicalService.objects.select_related('specialty').all()
    doctors = Doctor.objects.select_related('specialty').all()

    context = {
        'services': services,
        'doctors': doctors,
        'success_message': success_message,
    }
    return render(request, 'index.html', context)


def about_view(request):
    # Достаем всех практикующих врачей из базы данных с их специализациями
    doctors = Doctor.objects.select_related('specialty').all()

    context = {
        'doctors': doctors,
    }
    return render(request, 'about.html', context)
