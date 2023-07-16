# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum, Avg, F
from parametre.models import Facturation, Enlevement, Ordretransport, Carburant, Societe, Depense, Reglement, Client 
from facturation.forms import *
from parametre.forms import PeriodeForm
from Utilitaire import *
from ImprimerDoc import *
import random
import os
from datetime import datetime, timedelta


def accueil(request):
    form = PeriodeForm()
    periode_du = form['periode_du'].value()
    periode_au = form['periode_au'].value()

    facturation_list = Facturation.objects.order_by('-date_facture')
    context={'facturation_list':facturation_list }
    foot_montant=[]
    try:
        foot_montant = [(i.facture_commande()['montant_total_ht'], 
        i.facture_commande()['montant_tva'],     
        i.facture_commande()['montant_avance'],
        i.facture_commande()['montant_carburant'],
        i.facture_commande()['montant_debours'],
        i.facture_commande()['montant_net'],   
        i.facture_commande()['montant_reglement'],  
        i.facture_commande()['montant_solde']) 
        for i in facturation_list]
    except:pass
    try:
        foot_montant_ht = sum(list(zip(*foot_montant))[0])
        foot_montant_tva = sum(list(zip(*foot_montant))[1])
        foot_montant_ttc = foot_montant_ht + foot_montant_tva
        foot_montant_avance = sum(list(zip(*foot_montant))[2])
        foot_montant_carburant = sum(list(zip(*foot_montant))[3])
        foot_montant_debours = sum(list(zip(*foot_montant))[4])
        foot_montant_net = sum(list(zip(*foot_montant))[5])
        foot_montant_reglement = sum(list(zip(*foot_montant))[6])
        foot_montant_solde = sum(list(zip(*foot_montant))[7])
    except:
        foot_montant_ht = 0    
        foot_montant_tva = 0
        foot_montant_ttc = 0
        foot_montant_avance = 0
        foot_montant_carburant = 0
        foot_montant_debours = 0                
        foot_montant_net = 0
        foot_montant_reglement = 0
        foot_montant_solde = 0
    
    client_list = Client.objects.order_by('raison_sociale')
    date_list = [ dateAnglaisFrancais(i['date_facture']) for i in Facturation.objects.values('date_facture').order_by('-date_facture')]
    return render(request, 'facturation/facturation_lister.html', locals())


def alerte_prise_carburant(request):
    if request.method=='GET' and request.is_ajax():
        id_commande= request.GET.get('id_commande', None)
        if id_commande:
            montant = Carburant.objects.filter(ordretransport__commande=int(id_commande)).aggregate(Sum('montant'))['montant__sum']
            if montant:data={'reponse':'PRISE DE CARBURANT : {}'.format(millier(montant))}
            else:data={'reponse':'AUCUNE PRISE DE CARBURANT'}
        else:
            data={'reponse':''}
    else:
        data={'reponse':''}
    return JsonResponse(data)


