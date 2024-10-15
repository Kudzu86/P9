# LitreVu

LitreVu est une application web permettant aux utilisateurs de partager leurs critiques de livres et de suivre les billets des utilisateurs qu'ils apprécient. Ce projet a été développé en utilisant Django, un framework web Python, et propose une interface simple et intuitive pour découvrir de nouveaux livres et partager des avis.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Auteurs](#auteurs)
- [Licence](#licence)

## Fonctionnalités

- Authentification des utilisateurs : Connexion, déconnexion et enregistrement.
- Ajout et gestion de billets (tickets) et de critiques (reviews).
- Suivi des utilisateurs : Suivez d'autres utilisateurs et visualisez leur contenu dans votre flux.
- Interface utilisateur responsive et intuitive.

## Technologies Utilisées

- **Django** : Framework web Python.
- **SQLite** : Base de données utilisée pour le développement.
- **HTML/CSS** : Pour le rendu de l'interface utilisateur.
- **Bootstrap** : Pour la conception réactive et esthétique de l'application.

## Installation

Pour installer et exécuter ce projet sur votre machine locale, suivez les étapes suivantes :

1. **Clonez le dépôt** :

   ```bash
   git clone https://github.com/Kudzu86/P9.git
   ```

2. **Naviguez dans le répertoire du projet** :

   ```bash
   cd P9/mon_projet
   ```

3. **Créez un environnement virtuel** :

   ```bash
   python -m venv env
   ```

4. **Activez l'environnement virtuel** :

   - Sur Windows :

     ```bash
     .\env\Scripts\activate
     ```

   - Sur macOS/Linux :

     ```bash
     source env/bin/activate
     ```

5. **Installez les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

6. **Appliquez les migrations** :

   ```bash
   python manage.py migrate
   ```

7. **Démarrez le serveur de développement** :

   ```bash
   python manage.py runserver
   ```

8. **Ouvrez votre navigateur** et allez à l'adresse suivante :

   ```
   http://127.0.0.1:8000/
   ```

## Utilisation

Après avoir démarré le serveur, vous pouvez vous inscrire ou vous connecter pour commencer à utiliser l'application. Vous pourrez alors créer des billets, suivre d'autres utilisateurs et consulter leur contenu dans votre flux.

## Contribuer

Si vous souhaitez contribuer à ce projet, veuillez suivre ces étapes :

1. Fork ce dépôt.
2. Créez une nouvelle branche pour votre fonctionnalité ou correctif :
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Effectuez vos modifications et ajoutez des commits.
4. Poussez vos modifications :
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Créez une Pull Request.

## Auteurs

- **Kudzu86** - *Développeur principal* - [Kudzu86](https://github.com/Kudzu86)

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
