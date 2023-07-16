 #-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Utilitaire import *#dateAnglaisFrancais, iif, millier
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
#from multipleselectionfield import MultipleSelectionField
from django.core.validators import RegexValidator

from django.core.validators import int_list_validator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q, Sum, Avg, F

from django.shortcuts import render, get_object_or_404

MODE_REGLEMENTS = (('Chèque', 'Chèque'), ('Espèce', 'Espèce'), ('Virement', 'Virement'))
CIVILITES = (('M.', 'M.'), ('Mme', 'Mme'), ('Mlle', 'Mlle'))


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Continent(models.Model):
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    
    class Meta:
        ordering=('libelle',)
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Pays(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, verbose_name="continent")
    libelle = models.CharField(max_length=255, unique=True, verbose_name="libellé")
    
    class Meta:
        ordering=('libelle',)   
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Region(models.Model):
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, verbose_name="pays")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="libellé")
    
    class Meta:
        ordering=('libelle',)    
    def __str__(self):
        return "{0}".format(self.libelle)

class Departement(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="région")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="libellé")
    
    class Meta:
        ordering=('libelle',)    

    def __str__(self):
        return "{0}".format(self.libelle)

class Ville(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name="département")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="libellé")
    
    class Meta:
        ordering=('libelle',)    
    
    def __str__(self):
        return "{0}".format(self.libelle)

class Commune(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, verbose_name="ville")
    libelle = models.CharField(max_length=50, unique=True, verbose_name="libellé")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)


class Modele(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="marque")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)


class Marque(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="marque")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)


class Fonction(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="fonction")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)

class Profession(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="profession")

    class Meta:
        ordering=('libelle',)

    def __str__(self):
        return "{0}".format(self.libelle)


class Profil(TimeStampModel):
    GROUPES = (
        ('Direction', 'Direction'), 
        ('Commercial', 'Commercial'), 
        ('Comptabilité', 'Comptabilité'), 
        ('Administrateur', 'Administrateur'),
        ('Chauffeur', 'Chauffeur')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="utilisateur") # La liaison OneToOne vers le modèle User
    groupe = models.CharField(max_length=50, default="Commercial", choices=GROUPES, verbose_name="groupe")
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE, blank=True, null=True, verbose_name="fonction")
    login = models.CharField(max_length=50, verbose_name="nom de login")
    mdp = models.CharField(max_length=20, verbose_name="mot de passe")
    civilite = models.CharField(max_length=20,  default="M.", choices=CIVILITES, verbose_name="civilité")
    nom = models.CharField(max_length=100, verbose_name="nom")
    prenoms = models.CharField(max_length=100, verbose_name="prénoms")
    cellulaire = models.CharField(max_length=10, default="", blank=True, verbose_name="Cellulaire")
    email = models.CharField(max_length=200, default="", blank=True, verbose_name="E-mail")
    photo = models.ImageField(upload_to='users', blank=True, null=True, verbose_name="Photo")
    
    def __str__(self):
        return "{0}".format(self.nom.upper()+' '+self.prenoms.title())


class Trajet(models.Model):
    source = models.ForeignKey(Commune, related_name='itineraire_debut', on_delete=models.CASCADE, verbose_name="source")
    destination = models.ForeignKey(Commune, related_name='itineraire_fin', on_delete=models.CASCADE, verbose_name="destination")
    kilometrage = models.FloatField(default=20, verbose_name="kilométrage")
    
    class Meta:
        unique_together = (('source', 'destination', 'kilometrage'),)

    def __str__(self):
        return "{0}".format(self.source.libelle + ' - '+ self.destination.libelle)


class Client(models.Model):
    raison_sociale = models.CharField(max_length=100, unique=True, verbose_name="raison sociale") 
    adresse = models.CharField(max_length=150, default="", blank=True, verbose_name="adresse")
    boite_postale = models.CharField(max_length=100, default="", blank=True, verbose_name="boîte postale")
    telephone = models.CharField(max_length=30, default="", blank=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=30, default="", blank=True, verbose_name="cellulaire")
    compte_contribuable = models.CharField(max_length=50, default="", blank=True, verbose_name="compte contribuable")
    registre_commerce = models.CharField(max_length=50, default="", blank=True, verbose_name="registre commerce")
    
    class Meta:
        ordering=('raison_sociale',)
        
    def __str__(self):
        return "{0}".format(self.raison_sociale)


class Fournisseur(models.Model):
    raison_sociale = models.CharField(max_length=100, unique=True, verbose_name="raison sociale") 
    adresse = models.CharField(max_length=150, default="", blank=True, verbose_name="adresse")
    boite_postale = models.CharField(max_length=100, default="", blank=True, verbose_name="boîte postale")
    telephone = models.CharField(max_length=20, default="", blank=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=20, default="", blank=True, verbose_name="cellulaire")
    compte_contribuable = models.CharField(max_length=50, default="", blank=True, verbose_name="compte contribuable")
    registre_commerce = models.CharField(max_length=50, default="", blank=True, verbose_name="registre commerce")
 
    class Meta:
        ordering=('raison_sociale',)
        
    def __str__(self):
        return "{0}".format(self.raison_sociale)


class Pompe(models.Model):
    TYPE_CARBURANTS = (('Gazoil', 'Gazoil'), ('Essence', 'Essence'))
    type_carburant = models.CharField(max_length=10, default="Gazoil", choices=TYPE_CARBURANTS, verbose_name="type carburant")
    date_service = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date de mise en service")
    prix = models.FloatField(default=675, verbose_name="prix")
    class Meta:
        unique_together = ('type_carburant', 'date_service')
    
    def __str__(self):
        return "{0} {1} {2}".format(self.type_carburant, dateAnglaisFrancais(self.date_service), self.prix)


