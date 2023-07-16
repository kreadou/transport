# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum, F, Avg
from parametre.models import *#Devis, Detailsdevis, Societe, Para
from devis.forms import DevisForm, DetailsdevisForm, DevisFormSet
from datetime import datetime
from Utilitaire import *
from ImprimerDoc import *
import random
import os
from django.forms import ModelForm, formset_factory, modelformset_factory, inlineformset_factory


def accueil(request):
    montant_total = 0
    devis_list = Devis.objects.all()
    for i in devis_list:
        i.montant_total_ht = Detailsdevis.objects.filter(devis=i).aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
        if i.montant_total_ht:montant_total+=i.montant_total_ht
    return render(request, 'devis/devis_lister.html', locals())


def devis_creer(request):
    if request.method == 'POST':
        form = DevisForm(request.POST or None, request.FILES)
        formset = DevisFormSet(request.POST or None, queryset=Detailsdevis.objects.none())
        if form.is_valid():
            para = Para.objects.all()[0]
            dev = form.save(commit=False)
            dev.numero_devis = 'DEV{0}-{1}'.format(str(datetime.today().year)[2:], str(para.numero_devis+1).zfill(3))   
            dev.save()
            para.numero_devis += 1
            para.save()
            for instance in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['trajet'] and
                x.cleaned_data['marchandise']), formset):
                try:
                    print('001')
                    Detailsdevis.objects.create(
                        devis = dev,
                        trajet= instance.cleaned_data['trajet'],
                        marchandise = instance.cleaned_data['marchandise'],
                        quantite = instance.cleaned_data['quantite'],
                        prix_unitaire = instance.cleaned_data['prix_unitaire'])
                    #instance.save(commit=False)
                    print('002')
                    #instance.devis = dev
                    print('003')
                    #instance.save()
                    print('004')
                except:pass                
            return HttpResponseRedirect('/devis/accueil/')
        return render(request, 'devis/devis_creer.html', locals())  
    else:
        form = DevisForm()
        formset = DevisFormSet(queryset=Detailsdevis.objects.none())
        return render(request, 'devis/devis_creer.html', locals())


