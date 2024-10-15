from django.shortcuts import render, redirect, get_object_or_404  # Importation des fonctions pour rendre des templates et rediriger
from .models import Review, Ticket, UserFollows, Comment  # Importation des modèles nécessaires
from django.contrib.auth import authenticate, login, get_user_model  # Importation des fonctions d'authentification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm  # Importation du formulaire d'authentification
from django.contrib import messages  # Importation du module pour les messages flash
from .forms import CustomUserCreationForm, TicketForm, CommentForm # Importation du formulaire personnalisé pour l'inscription des utilisateurs
from itertools import chain
from django.db.models import CharField, Value
from django.db import models



def register_view(request):
    """Vue pour gérer l'inscription d'un nouvel utilisateur."""
    if request.method == 'POST':  # Vérifie si la méthode de la requête est POST
        form = CustomUserCreationForm(request.POST)  # Crée une instance du formulaire avec les données POST
        if form.is_valid():  # Cette ligne vérifie si les données du formulaire sont valides
            user = form.save()  # Enregistre l'utilisateur dans la base de données
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('feed')  # Redirection vers la page d'accueil ou 'feed'
        else:
            print(form.errors)  # Affiche les erreurs de formulaire dans la console
    else:
        form = CustomUserCreationForm()  # Crée un formulaire vide pour la première fois

    return render(request, 'register.html', {'form': form})  # Rendu du template avec le formulaire


def get_users_viewable_reviews(user):
    """Retourne les critiques des utilisateurs suivis par l'utilisateur donné et ses propres critiques."""
    # Récupère les utilisateurs suivis par l'utilisateur donné
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    
    # Obtenir les critiques des utilisateurs suivis et les critiques de l'utilisateur lui-même
    reviews = Review.objects.filter(user__in=followed_users).union(Review.objects.filter(user=user))
    
    return reviews  # Retourne les critiques trouvées


def get_users_viewable_tickets(user):
    """Retourne les tickets des utilisateurs suivis par l'utilisateur donné et ses propres tickets."""
    # Récupère les utilisateurs suivis par l'utilisateur donné
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    
    # Obtenir les tickets des utilisateurs suivis et les tickets de l'utilisateur lui-même
    tickets = Ticket.objects.filter(user__in=followed_users).union(Ticket.objects.filter(user=user))
    
    return tickets  # Retourne les tickets trouvés


@login_required
def feed(request):
    user = request.user  # Récupérer l'utilisateur actuellement connecté

    # Récupérer les utilisateurs suivis (des instances de CustomUser)
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

    # Récupérer tous les tickets (de l'utilisateur et des utilisateurs suivis)
    tickets = Ticket.objects.filter(
        models.Q(user=user) | models.Q(user__in=followed_users)
    ).annotate(content_type=Value('TICKET', CharField()))

    # Récupérer toutes les critiques (de l'utilisateur et des utilisateurs suivis)
    reviews = Review.objects.filter(
        models.Q(user=user) | models.Q(user__in=followed_users)
    ).annotate(content_type=Value('REVIEW', CharField()))

    # Récupérer les critiques sur les billets de l'utilisateur (postées par n'importe qui)
    reviews_on_user_tickets = Review.objects.filter(
        ticket__user=user
    ).annotate(content_type=Value('REVIEW', CharField()))

    # Utiliser la fonction chain() pour combiner les différents querysets (billets et avis) 
    # en une seule liste de "posts"
    posts = sorted(
        chain(
            tickets,
            reviews,
            reviews_on_user_tickets
        ),
        # Trier les posts selon le champ "time_created" (date de création) 
        # en ordre décroissant (les plus récents en premier)
        key=lambda post: post.time_created,
        reverse=True
    )

    # Renvoyer la page 'feed.html' avec les posts combinés dans le contexte
    return render(request, 'feed.html', {'posts': posts})