class Tarification(models.Model):
    MODE_TARIFICATIONS = (('Tonnage', 'Tonnage'), ('kilométrage', 'kilométrage'), ('Forfait', 'Forfait'), ('Autre', 'Autre'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client")
    mode_tarification = models.CharField(max_length=20, default="Tonnage", verbose_name="mode de tarification")
    cout = models.ImageField(default=0, verbose_name="coût unitaire")
    class Meta:
        ordering=('client',)
        
    def __str__(self):
        return "{0}".format(self.client)


class Alerte(models.Model):
    TYPE_ALERTES = [
        ('Assurance', 'Assurance'), 
        ('Visite technique', 'Visite technique'), 
        ('Stationnement', 'Stationnement'),
        ('Patente', 'Patente'), 
        ("Pièce d'identité", "Pièce d'identité"), 
        ('Permis de conduire', 'Permis de conduire'),
        ('Carte accès portuaire', 'Carte accès portuaire'),
        ('Prochain entretien en kilométrage', 'Prochain entretien en kilométrage'),
        ('Prochain entretien en date', 'Prochain entretien en date'),
    ]

    type_alerte = models.CharField(max_length=100, default="Assurance", choices=TYPE_ALERTES, unique = True, verbose_name="type d'alerte")
    delai = models.SmallIntegerField(blank=True, null=True, verbose_name="délai en jours")
    
    class Meta:
        ordering=('type_alerte',)
        
    def __str__(self):
        return "{0} {1}".format(self.type_alerte, self.delai)

    def alerte_view():    
        alerte_list = dict(Alerte.objects.values_list('type_alerte', 'delai'))
        date_jour = dateDuJour().split('/')
        vehicule_list = Vehicule.objects.all()
        chauffeur_list = Chauffeur.objects.order_by('nom', 'prenoms').all()
        entretien_list = Entretien.objects.all()

        for i in vehicule_list:
            if i.date_echeance_assurance != datetime.datetime.now().date():i.assurance = int(str(i.date_echeance_assurance - datetime.datetime.now().date()).split()[0])
            else:i.assurance=0
            print("assurance ok = ", i.immatriculation, i.assurance)
            
            if i.date_echeance_visite != datetime.datetime.now().date():i.visite = int(str(i.date_echeance_visite - datetime.datetime.now().date()).split()[0])
            else:i.visite=0    
            print("visite = ", i.visite)

            if i.date_echeance_stationnement != datetime.datetime.now().date():i.stationnement = int(str(i.date_echeance_stationnement - datetime.datetime.now().date()).split()[0])
            else:i.stationnement=0    
            print("stationnement = ", i.stationnement)

            if datetime.datetime.now().date() != i.date_echeance_patente:i.patente = int(str(i.date_echeance_patente - datetime.datetime.now().date()).split()[0])
            else:i.patente=0
            print("patente = ", i.patente)


        for i in chauffeur_list:
            if datetime.datetime.now().date() != i.piece_date_expiration:i.piece = int(str(i.piece_date_expiration - datetime.datetime.now().date()).split()[0])
            else:i.piece = 0
            print("piece = ", i.piece)

            if datetime.datetime.now().date() != i.permis_date_echeance:i.permis = int(str(i.permis_date_echeance - datetime.datetime.now().date()).split()[0])
            else:i.permis = 0    
            print("permis =  362 days, 0:00:00")
            #i.permis = int(i.permis[:len(i.permis)-14])

            if datetime.datetime.now().date() != i.carte_acces_echeance:i.acces = int(str(i.carte_acces_echeance - datetime.datetime.now().date()).split()[0])
            else:i.acces=0    
            print("acces = ", i.acces)

        for i in entretien_list:
            if datetime.datetime.now().date() != i.date_entretien_prochain:i.prochain = int(str(i.date_entretien_prochain - datetime.datetime.now().date()).split()[0])
            else:i.prochain=0
        
        return {'alerte_list': alerte_list, 'vehicule_list':vehicule_list, 'chauffeur_list':chauffeur_list, 'entretien_list':entretien_list}        


class Vehicule(models.Model):
    TYPE_VEHICULES = (('Camion', 'Camion'), ('Utilitaire', 'Utilitaire'), ('Personnel', 'Personnel'))
    TYPE_CARBURANTS = (('Gazoil', 'Gazoil'), ('Essence', 'Essence'))
    MODE_UTILISATIONS = (('Sous-Traitance', 'Sous-Traitance'), ('Patrimoine', 'Patrimoine'), )
    ASSIGNATIONS = (('Véhicule de service', 'Véhicule de service'), ('Véhicule de transport', 'Véhicule de transport'))
    ATTELAGES = (('Non attelé', 'Non attelé'), ('Remorque', 'Remorque'), ('Porte char', 'Porte char'), ('Citerne', 'Citerne'))

    marque = models.ForeignKey(Marque, default=1, on_delete=models.CASCADE, verbose_name="marque")
    modele = models.CharField(max_length=20, default="", blank=True, verbose_name="modèle")
    
    type_vehicule = models.CharField(max_length=20, default="Camion", choices=TYPE_VEHICULES, verbose_name="type de véhicules")
    type_carburant = models.CharField(max_length=10, default="Gazoil", choices=TYPE_CARBURANTS, verbose_name="type de carburant")
    mode_utilisation = models.CharField(max_length=20, default="Sous-Traitance", choices=MODE_UTILISATIONS, verbose_name="Mode d'utilisation")
    assignation = models.CharField(max_length=50, default="Véhicule de transport", choices=ASSIGNATIONS, verbose_name="assignation")
    attelage = models.CharField(max_length=50, default="Remorque", choices=ATTELAGES, verbose_name="attelage")
    
    immatriculation = models.CharField(max_length=20, verbose_name="immatriculation")
    date_mise_en_circulation = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date de mise en service")
    date_effet = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date d'effet assurance")
    date_echeance_visite = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date d'échéance visite technique")
    date_echeance_assurance = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date d'écheance assurance")
    date_echeance_stationnement = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="Date d'écheance stationnement")
    date_echeance_patente = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date d'écheance patente")    
    numero_chassis = models.CharField(max_length=20, default="", blank=True, verbose_name="numéro de chassis")
    
    poids_ptac = models.FloatField(default=0, verbose_name="poids totale en charge")
    poids_vide = models.FloatField(default=0, verbose_name="poids vide")
    poids_charge_utile = models.FloatField(default=0, verbose_name="charge utile")
    gps = models.BooleanField(default=False, verbose_name="gPS") 
    photo = models.ImageField(upload_to='vehicules', blank=True, null=True, verbose_name="photo du véhicule")

    def __str__(self):
        return "{0}".format(self.immatriculation.upper()+' '+self.type_vehicule.title())


class Chauffeur(models.Model):
    TYPE_CHAUFFEURS = (('Titulaire', 'Titulaire'), ('Supléant', 'Supléant'))
    STATUTS_CHAUFFEURS = (('Actif', 'Actif'), ('Sorti', 'sorti'))
    TYPE_CONTRATS = (('CDI', 'CDI'), ('CDD', 'CDD'))
    CATEGORIE_PERMIS = (('BCDE', 'BCDE'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))
    NATURE_PIECES = (
        ('CNI', 'CNI'), 
        ('ATTESTATION IDENTITE', 'ATTESTATION IDENTITE'), 
        ('PASSPORT', 'PASSPORT'), 
        ('CARTE CONULAIRE', 'CARTE CONULAIRE')
    )
    civilite = models.CharField(max_length=20,  default="M.", choices=CIVILITES, verbose_name="civilité")
    nom = models.CharField(max_length=100, verbose_name="nom")
    prenoms = models.CharField(max_length=100, verbose_name="prénoms")
    date_naissance = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date de naissance")   
    lieu_naissance = models.CharField(max_length=2250, default="", blank=True, verbose_name="lieu de naissance")
    
    type_chauffeur = models.CharField(max_length=20, default="Titulaire", choices=TYPE_CHAUFFEURS, verbose_name="type de chauffeurs")
    statut = models.CharField(max_length=20, default="Actif", choices=STATUTS_CHAUFFEURS, verbose_name="statut du chauffeur")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, verbose_name="affectation véhicule")
    matricule = models.CharField(max_length=10, default="", blank=True, unique=True, verbose_name="matricule")
    cellulaire = models.CharField(max_length=10, default="", blank=True, verbose_name="Cellulaire")
    cellulaire2 = models.CharField(max_length=10, default="", blank=True, verbose_name="Cellulaire 2")
    email = models.CharField(max_length=200, default="", blank=True, verbose_name="E-mail")
    type_contrat = models.CharField(max_length=20, default="Actif", choices=TYPE_CONTRATS, verbose_name="type de contrat")
    date_entree = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date entrée")    
    date_sortie = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date sortie")    
    piece_identite = models.CharField(max_length=100, default="", blank=True, verbose_name="N° pièce identité")   
    nature_piece = models.CharField(max_length=100, default="CNI", choices=NATURE_PIECES, verbose_name="nature pièce")   
    piece_date_etablissement = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date établissement pièce")  
    piece_date_expiration = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="pièce expiration")  
    permis_numero = models.CharField(max_length=100, default="", blank=True, verbose_name="numéro de permis")
    permis_categorie = models.CharField(max_length=5, default="BCDE", choices=CATEGORIE_PERMIS, verbose_name="catégorie de permis")
    permis_date_etablissement = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date d'établissement")  
    permis_date_echeance = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date d'échéance")  
    numero_carte_acces = models.CharField(max_length=100, default="", blank=True, verbose_name="numéro carte accès")   
    carte_acces_echeance = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date d'échéance carte accès")  
    contact = models.CharField(max_length=100, default="", blank=True, verbose_name="personne à contacter en cas d'urgence")
    photo_permis = models.ImageField(upload_to='permis', blank=True, null=True, verbose_name="photo permis de conduire")
    photo_piece = models.ImageField(upload_to='pieces', blank=True, null=True, verbose_name="photo pièce identité")
    photo = models.ImageField(upload_to='chauffeurs', blank=True, null=True, verbose_name="photo du chauffeur")
    
    class Meta:
        ordering = ('nom', 'prenoms')

    def __str__(self):
        return "{0} - {1}".format(self.matricule, self.nom.upper()+' '+self.prenoms.title())


