# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.views import generic
from django.conf import settings
from django.db.models import Sum, F
from parametre.forms import PeriodeForm
from parametre.models import Commande, Detailscommande, Client, Ordretransport, Marchandise, Trajet, Societe, Para, Devis#from parametre.forms import PeriodeForm
from commande.forms import *
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from Utilitaire import *
from ImprimerDoc import *
import random
import os
from datetime import datetime, timedelta

from alerte_synthese import *
from django.core import serializers

class CreateClient(CreatePopupMixin, generic.CreateView):
    model = Client
    fields = ['raison_sociale', 'adresse', 'telephone', 'cellulaire', 'boite_postale', 'compte_contribuable',
    'registre_commerce']
    template_name = 'commande/client_form.html'

class CreateMarchandise(CreatePopupMixin, generic.CreateView):
    model = Marchandise
    fields = ['etat_marchandise', 'libelle']
    template_name = 'commande/marchandise_form.html'

class CreateTrajet(CreatePopupMixin, generic.CreateView):
    model = Trajet
    fields = ['source', 'destination', 'kilometrage']
    template_name = 'commande/trajet_form.html'


def accueil(request):
    form = PeriodeForm()
    periode_du = form['periode_du'].value()
    periode_au = form['periode_au'].value()
    commande_list = Commande.objects.all()
    for i in commande_list:
        i.montant_commande = Detailscommande.objects.filter(commande = i).aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']
    montant_total = Detailscommande.objects.aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']  
    
    client_list = Client.objects.order_by('raison_sociale')
    navire_list = [ i[0] for i in list(set(list(Commande.objects.values_list('navire')) + list(Devis.objects.values_list('navire')))) if i[0] ]
    return render(request, 'commande/commande_lister.html', locals())


def commande_filtrer(request):
    if request.method == 'GET' and request.is_ajax():
        id_client = request.GET.get('id_client')
        id_navire = request.GET.get('id_navire')
        id_tarification = request.GET.get('id_tarification')
        id_periode_du = request.GET.get('id_periode_du')
        id_periode_au = request.GET.get('id_periode_au')

        commande_list = Commande.objects.filter(date_commande__range=[id_periode_du, id_periode_au])
        
        if id_client not in ('-1', None):
            commande_list = commande_list.filter(client__id = id_client)

        if id_navire not in ('-1', None):
            commande_list = commande_list.filter(navire = id_navire)

        if id_tarification not in ('-1', None):
            commande_list = commande_list.filter(mode_tarification = id_tarification)

        for i in commande_list:
            i.montant_commande = Detailscommande.objects.filter(commande = i).aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']
        montant_total = Detailscommande.objects.filter(commande__in = commande_list).aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']  
        return render(request, 'commande/commande_lister_filtrer.html', locals())

def commande_creer(request):
    form = CommandeForm()
    if request.method == 'POST':
        form = CommandeForm(request.POST, request.FILES)
        if form.is_valid():
            para = Para.objects.all()[0]
            cde = form.save(commit=False)
            cde.numero_dossier = 'DOS{0}-{1}'.format(str(datetime.today().year)[2:], str(para.numero_commande+1).zfill(3))
            cde.save()
            # creation de OT QUI_ENLEVE = ((, 'Coco Inter'), ('Sous-Traitance', 'Sous-Traitance'),)
            Ordretransport.objects.create(
                commande = cde, 
                qui_enleve = 'Coco Inter', 
                numero_ot = 'OT{0}-{1}'.format(str(datetime.today().year)[2:], str(para.numero_ot+1).zfill(3))
            )
            para.numero_commande +=1
            para.numero_ot +=1
            para.save() 
            if 'enregistrer_ajouter_detail' in request.POST:
                return HttpResponseRedirect('/detailscommande/detailscommande_creer/{0}/'.format(cde.id))

            return HttpResponseRedirect('/commande/accueil/')
        return render(request, 'commande/commande_creer.html', locals())    
    return render(request, 'commande/commande_creer.html', locals())


