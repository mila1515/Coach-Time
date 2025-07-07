from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout , authenticate
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Seance , Document , Temoignage
from .forms import SeanceForm , DocumentForm , TemoignageForm
from django.views import View
from django.http import HttpResponseForbidden , JsonResponse
from .utils import est_disponible, heures_disponibles
from django.contrib import messages
import datetime
from .forms import ReponseCoachForm  # formulaire à créer


def accueil(request):
    temoignages = Temoignage.objects.filter(signalement=False).order_by('-date')
    return render(request, 'rendezvous/accueil.html', {'temoignages': temoignages})



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'rendezvous/signup.html', {'form': form})



@login_required
def dashboard(request):
    user = request.user

    if user.groups.filter(name='coach').exists():
        # Coach voit toutes les séances
        seances = Seance.objects.all().order_by('date', 'heure_debut')
        template = 'rendezvous/dashboard_coach.html'
        context = {'seances': seances}
    else:
        # Client voit seulement ses séances
        seances = Seance.objects.filter(client=user).order_by('date', 'heure_debut')
        documents = Document.objects.filter(client=user)
        document_form = DocumentForm(request.POST or None, request.FILES or None)

        # Upload document
        if request.method == 'POST' and 'upload_document' in request.POST:
            if document_form.is_valid():
                doc = document_form.save(commit=False)
                doc.client = user
                doc.save()
                return redirect('dashboard')

        template = 'rendezvous/dashboard_client.html'
        context = {
            'seances': seances,
            'user': user,
            'documents': documents,
            'document_form': document_form
        }

    return render(request, template, context)



@login_required
def prise_rdv(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.client = request.user

            coach = form.cleaned_data['coach']
            date = form.cleaned_data['date']
            heure_debut = form.cleaned_data['heure_debut']
            heure_fin = form.cleaned_data['heure_fin']

            if est_disponible(coach, request.user, date, heure_debut, heure_fin):
                seance.save()
                messages.success(request, "Votre rendez-vous a bien été réservé.")
                return redirect('dashboard')
            else:
                messages.error(request, "Ce créneau est déjà réservé. Choisissez une autre heure.")
    else:
        form = SeanceForm()
    
    return render(request, 'rendezvous/prise_rdv.html', {'form': form})




class LogoutViewGET(View):
    def get(self, request):
        logout(request)
        return redirect('accueil')




@login_required
def supprimer_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    if document.client != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce document.")

    if request.method == 'POST':
        document.delete()
        return redirect('dashboard')  # Retour vers le dashboard après suppression

    # Sinon méthode GET : afficher page de confirmation
    return render(request, 'rendezvous/confirmation_suppression.html', {'document': document})




def connexion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirection selon rôle
            if user.seances_coach.exists():
                return redirect('dashboard_coach')
            elif user.seances_client.exists():
                return redirect('dashboard_client')
            else:
                return redirect('dashboard_mixte')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'rendezvous/login.html', {'form': form})




def heures_disponibles(request):
    coach_id = request.GET.get('coach_id')
    date_str = request.GET.get('date')

    if not coach_id or not date_str:
        return JsonResponse({'error': 'Données manquantes'}, status=400)

    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    heures = [datetime.time(h, 0) for h in range(9, 18)]
    seances = Seance.objects.filter(coach_id=coach_id, date=date)
    heures_occupees = [s.heure_debut for s in seances]
    heures_libres = [h.strftime('%H:%M') for h in heures if h not in heures_occupees]

    return JsonResponse({'heures': heures_libres})


def ajouter_temoignage(request):
    if request.method == 'POST':
        form = TemoignageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')  # ou une autre page après soumission
    else:
        form = TemoignageForm()
    return render(request, 'rendezvous/ajouter_temoignage.html', {'form': form})





def repondre_temoignage(request, pk):
    temoignage = get_object_or_404(Temoignage, pk=pk)
    if not request.user.is_coach:  # tu devras définir ce booléen dans User
        return redirect('accueil')
    if request.method == 'POST':
        form = ReponseCoachForm(request.POST, instance=temoignage)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = ReponseCoachForm(instance=temoignage)
    return render(request, 'rendezvous/repondre_temoignage.html', {'form': form, 'temoignage': temoignage})

def signaler_temoignage(request, pk):
    temoignage = get_object_or_404(Temoignage, pk=pk)
    temoignage.signalement = True
    temoignage.save()
    return redirect('accueil')

def supprimer_temoignage(request, pk):
    if not request.user.is_staff:  # seul admin peut supprimer
        return redirect('accueil')
    temoignage = get_object_or_404(Temoignage, pk=pk)
    temoignage.delete()
    return redirect('accueil')



@login_required
def coach_dashboard(request):
    seances = Seance.objects.filter(coach=request.user).order_by('date')
    coach_profile = CoachProfile.objects.get(user=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        notifications = request.POST.get('notifications') == 'on'

        request.user.email = email
        request.user.save()

        coach_profile.bio = bio
        coach_profile.notifications = notifications
        coach_profile.save()

        messages.success(request, "Paramètres mis à jour avec succès.")
        return redirect('coach_dashboard')

    return render(request, 'rendezvous/coach_dashboard.html', {
        'seances': seances,
        'coach_profile': coach_profile,
    })