class Marchandise(models.Model):
    ETAT_PHYSIQUES = (('Solide', 'Solide'), ('Liquide', 'Liquide'), ('Gazeux', 'Gazeux'), ('Service', 'Service'))
    etat_marchandise = models.CharField(max_length=20, default="Solide", choices=ETAT_PHYSIQUES, verbose_name="etat physique")
    libelle = models.CharField(max_length=200, unique=True, verbose_name='marchandise/service' )   

    def __str__(self):
        return "{0}".format(self.libelle)


class Commande(models.Model):
    MODE_TARIFICATIONS = (('Tonnage', 'Tonnage'), ('Kilométrage', 'Kilométrage'), ('Trajet', 'Trajet'), ('Autre', 'Autre'))
    ETAT_COMMANDES = (('En cours', 'En cours'), ('Livrée', 'Livrée'), )
    etat_commande = models.CharField(max_length=10, default="Gazoil", choices=ETAT_COMMANDES, verbose_name="état commande")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client")
    numero_commande = models.CharField(max_length=20, default="", blank=True, verbose_name="n°bon cde")
    date_bon_commande = models.DateField(blank=True, null=True, verbose_name="date bon cde")
    client_pour_compte  = models.CharField(max_length=100, default="", blank=True, verbose_name="pour le compte de")
    date_commande = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date saisie")
    lieu_chargement = models.CharField(max_length=150, default="", blank=True, verbose_name="lieu chargement")
    lieu_dechargement = models.CharField(max_length=150, default="", blank=True, verbose_name="lieu déchargement")  
    navire = models.CharField(max_length=150, default="", blank=True, verbose_name="navire")
    mode_tarification = models.CharField(max_length=30, default="Tonnage", choices=MODE_TARIFICATIONS, verbose_name="mode tarification")  
    tonnage_estime = models.FloatField(default=0, blank=True, verbose_name="tonnage estimé en T")  
    volume_estime = models.FloatField(default=0, blank=True, verbose_name="volume estimé en M3")  
    description = models.TextField(default="", blank=True, null=True, verbose_name="description") 
    numero_dossier = models.CharField(max_length=10, default="", blank=True, verbose_name="numéro dossier")
    #condition_vente = models.CharField(max_length=100, default="", blank=True, null=True, verbose_name="condition de vente")

    class Meta:
        ordering = ('-date_commande',)

    def __str__(self):
        return "{0}, {1}, {2}".format(self.numero_dossier, self.client, dateAnglaisFrancais(self.date_commande))


class Detailscommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, verbose_name="client")
    marchandise = models.ForeignKey(Marchandise, on_delete=models.CASCADE, verbose_name="marchandise")
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, verbose_name="itinéraire")
    rubrique = models.TextField(default="", blank=True, verbose_name="libellé complément marchdes ou services ")  
    
    lieu_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="lieu chargement")
    contact_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="contact")
    adresse_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="adresse")
    telephone_chargement = models.CharField(max_length=15, default="", blank=True, verbose_name="téléphone")

    lieu_dechargement = models.CharField(max_length=200, default="", blank=True, verbose_name="lieu déchargement")  
    contact_dechargement = models.CharField(max_length=100, default="", blank=True, verbose_name="contact")
    adresse_dechargement = models.CharField(max_length=100, default="", blank=True, verbose_name="adresse")
    telephone_dechargement = models.CharField(max_length=15, default="", blank=True, verbose_name="téléphone")

    quantite = models.FloatField(blank=True, null=True, verbose_name="quantité / km")
    prix_unitaire = models.FloatField(blank=True, null=True, verbose_name="prix unitaire")
    observation = models.TextField(default="", blank=True, verbose_name="observation")

    class Meta:
        unique_together = (('commande', 'marchandise', 'trajet'),)

    def __str__(self):
        return "{0}, {1}, {2}, {3} ".format(self.marchandise, self.trajet, self.quantite, self.prix_unitaire)


class Ordretransport(models.Model):
    QUI_ENLEVE = (('Coco Inter', 'Coco Inter'), ('Sous-Traitance', 'Sous-Traitance'),)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, verbose_name="commande")
    qui_enleve = models.CharField(max_length=30, default="Coco Inter", choices=QUI_ENLEVE, blank=True, null=True, verbose_name="transporteur")
    executant = models.CharField(max_length=150, default="", blank=True, verbose_name="exécutant")
    numero_ot = models.CharField(max_length=20, default="OT0000001", blank=True, verbose_name="n°bon commande")
    date_ot = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date saisie ot")
    numero_ot = models.CharField(max_length=10, default='', blank=True, verbose_name="numero ot")
    observation = models.CharField(max_length=255, default="", blank=True, verbose_name="observation")
    valide = models.BooleanField(default=False, verbose_name="validé")

    def __str__(self):
        return "{0}, {1}".format(self.numero_ot, self.commande)


class Detailsot(models.Model):
    ot = models.ForeignKey(Ordretransport, on_delete=models.CASCADE, verbose_name="ot")
    marchandise = models.ForeignKey(Marchandise, on_delete=models.CASCADE, verbose_name="marchandise")
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, verbose_name="itinéraire")
    rubrique = models.TextField(default="", blank=True, verbose_name="libellé complément marchdes ou services ")  

    lieu_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="lieu chargement")
    contact_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="contact")
    adresse_chargement = models.CharField(max_length=100, default="", blank=True, verbose_name="adresse")
    telephone_chargement = models.CharField(max_length=15, default="", blank=True, verbose_name="téléphone")

    lieu_dechargement = models.CharField(max_length=200, default="", blank=True, verbose_name="lieu déchargement")  
    contact_dechargement = models.CharField(max_length=100, default="", blank=True, verbose_name="contact")
    adresse_dechargement = models.CharField(max_length=100, default="", blank=True, verbose_name="adresse")
    telephone_dechargement = models.CharField(max_length=15, default="", blank=True, verbose_name="téléphone")

    quantite = models.FloatField(blank=True, null=True, verbose_name="quantité / km")
    prix_unitaire = models.FloatField(blank=True, null=True, verbose_name="prix unitaire")
    
    class Meta:
        unique_together = (('ot', 'marchandise', 'trajet'),)

    def __str__(self):
        return "{0}, {1}, {2}, {3} ".format(self.marchandise, self.trajet, self.quantite, self.prix_unitaire)


