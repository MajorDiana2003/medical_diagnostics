from django.db import models


class Specialty(models.Model):
    """Специализации врачей и услуг (Терапия, Кардиология, Неврология и т.д.)."""
    title = models.CharField('Название специализации', max_length=100, unique=True)
    description = models.TextField('Краткое описание направления', blank=True, null=True)

    class Meta:
        verbose_name = 'Направление / Специализация'
        verbose_name_plural = 'Направления / Специализации'

    def __str__(self) -> str:
        return self.title


class Doctor(models.Model):
    """Информация о врачах клиники."""
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    patronymic = models.CharField('Отчество', max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField('Возраст')
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='doctors',
        verbose_name='Специализация'
    )
    experience = models.PositiveIntegerField('Стаж работы (лет)')

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.specialty.title})"


class MedicalService(models.Model):
    """Медицинские услуги и диагностика (УЗИ, МРТ, Прием врача и т.д.)."""
    title = models.CharField('Название медицинской услуги', max_length=200)
    description = models.TextField('Подробное описание услуги')
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name='Направление'
    )
    price = models.DecimalField('Цена (руб.)', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Медицинская услуга'
        verbose_name_plural = 'Медицинские услуги'

    def __str__(self) -> str:
        return f"{self.title} — {self.price} руб."


class Feedback(models.Model):
    """Форма обратной связи с Главной страницы."""
    name = models.CharField('Имя заявителя', max_length=100)
    email = models.EmailField('Электронная почта')
    phone = models.CharField('Телефон', max_length=20)
    message = models.TextField('Текст сообщения')
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)
    is_processed = models.BooleanField('Обработано администратором', default=False)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь (Сообщения)'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Сообщение от {self.name} ({self.created_at.strftime('%d.%m.%Y')})"
