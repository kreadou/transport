from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from parametre.models import *
from django.db.models import Count, Q, Sum, F
import json
from . forms import FilterForm
from alerte_synthese import *

def requete_ajax(request):
    return render(request, 'tableaubord/base.html', locals())


def accueil(request):
    form = FilterForm()
    date_du = request.GET.get("date_du")
    date_au = request.GET.get("date_au")

    #################################### FACTURATION #################################
    ### FACTURES EMISES
    dataset_factures_emises = Facturation.emission_view()
    ### ENLEVEMENTS TOTAL
    dataset_enlevements = Enlevement.enlevement_view()
    ### ENLEVEMENTS FACTURES
    dataset_enlevements_factures = dataset_enlevements.filter(ordretransport__commande__in = tuple(set([ i.commande for i in dataset_factures_emises])))

    #CHIFFRE AFFAIRE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    chiffre_affaire_total = dataset_enlevements_factures.aggregate(chiffre_affaire_total = Sum(F('quantite') * F('prix_unitaire')))['chiffre_affaire_total']
    
    if dataset_factures_emises.exists():
        chiffre_affaire_m = [(lesMois[i.date_facture.month-1], i.facture_commande()['montant_total_ht']) for i in dataset_factures_emises]
        chiffre_affaire_mensuel = {}
        for i in chiffre_affaire_m:
            if chiffre_affaire_mensuel.get(i[0], 0):chiffre_affaire_mensuel[i[0]]+=i[1]
            else:chiffre_affaire_mensuel[i[0]]=i[1]
        # print('ooooooooooooo = ', chiffre_affaire_mensuel)
        chiffres_affaires_mensuels = [(t, chiffre_affaire_mensuel[t]) for x in lesMois for t in chiffre_affaire_mensuel if t == x]
        # print('ooooooooooooo = ', chiffres_affaires_mensuels)
        
        # CHIFFRE AFFAIRE PAR MOIS - 
        if chiffre_affaire_mensuel:
            data = list(chiffre_affaire_mensuel.items())
            chiffre_affaire_mensuel_plus_eleve = max(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moins_eleve = min(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moyen = sum(tuple(zip(*data))[1])/len(data)

            data = [t for x in lesMois for t in data[:] if t[0] == x]
            data.insert(0, ('Mois', 'CA'))
            #print("data = ", chiffre_affaire_mensuel_moins_eleve)
            data=json.dumps(data)# METTRE LA LISTE AU FORMAT JSON

    ## TONNAGE TOTAL PAR MOIS
    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES

    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']
    # print('tonnage = ', tonnage_total)

    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)

    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)

    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    #CARBURANT 
    dataset_carburants = Carburant.consommation_view()
    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)

    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    context = alerte_synthese()
    return render(request, 'tableaubord/accueil.html', locals())


