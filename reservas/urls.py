# reservas/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial que lista os espaços
    path('', views.lista_espacos, name='lista_espacos'),
   
    path('espaco/<int:espaco_id>/', views.detalhe_espaco, name='detalhe_espaco'),  # Detalhe de um espaço específico
   
    path('login/', auth_views.LoginView.as_view(template_name='reservas/login.html'), name='login'),  # Página de login
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Página de logout
    
    path('register/', views.register, name='register'),  # Página de registro
    # Página para gerenciar espaços
    path('gerenciar/', views.gerenciar_espacos, name='gerenciar_espacos'),
  
    path('newsletter_signup/', views.newsletter_signup, name='newsletter_signup'),
]
