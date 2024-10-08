from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render, redirect
from .models import Review, Ticket, UserFollows
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # Cette ligne vérifie si les données du formulaire sont valides
            user = form.save()  # Enregistre l'utilisateur dans la base de données
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('feed')  # Redirection vers la page d'accueil ou 'feed'
        else:
            print(form.errors)  # Affiche les erreurs de formulaire dans la console
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def get_users_viewable_reviews(user):
    """Retourne les critiques des utilisateurs suivis par l'utilisateur donné et ses propres critiques."""
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    
    # Obtenir les critiques des utilisateurs suivis et les critiques de l'utilisateur lui-même
    reviews = Review.objects.filter(user__in=followed_users).union(Review.objects.filter(user=user))
    
    return reviews


def get_users_viewable_tickets(user):
    """Retourne les tickets des utilisateurs suivis par l'utilisateur donné et ses propres tickets."""
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    
    # Obtenir les tickets des utilisateurs suivis et les tickets de l'utilisateur lui-même
    tickets = Ticket.objects.filter(user__in=followed_users).union(Ticket.objects.filter(user=user))
    
    return tickets


@login_required
def feed(request):
    """Affiche les critiques et billets (tickets) des utilisateurs suivis et de l'utilisateur connecté."""
    reviews = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    
    tickets = get_users_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    
    # Combine les critiques et les billets, puis les trie par date
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, 'feed.html', context={'posts': posts})


def login_view(request):
    """Gère la connexion de l'utilisateur."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} !")
                return redirect('feed')  # Redirection vers la page principale après connexion
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur lors de la soumission du formulaire.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})
