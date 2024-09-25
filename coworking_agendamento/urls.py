# coworking_agendamento/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from reservas import views as reservas_views  # Importe a view index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', reservas_views.index, name='index'),
    
    # Login, logout e registro de usuários
    path('login/', auth_views.LoginView.as_view(template_name='reservas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', reservas_views.register, name='register'),
    
    # Incluindo URLs da app 'reservas'
    path('reservas/', include('reservas.urls')),
    path('lista/', include('reservas.urls')),
    path('administrar/', reservas_views.administrar_espacos, name='administrar_espacos'),

    # URLs para gerenciamento de espaços de coworking
    path('espaco/novo/', reservas_views.editar_espaco_coworking, name='criar_espaco'),
    path('espaco/<int:espaco_id>/editar/', reservas_views.editar_espaco_coworking, name='editar_espaco'),
    

    # Allauth (login via contas sociais)
    path('accounts/', include('allauth.urls')),  









]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)