def login_view(request):
    """Gère la connexion de l'utilisateur."""
    if request.method == 'POST':  # Vérifie si la méthode de la requête est POST
        form = AuthenticationForm(request, data=request.POST)  # Crée une instance du formulaire d'authentification
        if form.is_valid():  # Vérifie si le formulaire est valide
            username = form.cleaned_data.get('username')  # Récupère le nom d'utilisateur du formulaire
            password = form.cleaned_data.get('password')  # Récupère le mot de passe du formulaire
            user = authenticate(username=username, password=password)  # Authentifie l'utilisateur
            if user is not None:  # Vérifie si l'utilisateur existe
                login(request, user)  # Connecte l'utilisateur
                messages.success(request, f"Bienvenue {username} !")  # Affiche un message de succès
                return redirect('feed')  # Redirection vers la page principale après connexion
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")  # Message d'erreur si l'authentification échoue
        else:
            messages.error(request, "Erreur lors de la soumission du formulaire.")  # Message d'erreur si le formulaire est invalide
    else:
        form = AuthenticationForm()  # Crée un formulaire vide pour la première fois
    
    return render(request, 'login.html', {'form': form})  # Rendu du template avec le formulaire d'authentification

# Vue pour ajouter un billet
@login_required  # L'utilisateur doit être connecté pour accéder à cette vue
def add_ticket(request):
    if request.method == 'POST':  # Vérifie si le formulaire est soumis (POST)
        form = TicketForm(request.POST)  # Remplit le formulaire avec les données soumises
        if form.is_valid():  # Vérifie si le formulaire est valide
            ticket = form.save(commit=False)  # Crée un objet Ticket mais ne l'enregistre pas encore
            ticket.user = request.user  # Associe le billet à l'utilisateur connecté
            ticket.save()  # Sauvegarde le billet dans la base de données
            return redirect('feed')  # Redirige l'utilisateur vers la page "feed" après l'ajout
    else:
        form = TicketForm()  # Crée un formulaire vide pour l'ajout d'un billet

    return render(request, 'add_ticket.html', {'form': form})  # Rendu du template d'ajout avec le formulaire

# Vue pour modifier un billet existant
@login_required
def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)  # Récupère le billet à modifier grâce à son ID
    
    if ticket.user != request.user:  # Vérifie que l'utilisateur connecté est bien l'auteur du billet
        return redirect('feed')  # Si ce n'est pas l'auteur, redirige vers le feed
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)  # Remplit le formulaire avec les données soumises et les données du billet existant
        if form.is_valid():
            form.save()  # Sauvegarde les modifications
            return redirect('feed')  # Redirige vers la page "feed" après la modification
    else:
        form = TicketForm(instance=ticket)  # Pré-remplit le formulaire avec les informations du billet existant

    return render(request, 'edit_ticket.html', {'form': form})  # Rendu du template de modification avec le formulaire

# Vue pour supprimer un billet
@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)  # Récupère le billet à supprimer grâce à son ID
    
    if ticket.user != request.user:  # Vérifie que l'utilisateur connecté est l'auteur du billet
        return redirect('feed')  # Si ce n'est pas l'auteur, redirige vers le feed
    
    if request.method == 'POST':  # Vérifie que la requête est bien une méthode POST pour la suppression
        ticket.delete()  # Supprime le billet
        return redirect('feed')  # Redirige vers la page "feed" après la suppression

    return render(request, 'delete_ticket.html', {'ticket': ticket})  # Affiche une page demandant confirmation avant suppression

# Vue pour ajouter un commentaire
def add_comment(request):
    if request.method == 'POST':  # Vérifie si la requête est de type POST
        form = CommentForm(request.POST)  # Remplit le formulaire avec les données soumises
        if form.is_valid():  # Vérifie que le formulaire est valide
            comment = form.save(commit=False)  # Crée un objet Comment sans le sauvegarder
            comment.user = request.user  # Associe le commentaire à l'utilisateur connecté
            comment.save()  # Sauvegarde le commentaire dans la base de données
            return redirect('feed')  # Redirige l'utilisateur vers la page 'feed'
    else:
        form = CommentForm()  # Si ce n'est pas une requête POST, affiche un formulaire vide

    return render(request, 'add_comment.html', {'form': form})  # Renvoie la page avec le formulaire

