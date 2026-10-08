from django.conf import settings
from django.db import models
from core.models import Doctor, MedicalService


class Appointment(models.Model):
    """Записи пациентов на медицинские услуги и приёмы."""

    STATUS_CHOICES = [
        ('planned', 'Запланирован'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пациент'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='Врач'
    )
    service = models.ForeignKey(
        MedicalService,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='Медицинская услуга'
    )
    date_time = models.DateTimeField('Дата и время приема')
    status = models.CharField('Статус приема', max_length=20, choices=STATUS_CHOICES, default='planned')

    # Поля для результатов диагностики (будут заполняться врачом/админом после приёма)
    medical_conclusion = models.TextField('Медицинское заключение / Рекомендации', blank=True, null=True)
    result_file = models.FileField(
        'Файл с результатами диагностики (PDF / Изображение)',
        upload_to='appointment_results/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField('Дата создания записи', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на приемы'
        ordering = ['-date_time']

    def __str__(self) -> str:
        date_str = self.date_time.strftime('%d.%m.%Y %H:%M')
        return (
            f"Запись #{self.id}: {self.user.last_name} "
            f"к {self.doctor.last_name} ({date_str})"
        )
