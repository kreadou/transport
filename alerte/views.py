# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from django.utils import timezone
from Utilitaire import dateAnglaisFrancais, dateDuJour
from parametre.models import Alerte, Vehicule, Chauffeur, Entretien, Para
from alerte.forms import *
import datetime


def accueil(request):
    alerte_list = dict(Alerte.objects.values_list('type_alerte', 'delai'))
    print("alerte = ", alerte_list)
    print(dateAnglaisFrancais(timezone.now()))
    date_jour = dateDuJour().split('/')
    print(date_jour)
    vehicule_list = Vehicule.objects.all()
    chauffeur_list = Chauffeur.objects.order_by('nom', 'prenoms').all()
    entretien_list = Entretien.objects.all()

    for i in vehicule_list:
        #i.assurance = int(str(i.date_echeance_assurance-datetime.date(int(date_jour[2]), int(date_jour[1]), int(date_jour[0]))).split()[0])
        i.assurance = str(i.date_echeance_assurance-datetime.datetime.now().date())
        if 'days' in i.assurance:i.assurance = int(i.assurance[:i.assurance.index('days')-1])
        else:i.assurance=0
        print("assurance = ", i.assurance)

        i.visite = str(i.date_echeance_visite-datetime.datetime.now().date())
        if 'days' in i.visite:i.visite = int(i.visite[:i.visite.index('days')-1])
        else: i.visite=0
        print("visite = ", i.visite)

        i.stationnement = str(i.date_echeance_stationnement-datetime.datetime.now().date())
        if 'days' in i.stationnement:i.stationnement = int(i.stationnement[:i.stationnement.index('days')-1])
        else:i.stationnement=0
        print("stationnement = ", i.stationnement)

        i.patente = str(i.date_echeance_patente-datetime.datetime.now().date())
        if 'days' in i.patente:i.patente = int(i.patente[:i.patente.index('days')-1])
        else:i.patente = 0
        print("patente = ", i.patente)

    for i in chauffeur_list:
        i.piece = str(i.piece_date_expiration-datetime.datetime.now().date())
        if 'days' in i.piece:i.piece = int(i.piece[:i.piece.index('days')-1])
        else:i.piece=0
        print("piece = ", i.piece, i.nom+' '+i.prenoms)

        i.permis = str(i.permis_date_echeance - datetime.datetime.now().date())
        if 'days' in i.permis:i.permis = int(i.permis[:i.permis.index('days')-1])
        else:i.permis = 0

        i.acces = str(i.carte_acces_echeance-datetime.datetime.now().date())
        if 'days' in i.acces:i.acces = int(i.acces[:i.acces.index('days')-1])
        else: i.acces = 0
        print("acces = ", i.acces)

    for i in entretien_list:
        i.prochain = str(i.date_entretien_prochain-datetime.datetime.now().date())
        if 'days' in i.prochain:i.prochain = int(i.prochain[:i.prochain.index('days')-1])
        else:i.prochain=0
        
    return render(request, 'alerte/alerte_lister.html', locals())
    """ 
    ('Visite technique', 'Visite technique'), 
    ('Stationnement', 'Stationnement'),
    ('Patente', 'Patente'), 
    ("Pièce d'identité", "Pièce d'identité"), 
    ('Permis de conduire', 'Permis de conduire'),
    ('Carte accès portuaire', 'Carte accès portuaire'),
    ('Prochain entretien en kilométrage', 'Prochain entretien en kilométrage'),
    ('Prochain entretien en date', 'Prochain entretien en date'),
    """

def alerte_creer(request):
    if request.method == 'POST':
        form = AlerteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/alerte/accueil/')
        return render(request, 'alerte/alerte_creer.html', locals())    
    form = AlerteForm()
    return render(request, 'alerte/alerte_creer.html', locals())

def alerte_modifier(request, pk):
    alerte = get_object_or_404(Alerte, pk=pk)
    if request.method == 'POST':
        form = AlerteForm(request.POST, request.FILES, instance=alerte)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/alerte/accueil/')
        return render(request, 'alerte/alerte_modifier.html', locals()) 
    form = AlerteForm(instance=alerte)
    return render(request, 'alerte/alerte_modifier.html', locals())

def alerte_visualiser(request, pk):
    alerte = get_object_or_404(Alerte, pk=pk)
    form = AlerteForm(instance=alerte)
    return render(request, 'alerte/alerte_visualiser.html', locals())


def alerte_delete(request, pk):
    alerte = get_object_or_404(Alerte, pk=pk)
    data = dict()
    if request.method == 'POST':
        alerte.delete()
        return HttpResponseRedirect('/alerte/accueil/')
    else:
        context = {'alerte': alerte}
        data['html_form'] = render_to_string('alerte/alerte_delete.html', context, request=request)
    return JsonResponse(data)


def alerte_parametre(request):
    alerteFormSet = modelformset_factory(Alerte, extra=1, exclude=())
    formset = alerteFormSet(queryset=Alerte.objects.order_by('type_alerte'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #form.fields['delai'].widget.attrs.update(size='100%')
    if request.method=='POST':
        formset = alerteFormSet(request.POST or None)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['type_alerte']), formset):
                i.save()
            formset = alerteFormSet(queryset=Alerte.objects.order_by('type_alerte'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #form.fields['delai'].widget.attrs.update(size='100%')
            return render(request, 'alerte/alerte.html', locals())
    return render(request, 'alerte/alerte.html', locals())


def alerte_parametre_creer(request):
    para = Para.objects.all()[0]
    form = ParaForm(instance=para)
    if request.method=='POST':
        form = ParaForm(request.POST, request.FILES, instance=para)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/alerte/accueil/')
        return render(request, 'alerte/alerte_parametre_creer.html', locals())    
    return render(request, 'alerte/alerte_parametre_creer.html', locals())