def accueil_filtrer(request):
    periode_du = request.GET.get('periode_du', None)
    periode_au = request.GET.get('periode_au', None)
    liste_critere = request.GET.get('liste_critere', None)
    print('date du au  = ', periode_du, periode_au)

    dossiers_id=[]
    clients_id=[]
    marchandises_id=[]
    trajets_id=[]
    vehicules_id=[]
    chauffeurs_id=[]
    if liste_critere:
        #print('liste critere = ', liste_critere)
        liste_critere = liste_critere.split(";")[:-1]
        liste_critere = list(set(grouperListe(3, liste_critere[:])))
        print('liste critere 2 = ', liste_critere)

        if len(liste_critere) > 1:
            liste_critere.reverse()
            #print('liste critere 3 = ', liste_critere)

            ## RETRAIT DES REQUETES TRUE = AJOUT
            critere_moins = list(set(filter(lambda x: x[1]=='false', liste_critere)))
            print('moins = ', critere_moins)

            critere_plus = list(set(filter(lambda x: x[1]=='true', liste_critere)))
            print('plus = ', critere_plus)
            """
            ### LISTE DES OPPOSES DES TRUE
            q = list([ j for i in critere_plus for j in critere_moins if (i[0]==j[0] and i[1] != j[1] and i[2]==j[2])])
            print('les données oppasees a supprimer = ', q)

            for i in q: 
                critere_moins.remove(i)
            print('critères a appliquer = ', critere_moins)
            """
            try:
                dossiers = list(filter(lambda x : x[0]=='dossiers', critere_moins))
                if dossiers:
                    dossiers_id = list(map(lambda x: int(x), list(zip(*dossiers[:]))[2]))
            except:pass

            try:
                clients = list(filter(lambda x : x[0]=='clients', critere_moins))
                if clients:
                    clients_id = list(map(lambda x: int(x), list(zip(*clients[:]))[2]))
            except:pass

            try:
                marchandises = list(filter(lambda x : x[0]=='marchandises', critere_moins))
                if marchandises:
                    marchandises_id = list(map(lambda x: int(x), list(zip(*marchandises[:]))[2]))
            except:pass

            try:
                trajets = list(filter(lambda x : x[0]=='trajets', critere_moins))
                if trajets:
                    trajets_id = list(map(lambda x: int(x), list(zip(*trajets[:]))[2]))
            except:pass

            try:
                vehicules = list(filter(lambda x : x[0]=='vehicules', critere_moins))
                if vehicules:
                    vehicules_id = list(map(lambda x: int(x), list(zip(*vehicules[:]))[2]))
            except:pass

            try:
                chauffeurs = list(filter(lambda x : x[0]=='chauffeurs', critere_moins))
                if chauffeurs:
                    chauffeurs_id = list(map(lambda x: int(x), list(zip(*chauffeurs[:]))[2]))
            except:pass

        else:
            if liste_critere[0][1] == 'false':
                if liste_critere[0][0] == 'dossiers':
                    dossiers_id=[int(liste_critere[0][2])] 
                elif liste_critere[0][0] == 'clients':
                    clients_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'marchandises':
                    marchandises_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'trajets':
                    trajets_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'vehicules':
                    vehicules_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'chauffeurs':
                    chauffeurs_id=[int(liste_critere[0][2])]

    #periode_du = periode_du[-4:]+'-'+periode_du[3:5]+'-'+periode_du[:2]
    #periode_au = periode_au[-4:]+'-'+periode_au[3:5]+'-'+periode_au[:2]

    print("periodes  = ", periode_du, periode_au)
    #################################### FACTURATION ########################################################
    ### FACTURES EMISES
    dataset_factures_emises = Facturation.emission_view().filter(date_facture__range = [periode_du, periode_au])
    if dossiers_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__client__id__in = clients_id)

    if marchandises_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__trajet__id__in = trajets_id)

    if vehicules_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__chauffeur__id__in = chauffeurs_id)


    ### ENLEVEMENTS TOTAL
    dataset_enlevements = Enlevement.enlevement_view()
    ### ENLEVEMENTS FACTURES
    dataset_enlevements_factures = dataset_enlevements.filter(ordretransport__commande__in = tuple(set([ i.commande for i in dataset_factures_emises])))

    #CHIFFRE AFFAIRE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    chiffre_affaire_total = dataset_enlevements_factures.aggregate(chiffre_affaire_total = Sum(F('quantite') * F('prix_unitaire')))['chiffre_affaire_total']
    
    if dataset_factures_emises.exists():
        chiffre_affaire_m = [(lesMois[i.date_facture.month-1], i.facture_commande()['montant_total_ht']) for i in dataset_factures_emises]
        chiffre_affaire_mensuel = {}
        for i in chiffre_affaire_m:
            if chiffre_affaire_mensuel.get(i[0], 0):chiffre_affaire_mensuel[i[0]]+=i[1]
            else:chiffre_affaire_mensuel[i[0]]=i[1]
        # print('ooooooooooooo = ', chiffre_affaire_mensuel)
        chiffres_affaires_mensuels = [(t, chiffre_affaire_mensuel[t]) for x in lesMois for t in chiffre_affaire_mensuel if t == x]
        # print('ooooooooooooo = ', chiffres_affaires_mensuels)
        
        # CHIFFRE AFFAIRE PAR MOIS - 
        if chiffre_affaire_mensuel:
            data = list(chiffre_affaire_mensuel.items())
            chiffre_affaire_mensuel_plus_eleve = max(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moins_eleve = min(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moyen = sum(tuple(zip(*data))[1])/len(data)

            data = [t for x in lesMois for t in data[:] if t[0] == x]
            data.insert(0, ('Mois', 'CA'))
            #print("data = ", chiffre_affaire_mensuel_moins_eleve)
            data=json.dumps(data)# METTRE LA LISTE AU FORMAT JSON


    ## TONNAGE TOTAL PAR MOIS
    dataset_enlevements = Enlevement.enlevement_view().filter(date_enlevement__range=(periode_du, periode_au))
    if dossiers_id:
        dataset_enlevements = dataset_enlevements.exclude(ordretransport__commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_enlevements = dataset_enlevements.exclude(ordretransport__commande__client__id__in = clients_id)
    
    if marchandises_id:
        dataset_enlevements = dataset_enlevements.exclude(marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_enlevements = dataset_enlevements.exclude(trajet__id__in = trajets_id)

    if vehicules_id:
        dataset_enlevements = dataset_enlevements.exclude(vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_enlevements = dataset_enlevements.exclude(chauffeur__id__in = chauffeurs_id)


    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']

    # print('tonnage = ', tonnage_total)
    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)


    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)


    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    #CARBURANT 
    dataset_carburants = Carburant.consommation_view().filter(date_prise__range=(periode_du, periode_au))

    if dossiers_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__commande__client__id__in = clients_id)

    if marchandises_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__trajet__id__in = trajets_id)
    
    if vehicules_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__chauffeur__id__in = chauffeurs_id)
    

    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)
    
    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    return render(request, 'tableaubord/accueil_filtrer.html', locals())
    
