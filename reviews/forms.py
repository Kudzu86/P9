from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ticket, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'gender')  # Ajoutez d'autres champs si nécessaire

class TicketForm(forms.ModelForm):
    # Classe Meta pour spécifier le modèle lié et les champs utilisés
    class Meta:
        model = Ticket  # Le formulaire se base sur le modèle Ticket
        fields = ['title', 'description']  # Le formulaire ne montrera que le titre et la description

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Utilise le modèle Comment
        fields = ['body']  # Inclut uniquement le champ 'body' (contenu du commentaire)