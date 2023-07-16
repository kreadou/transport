# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Reparation
from reparation.forms import *


def accueil(request):
	reparation_list = Reparation.objects.all()
	return render(request, 'reparation/reparation_lister.html', locals())


def reparation_creer(request):
	if request.method == 'POST':
		form = ReparationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/reparation/accueil/')
		return render(request, 'reparation/reparation_creer.html', locals())	
	form = ReparationForm()
	return render(request, 'reparation/reparation_creer.html', locals())

def reparation_modifier(request, pk):
	reparation = get_object_or_404(Reparation, pk=pk)
	if request.method == 'POST':
		form = ReparationForm(request.POST, request.FILES, instance=reparation)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/reparation/accueil/')
		return render(request, 'reparation/reparation_modifier.html', locals())	
	form = ReparationForm(instance=reparation)
	return render(request, 'reparation/reparation_modifier.html', locals())

def reparation_visualiser(request, pk):
	reparation = get_object_or_404(Reparation, pk=pk)
	form = ReparationForm(instance=reparation)
	return render(request, 'reparation/reparation_visualiser.html', locals())


def reparation_delete(request, pk):
    reparation = get_object_or_404(Reparation, pk=pk)
    data = dict()
    if request.method == 'POST':
        reparation.delete()
        return HttpResponseRedirect('/reparation/accueil/')
    else:
        context = {'reparation': reparation}
        data['html_form'] = render_to_string('reparation/reparation_delete.html', context, request=request)
    return JsonResponse(data)


