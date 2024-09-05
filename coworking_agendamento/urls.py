# coworking_agendamento/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from reservas import views as reservas_views  # Importe a view index

urlpatterns = [
    path('admin/', admin.site.urls),
    # Define a view index como a página inicial
    
    path('', reservas_views.index, name='index'),
    
    path('login/', auth_views.LoginView.as_view(template_name='reservas/login.html'), name='login'),  # Página de login
    
    path('reservas/', include('reservas.urls')),  # Inclui URLs do app reservas

    path('lista/', include('reservas.urls')), 
    
    path('register/', reservas_views.register, name='register'),  # Página de registro
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