################################## STATISTIQUE #####################################################

def statistique(request):
    form = FilterForm()
    date_du = request.GET.get("date_du")
    date_au = request.GET.get("date_au")

    #################################### FACTURATION #################################
    ### FACTURES EMISES
    dataset_factures_emises = Facturation.emission_view()
    ### ENLEVEMENTS TOTAL
    dataset_enlevements = Enlevement.enlevement_view()
    ### ENLEVEMENTS FACTURES
    dataset_enlevements_factures = dataset_enlevements.filter(ordretransport__commande__in = tuple(set([ i.commande for i in dataset_factures_emises])))

    #CHIFFRE AFFAIRE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    chiffre_affaire_total = dataset_enlevements_factures.aggregate(chiffre_affaire_total = Sum(F('quantite') * F('prix_unitaire')))['chiffre_affaire_total']
    
    if dataset_factures_emises.exists():
        chiffre_affaire_m = [(lesMois[i.date_facture.month-1], i.facture_commande()['montant_total_ht']) for i in dataset_factures_emises]
        chiffre_affaire_mensuel = {}
        for i in chiffre_affaire_m:
            if chiffre_affaire_mensuel.get(i[0], 0):chiffre_affaire_mensuel[i[0]]+=i[1]
            else:chiffre_affaire_mensuel[i[0]]=i[1]
        # print('ooooooooooooo = ', chiffre_affaire_mensuel)
        chiffres_affaires_mensuels = [(t, chiffre_affaire_mensuel[t]) for x in lesMois for t in chiffre_affaire_mensuel if t == x]
        # print('ooooooooooooo = ', chiffres_affaires_mensuels)
        
        # CHIFFRE AFFAIRE PAR MOIS - 
        if chiffre_affaire_mensuel:
            data = list(chiffre_affaire_mensuel.items())
            chiffre_affaire_mensuel_plus_eleve = max(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moins_eleve = min(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moyen = sum(tuple(zip(*data))[1])/len(data)

            data = [t for x in lesMois for t in data[:] if t[0] == x]
            data.insert(0, ('Mois', 'CA'))
            #print("data = ", chiffre_affaire_mensuel_moins_eleve)
            data=json.dumps(data)# METTRE LA LISTE AU FORMAT JSON

    ## TONNAGE TOTAL PAR MOIS
    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES

    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']
    # print('tonnage = ', tonnage_total)

    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)

    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)

    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    #CARBURANT 
    dataset_carburants = Carburant.consommation_view()
    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)

    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    context = alerte_synthese()
    return render(request, 'tableaubord/statistique.html', locals())


