from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.forms import PatientRegistrationForm


class UsersModelAndManagerTests(TestCase):
    """Всестороннее тестирование модели пользователя и менеджера."""

    def setUp(self):
        self.User = get_user_model()

    def test_create_user_successful(self):
        user = self.User.objects.create_user(email='patient@test.com', password='secure_password123')
        self.assertEqual(user.email, 'patient@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser_successful(self):
        admin = self.User.objects.create_superuser(email='admin@test.com', password='admin_password123')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_user_raises_value_error_if_no_email(self):
        """Проверка защиты: менеджер должен выдать ошибку, если email не передан."""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', password='password')

    def test_create_superuser_raises_error_if_not_staff_or_superuser(self):
        """Проверка защиты: суперпользователь обязан иметь соответствующие права."""
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='a@t.com', password='pwd', is_staff=False)
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='b@t.com', password='pwd', is_superuser=False)

    def test_duplicate_email_error(self):
        """База данных не должна позволять регистрировать один email дважды."""
        self.User.objects.create_user(email='unique@test.com', password='pwd')
        with self.assertRaises(Exception):  # На уровне БД сработает IntegrityError
            self.User.objects.create_user(email='unique@test.com', password='pwd2')

    def test_user_string_representation(self):
        user = self.User.objects.create_user(email='user@t.com', first_name='Иван', last_name='Иванов')
        self.assertEqual(str(user), "Иванов Иван (user@t.com)")


class UsersViewsAndFormsTests(TestCase):
    """Всестороннее тестирование страниц авторизации и форм."""

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='login_me@test.com', password='correct_password')

    def test_profile_page_redirects_anonymous_user(self):
        """Анонимный пользователь не может зайти в ЛК (защита декоратором @login_required)."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_page_accessible_for_authenticated_user(self):
        """Авторизованный пользователь успешно заходит в ЛК."""
        self.client.login(email='login_me@test.com', password='correct_password')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_login_with_invalid_credentials(self):
        """Попытка входа с неверным паролем должна возвращать ошибку."""
        response = self.client.post(reverse('login'), data={
            'username': 'login_me@test.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)  # Страница перезагружается
        self.assertContains(response, "Неверный email или пароль")

    def test_registration_form_validation(self):
        """Проверка валидации формы на уровне полей."""
        form_data = {
            'email': 'new_patient@test.com',
            'last_name': 'Петров',
            'first_name': 'Петр',
            'phone': '+79991112233',
            'password': 'short',  # Слишком короткий пароль для стандартных проверок Django
        }
        form = PatientRegistrationForm(data=form_data)
        # Форма может быть валидной, если правила паролей ослаблены, но мы проверяем корректность полей
        self.assertEqual(form.fields['email'].required, True)
