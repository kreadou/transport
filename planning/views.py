# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Planning
from planning.forms import *


def accueil(request):
	planning_list = Planning.objects.all()
	return render(request, 'planning/planning_lister.html', locals())


def planning_creer(request):
	if request.method == 'POST':
		form = PlanningForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/planning/accueil/')
		return render(request, 'planning/planning_creer.html', locals())	
	form = PlanningForm()
	return render(request, 'planning/planning_creer.html', locals())

def planning_modifier(request, pk):
	planning = get_object_or_404(Planning, pk=pk)
	if request.method == 'POST':
		form = PlanningForm(request.POST, request.FILES, instance=planning)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/planning/accueil/')
		return render(request, 'planning/planning_modifier.html', locals())	
	form = PlanningForm(instance=planning)
	return render(request, 'planning/planning_modifier.html', locals())

def planning_visualiser(request, pk):
	planning = get_object_or_404(Planning, pk=pk)
	form = PlanningForm(instance=planning)
	return render(request, 'planning/planning_visualiser.html', locals())


def planning_delete(request, pk):
    planning = get_object_or_404(Planning, pk=pk)
    data = dict()
    if request.method == 'POST':
        planning.delete()
        return HttpResponseRedirect('/planning/accueil/')
    else:
        context = {'planning': planning}
        data['html_form'] = render_to_string('planning/planning_delete.html', context, request=request)
    return JsonResponse(data)