def devis_modifier(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    form = DevisForm(instance=devis)
    formset = DevisFormSet(queryset=Detailsdevis.objects.filter(devis=devis))
    if request.method=='POST':
        form = DevisForm(request.POST, instance=devis)
        formset = DevisFormSet(request.POST)
        if all((form.is_valid(), formset.is_valid())):
            form.save()
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:obj.delete()
            for i in instances:
                try:
                    #f=i.save(commit=False)
                    i.devis=devis
                    i.save()
                    print('ok')
                except:pass#rint(f.errors)
            return HttpResponseRedirect('/devis/accueil/')
    return render(request, 'devis/devis_modifier.html', locals())


def devis_visualiser(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    form = DevisForm(instance=devis)
    return render(request, 'devis/devis_visualiser.html', locals())


def devis_delete(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    data = dict()
    if request.method == 'POST':
        devis.delete()
        return HttpResponseRedirect('/devis/accueil/')
    else:
        context = {'devis': devis}
        data['html_form'] = render_to_string('devis/devis_delete.html', context, request=request)
    return JsonResponse(data)


def devis_detail_lister(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    devisdetail_lister = Detailsdevis.objects.filter(devis=devis)
    montant_total = devisdetail_lister.aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
    return render(request, 'devis/devis_detail_lister.html', locals())


def devisdetail_creer(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    if request.method == 'POST':
        form = DetailsdevisForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.devis = devis
            instance.save()
            print('ok')
            if 'enregistrer_ajouter' in request.POST:
                form = DetailsdevisForm(instance=devis)
                return render(request, 'devis/devisdetail_creer.html', locals())
            return HttpResponseRedirect('/devis/accueil/')
        else:
            return render(request, 'devis/devisdetail_creer.html', locals())
    else:
        form = DetailsdevisForm()
        return render(request, 'devis/devisdetail_creer.html', locals())


def devisdetail_modifier(request, pk):
    detail = get_object_or_404(Detailsdevis, pk=pk)
    if request.method == 'POST':
        form = DetailsdevisForm(request.POST, request.FILES, instance=detail)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/devis/devis_detail_lister/{0}'.format(detail.devis.id))
        else:
            return render(request, 'devis/devisdetail_modifier.html', locals())
    else:
        form = DetailsdevisForm(instance=detail)
        return render(request, 'devis/devisdetail_modifier.html', locals())


def devis_transformer_facture(request, pk):
    para = Para.objects.all()[0]
    devis = get_object_or_404(Devis, pk=pk)
    detail_devis = Detailsdevis.objects.filter(devis=devis)
    # creer une commande automatique
    commande = Commande.objects.create(client = devis.client, 
        date_commande = devis.date_devis, 
        numero_dossier = 'DOS{0}-{1}'.format(str(datetime.today().year)[2:], str(para.numero_commande+1).zfill(3)),
        navire = devis.navire,
        mode_tarification = devis.mode_tarification,
        client_pour_compte = devis.client_pour_compte
    )

    for detail in detail_devis:
        Detailscommande.objects.create(
            commande=commande,
            trajet=detail.trajet,
            marchandise = detail.marchandise,
            quantite = detail.quantite,
            prix_unitaire = detail.prix_unitaire
        )

    # creer un ot automatique
    ot = Ordretransport.objects.create(
        commande = commande, 
        date_ot = commande.date_commande,
        qui_enleve = 'Coco Inter', 
        numero_ot = 'OT{0}-{1}'.format(str(datetime.today().year)[2:],str(para.numero_ot+1).zfill(3))
    )

    for detail in detail_devis:
        Detailsot.objects.create(
            ot=ot,
            trajet=detail.trajet,
            marchandise = detail.marchandise,
            quantite = detail.quantite,
            prix_unitaire = detail.prix_unitaire
        )
    """
    for detail in detail_devis:
        Enlevement.objects.create(
            ordretransport = ot,
            trajet = detail.trajet,
            marchandise = detail.marchandise,
            poids_net = detail.quantite,
            prix_unitaire = detail.prix_unitaire,
            vehicule = Vehicule.objects.all()[0],
            chauffeur = Chauffeur.objects.all()[0],

            lieu_chargement = devis.lieu_chargement,
            lieu_dechargement = devis.lieu_dechargement,
        )
    
    # creer une facture automatique
    Facturation.objects.create(
        commande = commande, 
        date_facture = commande.date_commande, 
        numero_facture = 'FA{0}-{1}'.format(str(datetime.today().year)[2:],str(para.numero_facture+1).zfill(3))
    )
    """
    try:
        para.numero_commande +=1
        para.numero_ot +=1
        #para.numero_facture +=1
        para.save()
    except:pass
    return HttpResponseRedirect('/ordretransport/accueil/')


def devis_imprimer(request, pk):
    devis = get_object_or_404(Devis, pk=pk)
    detail_list = Detailsdevis.objects.filter(devis=devis).order_by('id')
    montant_total_ht = detail_list.aggregate(montant=Sum(F('quantite') * F('prix_unitaire')))['montant']
    societe = Societe.objects.get(pk=1)
    ot_dict = {}
           
    context = {'devis': devis,
    'detail_list':detail_list,
    'montant_total_ht':int(montant_total_ht),
    'montant_net_lettre':chiffreLettre(int(montant_total_ht)),
    }

    ligneHauteur = 1.5
    imprimerPDF = ImprimerDoc()
    imprimerPDF.story = []
    #entetePage(imprimerPDF)
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
    ('DEVIS N° {0}'.format(devis.numero_devis), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('ADRESSE DE LIVRAISON', '', '', '', '', '', '', '', '', '', '', '', 'DOIT : ', '', '', '', '',  '', ''),
    ('{0}'.format(iif(devis.lieu_dechargement, devis.lieu_dechargement, '')), '', '', '', '', '', '', '', '', '', '', '','{0}'.format(devis.client),  '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '','{0}'.format(iif(devis.client.adresse, devis.client.adresse)), '', '', '',  '',  '', ''),
    ('VOS REFERENCES', '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(devis.client.telephone, devis.client.telephone, '')), '', '', '', '',  '', ''),
    ('{0}'.format(iif(devis.utiliser_ligne_bon_devis==True, devis.ligne_bon_devis, iif(devis.numero_devis, 'N° : {0}'.format(devis.numero_devis), ''))), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('{0}'.format(iif(devis.navire, devis.navire, '')), '', '', '', '', '', '', '', '', '', '', '', '{0}'.format(iif(devis.client.registre_commerce, devis.client.registre_commerce, '')), '', '', '', '',  '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('NOS REFERENCES', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', ''),
    ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '', ''),
    ('{0}'.format(''), '', '', '', '', '', '', '', '', '', '', '','Abidjan, le {0}'.format(dateAnglaisFrancais(devis.date_devis)),  '',  '', '', '',  '', ''),
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

        if devis.mode_tarification !="Tonnage":
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

    print('oooooooooooo = ', rubrique_list)
    data.insert(0, ('N°', 'RUBRIQUES', '', 'QUANTITE', 'PU HT', 'MONTANT'))
    data.append(('MONTANT HT', '', '', '', '', millier(int(montant_total_ht))))
    data.append(('MONTANT TVA', '', '', '', '', millier(int(montant_total_ht * devis.tva))))
    data.append(('MONTANT TTC', '', '', '', '', millier(int(montant_total_ht + montant_total_ht * devis.tva))))

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

    ('SPAN', (0,-3), (-2,-3)),
    ('ALIGN', (0,-3), (-2,-3), 'RIGHT'),

    ('SPAN', (0,-2), (-2,-2)),
    ('ALIGN', (0,-2), (-2,-2), 'RIGHT'),

    ('SPAN', (0,-1), (-2,-1)),
    ('ALIGN', (0,-1), (-2,-1), 'RIGHT'),

    ]

    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    #imprimerPDF.story.append(Spacer(0,0.2*inch))

    zone_pied=[
    ('ARRETE LE PRESENT DEVIS A LA SOMME DE : {0} FRANCS CFA'.format(chiffreLettre(int(montant_total_ht + montant_total_ht * devis.tva)).upper()), '', '', '',''),
    ('{0}'.format(devis.condition_vente), '', '', '', ''),
    ('', '', '', '', 'VISA SERVICE COMPTABILITE'),
    ]

    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    zone_pied = [[Paragraph(cell, s) for cell in row] for row in zone_pied[:]]

    t=Table(zone_pied,[200, 20, 20, 60, 200], len(zone_pied)*[1*cm])
    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('SPAN', (0,0), (-1,0)),
    ('ALIGN', (0,0), (-1,0), 'LEFT'),

    #('SPAN', (0,1), (-1,1)),
    ('ALIGN', (0,1), (-1,1), 'LEFT'),

    #('SPAN', (0,2), (-1,2)),
    ('ALIGN', (0,2), (-1,2), 'RIGHT'),

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

