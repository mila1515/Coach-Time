from django import forms
from django.contrib.auth.models import User
from .models import Seance , Document
from .models import Temoignage

import datetime

class SeanceForm(forms.ModelForm):
    coach = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), label="Coach")
    heure_debut = forms.ChoiceField(choices=[], label="Heure")
    
    class Meta:
        model = Seance
        fields = ['coach', 'date', 'heure_debut', 'heure_fin', 'objet']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        heure_debut = cleaned_data.get("heure_debut")
        heure_fin = cleaned_data.get("heure_fin")

        # Validation horaire logique
        if heure_debut and heure_fin and heure_fin <= heure_debut:
            raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")

        # Validation de l'heure dans la plage autorisée (9h-18h)
        if heure_debut and not (datetime.time(9, 0) <= heure_debut <= datetime.time(18, 0)):
            raise forms.ValidationError("L'heure de début doit être entre 9h et 18h.")

        if heure_fin and not (datetime.time(9, 0) <= heure_fin <= datetime.time(18, 0)):
            raise forms.ValidationError("L'heure de fin doit être entre 9h et 18h.")



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'fichier']



class TemoignageForm(forms.ModelForm):
    class Meta:
        model = Temoignage
        fields = ['nom', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre témoignage'}),
        }




class ReponseCoachForm(forms.ModelForm):
    class Meta:
        model = Temoignage
        fields = ['reponse_coach']
        widgets = {
            'reponse_coach': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre réponse...'}),
        }
