from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import LogoutViewGET



urlpatterns = [
    path('ajouter-temoignage/', views.ajouter_temoignage, name='ajouter_temoignage'),
    path('connexion/', views.connexion, name='connexion'),
    path('ajax/heures-disponibles/', views.heures_disponibles, name='heures_disponibles'),
    path('document/supprimer/<int:document_id>/', views.supprimer_document, name='supprimer_document'),
    path('prendre-rdv/', views.prise_rdv, name='prendre_rdv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.accueil, name='accueil'),
    path('login/', auth_views.LoginView.as_view(template_name='rendezvous/login.html'), name='login'),
    path('logout/', views.LogoutViewGET.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]