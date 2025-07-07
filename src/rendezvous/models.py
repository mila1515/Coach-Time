# Create your models here.
import os
from django.db import models
from django.contrib.auth.models import User
from datetime import time

# Create your models here.
class Seance(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seances_coach')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seances_client')
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    objet = models.CharField(max_length=255)
    notes_coach = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.client.username} avec {self.coach.username} le {self.date} de {self.heure_debut} à {self.heure_fin}"



class Document(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    fichier = models.FileField(upload_to='documents_clients/')
    titre = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.client.username})"

    @property
    def filename(self):
        return os.path.basename(self.fichier.name)


# rendezvous/models.py


class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    reponse_coach = models.TextField(blank=True, null=True)  # Réponse du coach
    signalement = models.BooleanField(default=False)  # Marqué comme arnaque ou abus
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # utilisateur qui a posté

    def __str__(self):
        
        return f"{self.nom} - {self.message[:30]}... - {self.date.strftime('%d %b %Y')}"





class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
