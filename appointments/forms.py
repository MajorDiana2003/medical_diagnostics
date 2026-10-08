from django import forms
from .models import Appointment
from core.models import Doctor, MedicalService


class AppointmentCreateForm(forms.ModelForm):
    """Форма для онлайн-записи на медицинскую услугу с русифицированными полями."""

    # Явно переопределяем поля, чтобы задать пустой вариант на русском языке
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.select_related('specialty').all(),
        label='Выберите врача',
        empty_label='— Выберите специалиста из списка —'
    )
    service = forms.ModelChoiceField(
        queryset=MedicalService.objects.select_related('specialty').all(),
        label='Медицинская услуга',
        empty_label='— Выберите медицинскую услугу —'
    )

    # Оставляем наш календарь
    date_time = forms.DateTimeField(
        label='Дата и время приема',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Appointment
        fields = ('doctor', 'service', 'date_time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Применяем единый CSS-класс ко всем полям формы
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
