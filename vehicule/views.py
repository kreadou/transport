# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from parametre.models import Vehicule, Societe
from vehicule.forms import *
from Utilitaire import *
from ImprimerDoc import *
import random
import os
import datetime
import time


def accueil(request):
	vehicule_list = Vehicule.objects.all()
	return render(request, 'vehicule/vehicule_lister.html', locals())


def vehicule_creer(request):
	if request.method == 'POST':
		form = VehiculeForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/vehicule/accueil/')
		return render(request, 'vehicule/vehicule_creer.html', locals())	
	form = VehiculeForm()
	return render(request, 'vehicule/vehicule_creer.html', locals())

def vehicule_modifier(request, pk):
	vehicule = get_object_or_404(Vehicule, pk=pk)
	if request.method == 'POST':
		form = VehiculeForm(request.POST, request.FILES, instance=vehicule)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/vehicule/accueil/')
		return render(request, 'vehicule/vehicule_modifier.html', locals())	
	form = VehiculeForm(instance=vehicule)
	return render(request, 'vehicule/vehicule_modifier.html', locals())

def vehicule_visualiser(request, pk):
	vehicule = get_object_or_404(Vehicule, pk=pk)
	form = VehiculeForm(instance=vehicule)
	return render(request, 'vehicule/vehicule_visualiser.html', locals())


def vehicule_delete(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    data = dict()
    if request.method == 'POST':
        vehicule.delete()
        return HttpResponseRedirect('/vehicule/accueil/')
    else:
        context = {'vehicule': vehicule}
        data['html_form'] = render_to_string('vehicule/vehicule_delete.html', context, request=request)
    return JsonResponse(data)


def imprimer_fiche(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    print('je suis en impression_vehicule')
    user=request.user
    ligneHauteur=1
    imprimerPDF=ImprimerDoc()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    imprimerPDF.story=[]
    entetePage(imprimerPDF)
    fichier=settings.CHEMIN_ETATS+"vehicule_fiche"+str(random.randint(1,10000))+'.pdf'
    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    imprimerPDF.story.append(Paragraph("<b><h1>FICHE D'IDENTIFICATION DU VEHICULE</h1></b>", styles['Center']))
    imprimerPDF.story.append(Paragraph("<b><h2>{0} - {1}</h2></b>".format(vehicule.immatriculation.upper(), vehicule.marque.libelle), styles['Center']))
    try:
    	imprimerPDF.story.append(Image(vehicule.photo, width=1.3*inch, height=1.3*inch))
    except:pass

    imprimerPDF.story.append(Spacer(0,0.2*inch))
    ligne=[]
    compteur=0
    coordonnee=[
    	('CARACTERISTIQUES', '', '', '', ''),
        ('Marque : ', '{0}'.format(iif(vehicule.marque, vehicule.marque, '')), 'Modèle : ', '{0}'.format(vehicule.modele), ''),
    	('Type : ', '{0}'.format(vehicule.type_vehicule), 'Type carburant: ', '{0}'.format(vehicule.type_carburant), ''),
		('Mode utilisation : ', '{0}'.format(vehicule.mode_utilisation), 'Assignation : ', '{0}'.format(vehicule.assignation), ''),
		('Chassis : ', '{0}'.format(vehicule.numero_chassis), 'Attelage : ', '{0}'.format(vehicule.attelage), ''),
		('Date MEC : ', '{0}'.format(dateAnglaisFrancais(vehicule.date_mise_en_circulation)), '', '', ''),
		('', '', '', '', ''),
		('Poids total à charge : ', '{0}'.format(vehicule.poids_ptac), '', '', ''),
		('Poids à vide : ', '{0}'.format(vehicule.poids_vide), '', '', ''),
		('Poids charge utile : ', '{0}'.format(vehicule.poids_charge_utile), '', '', ''),
		('Coordonnées GPS : ', '{0}'.format(iif(vehicule.gps, 'oui', 'non')), '', '', ''),
    ]

    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 0.5, colors.black),
        #('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        #('ALIGN', (0,0), (-1,0), 'CENTER'),
        #('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        #('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
    ]
    #data = [[Paragraph(str(cell) if cell else '', s) for cell in row] for row in data]
    t=Table(coordonnee, [110, 130, 110, 80], len(coordonnee)*[1*cm])

    t.setStyle(GRID_STYLE)    
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))


    contrat=[
    	('ASSURANCES', '', '', '', ''),
		("Date d'effet : ", '{0}'.format(dateAnglaisFrancais(vehicule.date_effet)), "Date d'échéance : ", '{0}'.format(dateAnglaisFrancais(vehicule.date_echeance_assurance)), ''),
    ]

    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 0.5, colors.black),
        #('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        #('ALIGN', (0,0), (-1,0), 'CENTER'),
        #('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        #('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),

    ]
    #data = [[Paragraph(str(cell) if cell else '', s) for cell in row] for row in data]
    t=Table(contrat, [110, 130, 110, 80], len(contrat)*[1*cm])
    t.setStyle(GRID_STYLE)
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    permis_conduire = [
    	('VISITE TECHNIQUE - STATIONNEMENT - PATENTE', '', '', '', ''),
    	('Date expiration visite : ', '{0}'.format(dateAnglaisFrancais(vehicule.date_echeance_visite)), '', '', ''),
		('Date expiration station : ', '{0}'.format(dateAnglaisFrancais(vehicule.date_echeance_stationnement)), '', '', ''),
    	('Date expiration patente : ', '{0}'.format(dateAnglaisFrancais(vehicule.date_echeance_patente)), '', '', ''),
    ]

    GRID_STYLE=[#('GRID', (0,0), (-1,-1), 0.5, colors.black),
        #('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        #('ALIGN', (0,0), (-1,0), 'CENTER'),
        #('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        #('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
    ]
    #data = [[Paragraph(str(cell) if cell else '', s) for cell in row] for row in data]
    t=Table(permis_conduire, [110, 130, 110, 80], len(permis_conduire)*[1*cm])
    t.setStyle(GRID_STYLE)    
    imprimerPDF.story.append(t)
    imprimerPDF.story.append(Spacer(0,0.2*inch))

    #imprimerPDF.story.append(Paragraph("Editée le {0}".format(dateAnglaisFrancais(datetime.date.today())), styles['Right']))
    #imprimerPDF.story.append(Spacer(0,0.5*inch))
    #imprimerPDF.story.append(Paragraph("Utilisateur : {0}".format(user), styles['Right']))
    imprimerPDF.go(fichier, portrait(A4))
    #ouvrirPDF(fichier)
    #for i in range(1000):pass
    with open(fichier, 'r',  encoding="utf8", errors='ignore') as pdf:
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