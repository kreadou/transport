
from django.contrib import admin
from .models import *

admin.site.register(Continent)
admin.site.register(Pays)
admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(Ville)
admin.site.register(Commune)
admin.site.register(Fonction)
admin.site.register(Profil)
admin.site.register(Trajet)
admin.site.register(Client)
admin.site.register(Fournisseur)
admin.site.register(Depense)
admin.site.register(Tarification)
admin.site.register(Chauffeur)
admin.site.register(Vehicule)
admin.site.register(Marque)
admin.site.register(Carburant)

admin.site.register(Marchandise)
admin.site.register(Detailscommande)

admin.site.register(Pompe)
admin.site.register(Societe)

admin.site.register(Reparation)
admin.site.register(Entretien)
admin.site.register(Facturation)

admin.site.register(Reglement)
admin.site.register(Planning)
admin.site.register(Alerte)

admin.site.register(Detailsdevis)
admin.site.register(Para)

class DetailscommandeInline(admin.TabularInline):
    model = Detailscommande
    extra = 3


class CommandeAdmin(admin.ModelAdmin):
    inlines = (DetailscommandeInline,)

#class MembreAdmin(admin.ModelAdmin):
#    inlines = (JuryInline,)

admin.site.register(Commande, CommandeAdmin)



class EnlevementInline(admin.TabularInline):
    model = Enlevement
    extra = 3

class OrdretransportAdmin(admin.ModelAdmin):
    inlines = (EnlevementInline,)

admin.site.register(Ordretransport, OrdretransportAdmin)
admin.site.register(Enlevement)


class DetailsdevisInline(admin.TabularInline):
    model = Detailsdevis
    extra = 3


class DevisAdmin(admin.ModelAdmin):
    inlines = (DetailsdevisInline,)

admin.site.register(Devis, DevisAdmin)




