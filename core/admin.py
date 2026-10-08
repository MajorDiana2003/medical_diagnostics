from django.contrib import admin
from .models import Specialty, Doctor, MedicalService, Feedback


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'specialty', 'experience')
    list_filter = ('specialty', 'experience')
    search_fields = ('last_name', 'first_name')


@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'price')
    list_filter = ('specialty',)
    search_fields = ('title',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    readonly_fields = ('created_at',)
