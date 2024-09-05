# reservas/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial que lista os espaços
    path('', views.lista_espacos, name='lista_espacos'),
   
    path('espaco/<int:espaco_id>/', views.detalhe_espaco, name='detalhe_espaco'),  # Detalhe de um espaço específico
    
    
    
    # Página para gerenciar espaços
    path('gerenciar/', views.gerenciar_espacos, name='gerenciar_espacos'),
  
    path('newsletter_signup/', views.newsletter_signup, name='newsletter_signup'),
]