class Enlevement(models.Model):

    def validate_interval(value):
        if not value > 0 or value==None:
            raise ValidationError(_('%(value)s doit etre supérieur à zéro'), params={'value': value},)

    ETAT_ENLEVEMENTS = (
        ('En cours', 'En cours'), 
        ('Fin enlèvement', 'Fin enlèvement'), 
        ('En route déchargement', 'En route déchargement'),
        ('Déchargement en cours', 'Déchargement en cours'), 
        ('Fin déchargement', 'Fin déchargement'), 
    )
    MODE_TARIFICATIONS = (('Tonnage', 'Tonnage'), ('kilométrage', 'kilométrage'), ('Forfait', 'Forfait'), ('Autre', 'Autre'))
    ordretransport = models.ForeignKey(Ordretransport, on_delete=models.CASCADE, verbose_name="client")
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, db_index=True, verbose_name="itinéraire")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, db_index=True, verbose_name="vehicule")
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE, db_index=True, verbose_name="chauffeur")
    marchandise = models.ForeignKey(Marchandise, on_delete=models.CASCADE, db_index=True, verbose_name="marchandise")
    rubrique = models.TextField(default="", blank=True, verbose_name="libellé complément marchandises ou services")  
    date_enlevement = models.DateField(default=datetime.date.today, blank=True, null=True, db_index=True, verbose_name="date enlèvement")

    lieu_chargement = models.CharField(max_length=255, default="", blank=True, verbose_name="lieu de chargement")       
    contact_chargement = models.CharField(max_length=255, default="", blank=True, verbose_name="contact chargement")   
    telephone_chargement = models.CharField(max_length=20, default="", blank=True, verbose_name="téléphone chargement")     

    date_dechargement = models.DateField(default=datetime.date.today, blank=True, verbose_name="date déchargement")
    lieu_dechargement = models.CharField(max_length=255, default="", blank=True, verbose_name="lieu du déchargement")       
    contact_dechargement = models.CharField(max_length=255, default="", blank=True, verbose_name="contact déchargement")   
    telephone_dechargement = models.CharField(max_length=20, default="", blank=True, verbose_name="Téléphone déchargement")     
    
    poids_vide = models.FloatField(default=0, verbose_name="poids à vide (Tonne)")
    poids_charge = models.FloatField(default=0, verbose_name="poids brut (Tonne)")
    poids_net = models.FloatField(default=0, blank=True, null=True, verbose_name="poids net-Tonne")#validators=[validate_interval], blank=True, null=True,
    quantite = models.FloatField(default=0, blank=True, verbose_name="quantité (Poids net-Tonne / Kilometrage-km / Autres")#validators=[validate_interval], blank=True, null=True,

    mode_tarification = models.CharField(max_length=30, default="Tonnage", choices=MODE_TARIFICATIONS, verbose_name="mode tarification")
    prix_unitaire = models.FloatField(default=0, verbose_name="prix unitaire")
    numero_ticket = models.CharField(max_length=20, default='', blank=True, verbose_name="numéro de ticket")## DOSSIER + NUMERO TICKET
    etat_enlevement = models.CharField(max_length=30, default="En cours", choices=ETAT_ENLEVEMENTS, blank=True, null=True, verbose_name="état enlèvement")
    observation = models.TextField(default="", blank=True, null=True, verbose_name="observation")       

    def __str__(self):
        return "{0}, {1}, {2}".format(self.ordretransport, dateAnglaisFrancais(self.date_enlevement), self.etat_enlevement)

    def enlevement_view():
        dataset = Enlevement.objects.all()
        return dataset


class Carburant(models.Model):
    ordretransport = models.ForeignKey(Ordretransport, blank=True, on_delete=models.CASCADE, null=True, verbose_name="ot (pas de OT pour les prises ordinaires)")
    IMPUTATIONS = (('Préfinancement', 'Préfinancement'), ('Coco Inter', 'Coco Inter'))
    TYPE_CARBURANTS = (('Gazoil', 'Gazoil'), ('Essence', 'Essence'))
    numero_bon = models.CharField(max_length=20, default="", blank=True, verbose_name="numéro bon")
    navire = models.CharField(max_length=100, default="", blank=True, verbose_name="navire")
    type_carburant = models.CharField(max_length=10, default="Gazoil", choices=TYPE_CARBURANTS, verbose_name="type de carburant")
    imputation = models.CharField(max_length=20, default="Préfinancement", choices=IMPUTATIONS, verbose_name="imputation")
    client = models.CharField(max_length=100, default="", blank=True, verbose_name="client")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, db_index=True, verbose_name="vehicule")
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE, db_index=True, verbose_name="chauffeur")
    date_prise = models.DateField(default=timezone.now, blank=True,  null=True, verbose_name="date de prise")
    quantite = models.SmallIntegerField(default=0, verbose_name="quantité")
    montant = models.IntegerField(default=0, verbose_name="montant")
    kilometrage = models.IntegerField(default=0, verbose_name="kilométrage avant prise")
    station = models.CharField(max_length=100, default="", blank=True, verbose_name="station")  
    prix_pompe = models.IntegerField(default=610, blank=True, verbose_name="prix à la pompe")

    class Meta:
        ordering=('-date_prise',)

    def __str__(self):
        return "{0}, {1}, {2}".format(self.vehicule, self.quantite, self.chauffeur)

    def consommation_view():
        dataset = Carburant.objects.all()
        return dataset