def statistique_filtrer(request):
    periode_du = request.GET.get('periode_du', None)
    periode_au = request.GET.get('periode_au', None)
    liste_critere = request.GET.get('liste_critere', None)
    print('date du au  = ', periode_du, periode_au)

    dossiers_id=[]
    clients_id=[]
    marchandises_id=[]
    trajets_id=[]
    vehicules_id=[]
    chauffeurs_id=[]
    if liste_critere:
        #print('liste critere = ', liste_critere)
        liste_critere = liste_critere.split(";")[:-1]
        liste_critere = list(set(grouperListe(3, liste_critere[:])))
        print('liste critere 2 = ', liste_critere)

        if len(liste_critere) > 1:
            liste_critere.reverse()
            #print('liste critere 3 = ', liste_critere)

            ## RETRAIT DES REQUETES TRUE = AJOUT
            critere_moins = list(set(filter(lambda x: x[1]=='false', liste_critere)))
            print('moins = ', critere_moins)

            critere_plus = list(set(filter(lambda x: x[1]=='true', liste_critere)))
            print('plus = ', critere_plus)
            """
            ### LISTE DES OPPOSES DES TRUE
            q = list([ j for i in critere_plus for j in critere_moins if (i[0]==j[0] and i[1] != j[1] and i[2]==j[2])])
            print('les données oppasees a supprimer = ', q)

            for i in q: 
                critere_moins.remove(i)
            print('critères a appliquer = ', critere_moins)
            """
            try:
                dossiers = list(filter(lambda x : x[0]=='dossiers', critere_moins))
                if dossiers:
                    dossiers_id = list(map(lambda x: int(x), list(zip(*dossiers[:]))[2]))
            except:pass

            try:
                clients = list(filter(lambda x : x[0]=='clients', critere_moins))
                if clients:
                    clients_id = list(map(lambda x: int(x), list(zip(*clients[:]))[2]))
            except:pass

            try:
                marchandises = list(filter(lambda x : x[0]=='marchandises', critere_moins))
                if marchandises:
                    marchandises_id = list(map(lambda x: int(x), list(zip(*marchandises[:]))[2]))
            except:pass

            try:
                trajets = list(filter(lambda x : x[0]=='trajets', critere_moins))
                if trajets:
                    trajets_id = list(map(lambda x: int(x), list(zip(*trajets[:]))[2]))
            except:pass

            try:
                vehicules = list(filter(lambda x : x[0]=='vehicules', critere_moins))
                if vehicules:
                    vehicules_id = list(map(lambda x: int(x), list(zip(*vehicules[:]))[2]))
            except:pass

            try:
                chauffeurs = list(filter(lambda x : x[0]=='chauffeurs', critere_moins))
                if chauffeurs:
                    chauffeurs_id = list(map(lambda x: int(x), list(zip(*chauffeurs[:]))[2]))
            except:pass

        else:
            if liste_critere[0][1] == 'false':
                if liste_critere[0][0] == 'dossiers':
                    dossiers_id=[int(liste_critere[0][2])] 
                elif liste_critere[0][0] == 'clients':
                    clients_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'marchandises':
                    marchandises_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'trajets':
                    trajets_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'vehicules':
                    vehicules_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'chauffeurs':
                    chauffeurs_id=[int(liste_critere[0][2])]

    #periode_du = periode_du[-4:]+'-'+periode_du[3:5]+'-'+periode_du[:2]
    #periode_au = periode_au[-4:]+'-'+periode_au[3:5]+'-'+periode_au[:2]

    print("periodes  = ", periode_du, periode_au)
    #################################### FACTURATION ########################################################
    ### FACTURES EMISES
    dataset_factures_emises = Facturation.emission_view().filter(date_facture__range = [periode_du, periode_au])
    if dossiers_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__client__id__in = clients_id)

    if marchandises_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__trajet__id__in = trajets_id)

    if vehicules_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_factures_emises = dataset_factures_emises.exclude(commande__ordretransport__enlevement__chauffeur__id__in = chauffeurs_id)


    ### ENLEVEMENTS TOTAL
    dataset_enlevements = Enlevement.enlevement_view()
    ### ENLEVEMENTS FACTURES
    dataset_enlevements_factures = dataset_enlevements.filter(ordretransport__commande__in = tuple(set([ i.commande for i in dataset_factures_emises])))

    #CHIFFRE AFFAIRE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    chiffre_affaire_total = dataset_enlevements_factures.aggregate(chiffre_affaire_total = Sum(F('quantite') * F('prix_unitaire')))['chiffre_affaire_total']
    
    if dataset_factures_emises.exists():
        chiffre_affaire_m = [(lesMois[i.date_facture.month-1], i.facture_commande()['montant_total_ht']) for i in dataset_factures_emises]
        chiffre_affaire_mensuel = {}
        for i in chiffre_affaire_m:
            if chiffre_affaire_mensuel.get(i[0], 0):chiffre_affaire_mensuel[i[0]]+=i[1]
            else:chiffre_affaire_mensuel[i[0]]=i[1]
        # print('ooooooooooooo = ', chiffre_affaire_mensuel)
        chiffres_affaires_mensuels = [(t, chiffre_affaire_mensuel[t]) for x in lesMois for t in chiffre_affaire_mensuel if t == x]
        # print('ooooooooooooo = ', chiffres_affaires_mensuels)
        
        # CHIFFRE AFFAIRE PAR MOIS - 
        if chiffre_affaire_mensuel:
            data = list(chiffre_affaire_mensuel.items())
            chiffre_affaire_mensuel_plus_eleve = max(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moins_eleve = min(data, key=lambda x:x[1])
            chiffre_affaire_mensuel_moyen = sum(tuple(zip(*data))[1])/len(data)

            data = [t for x in lesMois for t in data[:] if t[0] == x]
            data.insert(0, ('Mois', 'CA'))
            #print("data = ", chiffre_affaire_mensuel_moins_eleve)
            data=json.dumps(data)# METTRE LA LISTE AU FORMAT JSON


    ## TONNAGE TOTAL PAR MOIS
    dataset_enlevements = Enlevement.enlevement_view().filter(date_enlevement__range=(periode_du, periode_au))
    if dossiers_id:
        dataset_enlevements = dataset_enlevements.exclude(ordretransport__commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_enlevements = dataset_enlevements.exclude(ordretransport__commande__client__id__in = clients_id)
    
    if marchandises_id:
        dataset_enlevements = dataset_enlevements.exclude(marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_enlevements = dataset_enlevements.exclude(trajet__id__in = trajets_id)

    if vehicules_id:
        dataset_enlevements = dataset_enlevements.exclude(vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_enlevements = dataset_enlevements.exclude(chauffeur__id__in = chauffeurs_id)


    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']

    # print('tonnage = ', tonnage_total)
    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)


    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)


    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    #CARBURANT 
    dataset_carburants = Carburant.consommation_view().filter(date_prise__range=(periode_du, periode_au))

    if dossiers_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__commande__id__in = dossiers_id)
    
    if clients_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__commande__client__id__in = clients_id)

    if marchandises_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__trajet__id__in = trajets_id)
    
    if vehicules_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_carburants = dataset_carburants.exclude(ordretransport__enlevement__chauffeur__id__in = chauffeurs_id)
    

    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)
    
    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    return render(request, 'tableaubord/statistique_filtrer.html', locals())
    
















