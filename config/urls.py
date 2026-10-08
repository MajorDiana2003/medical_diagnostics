from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import index_view, about_view
from users.views import register_view, login_view, logout_view, profile_view
from appointments.views import create_appointment_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('about/', about_view, name='about'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('book/', create_appointment_view, name='book'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