class Facturation(models.Model):
    ETAT_TRANSACTIONS = (
        ('Emise', 'Emise'), 
        ('Attente', 'Attente'), 
        ('Soldée', 'Soldée'), 
    )
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, verbose_name="client")
    etat_facture = models.CharField(max_length=30, default="Emise", choices=ETAT_TRANSACTIONS, verbose_name="état")
    date_facture = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date facture")    
    delai = models.SmallIntegerField(default=30, blank=True, verbose_name="délai")    
    bon_livraison = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name="bon de livraison")
    tva = models.FloatField(default=0, blank=True, verbose_name="tva")  
    numero_facture = models.CharField(max_length=10, default='', blank=True, verbose_name="numero facture")
    avance = models.FloatField(default=0, blank=True, verbose_name="avance perçue")
    debours = models.FloatField(default=0, blank=True, verbose_name="debours")   
    montant = models.FloatField(default=0, blank=True, verbose_name="montant de la facture") 
    montant_lettre = models.CharField(max_length=255, default='', blank=True, verbose_name="montant en lettre")
    utiliser_montant_lettre = models.BooleanField(default=False, blank=True, verbose_name="utiliser le montant en lettre")
    condition_vente = models.CharField(max_length=100, default="", blank=True, null=True, verbose_name="condition de vente")
    
    ligne_bon_commande = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name="Remplacer vos références")
    utiliser_ligne_bon_commande = models.BooleanField(default=False, blank=True, verbose_name="Je voudrais remplacer vos références")
    
    def __str__(self):
        return "{0}, {1}, {2}".format(self.commande, dateAnglaisFrancais(self.date_facture), self.etat_facture)

    def emission_view():
        dataset = Facturation.objects.all()
        return dataset

    def facture_commande(self):
        societe = Societe.objects.get(pk=1)
        ot_dict = {}
        montant_total_ht = 0
        montant_tva = 0
        montant_carburant = 0
        facturation = get_object_or_404(Facturation, pk=self.pk)
        ot_list = facturation.commande.ordretransport_set.all() 
        enlevement_list = Enlevement.objects.filter(ordretransport__in = ot_list).order_by('-date_enlevement')

        enlevement_group = enlevement_list.values_list(
            'ordretransport__numero_ot', 
            'trajet__source__libelle', 
            'trajet__destination__libelle', 
            'marchandise__libelle').order_by(
                                    'ordretransport__numero_ot', 
                                    'marchandise__libelle').annotate(
                                    qte=Sum(F('quantite')),
                                    pu=Avg(F('prix_unitaire')),
                                    total=Sum(F('quantite') * F('prix_unitaire')),
                                )
        for i in enlevement_group:
            if ot_dict.get(i[0]):
                ot_dict[i[0]].append(i[1:])
                montant_total_ht+=i[6]
            else:
                ot_dict[i[0]] = [i[1:]]  
                montant_total_ht+=i[6]
        
        #print("enlevement_group", enlevement_group)
        #print("ot_dict", ot_dict)
        montant_total_ht = int(montant_total_ht)
        # CARBURANT
        montant_tva = int(montant_total_ht * facturation.tva)

        montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
        if montant_carburant is None:montant_carburant=0

        montant_total_ttc = int(montant_total_ht+montant_tva)
        montant_net = int(montant_total_ttc-montant_carburant-facturation.debours-facturation.avance)

        montant_reglement = Reglement.objects.filter(facturation__id = self.id).aggregate(montant=Sum(F('montant')))['montant']
        if montant_reglement is None:montant_reglement=0

        etat='Emise'
        solde = int(montant_net - montant_reglement)
        if solde > 100:etat = "Emise"
        elif solde <= 100:etat = 'Soldée'

        context = {'facturation': facturation, 
        'ot_list':ot_list, 
        'enlevement_list':enlevement_list,
        'ot_dict':ot_dict,
        'montant_total_ht':int(montant_total_ht),
        'montant_tva':int(montant_tva),
        'montant_total_ttc':int(montant_total_ttc),
        'montant_carburant':int(montant_carburant),
        'montant_avance':int(facturation.avance),
        'montant_debours':int(facturation.debours),
        'montant_avance_carburant_debours':int(montant_carburant)+facturation.avance+facturation.debours,
        'montant_net':int(montant_net),
        'montant_reglement':int(montant_reglement),
        'montant_solde':solde,
        'montant_net_lettre':chiffreLettre(montant_net),
        'etat': etat
        }
        return context


    def facture_view(pk):
        ot_dict = {}
        montant_total_ht = 0
        montant_tva = 0
        montant_carburant = 0
        facturation = get_object_or_404(Facturation, pk=pk)
        ot_list = facturation.commande.ordretransport_set.all() 
        enlevement_list = Enlevement.objects.filter(ordretransport__in = ot_list).order_by('-date_enlevement')

        enlevement_group = enlevement_list.values_list(
            'ordretransport__numero_ot', 
            'trajet__source__libelle', 
            'trajet__destination__libelle', 
            'marchandise__libelle').order_by(
                                    'ordretransport__numero_ot', 
                                    'marchandise__libelle').annotate(
                                    quantite=Sum(F('quantite')),
                                    pu=Avg(F('prix_unitaire')),
                                    total=Sum(F('quantite') * F('prix_unitaire')),
                                )
        for i in enlevement_group:
            if ot_dict.get(i[0]):
                ot_dict[i[0]].append(i[1:])
                montant_total_ht+=i[6]
            else:
                ot_dict[i[0]] = [i[1:]]  
                montant_total_ht+=i[6]
        
        #print("enlevement_group", enlevement_group)
        #print("ot_dict", ot_dict)

        montant_total_ht = int(montant_total_ht)
        # CARBURANT
        montant_tva = montant_total_ht * societe.tva

        montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
        if montant_carburant is None:montant_carburant=0

        montant_total_ttc = int(montant_total_ht+montant_tva)
        montant_net = int(montant_total_ttc-montant_carburant-facturation.debours)

        context = {'facturation': facturation, 
        'ot_list':ot_list, 
        'enlevement_list':enlevement_list,
        'ot_dict':ot_dict,
        'montant_total_ht':int(montant_total_ht),
        'montant_tva':int(montant_tva),
        'montant_total_ttc':int(montant_total_ttc),
        'montant_carburant':int(montant_carburant),
        'montant_net':int(montant_net),
        'montant_net_lettre':chiffreLettre(montant_net),
        }

        return context


