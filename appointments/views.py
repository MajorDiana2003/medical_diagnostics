from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentCreateForm


@login_required
def create_appointment_view(request):
    """Контроллер создания записи на прием."""
    if request.method == 'POST':
        form = AppointmentCreateForm(request.POST)
        if form.is_valid():
            # commit=False позволяет дописать пользователя перед сохранением в БД
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.status = 'planned'
            appointment.save()
            # После успешной записи отправляем пациента в его Личный кабинет
            return redirect('profile')
    else:
        # Если перешли по кнопке конкретной услуги, подставим её по умолчанию
        initial_data = {}
        service_id = request.GET.get('service_id')
        if service_id:
            initial_data['service'] = service_id

        form = AppointmentCreateForm(initial=initial_data)

    return render(request, 'appointments/book.html', {'form': form})
