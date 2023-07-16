# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Reglement
from reglement.forms import *


def accueil(request):
	reglement_list = Reglement.objects.all()
	return render(request, 'reglement/reglement_lister.html', locals())

def reglement_creer(request):
	if request.method == 'POST':
		form = ReglementForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/reglement/accueil/')
		return render(request, 'reglement/reglement_creer.html', locals())
	form = ReglementForm()
	return render(request, 'reglement/reglement_creer.html', locals())

def reglement_modifier(request, pk):
	reglement = get_object_or_404(Reglement, pk=pk)
	if request.method == 'POST':
		form = ReglementForm(request.POST, request.FILES, instance=reglement)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/reglement/accueil/')
		return render(request, 'reglement/reglement_modifier.html', locals())	
	form = ReglementForm(instance=reglement)
	form.fields['facturation'].choices = [(reglement.facturation.id, reglement.facturation.commande.numero_dossier +' - '+reglement.facturation.commande.client.raison_sociale)]
	return render(request, 'reglement/reglement_modifier.html', locals())

def reglement_visualiser(request, pk):
	reglement = get_object_or_404(Reglement, pk=pk)
	form = ReglementForm(instance=reglement)
	return render(request, 'reglement/reglement_visualiser.html', locals())


def reglement_delete(request, pk):
    reglement = get_object_or_404(Reglement, pk=pk)
    data = dict()
    if request.method == 'POST':
        reglement.delete()
        return HttpResponseRedirect('/reglement/accueil/')
    else:
        context = {'reglement': reglement}
        data['html_form'] = render_to_string('reglement/reglement_delete.html', context, request=request)
    return JsonResponse(data)


