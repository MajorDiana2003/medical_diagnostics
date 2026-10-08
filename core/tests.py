from django.test import TestCase
from django.urls import reverse
from core.models import Specialty, Doctor, MedicalService, Feedback


class CoreViewsAndFeedbackTests(TestCase):
    """Всестороннее тестирование публичных страниц и обратной связи."""

    def setUp(self):
        self.specialty = Specialty.objects.create(title='Кардиолог')
        self.doctor = Doctor.objects.create(
            first_name='Кирилл', last_name='Каркарин', age=42, specialty=self.specialty, experience=17
        )
        self.service = MedicalService.objects.create(
            title='УЗИ сердца', description='Описание', specialty=self.specialty, price=3200.00
        )

    def test_home_page_status_and_content(self):
        """Главная страница открывается и содержит информацию об услугах и врачах."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('УЗИ сердца', content)
        self.assertIn('Каркарин', content)

    def test_about_page_status_and_content(self):
        """Страница 'О компании' открывается и выводит историческую справку."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        # Ищем по уникальным ключевым словам, чтобы тест никогда не падал из-за пробелов или переносов строк
        self.assertIn('Рахманинов', content)
        self.assertIn('Каркарин', content)

    def test_feedback_form_submission_successful(self):
        """Отправка формы обратной связи по симптомам с главной страницы."""
        feedback_data = {
            'name': 'Алексей',
            'email': 'alex@test.com',
            'phone': '+79998887766',
            'message': 'Беспокоят частые покалывания в груди, хочу провериться.'
        }
        response = self.client.post(reverse('home'), data=feedback_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success_message'])

        self.assertEqual(Feedback.objects.count(), 1)
        fb = Feedback.objects.first()
        self.assertEqual(fb.name, 'Алексей')
        self.assertEqual(fb.is_processed, False)


class CoreModelsConstraintsTests(TestCase):
    """Тестирование ограничений и связей в моделях core."""

    def test_specialty_unique_constraint(self):
        """Названия специализаций не должны дублироваться."""
        Specialty.objects.create(title='Невролог')
        with self.assertRaises(Exception):
            Specialty.objects.create(title='Невролог')

    def test_medical_service_string_representation(self):
        spec = Specialty.objects.create(title='Тест')
        service = MedicalService.objects.create(title='МРТ', description='...', specialty=spec, price=5000.00)
        self.assertEqual(str(service), "МРТ — 5000.0 руб.")
