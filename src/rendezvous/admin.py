

# Register your models here.
from django.contrib import admin
from .models import Seance
from .models import Temoignage


@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'heure_debut', 'client', 'objet', 'notes_coach')


admin.site.register(Temoignage)

# class TemoignageAdmin(admin.ModelAdmin):
#     list_display = ('nom', 'date')
#     search_fields = ('nom', 'message')
#     list_filter = ('date',)

#     def has_add_permission(self, request):
#         return False  # Désactiver l'ajout de témoignages via l'admin

#     def has_delete_permission(self, request, obj=None):
#         return False  # Désactiver la suppression de témoignages via l'admin