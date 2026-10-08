from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class PatientRegistrationForm(UserCreationForm):
    """Форма регистрации нового пациента."""
    first_name = forms.CharField(label='Имя', max_length=50, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=50, required=True)
    patronymic = forms.CharField(label='Отчество', max_length=50, required=False)
    phone = forms.CharField(label='Номер телефона', max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')


class PatientLoginForm(AuthenticationForm):
    """Форма входа по Email."""
    username = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'autofocus': True}))