class Reglement(models.Model):
    facturation = models.ForeignKey(Facturation, on_delete=models.CASCADE, verbose_name="facture")
    date_reglement = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date règlement")
    mode_reglement = models.CharField(max_length=10, default="Chèque", choices=MODE_REGLEMENTS, verbose_name="mode")
    reference = models.CharField(max_length=250, default="", blank=True, verbose_name="référence")       
    montant = models.FloatField(default=0, blank=True, null=True, verbose_name="montant")
    observation = models.TextField(default="", blank=True, verbose_name="observation")       

    def __str__(self):
        return "{0}, {1}, {2}".format(self.facturation, dateAnglaisFrancais(self.date_reglement), self.montant)
     

class Entretien(models.Model):
    TYPE_ENTRETIENS = (
        ('Vidange', 'Vidange'), 
        ('Pneumatique', 'Pneumatique'), 
        ('Climatisation', 'Climatisation'),
        ('Autre', 'Autre'), 
    )

    PROCHAIN_ENTRETIEN_DATE_KM = (
        ('Prochain entretien en Date', 'Prochain entretien en date'), 
        ('Prochain entretien en Km', 'Prochain entretien en Km'), 
    )
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, verbose_name="véhicule")
    type_entretien = models.CharField(max_length=30, default="Vidange", choices=TYPE_ENTRETIENS, verbose_name="type d'entretien")
    date_entretien_debut = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date début entretien")
    date_entretien_fin = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date fin entretien")
    nature_prochain_entretien = models.CharField(max_length=100, default="Prochain entretien en Date", choices=PROCHAIN_ENTRETIEN_DATE_KM, verbose_name="Nature prochain entretien")
    
    date_entretien_prochain = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date prochain entretien")
    kilometrage = models.FloatField(default=0, blank=True, null=True, verbose_name="kilométrage avant entretien")
    kilometrage_prochain_entretien = models.FloatField(default=0, blank=True, null=True, verbose_name="kilométrage prochain entretien")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, verbose_name="fournisseur")
    montant = models.FloatField(default=0, blank=True, null=True, verbose_name="montant")
    observation = models.TextField(default="", blank=True, null=True, verbose_name="observation")

    def __str__(self):
        return "{0}, {1}, {2}".format(self.vehicule, dateAnglaisFrancais(self.date_entretien_debut), self.montant)


class Reparation(models.Model):
    TYPE_REPARATIONS = (
        ('Electricité', 'Electricité'), 
        ('Mécanique', 'Mécanique'),
        ('Tolerie', 'Tolerie'),        
        ('Vidange', 'Vidange'), 
        ('Pneumatique', 'Pneumatique'), 
        ('Climatisation', 'Climatisation'),
        ('Autre', 'Autre'),
    )
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, verbose_name="véhicule")
    type_reparation = models.CharField(max_length=30, default="Vidange", choices=TYPE_REPARATIONS, verbose_name="type de réparation")
    date_reparation_debut = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date début réparation")
    date_reparation_fin = models.DateField(default=datetime.date.today, blank=True, null=True, verbose_name="date fin réparation")
    kilometrage = models.FloatField(default=0, blank=True, null=True, verbose_name="kilométrage avant réparation")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, verbose_name="fournisseur")
    montant = models.FloatField(default=0, blank=True, null=True, verbose_name="montant")
    observation = models.TextField(default="", blank=True, verbose_name="observation")

    def __str__(self):
        return "{0}, {1}, {2}".format(self.vehicule, dateAnglaisFrancais(self.date_reparation_debut), self.montant)


class Planning(models.Model):
    date_planning = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="planning date")
    


class Devis(models.Model):
    MODE_TARIFICATIONS = (('Tonnage', 'Tonnage'), ('Kilométrage', 'Kilométrage'), ('Trajet', 'Trajet'), ('Autre', 'Autre'),)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client")
    date_devis = models.DateField(default=datetime.date.today, blank=True,  null=True, verbose_name="date devis")
    client_pour_compte  = models.CharField(max_length=100, default="", blank=True, verbose_name="pour le compte de")
 
    lieu_chargement = models.CharField(max_length=150, default="", blank=True, verbose_name="lieu chargement")
    lieu_dechargement = models.CharField(max_length=150, default="", blank=True, verbose_name="lieu déchargement")  
    navire = models.CharField(max_length=150, default="", blank=True, verbose_name="navire")
    mode_tarification = models.CharField(max_length=30, default="Tonnage", choices=MODE_TARIFICATIONS, verbose_name="mode tarification")
    description = models.TextField(default="", blank=True, verbose_name="description") 
    valide = models.BooleanField(default=False, verbose_name="validé") 
    numero_devis = models.CharField(max_length=10, default='', blank=True, verbose_name="numero devis")
    tva = models.FloatField(default=0, blank=True, verbose_name="tva")
    condition_vente = models.TextField(default="", blank=True, null=True, verbose_name="condition de vente")

    ligne_bon_devis = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name="Remplacer vos références")
    utiliser_ligne_bon_devis = models.BooleanField(default=False, blank=True, verbose_name="Je voudrais remplacer vos références")


    class Meta:
        ordering = ('-date_devis',)

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(dateAnglaisFrancais(self.date_devis), self.client, self.navire, self.mode_tarification)


class Detailsdevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, verbose_name="devis")
    marchandise = models.ForeignKey(Marchandise, on_delete=models.CASCADE, verbose_name="marchandise")
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, verbose_name="itinéraire")
    rubrique = models.TextField(default="", blank=True, verbose_name="libellé complément marchandises ou services")
    quantite = models.FloatField(blank=True, null=True, verbose_name="quantité / km")
    prix_unitaire = models.FloatField(blank=True, null=True, verbose_name="prix unitaire")

    class Meta:
        unique_together = (('devis', 'marchandise', 'trajet'),)

    def __str__(self):
        return "{0}, {1}, {2}, {3} ".format(self.marchandise, self.trajet, self.quantite, self.prix_unitaire)


class Societe(models.Model):
    raisonSociale = models.CharField(max_length=255, verbose_name="raison sociale")
    sigle = models.CharField(max_length=50, default="", blank=True, verbose_name="sigle")
    telephone = models.CharField(max_length=20, default="", blank=True, verbose_name="téléphone")
    cellulaire = models.CharField(max_length=20, default="", blank=True, verbose_name="cellulaire")
    pagination = models.PositiveIntegerField(default=5, blank=True, verbose_name="nombre de ligne des tableaux")
    photo = models.ImageField(upload_to='images', default="", blank=True, null=True, verbose_name="photo")
    logo = models.ImageField(upload_to='images', default="", blank=True, null=True, verbose_name="logo")
    email = models.EmailField(default="", blank=True, verbose_name="e-mail")
    alerte_email_jour = models.PositiveIntegerField(default=5, blank=True, null=True, verbose_name="alerte email (en jours)")
    dateEnvoiEmail = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date envoi des email")
    envoiEmailEffectue = models.BooleanField(default=False, blank=True, verbose_name="envoi de mail effectué")
    nbreJourMaxDateEcheance = models.SmallIntegerField(default=90, blank=True,  null=True, verbose_name="nombre de jours max avant échéance")
    entete_table = models.BooleanField(default=False, blank=True, verbose_name="entêtes des tableaux en couleur des apps")
    tva = models.FloatField(default=0.18, blank=True, verbose_name="tva")
    
    def __str__(self):
        return "{0}".format(self.raisonSociale)


class Para(models.Model):
    alerte_email_jour = models.PositiveIntegerField(default=5, blank=True, null=True, verbose_name="alerte email (en jours)")
    dateEnvoiEmail = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date envoi des email")
    envoiEmailEffectue = models.BooleanField(default=False, blank=True, verbose_name="envoi de mail effectué")
    nbreJourMaxDateEcheance = models.SmallIntegerField(default=90, blank=True, null=True, verbose_name="nombre de jours max avant échéance")
    tva = models.FloatField(default=0.18, blank=True, verbose_name="tva")
    numero_devis = models.IntegerField(default=0, blank=True, verbose_name="compteur de devis")
    numero_commande = models.IntegerField(default=0, blank=True, verbose_name="compteur de commande")
    numero_ot = models.IntegerField(default=0, blank=True, verbose_name="compteur de ot")
    numero_facture = models.IntegerField(default=0, blank=True, verbose_name="compteur de facture")

    delai_piece_date_expiration = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel pièce expiration")  
    delai_permis_date_echeance = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel permis")  
    delai_carte_acces_echeance = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel carte accès")  
    
    delai_entretien_prochain = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel prochain entretien")
    delai_kilometrage_prochain_entretien = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel kilométrage prochain")
  
    delai_echeance_visite = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel visite technique")
    delai_echeance_assurance = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel assurance")
    delai_echeance_stationnement = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel stationnement")
    delai_echeance_patente = models.SmallIntegerField(default=10, blank=True, verbose_name="délai de rappel patente")    

    date_debut = models.DateField(default=timezone.now, blank=True, verbose_name="date début exercice")
    date_fin = models.DateField(default=timezone.now, blank=True, verbose_name="date fin exercice")

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(dateAnglaisFrancais(self.date_debut), dateAnglaisFrancais(self.date_fin), self.numero_ot, self.numero_facture)


class Depense(models.Model):
    TYPE_DEPENSES = (
        ('Chargement', 'Chargement'),
        ('Déchargement', 'Déchargement'), 
        ('Annexe', 'Annexe'), 
        ('Pourboire', 'Pourboire'),
    )
    ordretransport = models.ForeignKey(Ordretransport, blank=True, on_delete=models.CASCADE, null=True, verbose_name="ot (pas de OT pour dépenses ordinaires)")
    type_depense = models.CharField(max_length=30, default="Chargement", choices=TYPE_DEPENSES, verbose_name="type de dépense")
    date_depense = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="date dépense")
    montant = models.FloatField(default=0, verbose_name="montant")
    observation = models.TextField(default="", blank=True, verbose_name="observation")

    class Meta:
        ordering=('-date_depense',)

    def __str__(self):
        return "{0}, {1}, {2}, {3}".format(dateAnglaisFrancais(self.date_depense), self.ordretransport, self.type_depense, self.montant)

