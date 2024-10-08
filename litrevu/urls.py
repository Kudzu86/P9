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
from reviews import views  # Assurez-vous d'importer vos vues

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pour accéder à l'interface d'administration
    path('login/', views.login_view, name='login'),  # Route pour la connexion
    path('feed/', views.feed, name='feed'),  # Route pour le fil d'actualité
    path('register/', views.register_view, name='register'),
]