# Vue pour modifier un commentaire
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Récupère le commentaire ou renvoie une erreur 404
    
    if comment.user != request.user:  # Vérifie que l'utilisateur connecté est bien celui qui a créé le commentaire
        return redirect('feed')  # Si ce n'est pas le cas, on le redirige

    if request.method == 'POST':  # Si la requête est de type POST
        form = CommentForm(request.POST, instance=comment)  # Remplit le formulaire avec les données du POST et du commentaire existant
        if form.is_valid():  # Vérifie que les données sont valides
            form.save()  # Sauvegarde les modifications
            return redirect('feed')  # Redirige vers la page 'feed'
    else:
        form = CommentForm(instance=comment)  # Sinon, affiche le formulaire pré-rempli avec les données existantes

    return render(request, 'edit_comment.html', {'form': form})  # Renvoie la page de modification avec le formulaire

# Vue pour supprimer un commentaire
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Récupère le commentaire ou renvoie une erreur 404
    
    if comment.user != request.user:  # Vérifie que l'utilisateur est celui qui a créé le commentaire
        return redirect('feed')  # Redirige si ce n'est pas le cas

    if request.method == 'POST':  # Si la requête est de type POST (pour la suppression)
        comment.delete()  # Supprime le commentaire
        return redirect('feed')  # Redirige vers la page 'feed'

    return render(request, 'delete_comment.html', {'comment': comment})  # Affiche une page de confirmation de suppression

@login_required  # Décorateur pour exiger que l'utilisateur soit connecté avant d'accéder à cette vue
def list_followed_users(request):  # Vue pour lister les utilisateurs suivis par l'utilisateur connecté
    followed_users = UserFollows.objects.filter(user=request.user)  # Récupérer tous les utilisateurs suivis par l'utilisateur connecté
    return render(request, 'followed_users_list.html', {'followed_users': followed_users})  # Retourner la page HTML avec les utilisateurs suivis

@login_required  # Décorateur pour exiger que l'utilisateur soit connecté avant d'accéder à cette vue
def add_follow(request):  # Vue pour ajouter un utilisateur à suivre
    if request.method == 'POST':  # Vérifie si la requête est de type POST (formulaire soumis)
        username_to_follow = request.POST.get('username')  # Récupère le nom d'utilisateur saisi dans le formulaire
        try:
            user_to_follow = get_user_model().objects.get(username=username_to_follow)  # Récupère l'utilisateur par son nom d'utilisateur
            if user_to_follow == request.user:  # Vérifie que l'utilisateur ne se suit pas lui-même
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")  # Affiche un message d'erreur si c'est le cas
            elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():  # Vérifie si l'utilisateur suit déjà cette personne
                messages.error(request, "Vous suivez déjà cet utilisateur.")  # Affiche un message si la relation existe déjà
            else:
                UserFollows.objects.create(user=request.user, followed_user=user_to_follow)  # Crée une nouvelle relation de suivi
                messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")  # Affiche un message de succès
            return redirect('list_followed_users')  # Redirige vers la page des utilisateurs suivis
        except get_user_model.DoesNotExist:  # Si l'utilisateur n'existe pas dans la base de données
            messages.error(request, "Cet utilisateur n'existe pas.")  # Affiche un message d'erreur
    
    return render(request, 'add_follow.html')  # Affiche la page avec le formulaire d'ajout si la requête n'est pas de type POST


@login_required  # Décorateur pour exiger que l'utilisateur soit connecté avant d'accéder à cette vue
def remove_follow(request, follow_id):  # Vue pour supprimer un utilisateur suivi
    try:
        follow = UserFollows.objects.get(id=follow_id, user=request.user)  # Récupère la relation de suivi en fonction de l'ID et de l'utilisateur connecté
        follow.delete()  # Supprime la relation de suivi
        messages.success(request, f"Vous avez cessé de suivre {follow.followed_user.username}.")  # Affiche un message de succès
    except UserFollows.DoesNotExist:  # Si la relation de suivi n'existe pas
        messages.error(request, "Relation de suivi introuvable.")  # Affiche un message d'erreur
    
    return redirect('list_followed_users')  # Redirige vers la page des utilisateurs suivis




# Vérifie si l'utilisateur est le propriétaire du ticket.
# def user_is_ticket_owner(ticket, user):
#     return ticket.user == user
