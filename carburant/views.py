# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Carburant, Ordretransport, Facturation
from carburant.forms import *


def accueil(request):
	carburant_list = Carburant.objects.all()
	return render(request, 'carburant/carburant_lister.html', locals())


def carburant_creer(request):
	if request.method == 'POST':
		form = CarburantForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			if not 'enregistrer_copier' in request.POST:return HttpResponseRedirect('/carburant/accueil/')
			else : form = CarburantForm()
		else:
			return render(request, 'carburant/carburant_creer.html', locals())	
	else:
		form = CarburantForm()
		form.fields['ordretransport'].choices = [('', '---------')]+[(i.id, i.numero_ot +' - '+i.commande.numero_dossier + ' - '+ i.commande.client.raison_sociale) for i in Ordretransport.objects.all() if i.commande.id not in Facturation.objects.values_list('commande', flat=True)] 
		print(form)
	return render(request, 'carburant/carburant_creer.html', locals())


def carburant_modifier(request, pk):
	carburant = get_object_or_404(Carburant, pk=pk)
	if request.method == 'POST':
		form = CarburantForm(request.POST, request.FILES, instance=carburant)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/carburant/accueil/')
		return render(request, 'carburant/carburant_modifier.html', locals())	
	form = CarburantForm(instance=carburant)
	return render(request, 'carburant/carburant_modifier.html', locals())

def carburant_visualiser(request, pk):
	carburant = get_object_or_404(Carburant, pk=pk)
	form = CarburantForm(instance=carburant)
	return render(request, 'carburant/carburant_visualiser.html', locals())


def carburant_delete(request, pk):
    carburant = get_object_or_404(Carburant, pk=pk)
    data = dict()
    if request.method == 'POST':
        carburant.delete()
        return HttpResponseRedirect('/carburant/accueil/')
    else:
        context = {'carburant': carburant}
        data['html_form'] = render_to_string('carburant/carburant_delete.html', context, request=request)
    return JsonResponse(data)


