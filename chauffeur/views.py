# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from parametre.models import Chauffeur, Societe
from chauffeur.forms import *
from Utilitaire import *
from ImprimerDoc import *
import random
import os
import datetime
import time


def accueil(request):
	chauffeur_list = Chauffeur.objects.all()
	return render(request, 'chauffeur/chauffeur_lister.html', locals())


def chauffeur_creer(request):
	if request.method == 'POST':
		form = ChauffeurForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/chauffeur/accueil/')
		return render(request, 'chauffeur/chauffeur_creer.html', locals())	
	form = ChauffeurForm()
	return render(request, 'chauffeur/chauffeur_creer.html', locals())

def chauffeur_modifier(request, pk):
	chauffeur = get_object_or_404(Chauffeur, pk=pk)
	if request.method == 'POST':
		form = ChauffeurForm(request.POST, request.FILES, instance=chauffeur)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/chauffeur/accueil/')
		return render(request, 'chauffeur/chauffeur_modifier.html', locals())	
	form = ChauffeurForm(instance=chauffeur)
	return render(request, 'chauffeur/chauffeur_modifier.html', locals())

def chauffeur_visualiser(request, pk):
	chauffeur = get_object_or_404(Chauffeur, pk=pk)
	form = ChauffeurForm(instance=chauffeur)
	return render(request, 'chauffeur/chauffeur_visualiser.html', locals())


def chauffeur_delete(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    data = dict()
    if request.method == 'POST':
        chauffeur.delete()
        return HttpResponseRedirect('/chauffeur/accueil/')
    else:
        context = {'chauffeur': chauffeur}
        data['html_form'] = render_to_string('chauffeur/chauffeur_delete.html', context, request=request)
    return JsonResponse(data)



def imprimer_fiche(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    print('je suis en impression_chauffeur')
    user=request.user
    ligneHauteur=1
    imprimerPDF=ImprimerDoc()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    imprimerPDF.story=[]
    entetePage(imprimerPDF)
    fichier=settings.CHEMIN_ETATS+"chauffeur_fiche"+str(random.randint(1,10000))+'.pdf'
    #Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    imprimerPDF.story.append(Paragraph("<b><h1>FICHE D'IDENTIFICATION DU CHAUFFEUR</h1></b>", styles['Center']))
    #imprimerPDF.story.append(Paragraph("<b><h2>{0} {1}</h2></b>".format(chauffeur.nom.upper(), chauffeur.prenoms.title()), styles['Center']))
    imprimerPDF.story.append(Spacer(0,0.2*inch))
    try:
    	imprimerPDF.story.append(Image(chauffeur.photo, width=1.3*inch, height=1.3*inch))
    except:pass

    imprimerPDF.story.append(Spacer(0,0.2*inch))
    ligne=[]
    compteur=0
    coordonnee=[
    	('COORDONNEES', '', '', '', ''),
        ('Nom : ', '{0}'.format(chauffeur.nom.upper()), 'Prénoms : ', '{0}'.format(chauffeur.prenoms.title()), ''),
        ('Né le : ', '{0}'.format(iif(chauffeur.date_naissance, dateAnglaisFrancais(chauffeur.date_naissance), '')), 'A : ', '{0}'.format(iif(chauffeur.lieu_naissance, chauffeur.lieu_naissance, '')), ''),
    	('Matricule : ', '{0}'.format(chauffeur.matricule), 'Type : ', '{0}'.format(chauffeur.type_chauffeur), ''),
		('Statut : ', '{0}'.format(chauffeur.statut), 'Véhicule affecté : ', '{0}'.format(chauffeur.vehicule), ''),
		('Cellulaire : ', '{0} {1}'.format(chauffeur.cellulaire, chauffeur.cellulaire2), 'E-mail : ', '{0}'.format(chauffeur.email), ''),
		('Personne à contacter : ', '{0}'.format(chauffeur.contact), '', '', ''),
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
    	('CONTRAT & DIFFERENTES PIECES', '', '', '', ''),
    	('type contrat : ', '{0}'.format(chauffeur.type_contrat), "Date d'éntrée : ", '{0}'.format(dateAnglaisFrancais(chauffeur.date_entree)), ''),
		('Nature pièce : ', '{0}'.format(chauffeur.nature_piece), 'Numéro de la pièce : ', '{0}'.format(chauffeur.piece_identite), ''),
		('Date établissement : ', '{0}'.format(dateAnglaisFrancais(chauffeur.piece_date_etablissement)), 'Date expiration : ', '{0}'.format(dateAnglaisFrancais(chauffeur.piece_date_expiration)), ''),
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
    	('PERMIS DE CONDUIRE', '', '', '', ''),
    	('Catégorie : ', '{0}'.format(chauffeur.permis_categorie), "Numéro : ", '{0}'.format(chauffeur.permis_numero), ''),
		('Date établissement : ', '{0}'.format(dateAnglaisFrancais(chauffeur.permis_date_etablissement)), 'Date expiration : ', '{0}'.format(dateAnglaisFrancais(chauffeur.permis_date_echeance)), ''),
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