def facturation_lister_filtrer(request):
    foot_montant_ht = 0
    foot_montant_tva = 0
    foot_montant_ttc = 0
    foot_montant_avance = 0
    foot_montant_carburant = 0
    foot_montant_debours = 0
    foot_montant_net = 0
    foot_montant_reglement = 0
    foot_montant_solde = 0

    if request.method == 'GET' and request.is_ajax():
        id_client = request.GET.get('id_client')
        id_etat = request.GET.get('id_etat')
        id_date = request.GET.get('id_date')
        id_periode_du = request.GET.get('id_periode_du')
        id_periode_au = request.GET.get('id_periode_au')
        
        facturation_list = Facturation.objects.filter(date_facture__range=[id_periode_du, id_periode_au]).order_by('-date_facture')

        if id_client not in ('-1', None):
            facturation_list = facturation_list.filter(commande__client__id = id_client)

        if id_etat not in ('-1', None):
            facturation_list = facturation_list.filter(etat_facture = id_etat)
            print("fac", facturation_list)

        if id_date not in ('-1', None):
            facturation_list = facturation_list.filter(date_facture = dateAnglais(id_date))

        context={'facturation_list':facturation_list }
        foot_montant=[]
        try:
            foot_montant = [(i.facture_commande()['montant_total_ht'], 
            i.facture_commande()['montant_tva'],     
            i.facture_commande()['montant_avance'],
            i.facture_commande()['montant_carburant'],
            i.facture_commande()['montant_debours'],
            i.facture_commande()['montant_net'],   
            i.facture_commande()['montant_reglement'],  
            i.facture_commande()['montant_solde']) 
            for i in facturation_list]
        except:pass
        try:
            foot_montant_ht = sum(list(zip(*foot_montant))[0])
            foot_montant_tva = sum(list(zip(*foot_montant))[1])
            foot_montant_ttc = foot_montant_ht + foot_montant_tva
            foot_montant_avance = sum(list(zip(*foot_montant))[2])
            foot_montant_carburant = sum(list(zip(*foot_montant))[3])
            foot_montant_debours = sum(list(zip(*foot_montant))[4])
            foot_montant_net = sum(list(zip(*foot_montant))[5])
            foot_montant_reglement = sum(list(zip(*foot_montant))[6])
            foot_montant_solde = sum(list(zip(*foot_montant))[7])
        except:
            foot_montant_ht = 0
            foot_montant_tva = 0
            foot_montant_ttc = 0
            foot_montant_avance = 0
            foot_montant_carburant = 0
            foot_montant_debours = 0
            foot_montant_net = 0
            foot_montant_reglement = 0
            foot_montant_solde = 0
    
        html_footer = """
          <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td align="right"><b>Cumul</b></td>
            <td align="right"><b>{0}</b></td>
            <td align="right"><b>{1}</b></td>
            <td align="right"><b>{2}</b></td>
            <td align="right"><b>{3}</b></td>
            <td align="right"><b>{4}</b></td>
            <td></td> 
          </tr>""".format(
                millier(foot_montant_ht),
                millier(foot_montant_tva),
                millier(foot_montant_ttc),
                millier(foot_montant_avance + foot_montant_carburant + foot_montant_debours),                 
                millier(foot_montant_net)
        )
    return render(request, 'facturation/facturation_lister_filtrer.html', locals())

