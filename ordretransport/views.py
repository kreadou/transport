# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum, F, Avg
from parametre.models import *#Ordretransport, Detailsot
from ordretransport.forms import *
from datetime import datetime
from Utilitaire import *
from ImprimerDoc import *
import random
import os
from django.forms import ModelForm, formset_factory, modelformset_factory, inlineformset_factory


def accueil(request):
    montant_total = 0
    ordretransport_list = Ordretransport.objects.order_by('-date_ot')
    for i in ordretransport_list:
        try:
            i.montant_total_ht = Detailsot.objects.filter(ot=i).aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
            montant_total+=i.montant_total_ht
        except:pass

    client_list = Client.objects.order_by('raison_sociale')
    date_list = [ dateAnglaisFrancais(i['date_ot']) for i in Ordretransport.objects.values('date_ot').order_by('-date_ot').distinct()]
    return render(request, 'ordretransport/ordretransport_lister.html', locals())


def ordretransport_lister_filtrer(request):
    if request.method == 'GET' and request.is_ajax():
        id_client = request.GET.get('id_client')
        id_date = request.GET.get('id_date')
        id_executant = request.GET.get('id_executant')

        ordretransport_list = Ordretransport.objects.all()
        if id_client not in ('-1', None):
            ordretransport_list = ordretransport_list.filter(commande__client__id = id_client)

        if id_date not in ('-1', None):
            ordretransport_list = ordretransport_list.filter(date_ot = dateAnglais(id_date))

        if id_executant not in ('-1', None):
            ordretransport_list = ordretransport_list.filter(qui_enleve = id_executant)

        for i in ordretransport_list:
            i.montant_total_ht = Detailsot.objects.filter(ot = i).aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']
        montant_total = Detailsot.objects.filter(ot__in = ordretransport_list).aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']  
    return render(request, 'ordretransport/ordretransport_lister_filtrer.html', locals())


def ordretransport_creer(request):
    form = OrdretransportForm()
    formset = OtFormSet(queryset=Detailsot.objects.none())
    if request.method == 'POST':
        form = OrdretransportForm(request.POST, request.FILES)
        formset = OtFormSet(request.POST)
        if all((form.is_valid(), formset.is_valid())):
            print('111')
            para = Para.objects.all()[0]
            print('222')
            ot=form.save()
            print('333')
            ot.numero_ot = 'OT{0}-{1}'.format(str(datetime.today().year)[2:], str(para.numero_ot+1).zfill(3))  
            print('444')
            ot.save() 
            print('555')
            para.numero_ot += 1            
            print('666')        
            para.save()
            print('777')
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:obj.delete()
            for i in instances:
                try:
                    i.ot=ot
                    i.save()
                except:pass
            return HttpResponseRedirect('/ordretransport/accueil/')
        return render(request, 'ordretransport/ordretransport_creer.html', locals())    
    return render(request, 'ordretransport/ordretransport_creer.html', locals())


def ordretransport_modifier(request, pk):
    ordretransport = get_object_or_404(Ordretransport, pk=pk)
    form = OrdretransportForm(instance=ordretransport)
    formset = OtFormSet(queryset=Detailsot.objects.filter(ot=ordretransport))
    if request.method == 'POST':
        form = OrdretransportForm(request.POST, request.FILES, instance=ordretransport)
        formset = OtFormSet(request.POST)
        if all((form.is_valid(), formset.is_valid())):
            form.save()
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:obj.delete()
            for i in instances:
                try:
                    i.ot=ordretransport
                    i.save()
                    print('ok')
                except:pass
            return HttpResponseRedirect('/ordretransport/accueil/')
        return render(request, 'ordretransport/ordretransport_modifier.html', locals()) 
    return render(request, 'ordretransport/ordretransport_modifier.html', locals())


def ordretransport_visualiser(request, pk):
    ordretransport = get_object_or_404(Ordretransport, pk=pk)
    form = OrdretransportForm(instance=ordretransport)
    return render(request, 'ordretransport/ordretransport_visualiser.html', locals())


def ordretransport_delete(request, pk):
    ordretransport = get_object_or_404(Ordretransport, pk=pk)
    data = dict()
    if request.method == 'POST':
        ordretransport.delete()
        return HttpResponseRedirect('/ordretransport/accueil/')
    else:
        context = {'ordretransport': ordretransport}
        data['html_form'] = render_to_string('ordretransport/ordretransport_delete.html', context, request=request)
    return JsonResponse(data)



