# Coach-Time

Coach-Time est une application web de coaching personnel développée avec Django. Elle permet la gestion des rendez-vous, des ateliers, des documents clients, des témoignages, et bien plus, pour les coachs et leurs clients.

## Fonctionnalités principales

- Gestion des séances de coaching (prise de rendez-vous, annulation, notes, packs de séances)
- Gestion des ateliers (création, inscription, suivi des présences)
- Espace coach et espace client personnalisés
- Téléversement et gestion de documents pour les clients
- Système de témoignages et réponses du coach
- Gestion des indisponibilités du coach
- Actualités et page d’informations générales
- Formulaire de contact

## Prérequis

- Python 3.8+
- pip
- Virtualenv (recommandé)
- [Django](https://www.djangoproject.com/) (voir requirements.txt pour la version exacte)

## Installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/mila1515/Coach-Time.git
   cd Coach-Time/src
   ```

2. **Créer et activer un environnement virtuel :**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Sur Windows
   # ou
   source venv/bin/activate  # Sur Mac/Linux
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Appliquer les migrations :**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur (admin) :**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur de développement :**
   ```bash
   python manage.py runserver
   ```

7. Accéder à l’application sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Structure du projet

```
Coach-Time/
│
├── src/
│   ├── coach_project/         # Configuration principale Django
│   ├── rendezvous/            # Application principale (modèles, vues, templates)
│   ├── static/                # Fichiers statiques (CSS, images)
│   ├── media/                 # Fichiers uploadés (documents, photos)
│   └── manage.py              # Commande de gestion Django
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

## Configuration

- Les fichiers uploadés sont stockés dans `src/media/`.
- Les fichiers statiques sont dans `src/static/`.
- Les paramètres de la base de données et autres configurations sont dans `src/coach_project/settings.py`.

## Personnalisation

- Les styles CSS sont sobres et professionnels, inspirés de l’univers du coaching.
- Les templates HTML sont dans `src/rendezvous/templates/rendezvous/`.

## Déploiement

Pour un déploiement en production, il est recommandé d’utiliser un serveur WSGI (ex : Gunicorn), de configurer un serveur web (ex : Nginx), et d’utiliser une base de données robuste (ex : PostgreSQL). Pensez à configurer les variables d’environnement pour la sécurité.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d’informations. 