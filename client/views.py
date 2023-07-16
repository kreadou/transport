# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Client
from client.forms import *


def accueil(request):
	client_list = Client.objects.all()
	return render(request, 'client/client_lister.html', locals())


def client_creer(request):
	if request.method == 'POST':
		form = ClientForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/client/accueil/')
		return render(request, 'client/client_creer.html', locals())	
	form = ClientForm()
	return render(request, 'client/client_creer.html', locals())


def client_modifier(request, pk):
	client = get_object_or_404(Client, pk=pk)
	if request.method == 'POST':
		form = ClientForm(request.POST, request.FILES, instance=client)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/client/accueil/')
		return render(request, 'client/client_modifier.html', locals())	
	form = ClientForm(instance=client)
	return render(request, 'client/client_modifier.html', locals())


def client_visualiser(request, pk):
	client = get_object_or_404(Client, pk=pk)
	form = ClientForm(instance=client)
	return render(request, 'client/client_visualiser.html', locals())


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    data = dict()
    if request.method == 'POST':
        client.delete()
        return HttpResponseRedirect('/client/accueil/')
    else:
        context = {'client': client}
        data['html_form'] = render_to_string('client/client_delete.html', context, request=request)
    return JsonResponse(data)