def facturation_creer(request):
    form = FacturationForm(initial={'tva':Societe.objects.get(pk=1).tva})
    print(form)
    if request.method == 'POST':
        form = FacturationForm(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.numero_facture = 'FA{0}-{1}'.format(str(datetime.today().year)[2:],str(Facturation.objects.count()+1).zfill(3))
            f.save()
            return HttpResponseRedirect('/facturation/accueil/')
        return render(request, 'facturation/facturation_creer.html', locals())  
    return render(request, 'facturation/facturation_creer.html', locals())


def facturation_modifier(request, pk):
    facturation = get_object_or_404(Facturation, pk=pk)
    if request.method == 'POST':
        form = FacturationForm(request.POST, request.FILES, instance=facturation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/facturation/accueil/')
        return render(request, 'facturation/facturation_modifier.html', locals())   
    form = FacturationForm(instance=facturation)
    return render(request, 'facturation/facturation_modifier.html', locals())


def facturation_delete(request, pk):
    facturation = get_object_or_404(Facturation, pk=pk)
    data = dict()
    if request.method == 'POST':
        facturation.delete()
        return HttpResponseRedirect('/facturation/accueil/')
    else:
        context = {'facturation': facturation}
        data['html_form'] = render_to_string('facturation/facturation_delete.html', context, request=request)
    return JsonResponse(data)


def facturation_visualiser(request, pk):
    societe = Societe.objects.get(pk=1)
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
        'marchandise__libelle',
        'rubrique').order_by(
                                'ordretransport__numero_ot', 
                                'marchandise__libelle').annotate(
                                quantite=Sum(F('quantite')),
                                pu=Avg(F('prix_unitaire')),
                                total=Sum((F('quantite') * F('prix_unitaire'))),
                            )
    for i in enlevement_group:
        if ot_dict.get(i[0]):
            ot_dict[i[0]].append(i[1:])
            montant_total_ht+=i[6]
        else:
            ot_dict[i[0]] = [i[1:]]  
            montant_total_ht+=i[6]
    #print("montant_total_ht", montant_total_ht)
    #print("ot_dict", ot_dict)

    # CARBURANT
    montant_tva = montant_total_ht * societe.tva
    montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
    if montant_carburant is None:montant_carburant=0

    montant_depense = Depense.objects.filter(ordretransport__in=ot_list).values_list("type_depense").annotate(Sum('montant'))
    #print("montant depense", montant_depense)

    if montant_depense is None:montant_depense=0

    context = {'facturation': facturation, 
    'ot_list':ot_list, 
    'enlevement_list':enlevement_list,
    'ot_dict':ot_dict,
    'montant_total_ht':montant_total_ht,
    'montant_tva':montant_tva,

    'montant_carburant':montant_carburant,
    'montant_net':montant_total_ht+montant_tva-montant_carburant,
    'montant_net_lettre':chiffreLettre(int(montant_total_ht+montant_tva-montant_carburant)),
    }
    return render(request, 'facturation/facturation_visualiser.html', context)


def facturation_situation_ca(request):
    facturation_list=[]
    form = PeriodeForm()
    if request.POST:
        form = PeriodeForm(request.POST)
        if form.is_valid():
            facturation_list = [ i for i in Facturation.objects.order_by('-date_facture').filter(date_facture__range = [form.cleaned_data['periode_du'], form.cleaned_data['periode_au']])]
            try:
                foot_montant = [(i.facture_commande()['montant_total_ht'], 
                i.facture_commande()['montant_tva'],     
                i.facture_commande()['montant_avance'],
                i.facture_commande()['montant_carburant'],
                i.facture_commande()['montant_debours'],
                i.facture_commande()['montant_net'],   
                i.facture_commande()['montant_reglement'],  
                i.facture_commande()['montant_solde']) 
                for i in facturation_list]
            except:pass
            try:
                foot_montant_ht = sum(list(zip(*foot_montant))[0])
                foot_montant_tva = sum(list(zip(*foot_montant))[1])
                foot_montant_ttc = foot_montant_ht + foot_montant_tva
                foot_montant_avance = sum(list(zip(*foot_montant))[2])
                foot_montant_carburant = sum(list(zip(*foot_montant))[3])
                foot_montant_debours = sum(list(zip(*foot_montant))[4])
                foot_montant_net = sum(list(zip(*foot_montant))[5])
                foot_montant_reglement = sum(list(zip(*foot_montant))[6])
                foot_montant_solde = sum(list(zip(*foot_montant))[7])
            except:
                foot_montant_ht = 0    
                foot_montant_tva = 0
                foot_montant_ttc = 0
                foot_montant_avance = 0
                foot_montant_carburant = 0
                foot_montant_debours = 0                
                foot_montant_net = 0
                foot_montant_reglement = 0
                foot_montant_solde = 0
    return render(request, 'facturation/facturation_situation_ca.html', locals())


def facturation_situation_impaye(request):
    facturation_list=[]
    form = PeriodeForm()
    if request.POST:
        form = PeriodeForm(request.POST)
        if form.is_valid():
            facturation_list = [ i for i in Facturation.objects.order_by('-date_facture').filter(date_facture__range = [form.cleaned_data['periode_du'], form.cleaned_data['periode_au']]) if i.facture_commande()['montant_solde']]
            try:
                foot_montant = [(i.facture_commande()['montant_total_ht'], 
                i.facture_commande()['montant_tva'],     
                i.facture_commande()['montant_avance'],
                i.facture_commande()['montant_carburant'],
                i.facture_commande()['montant_debours'],
                i.facture_commande()['montant_avance_carburant_debours'],
                i.facture_commande()['montant_net'],   
                i.facture_commande()['montant_reglement'],  
                i.facture_commande()['montant_solde']) 
                for i in facturation_list]
            except:pass
            try:
                foot_montant_ht = sum(list(zip(*foot_montant))[0])
                foot_montant_tva = sum(list(zip(*foot_montant))[1])
                foot_montant_ttc = foot_montant_ht + foot_montant_tva
                foot_montant_avance = sum(list(zip(*foot_montant))[2])
                foot_montant_carburant = sum(list(zip(*foot_montant))[3])
                foot_montant_debours = sum(list(zip(*foot_montant))[4])
                foot_montant_avance_carburant_debours = sum(list(zip(*foot_montant))[5])
                foot_montant_net = sum(list(zip(*foot_montant))[6])
                foot_montant_reglement = sum(list(zip(*foot_montant))[7])
                foot_montant_solde = sum(list(zip(*foot_montant))[8])
            except:
                foot_montant_ht = 0    
                foot_montant_tva = 0
                foot_montant_ttc = 0
                foot_montant_avance = 0
                foot_montant_carburant = 0
                foot_montant_debours = 0  
                foot_montant_abvance_carburant_debours = 0              
                foot_montant_net = 0
                foot_montant_reglement = 0
                foot_montant_solde = 0
    return render(request, 'facturation/facturation_situation_impaye.html', locals())


def facturation_imprimer(request, pk):
    #user=request.user
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
    montant_total_ht = 0
    montant_tva = 0
    montant_carburant = 0
    facturation = get_object_or_404(Facturation, pk=pk)
    ot_list = facturation.commande.ordretransport_set.all() 

    enlevement_list = Enlevement.objects.filter(ordretransport__in = ot_list).order_by('-date_enlevement')
    #print("LES OTS = ", enlevement_list)
    enlevement_group = enlevement_list.values_list(
        'ordretransport__numero_ot', 
        'trajet__source__libelle', 
        'trajet__destination__libelle', 
        'marchandise__libelle',
        'rubrique').order_by(
                            'ordretransport__numero_ot', 
                            'marchandise__libelle').annotate(
                            qte=Sum(F('quantite')),
                            pu=F('prix_unitaire'),
                            total=Sum(F('quantite') * F('prix_unitaire'))
        )
    #print("LES enlevement_group = ", enlevement_group)
    for i in enlevement_group:
        if ot_dict.get(i[0]):
            ot_dict[i[0]].append(i[1:])
            montant_total_ht+=i[7]
        else:
            ot_dict[i[0]] = [i[1:]]  
            montant_total_ht+=i[7]
    #print("enlevement_group", len(enlevement_group.values()))
    #print("ot_dict", ot_dict)
    montant_total_ht = int(montant_total_ht)
    # CARBURANT
    montant_tva = int(montant_total_ht * facturation.tva)

    montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
    if montant_carburant is None:montant_carburant=0

    montant_total_ttc = int(montant_total_ht+montant_tva)
    montant_net = int(montant_total_ttc-facturation.avance-montant_carburant-facturation.debours)

    context = {'facturation': facturation, 
    'ot_list':ot_list, 
    'enlevement_list':enlevement_list,
    'ot_dict':ot_dict,
    'montant_total_ht':int(montant_total_ht),
    'montant_tva':int(montant_tva),
    'montant_total_ttc':int(montant_total_ttc),
    'montant_avance':facturation.avance,
    'montant_carburant':int(montant_carburant),
    'montant_debours':facturation.debours,
    'montant_net':int(montant_net),
    'montant_net_lettre':chiffreLettre(montant_net),
    }

    carburant_prise_list = []
    if montant_carburant:
        ### toutes les prises de carburants
        carburant_prise_list = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement')
    #if carburant_prise_list: return HttpResponseRedirect('facturation/facturation_imprimer_carburant/{0}'.format(facturation.id))
   
    ligneHauteur = 5
    imprimerPDF = ImprimerDoc()
    imprimerPDF.story = []
    #entetePage(imprimerPDF)
    #imprimerPDF.story.append(Spacer(0,0.1*inch))
    fichier = settings.CHEMIN_ETATS+"facturation" + str(random.randint(1,10000))+'.pdf'

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='JustifyInd', alignment=TA_JUSTIFY, firstLineIndent=24))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    
    #Configure style and word wrap
    #s = getSampleStyleSheet()
    #s = s["BodyText"]
    #s.wordWrap = 'LTR'#'CJK'  
    #s.wordWrap = 'LTR'

    zone_entete=[
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('ADRESSE DE LIVRAISON', '', '', '', '', '', '', '', '', '', '', '', 'DOIT : ', '', '', '', '',  '', ''),
    ('{0}'.format(iif(facturation.commande.lieu_dechargement, facturation.commande.lieu_dechargement, '')), '', '', '', '', '', '', '', '', '', '', '','{0}'.format(facturation.commande.client),  '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '','{0}'.format(iif(facturation.commande.client.adresse, facturation.commande.client.adresse, '')), '', '', '',  '',  '', ''),
    ('VOS REFERENCES', '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(facturation.commande.client.telephone, facturation.commande.client.telephone, '')), '', '', '', '',  '', ''),
    ('{0}'.format(iif(facturation.utiliser_ligne_bon_commande==True, facturation.ligne_bon_commande, iif(facturation.commande.numero_commande, 'BC : {0}'.format(facturation.commande.numero_commande), ''))), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('{0}'.format(iif(facturation.commande.navire, facturation.commande.navire, '')), '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(facturation.commande.client.registre_commerce, facturation.commande.client.registre_commerce, '')), '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('NOS REFERENCES', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', ''),
    ('FACTURE N° : {0}'.format(facturation.numero_facture), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('BL : {0}'.format(iif(facturation.bon_livraison, facturation.bon_livraison, '')), '', '', '', '', '', '', '', '', '', '', '','Abidjan, le {0}'.format(dateAnglaisFrancais(facturation.date_facture)),  '',  '', '', '',  '', ''),
    ]
    
    t=Table(zone_entete,[25, 25], len(zone_entete)*[0.5*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 1, colors.black),
    
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    
    rubrique_list = []

    ligne_ot=[]
    k=-1
    for i in ot_dict:
        k+=1
        if not k:ligne_ot.append(1)
        else:ligne_ot.append(len(ot_dict[tampon])+ligne_ot[k-1]+1)
        tampon=i
    data=[]
    
    k=0
    for i in ot_dict:
        #k=0
        for j in ot_dict[i]:
            k+=1
            print('kkkkkkkkkkkk = ', k)
            print("JJJJJJJJJJJJ = ", j[3].count("\n"))
            rubrique_list.append((k, j[3].count("\n")+1))
            data.append(
                (str(k).zfill(2), 
                reduireChaine(j[2], 30) + ' (Tonne)'+'\n'+ \
                'itinéraire : '+ reduireChaine(j[0]+' - '+ j[1], 40)+iif(j[3], '\n'+j[3].replace("\r", ""),''), 
                '',
                floatChaine(valeur=j[4], point=',', decimal=3),
                millier(int(j[5])),
                millier(int(j[6]))
    ))
    print("ooooooooo ", rubrique_list)
    nombre_ligne = k
    print('nombre_ligne kkkk = ', nombre_ligne)

    data.append(('MONTANT TOTAL HT', '', '', '', '', millier(montant_total_ht)))
    data.append(('TVA 18%', '', '', '', '', iif(montant_tva, millier(montant_tva), '-')))
    data.append(('MONTANT TTC', '', '', '', '', millier(montant_total_ttc))) 

    if facturation.avance:
        data.append(('AVANCE PERCUE', '', '', '', '', '-'+ millier(int(facturation.avance))))

    if montant_carburant:
        data.append(('AVANCE CARBURANT', '', '', '', '', '-'+ millier(montant_carburant)))
 
    if facturation.debours:
        data.append(('DEBOURS', '', '', '', '', '-'+ millier(int(facturation.debours))))

    if not any((facturation.avance, montant_carburant, facturation.debours)):
        data.append(('AVANCE PERCUE', '', '', '', '', '-'))

    data.append(('MONTANT NET', '', '', '', '', millier(montant_net)))           
    data.insert(0, ('N°', 'RUBRIQUES', '', 'QUANTITE', 'PU HT', 'MONTANT'))

    nombre_ligne_total = len(data)
    print('nombre_ligne_total = ', nombre_ligne_total)

    hauteur_flexible = [i[1]*0.81*cm if i[1] > 1 else 1.3*cm for i in rubrique_list[:]]
    print('hauteur hauteur_flexible = ', hauteur_flexible)
    zone_details = data[:]
    t=Table(zone_details,[25, 300, 0, 55, 50, 70], [0.7*cm] + hauteur_flexible + (nombre_ligne_total-nombre_ligne-1)*[0.6*cm]
    )
    print('ttttttttttttttttt = ', t)
    GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ]

    for i in range(nombre_ligne+1, nombre_ligne_total):
        GRID_STYLE.append(('SPAN', (0, i), (-2, i)))
        GRID_STYLE.append(('ALIGN', (0, i), (-2, i), 'RIGHT'))

    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    zone_pied = [
    ('ARRETE LA PRESENTE FACTURE A LA SOMME DE : {0}'.format(iif(facturation.utiliser_montant_lettre==True, facturation.montant_lettre, chiffreLettre(montant_net).upper() +' FRANCS CFA')), '', '', '',''),
    ('', '', '', 'VISA SERVICE COMPTABILITE', ''),
    ]

    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    zone_pied = [[Paragraph(cell, s) for cell in row] for row in zone_pied[:]]

    t=Table(zone_pied,[130, 100, 100, 100, 75], len(zone_pied)*[0.6*cm])
    GRID_STYLE=[
        ('SPAN', (0,0), (-1,0)),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        ('SPAN', (3,1), (-1,1)),
    ]

    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.go(fichier, portrait(A4))
    #ouvrirPDF(fichier)
    for i in range(1000):pass
    with open(fichier, 'r', encoding="utf8", errors='ignore') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename='+fichier
        return response
    pdf.closed
    


def facturation_imprimer_carburant(request, pk):
    #user=request.user
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
    montant_carburant = 0
    facturation = get_object_or_404(Facturation, pk=pk)
    ot_list = facturation.commande.ordretransport_set.all() 

    montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
    if montant_carburant is None:montant_carburant=0

    carburant_prise_list = []
    if montant_carburant:
        ### toutes les prises de carburants
        carburant_prise_list = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement')
    #print("carburant prises ok = ", carburant_prise_list) 
    if not carburant_prise_list: return HttpResponseRedirect('facturation/accueil/')

    ligneHauteur = 0.7
    imprimerPDF = ImprimerDoc()
    imprimerPDF.story = []
    fichier = settings.CHEMIN_ETATS+"carburant_prise" + str(random.randint(1,10000))+'.pdf'
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='JustifyInd', alignment=TA_JUSTIFY, firstLineIndent=24))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
   
    imprimerPDF.story.append(Paragraph("<b><h1>PRISES DE CARBURANT POUR LE PREFINANCEMENT</h1></b>", styles['Center']))
    imprimerPDF.story.append(Paragraph("<b><h2>DOSSIER : {0}, CLIENT : {1}</h2></b>".format(facturation.commande.numero_dossier, facturation.commande.client), styles['Center']))
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    data_carburant = []
    if carburant_prise_list:
        for i in carburant_prise_list:
            data_carburant.append((
                dateAnglaisFrancais(i.date_prise),
                i.numero_bon,
                i.type_carburant,
                i.vehicule,
                i.chauffeur,
                floatChaine(i.quantite),
                millier(i.montant),
                #i.kilometrage,
                i.prix_pompe,
                reduireChaine(i.station,30),
            ))
    quantite_total = sum(map(lambda x: nombre(x), list(zip(*data_carburant))[5]))
    montant_total = sum(map(lambda x: nombre(x), list(zip(*data_carburant))[6]))
    km_total = sum(map(lambda x: nombre(x), list(zip(*data_carburant))[8]))
    data_carburant.append(('', '', '', '', 'Cumul', millier(quantite_total), millier(montant_total),  '',  ''))
    data_carburant.insert(0, ('Date', 'N° Bon', 'Type', 'Véhicule', 'Chauffeur', 'Quantité', 'Montant', 'P.U', 'Station'))           
    t=Table(data_carburant,[60, 55, 50, 100, 150, 50, 60, 30, 130], len(data_carburant)*[ligneHauteur*cm])
    GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (5,1), (6,-1), 'RIGHT'),
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)

    zone_pied=[
    ('', '', '', '',''),
    ('', '', '', 'VISA SERVICE COMPTABILITE', ''),
    ]
    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    zone_pied = [[Paragraph(cell, s) for cell in row] for row in zone_pied[:]]

    t=Table(zone_pied,[130, 100, 100, 100, 75], len(zone_pied)*[ligneHauteur*cm])
    GRID_STYLE=[
        ('SPAN', (0,0), (-1,0)),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        ('SPAN', (3,1), (-1,1)),
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)

    imprimerPDF.go(fichier, landscape(A4))

    #ouvrirPDF(fichier)

    for i in range(1000):pass
    with open(fichier, 'r', encoding="utf8", errors='ignore') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename='+fichier
        return response
    pdf.closed


def entetePage(imprimer=None):
    try:
        societe=Societe.objects.all()[0]
        imprimer.t._cellvalues[3][0]=Image(societe.logo, width=1.7*inch, height=1*inch) #Image(os.getcwd()+'\\static\\images\\logo.png',width=1.5*inch, height=1.5*inch)
        imprimer.t._cellvalues[2][1]=''
        imprimer.t._cellvalues[3][1]=''
        imprimer.t._cellvalues[4][1]=''
    except:print("erreur de societe")
 
def entetePagePaysage(imprimer=None):
    try:
        societe=Societe.objects.all()[0]
        imprimer.t._cellvalues[3][0]=Image(societe.logo, width=2*inch, height=1.2*inch) #Image(os.getcwd()+'\\static\\images\\logo.png',width=1.5*inch, height=1.5*inch)
        #imprimer.t._cellvalues[0][2]=u"{0}".format(cabinet.telephone)
        #imprimer.t._cellvalues[1][2]=u"{0}".format(cabinet.cellulaire)
        #imprimer.t._cellvalues[2][2]=u"{0}".format(cabinet.email)
        #imprimer.t._cellvalues[3][2]=u"{0}".format(cabinet.telephone)
    except:pass