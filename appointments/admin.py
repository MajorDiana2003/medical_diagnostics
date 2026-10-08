from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'service', 'date_time', 'status')
    list_filter = ('status', 'date_time', 'doctor')
    search_fields = ('user__last_name', 'user__email', 'doctor__last_name')
    date_hierarchy = 'date_time'
