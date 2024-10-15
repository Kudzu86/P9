"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# litrevu/urls.py (ou your_app_name/urls.py si vous souhaitez garder le nom de votre application)
from django.contrib import admin
from django.urls import path
from reviews import views  
from django.contrib.auth.views import LogoutView  # Importation de la vue de déconnexion


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),  # URL pour accéder à l'interface d'administration
    path('login/', views.login_view, name='login'),  # Route pour la connexion
    path('', views.feed, name='feed'),  # Route pour le fil d'actualité
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Route pour la déconnexion
    path('ticket/add/', views.add_ticket, name='add_ticket'),  # Route pour ajouter un billet
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),  # Route pour modifier un billet existant
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),  # Route pour supprimer un billet
    path('add_comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('follows/', views.list_followed_users, name='list_followed_users'),  # URL pour lister les utilisateurs suivis
    path('follows/add/', views.add_follow, name='add_follow'),  # URL pour ajouter un utilisateur suivi
    path('follows/remove/<int:follow_id>/', views.remove_follow, name='remove_follow'),  # URL pour supprimer un utilisateur suivi
]