def ordretransport_imprimer(request, pk):
    ot = get_object_or_404(Ordretransport, pk=pk)
    detail_list = Detailsot.objects.filter(ot=ot)
    montant_total_ht = detail_list.aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
           

    context = {'ot': ot,
    'detail_list':detail_list,
    'montant_total_ht': int(montant_total_ht) if montant_total_ht else 0,
    'montant_net_lettre':chiffreLettre(int(montant_total_ht)) if montant_total_ht else 0
    }

    ligneHauteur = 1.5
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
    ('OT N° {0}'.format(ot.numero_ot), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('ADRESSE DE LIVRAISON', '', '', '', '', '', '', '', '', '', '', '', 'DOIT : ', '', '', '', '',  '', ''),
    ('{0}'.format(iif(ot.commande.lieu_dechargement, ot.commande.lieu_dechargement, '')), '', '', '', '', '', '', '', '', '', '', '','{0}'.format(ot.commande.client),  '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '','{0}'.format(iif(ot.commande.client.adresse, ot.commande.client.adresse)), '', '', '',  '',  '', ''),
    ('VOS REFERENCES', '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(ot.commande.client.telephone, ot.commande.client.telephone, '')), '', '', '', '',  '', ''),
    ('{0}'.format(iif(ot.commande.navire, ot.commande.navire, '')), '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(ot.commande.client.registre_commerce, ot.commande.client.registre_commerce, '')), '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('NOS REFERENCES', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('{0}'.format(''), '', '', '', '', '', '', '', '', '', '', '','Abidjan, le {0}'.format(dateAnglaisFrancais(ot.commande.date_commande)),  '',  '', '', '',  '', ''),
    ]
    
    t=Table(zone_entete,[25, 25], len(zone_entete)*[0.5*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 1, colors.black),
    
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    k=0
    #flotChaine(valeur, separateur = ' ', point = '.', decimal = 2):
    data=[]
    for i in detail_list:
        k+=1
        total_ligne=''
        
        if (i.quantite and i.prix_unitaire):
            total_ligne = millier(int(i.quantite * i.prix_unitaire))

        if ot.commande.mode_tarification !="Tonnage":
            if i.quantite != None:quantite = millier(int(i.quantite))
            else: quantite = i.quantite   
        else:quantite = floatChaine(valeur=i.quantite, point=',', decimal=3)

        data.append(
            (str(k).zfill(2),
            reduireChaine(i.marchandise.libelle, 30) + ' ' + \
            iif(i.marchandise.etat_marchandise !='Service', '(Tonne)', '') +'\n'+ \
            'itinéraire : '+ \
            reduireChaine(i.trajet.source.libelle +' - '+i.trajet.destination.libelle, 40),
            '',
            quantite,
            millier(int(i.prix_unitaire)) if i.prix_unitaire else '',
            total_ligne
        ))

    data.insert(0, ('N°', 'RUBRIQUES', '', 'QUANTITE', 'PU HT', 'MONTANT'))
    data.append(('MONTANT TOTAL', '', '', '', '', millier(int(montant_total_ht)) if montant_total_ht else ''))

    zone_details = data[:]
    t=Table(zone_details,[25, 300, 0, 55, 50, 70], len(zone_details)*[ligneHauteur*cm])
    GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
    
    ('ALIGN', (0,0), (0,-1), 'CENTER'),

    ('SPAN', (0,-1), (-2,-1)),
    ('ALIGN', (0,-1), (-2,-1), 'RIGHT'),
    ]

    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    zone_pied=[
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
    #('ALIGN', (3,2), (-1,2), 'RIGHT'),
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







def ote_imprimer(request, pk):
    #user=request.user
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
    montant_total_ht = 0
    montant_tva = 0
    montant_carburant = 0
    ot = get_object_or_404(Ordretransport, pk=pk)
    enlevement_list = Enlevement.objects.filter(ordretransport=ot).order_by('-date_enlevement')

    enlevement_group = enlevement_list.values_list(
        'ordretransport__numero_ot', 
        'trajet__source__libelle', 
        'trajet__destination__libelle', 
        'marchandise__libelle').order_by(
                                'ordretransport__numero_ot', 
                                'marchandise__libelle').annotate(
                                quantite=Sum((F('poids_net'))),
                                pu=Avg(F('prix_unitaire')),
                                total=Sum((F('poids_net') * F('prix_unitaire'))),
                            )
    for i in enlevement_group:
        if ot_dict.get(i[0]):
            ot_dict[i[0]].append(i[1:])
            montant_total_ht+=i[6]
        else:
            ot_dict[i[0]] = [i[1:]]  
            montant_total_ht+=i[6]
    
    print("enlevement_group", enlevement_group)

    print("ot_dict", ot_dict)

    montant_total_ht = int(montant_total_ht)
    # CARBURANT
    montant_tva = montant_total_ht * societe.tva

    montant_carburant = Carburant.objects.filter(ordretransport__in=ot_list, imputation='Préfinancement').aggregate(montant_carburant=Sum('montant'))['montant_carburant']
    if montant_carburant is None:montant_carburant=0

    montant_net = int(montant_total_ht+montant_tva-montant_carburant)

    context = {'facturation': facturation, 
    'ot_list':ot_list, 
    'enlevement_list':enlevement_list,
    'ot_dict':ot_dict,
    'montant_total_ht':int(montant_total_ht),
    'montant_tva':int(montant_tva),

    'montant_carburant':int(montant_carburant),
    'montant_net':int(montant_net),
    'montant_net_lettre':chiffreLettre(int(montant_total_ht+montant_tva-montant_carburant)),
    }

    ligneHauteur = 1
    imprimerPDF = ImprimerDoc()
    imprimerPDF.story = []
    entetePage(imprimerPDF)
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
    ('FACTURE N° {0}'.format(facturation.numero_facture), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('ADRESSE DE LIVRAISON', '', '', '', '', '', '', '', '', '', '', '', 'DOIT : ', '', '', '', '',  '', ''),
    ('{0}'.format(iif(facturation.commande.lieu_dechargement, facturation.commande.lieu_dechargement, '')), '', '', '', '', '', '', '', '', '', '', '','{0}'.format(facturation.commande.client),  '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '','{0}'.format(iif(facturation.commande.client.adresse, facturation.commande.client.adresse, '')), '', '', '',  '',  '', ''),
    ('VOS REFERENCES', '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(facturation.commande.client.telephone, facturation.commande.client.telephone, '')), '', '', '', '',  '', ''),
    ('{0}'.format(iif(facturation.commande.navire, facturation.commande.navire, '')), '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(facturation.commande.client.registre_commerce, facturation.commande.client.registre_commerce, '')), '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('NOS REFERENCES', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('BL : {0}'.format(iif(facturation.bon_livraison, facturation.bon_livraison, '')), '', '', '', '', '', '', '', '', '', '', '','Abidjan, le {0}'.format(dateAnglaisFrancais(facturation.date_facture)),  '',  '', '', '',  '', ''),
    ]
    
    t=Table(zone_entete,[25, 25], len(zone_entete)*[0.5*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 1, colors.black),
    
    ]
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    
    ligne_ot=[]
    k=-1
    for i in ot_dict:
        k+=1
        if not k:ligne_ot.append(1)
        else:ligne_ot.append(len(ot_dict[tampon])+ligne_ot[k-1]+1)
        tampon=i

    data=[]
    for i in ot_dict:
        k=0
        #data.append(('', '', '', '', '', ''))# i
        for j in ot_dict[i]:
            k+=1
            data.append(
                (str(k).zfill(2), 
                reduireChaine(j[0]+' - '+ j[1],23), 
                reduireChaine(j[2], 23),
                millier(int(j[3])),
                millier(int(j[4])),
                millier(int(j[5]))
    ))

    data.append(('MONTANT TOTAL HT', '', '', '', '', millier(montant_total_ht)))
    data.append(('TVA 18%', '', '', '', '', iif(montant_tva, millier(montant_tva), '-')))
    if montant_carburant: data.append(('AVANCE PERCUE', '', '', '', '', '-'+millier(montant_carburant)))
    data.append(('MONTANT TOTAL NET A PAYER', '', '', '', '', millier(montant_net)))           
    data.insert(0, ('N°', 'ITINERAIRES', 'MARCHANDISES', 'QUANTITE', 'PU HT', 'MONTANT'))

    zone_details = data[:]
    t=Table(zone_details,[25, 150, 150, 55, 50, 70], len(zone_details)*[ligneHauteur*cm])
    if montant_carburant:
        GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (3,1), (-1,-1), 'RIGHT'),

            ('ALIGN', (0,0), (0,-1), 'CENTER'),

            ('SPAN', (0,-4), (-2,-4)),
            ('ALIGN', (0,-4), (-2,-4), 'RIGHT'),
            ('SPAN', (0,-3), (-2,-3)),
            ('ALIGN', (0,-3), (-2,-3), 'RIGHT'),
            ('SPAN', (0,-2), (-2,-2)),
            ('ALIGN', (0,-2), (-2,-2), 'RIGHT'),
            ('SPAN', (0,-1), (-2,-1)),
            ('ALIGN', (0,-1), (-2,-1), 'RIGHT'),
        ]
    else:
        GRID_STYLE=[('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
            
            ('ALIGN', (0,0), (0,-1), 'CENTER'),

            ('SPAN', (0,-3), (-2,-3)),
            ('ALIGN', (0,-3), (-2,-3), 'RIGHT'),
            ('SPAN', (0,-2), (-2,-2)),
            ('ALIGN', (0,-2), (-2,-2), 'RIGHT'),
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
    ('ARRETE LA PRESENTE FACTURE A LA SOMME DE : {0} FRANCS CFA'.format(chiffreLettre(montant_net).upper()), '', '', '',''),
    ('', '', '', '', ''),
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

    ('SPAN', (3,2), (-1,2)),
    #('ALIGN', (3,2), (-1,2), 'RIGHT'),
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