from django.core.validators import MinValueValidator, MaxValueValidator  # Importation des validateurs pour les champs
from django.conf import settings  # Importation des paramètres de configuration de Django
from django.db import models  # Importation du module pour définir des modèles Django
from django.contrib.auth.models import AbstractUser  # Importation de la classe de base pour les utilisateurs


class CustomUser(AbstractUser):  # Définition d'un modèle utilisateur personnalisé en étendant AbstractUser
    email = models.EmailField(unique=True)  # Champ email, doit être unique pour chaque utilisateur
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):  # Méthode pour définir la représentation en chaîne de l'utilisateur
        return self.username  # Retourne le nom d'utilisateur


class Ticket(models.Model):  # Définition du modèle Ticket
    title = models.CharField(max_length=128)  # Champ pour le titre du ticket
    description = models.TextField(max_length=2048, blank=True)  # Champ optionnel pour la description du ticket
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relation avec le modèle utilisateur
    time_created = models.DateTimeField(auto_now_add=True)  # Date de création du ticket, ajoutée automatiquement

    def __str__(self):  # Méthode pour définir la représentation en chaîne du ticket
        return self.title  # Retourne le titre du ticket


class Review(models.Model):  # Définition du modèle Review
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)  # Relation avec le modèle Ticket
    rating = models.PositiveSmallIntegerField(  # Champ pour la note, un entier positif
        # valide que la note doit être entre 0 et 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])  # Validateurs pour limiter les valeurs
    headline = models.CharField(max_length=128)  # Champ pour le titre de la critique
    body = models.CharField(max_length=8192, blank=True)  # Champ optionnel pour le corps de la critique
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relation avec le modèle utilisateur
    time_created = models.DateTimeField(auto_now_add=True)  # Date de création de la critique, ajoutée automatiquement


class UserFollows(models.Model):  # Définition du modèle UserFollows pour gérer les suivis
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')  # Utilisateur qui suit
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')  # Utilisateur suivi

    class Meta:  # Classe Meta pour définir des options supplémentaires
        # Assure qu'il n'y a pas de doublons dans les instances UserFollows
        # pour des paires utilisateur-utilisateur suivis uniques
        unique_together = ('user', 'followed_user', )  # Définir la contrainte d'unicité


class Comment(models.Model):
    body = models.TextField(max_length=2048)  # Le contenu du commentaire, limité à 2048 caractères
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relation avec le modèle utilisateur, supprime le commentaire si l'utilisateur est supprimé
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)  # Relation avec le modèle Ticket, supprime le commentaire si le ticket est supprimé
    time_created = models.DateTimeField(auto_now_add=True)  # Date de création du commentaire, ajoutée automatiquement

    def __str__(self):  # Méthode pour définir la représentation en chaîne du commentaire
        return f'Comment by {self.user} on {self.ticket}'  # Retourne une description du commentaire