def commande_modifier(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    form = CommandeForm(instance=commande)
    if request.method == 'POST':
        form = CommandeForm(request.POST, request.FILES, instance=commande)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/commande/accueil/')
        return render(request, 'commande/commande_modifier.html', locals()) 
    return render(request, 'commande/commande_modifier.html', locals())


def commande_visualiser(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    form = CommandeForm(instance=commande)
    return render(request, 'commande/commande_visualiser.html', locals())


def commande_delete(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    data = dict()
    if request.method == 'POST':
        commande.delete()
        return HttpResponseRedirect('/commande/accueil/')
    else:
        context = {'commande': commande}
        data['html_form'] = render_to_string('commande/commande_delete.html', context, request=request)
    return JsonResponse(data)


def commande_imprimer(request, pk):
    #user=request.user
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
    montant_total_ht = 0
    montant_tva = 0
    montant_carburant = 0
    commande = get_object_or_404(Commande, pk=pk)
    detail_list = Detailscommande.objects.filter(commande=commande)
    montant_total_ht = detail_list.aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
       
    context = {'commande': commande,
    'detail_list':detail_list,
    'montant_total_ht':int(montant_total_ht),
    'montant_net_lettre':chiffreLettre(int(montant_total_ht)),
    }

    ligneHauteur = 1.2
    imprimerPDF = ImprimerDoc()
    imprimerPDF.story = []
    entetePage(imprimerPDF)
    #imprimerPDF.story.append(Spacer(0,0.1*inch))
    fichier = settings.CHEMIN_ETATS+"commande" + str(random.randint(1,10000))+'.pdf'

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
    ('BC N° {0}'.format(iif(commande.numero_commande, commande.numero_commande, '')), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('ADRESSE DE LIVRAISON', '', '', '', '', '', '', '', '', '', '', '', 'DOIT : ', '', '', '', '',  '', ''),
    ('{0}'.format(iif(commande.lieu_dechargement, commande.lieu_dechargement, '')), '', '', '', '', '', '', '', '', '', '', '','{0}'.format(commande.client),  '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '','{0}'.format(iif(commande.client.adresse, commande.client.adresse, '')), '', '', '',  '',  '', ''),
    ('VOS REFERENCES', '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(commande.client.telephone, commande.client.telephone, '')), '', '', '', '',  '', ''),
    ('{0}'.format(iif(commande.navire, commande.navire, '')), '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(commande.client.registre_commerce, commande.client.registre_commerce, '')), '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('NOS REFERENCES', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('Dossier : {0}'.format(commande.numero_dossier), '', '', '', '', '', '', '', '', '', '', '','Abidjan, le {0}'.format(dateAnglaisFrancais(commande.date_commande)),  '',  '', '', '',  '', ''),
    ]
    
    t=Table(zone_entete,[25, 25], len(zone_entete)*[0.5*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 1, colors.black),
    
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    rubrique_list=[]
    k=0
    data=[]
    for i in detail_list:
        k+=1
        total_ligne=''
        
        if (i.quantite and i.prix_unitaire):
            total_ligne = millier(int(i.quantite * i.prix_unitaire))

        if commande.mode_tarification !="Tonnage":
            if i.quantite != None:quantite = millier(int(i.quantite))
            else: quantite = i.quantite   
        else:quantite = floatChaine(valeur=i.quantite, point=',', decimal=3)

        rubrique_list.append((k, i.rubrique.count("\n")+1))

        data.append(
            (str(k).zfill(2),
            reduireChaine(i.marchandise.libelle, 30) + ' ' + \
            iif(i.marchandise.etat_marchandise !='Service', '(Tonne)', '') +'\n'+ \
            'itinéraire : '+ \
            reduireChaine(i.trajet.source.libelle +' - '+i.trajet.destination.libelle, 40)+iif(i.rubrique, '\n'+i.rubrique.replace("\r", ""),''),
            '',
            quantite,
            millier(int(i.prix_unitaire)) if i.prix_unitaire else '',
            total_ligne
        ))

    nombre_ligne = k
    print('nombre_ligne = ', nombre_ligne)

    hauteur_flexible = [i[1]*0.8*cm if i[1] > 1 else 1.3*cm for i in rubrique_list[:]]
    print('hauteur hauteur_flexible = ', hauteur_flexible)

    data.insert(0, ('N°', 'RUBRIQUES', '', 'QUANTITE', 'PU HT', 'MONTANT'))
    data.append(('MONANT TOTAL', '', '', '', '', millier(int(montant_total_ht))))

    nombre_ligne_total = len(data)
    print('nombre_ligne_total = ', nombre_ligne_total)

    zone_details = data[:]
    t=Table(zone_details,[25, 300, 0, 55, 50, 70], [0.7*cm] + hauteur_flexible + (nombre_ligne_total-nombre_ligne-1)*[0.6*cm])
    GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
    
    ('ALIGN', (0,0), (0,-1), 'CENTER'),

    ('SPAN', (0,-1), (-2,-1)),
    ('ALIGN', (0,-1), (-2,-1), 'RIGHT'),
    ]

    """
    for i in ligne_ot:
        GRID_STYLE.append(('SPAN', (0,i), (-1,i)))
        GRID_STYLE.append(('ALIGN', (0,i), (-1,i), 'LEFT'))
    """    
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    zone_pied=[
('ARRETE LA PRESENTE FACTURE A LA SOMME DE : {0} FRANCS CFA'.format(context['montant_net_lettre'].upper()), '', '', '',''),
    ('', '', '', 'VISA SERVICE COMPTABILITE', ''),
    ]

    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    zone_pied = [[Paragraph(cell, s) for cell in row] for row in zone_pied[:]]

    t=Table(zone_pied,[100, 100, 100, 100, 75], len(zone_pied)*[ligneHauteur*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('SPAN', (0,0), (-1,0)),
    ('ALIGN', (0,0), (-1,0), 'LEFT'),

    ('SPAN', (3,0), (-1,0)),
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