def enlevement(request):
    form = FilterForm()
    date_du = request.GET.get("date_du")
    date_au = request.GET.get("date_au")

    #################################### FACTURATION #################################
    ### ENLEVEMENTS TOTAL
    dataset_enlevements = Enlevement.enlevement_view()

    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES

    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']

    # print('tonnage = ', tonnage_total)

    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)


    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)


    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    
    #CARBURANT 
    dataset_carburants = Carburant.consommation_view()
    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)
    
    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    return render(request, 'tableaubord/enlevement.html', locals())


def enlevement_traitement(request):
    periode_du = request.GET.get('periode_du', None)
    periode_au = request.GET.get('periode_au', None)
    liste_critere = request.GET.get('liste_critere', None)

    dossiers_id=[]
    marchandises_id=[]
    trajets_id=[]
    vehicules_id=[]
    chauffeurs_id=[]
    if liste_critere:
        #print('liste critere = ', liste_critere)
        liste_critere = liste_critere.split(";")[:-1]
        liste_critere = list(set(grouperListe(3, liste_critere[:])))
        print('liste critere 2 enlev trat= ', liste_critere)

        if len(liste_critere) > 1:
            liste_critere.reverse()
            #print('liste critere 3 = ', liste_critere)

            ## RETRAIT DES REQUETES TRUE = AJOUT
            critere_moins = list(set(filter(lambda x: x[1]=='false', liste_critere)))
            print('moins = ', critere_moins)

            critere_plus = list(set(filter(lambda x: x[1]=='true', liste_critere)))
            print('plus = ', critere_plus)

            ### LISTE DES OPPOSES DES TRUE
            q = list([ j for i in critere_plus for j in critere_moins if (i[0]==j[0] and i[1] != j[1] and i[2]==j[2])])
            print('les données oppasees a supprimer = ', q)

            for i in q: 
                critere_moins.remove(i)
            print('critères a appliquer = ', critere_moins)

            dossiers = list(filter(lambda x : x[0]=='dossiers', critere_moins))
            if dossiers:
                dossiers_id = list(map(lambda x: int(x), list(zip(*dossiers[:]))[2]))

            marchandises = list(filter(lambda x : x[0]=='marchandises', critere_moins))
            if marchandises:
                marchandises_id = list(map(lambda x: int(x), list(zip(*marchandises[:]))[2]))

            trajets = list(filter(lambda x : x[0]=='trajets', critere_moins))
            if trajets:
                trajets_id = list(map(lambda x: int(x), list(zip(*trajets[:]))[2]))

            vehicules = list(filter(lambda x : x[0]=='vehicules', critere_moins))
            if vehicules:
                vehicules_id = list(map(lambda x: int(x), list(zip(*vehicules[:]))[2]))

            chauffeurs = list(filter(lambda x : x[0]=='chauffeurs', critere_moins))
            if chauffeurs:
                chauffeurs_id = list(map(lambda x: int(x), list(zip(*chauffeurs[:]))[2]))

        else:
            if liste_critere[0][1] == 'false':
                if liste_critere[0][0] == 'dossiers':
                    dossiers_id=[int(liste_critere[0][2])] 
                elif liste_critere[0][0] == 'marchandises':
                    marchandises_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'trajets':
                    trajets_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'vehicules':
                    vehicules_id=[int(liste_critere[0][2])]
                elif liste_critere[0][0] == 'chauffeurs':
                    chauffeurs_id=[int(liste_critere[0][2])]

    periode_du = periode_du[-4:]+'-'+periode_du[3:5]+'-'+periode_du[:2]
    periode_au = periode_au[-4:]+'-'+periode_au[3:5]+'-'+periode_au[:2]

    #################################### ENLEVEMENTS ########################################################
       
    ## TONNAGE TOTAL PAR MOIS
    dataset_enlevements = Enlevement.enlevement_view().filter(date_enlevement__range=(periode_du, periode_au))
    if dossiers_id:
        dataset_enlevements = dataset_enlevements.exclude(ordretransport__commande__id__in = dossiers_id)
    
    if marchandises_id:
        dataset_enlevements = dataset_enlevements.exclude(marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_enlevements = dataset_enlevements.exclude(trajet__id__in = trajets_id)

    if vehicules_id:
        dataset_enlevements = dataset_enlevements.exclude(vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_enlevements = dataset_enlevements.exclude(chauffeur__id__in = chauffeurs_id)


    #TONNAGE TOTAL HT SUR LES ENLEVEMENTS FACTURES
    tonnage_total = dataset_enlevements.aggregate(tonnage_total = Sum(F('quantite')))['tonnage_total']

    # print('tonnage = ', tonnage_total)
    tonnage_mois  = dataset_enlevements.values_list('date_enlevement__month').annotate(poids = Sum('quantite'))
    # print('tonnage par mois = ', tonnage_mois)
    ### tonnage par mois =  <QuerySet [(3, 6305.0), (1, 3120.0), (2, 3.0)]>
    tonnage_mensuel = [(lesMois[i[0]-1], i[1]) for i in tonnage_mois]
    # print('tonnage mensuel = ', tonnage_mensuel)

    tonnage_mensuel = [(i, j[1]) for i in lesMois for j in tonnage_mensuel if i == j[0]]
    # print('ooooooooooooo = ', tonnage_mensuel)
    
    # TONNAGE  PAR MOIS - 
    if tonnage_mensuel:
        data_tonnage = tonnage_mensuel[:]
        tonnage_mensuel_plus_eleve = max(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moins_eleve = min(data_tonnage, key=lambda x:x[1])
        tonnage_mensuel_moyen = sum(tuple(zip(*data_tonnage))[1])/len(data_tonnage)

        data_tonnage = [t for x in lesMois for t in data_tonnage[:] if t[0] == x]
        data_tonnage.insert(0, ('Mois', 'Tonnage'))
        #print("data = ", chiffre_affaire_mensuel_moins_eleve)
        data_tonnage=json.dumps(data_tonnage)# METTRE LA LISTE AU FORMAT JSON

    ### TONNAGE PAR CLIENT
    tonnage_client_list  = list(dataset_enlevements.values_list('ordretransport__commande__client__raison_sociale').annotate(quantite=Sum('quantite')))
    tonnage_client_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_client = tonnage_client_list[:]
    data_tonnage_client.insert(0, ('Clients', 'Tonnage'))
    data_tonnage_client = json.dumps(data_tonnage_client)


    ### TONNAGE PAR PRODUIT
    tonnage_produit_list  = list(dataset_enlevements.values_list('marchandise__libelle').annotate(quantite=Sum('quantite')))
    tonnage_produit_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_produit = tonnage_produit_list[:]
    data_tonnage_produit.insert(0, ('Produits', 'Tonnage'))
    data_tonnage_produit = json.dumps(data_tonnage_produit)

    ### TONNAGE PAR CHAUFFEUR
    tonnage_chauffeur_list  = list(dataset_enlevements.values_list('chauffeur__matricule', 'chauffeur__nom', 'chauffeur__prenoms').annotate(quantite=Sum('quantite')))
    tonnage_chauffeur_list.sort(reverse=True, key=lambda x: x[3])

    data_tonnage_chauffeur = [ (i[0]+' '+i[1], i[3]) for i in tonnage_chauffeur_list[:]]

    data_tonnage_chauffeur.insert(0, ('Chauffeurs', 'Tonnage'))
    data_tonnage_chauffeur = json.dumps(data_tonnage_chauffeur)


    ### TONNAGE PAR VEHICULE
    tonnage_vehicule_list  = list(dataset_enlevements.values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite')))
    tonnage_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_tonnage_vehicule = [ (i[0], i[2]) for i in tonnage_vehicule_list[:]]
    data_tonnage_vehicule.insert(0, ('Véhicules', 'Tonnage'))
    data_tonnage_vehicule = json.dumps(data_tonnage_vehicule)


    ### TONNAGE PAR DOSSIER / NBRE DE VEHICULE
    tonnage_dossier_list  = list(dataset_enlevements.values_list('ordretransport__commande__numero_dossier').annotate(quantite=Sum('quantite'), vehicule=Count('vehicule__immatriculation')))
    tonnage_dossier_list.sort(reverse=True, key=lambda x: x[1])

    data_tonnage_dossier = [(i[0], i[1], i[2]) for i in tonnage_dossier_list[:]]
    data_tonnage_dossier.insert(0, ('Dossiers', 'Tonnage', 'Véhicule'))
    data_tonnage_dossier = json.dumps(data_tonnage_dossier)

    
    #CARBURANT 
    dataset_carburants = Carburant.consommation_view().filter(date_prise__range=(periode_du, periode_au))

    if dossiers_id:pass
        #dataset_carburants = dataset_carburants.exclude(commande__id__in = dossiers_id)
    """
    if marchandises_id:
        dataset_carburants = dataset_carburants.exclude(marchandise__id__in = marchandises_id)

    if trajets_id:
        dataset_carburants = dataset_carburants.exclude(trajet__id__in = trajets_id)
    
    if vehicules_id:
        dataset_carburants = dataset_carburants.exclude(vehicule__id__in = vehicules_id)

    if chauffeurs_id:
        dataset_carburants = dataset_carburants.exclude(chauffeur__id__in = chauffeurs_id)
    """

    carburant_total = dataset_carburants.aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant totale = ', carburant_total)

    carburant_prefinancement = dataset_carburants.filter(imputation="Préfinancement").aggregate(quantite_totale=Sum('quantite'), montant_total=Sum('montant'))
    # print('carburant carburant_prefinancement = ', carburant_prefinancement)

    quantite_mois  = dataset_carburants.filter(imputation="Préfinancement").values_list('date_prise__month').annotate(quantite=Sum('quantite'), montant=Sum('montant'))

    quantite_mensuelle = [(lesMois[i[0]-1], i[1], i[2]) for i in quantite_mois]
    # print('quantite mensuelle = ', quantite_mensuelle)

    quantite_mensuelle_carburant = [(i, j[1], j[2]) for i in lesMois for j in quantite_mensuelle if i == j[0]]
    # print('ooooooooooooo = ', quantite_mensuelle_carburant)
    
    # QUANTITE PAR MOIS - 
    if quantite_mensuelle_carburant:
        data_quantite_carburant = quantite_mensuelle_carburant[:]
        quantite_mensuelle_plus_eleve = max(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moins_eleve = min(data_quantite_carburant, key=lambda x:x[1])
        quantite_mensuelle_moyen = sum(tuple(zip(*data_quantite_carburant))[1])/len(data_quantite_carburant)

        data_quantite_carburant = [t for x in lesMois for t in data_quantite_carburant[:] if t[0] == x]
        data_quantite_carburant.insert(0, ('Mois', 'Quantité', 'Montant'))
        data_quantite_carburant = json.dumps(data_quantite_carburant)

    ### CARBURANT PAR VEHICULE / NBRE DE VEHICULE
    carburant_vehicule_list  = list(dataset_carburants.filter(imputation="Préfinancement").values_list('vehicule__immatriculation', 'vehicule__marque__libelle').annotate(quantite=Sum('quantite'), montant=Sum('montant')))
    carburant_vehicule_list.sort(reverse=True, key=lambda x: x[2])

    data_quantite_vehicule = [(i[0]+' '+i[1], i[2], i[3]) for i in carburant_vehicule_list[:]]
    data_quantite_vehicule.insert(0, ('Véhicules', 'Quantité', 'Montant'))
    data_quantite_vehicule = json.dumps(data_quantite_vehicule)

    return render(request, 'tableaubord/enlevement_filtrer.html', locals())


def vehicule_tableaubord(request):
    type_alerte_vehicule = {}
    type_alerte_chauffeur = {}
    type_alerte_entretien = {}

    dataset = Alerte.alerte_view()
    vehicule_list = dataset['vehicule_list']
    type_alerte_vehicule['assurance']=len(list(filter(lambda x: x.assurance <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['visite']=len(list(filter(lambda x: x.visite <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['stationnement']=len(list(filter(lambda x: x.stationnement <= 0, dataset['vehicule_list'])))
    type_alerte_vehicule['patente']=len(list(filter(lambda x: x.patente <= 0, dataset['vehicule_list'])))
    total_alerte_vehicule = sum(type_alerte_vehicule.values())
    
    chauffeur_list = dataset['chauffeur_list']
    type_alerte_chauffeur['piece']=len(list(filter(lambda x: x.piece <= 0, dataset['chauffeur_list'])))
    type_alerte_chauffeur['permis']=len(list(filter(lambda x: x.permis <= 0, dataset['chauffeur_list'])))
    type_alerte_chauffeur['acces']=len(list(filter(lambda x: x.acces <= 0, dataset['chauffeur_list'])))
    total_alerte_chauffeur = sum(type_alerte_chauffeur.values())

    entretien_list = dataset['entretien_list']
    type_alerte_entretien['entretien']=len(list(filter(lambda x: x.prochain <= 0, dataset['entretien_list'])))
    total_alerte_entretien = sum(type_alerte_entretien.values())

    return render(request, 'tableaubord/vehicule_tableaubord.html', locals())


def chauffeur_tableaubord(request):
    dataset = Alerte.alerte_view()
    chauffeur_list = dataset['chauffeur_list']
    return render(request, 'tableaubord/chauffeur_tableaubord.html', locals())


def entretien_tableaubord(request):
    dataset = Alerte.alerte_view()
    print ("alerte = ", dataset)
    vehicule_list = dataset['vehicule_list']
    for i in vehicule_list:
        print("assurance = ", i.assurance)
        print("visite = ", i.visite)
        print("stationnement = ", i.stationnement)
        print("patente = ", i.patente)
    return render(request, 'tableaubord/entretien_tableaubord.html', locals())


def carburant_tableaubord(request):
    dataset = Alerte.alerte_view()
    print ("alerte = ", dataset)
    vehicule_list = dataset['vehicule_list']
    for i in vehicule_list:
        print("assurance = ", i.assurance)
        print("visite = ", i.visite)
        print("stationnement = ", i.stationnement)
        print("patente = ", i.patente)
    return render(request, 'tableaubord/carburant_tableaubord.html', locals())


def reparation_tableaubord(request):
    dataset = Alerte.alerte_view()
    print ("alerte = ", dataset)
    vehicule_list = dataset['vehicule_list']
    for i in vehicule_list:
        print("assurance = ", i.assurance)
        print("visite = ", i.visite)
        print("stationnement = ", i.stationnement)
        print("patente = ", i.patente)
    return render(request, 'tableaubord/reparation_tableaubord.html', locals()) 