# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from django.views import generic
from parametre.models import Entretien, Fournisseur
from entretien.forms import *


class CreateFournisseur(CreatePopupMixin, generic.CreateView):
    model = Fournisseur
    fields = ['raison_sociale', 'adresse', 'telephone', 'cellulaire', 'boite_postale', 'compte_contribuable', 'registre_commerce']
    template_name = 'entretien/fournisseur_form.html'

def accueil(request):
	entretien_list = Entretien.objects.all()
	return render(request, 'entretien/entretien_lister.html', locals())


def entretien_creer(request):
	if request.method == 'POST':
		form = EntretienForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/entretien/accueil/')
		return render(request, 'entretien/entretien_creer.html', locals())	
	form = EntretienForm()
	return render(request, 'entretien/entretien_creer.html', locals())

def entretien_modifier(request, pk):
	entretien = get_object_or_404(Entretien, pk=pk)
	if request.method == 'POST':
		form = EntretienForm(request.POST, request.FILES, instance=entretien)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/entretien/accueil/')
		return render(request, 'entretien/entretien_modifier.html', locals())	
	form = EntretienForm(instance=entretien)
	return render(request, 'entretien/entretien_modifier.html', locals())

def entretien_visualiser(request, pk):
	entretien = get_object_or_404(Entretien, pk=pk)
	form = EntretienForm(instance=entretien)
	return render(request, 'entretien/entretien_visualiser.html', locals())


def entretien_delete(request, pk):
    entretien = get_object_or_404(Entretien, pk=pk)
    data = dict()
    if request.method == 'POST':
        entretien.delete()
        return HttpResponseRedirect('/entretien/accueil/')
    else:
        context = {'entretien': entretien}
        data['html_form'] = render_to_string('entretien/entretien_delete.html', context, request=request)
    return JsonResponse(data)


