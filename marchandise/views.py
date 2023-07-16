# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django.views import generic
from parametre.models import Marchandise, Trajet, Commune, Vehicule, Chauffeur
from marchandise.forms import *
from parametre.forms import *

from django_addanother.views import CreatePopupMixin, UpdatePopupMixin


class CreateMarchandise(CreatePopupMixin, generic.CreateView):
    model = Marchandise
    fields = ['etat_marchandise', 'libelle']
    template_name = 'marchandise/marchandise_form.html'

class CreateTrajet(CreatePopupMixin, generic.CreateView):
    model = Trajet
    fields = ['source', 'destination', 'kilometrage']
    template_name = 'marchandise/trajet_form.html'


class CreateSource(CreatePopupMixin, generic.CreateView):
    model = Commune
    fields = ['libelle']
    template_name = 'marchandise/commune_form.html'

class CreateDestination(CreatePopupMixin, generic.CreateView):
    model = Commune
    fields = ['libelle']
    template_name = 'marchandise/commune_form.html'


class CreateCommune(CreatePopupMixin, generic.CreateView):
    model = Commune
    fields = ['ville', 'libelle', ]
    template_name = 'marchandise/commune_form.html'


class CreateVehicule(CreatePopupMixin, generic.CreateView):
    model = Vehicule
    fields = ['immatriculation', 'marque', 'type_carburant', 'mode_utilisation',]
    template_name = 'marchandise/vehicule_form.html'

class CreateChauffeur(CreatePopupMixin, generic.CreateView):
    model = Chauffeur
    fields = ['matricule', 'nom', 'prenoms', 'vehicule']
    template_name = 'marchandise/chauffeur_form.html'

class CreateCommune(CreatePopupMixin, generic.CreateView):
    model = Commune
    fields = ['ville', 'libelle', ]
    template_name = 'marchandise/commune_form.html'


def CommuneCreatePopup(request):
    form = CommuneForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_commune");</script>' % (instance.pk, instance))
    
    return render(request, "marchandise/commune_form.html", {"form" : form})


def commune(request, pk=0):
    form = CommuneForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        if not int(pk) :return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_source");</script>' % (instance.pk, instance))
        else:return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_destination");</script>' % (instance.pk, instance))
    return render(request, "marchandise/commune.html", {"form" : form})

def accueil(request):
	marchandise_list = Marchandise.objects.all()
	return render(request, 'marchandise/marchandise_lister.html', locals())

def marchandise_creer(request):
	if request.method == 'POST':
		form = MarchandiseForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/marchandise/accueil/')
		return render(request, 'marchandise/marchandise_creer.html', locals())	
	form = MarchandiseForm()
	return render(request, 'marchandise/marchandise_creer.html', locals())

def marchandise_modifier(request, pk):
	marchandise = get_object_or_404(Marchandise, pk=pk)
	if request.method == 'POST':
		form = MarchandiseForm(request.POST, request.FILES, instance=marchandise)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/marchandise/accueil/')
		return render(request, 'marchandise/marchandise_modifier.html', locals())	
	form = MarchandiseForm(instance=marchandise)
	return render(request, 'marchandise/marchandise_modifier.html', locals())

def marchandise_visualiser(request, pk):
	marchandise = get_object_or_404(Marchandise, pk=pk)
	form = MarchandiseForm(instance=marchandise)
	return render(request, 'marchandise/marchandise_visualiser.html', locals())


def marchandise_delete(request, pk):
    marchandise = get_object_or_404(Marchandise, pk=pk)
    data = dict()
    if request.method == 'POST':
        marchandise.delete()
        return HttpResponseRedirect('/marchandise/accueil/')
    else:
        context = {'marchandise': marchandise}
        data['html_form'] = render_to_string('marchandise/marchandise_delete.html', context, request=request)
    return JsonResponse(data)


