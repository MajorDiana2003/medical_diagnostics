from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Specialty, Doctor, MedicalService
from appointments.models import Appointment


class AppointmentsComprehensiveTests(TestCase):
    """Полное тестирование логики онлайн-записи на диагностику."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='patient_test@test.com', password='password123')

        self.specialty = Specialty.objects.create(title='Невролог')
        self.doctor = Doctor.objects.create(
            first_name='Олег', last_name='Быков', age=45, specialty=self.specialty, experience=22
        )
        self.service = MedicalService.objects.create(
            title='МРТ', description='Описание', specialty=self.specialty, price=6000.00
        )

    def test_appointment_form_rendering_with_initial_service(self):
        """Если перешли с карточки конкретной услуги, она должна автоматически выбраться в форме."""
        self.client.login(email='patient_test@test.com', password='password123')
        response = self.client.get(f"{reverse('book')}?service_id={self.service.id}")
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма получила начальное значение для услуги
        self.assertEqual(response.context['form'].initial['service'], str(self.service.id))

    def test_appointment_invalid_data_submission(self):
        """Отправка пустой или некорректной формы не должна создавать запись."""
        self.client.login(email='patient_test@test.com', password='password123')
        # Отправляем пустые данные
        response = self.client.post(reverse('book'), data={})
        self.assertEqual(response.status_code, 200)  # Страница перерендерится с ошибками
        self.assertEqual(Appointment.objects.count(), 0)  # Запись не создана

    def test_appointment_appears_in_profile_history(self):
        """После успешного создания запись обязана отображаться в Личном кабинете пациента."""
        self.client.login(email='patient_test@test.com', password='password123')

        # Создаем запись напрямую
        Appointment.objects.create(
            user=self.user,
            doctor=self.doctor,
            service=self.service,
            date_time='2026-12-01T12:00:00Z',
            status='planned'
        )

        # Запрашиваем личный кабинет
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'МРТ')
        self.assertContains(response, 'Быков')
        self.assertContains(response, 'Запланирован')
