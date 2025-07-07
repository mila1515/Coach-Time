# rendezvous/utils.py
from django.db.models import Q
from .models import Seance
from django.http import JsonResponse
import datetime

def est_disponible(coach, client, date, heure_debut, heure_fin):
    # Vérifie les conflits du coach
    rdv_coach = Seance.objects.filter(
        coach=coach,
        date=date,
        heure_debut__lt=heure_fin,
        heure_fin__gt=heure_debut
    ).exists()
    
    # Vérifie les conflits du client
    rdv_client = Seance.objects.filter(
        client=client,
        date=date,
        heure_debut__lt=heure_fin,
        heure_fin__gt=heure_debut
    ).exists()

    return not (rdv_coach or rdv_client)




def heures_disponibles(request):
    coach_id = request.GET.get('coach_id')
    date_str = request.GET.get('date')

    if not coach_id or not date_str:
        return JsonResponse({'error': 'Données manquantes'}, status=400)

    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    # Générer les heures de 9h à 18h
    heures = [datetime.time(h, 0) for h in range(9, 18)]

    # Filtrer les séances existantes du coach ce jour-là
    seances = Seance.objects.filter(coach_id=coach_id, date=date)

    # Retirer les heures déjà prises
    heures_occupees = [s.heure_debut for s in seances]
    heures_libres = [h.strftime('%H:%M') for h in heures if h not in heures_occupees]

    return JsonResponse({'heures': heures_libres})
