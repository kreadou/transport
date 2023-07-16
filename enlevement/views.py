# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Ordretransport, Enlevement, Detailscommande
from enlevement.forms import *
from django.db.models import Sum, F

def enlevement_lister(request, pk):
	ot = get_object_or_404(Ordretransport, pk=pk)
	enlevement_list = Enlevement.objects.filter(ordretransport = ot).order_by('-id')
	montant_total_enlevement = enlevement_list.aggregate(total=Sum((F('quantite') * F('prix_unitaire'))))['total']
	tonnage = enlevement_list.aggregate(Sum('quantite'))['quantite__sum']# en tonne
	print("montant enlevement", montant_total_enlevement)
	return render(request, 'enlevement/enlevement_lister.html', locals())


def enlevement_creer(request, pk):
	ot= get_object_or_404(Ordretransport, pk=pk)
	enlevement = Enlevement.objects.filter(ordretransport=ot).order_by('-id')
	if enlevement:
		tonnage = enlevement.aggregate(Sum('poids_net'))['poids_net__sum']# en tonne
	if request.method == 'POST':
		form = EnlevementForm(request.POST, request.FILES)
		if form.is_valid():
			print('oui validé')
			f = form.save(commit=False)
			f.poids_net = f.poids_net/1000 # conversion en tonne
			f.save()
			print('oui sauvé')
			if 'enregistrer_copier' in request.POST:
				form = EnlevementForm(initial={
					'date_enlevement':f.date_enlevement,
					'trajet':f.trajet,
					'marchandise':f.marchandise,
					'mode_tarification':f.mode_tarification,
					'vehicule':f.vehicule,
					'chauffeur':f.chauffeur,
					'poids_vide':f.poids_vide,					

					'prix_unitaire':f.prix_unitaire,
					},
					instance=ot)

				form.fields['ordretransport'].choices = [(ot.id, ot.commande.client)]
				return render(request, 'enlevement/enlevement_creer.html', locals())

			elif 'submit' in request.POST:

				return HttpResponseRedirect('/enlevement/enlevement_lister/{0}/'.format(ot.id))
		else:
			form.fields['ordretransport'].choices = [(ot.id, ot.commande.client)]

			if [(i['trajet__id'], i['trajet__source__libelle']+' '+ i['trajet__destination__libelle'],) for i in Detailscommande.objects.values('trajet__id', 'trajet__source__libelle', 'trajet__destination__libelle',).filter(commande=ot.commande)]:
				form.fields['trajet'].choices = [(i['trajet__id'], i['trajet__source__libelle']+' '+ i['trajet__destination__libelle'],) for i in Detailscommande.objects.values('trajet__id', 'trajet__source__libelle', 'trajet__destination__libelle',).filter(commande=ot.commande).distinct()]
			
			if [(i['marchandise__id'], i['marchandise__libelle']) for i in Detailscommande.objects.values('marchandise__id', 'marchandise__libelle').filter(commande=ot.commande)]:
				form.fields['marchandise'].choices = [(i['marchandise__id'], i['marchandise__libelle']) for i in Detailscommande.objects.values('marchandise__id', 'marchandise__libelle').filter(commande=ot.commande).distinct()]

			return render(request, 'enlevement/enlevement_creer.html', locals())
	else:
		form = EnlevementForm()
		if enlevement:
			form = EnlevementForm(initial={
				'date_enlevement':enlevement[0].date_enlevement,
				'trajet':enlevement[0].trajet,
				'marchandise':enlevement[0].marchandise,
				'mode_tarification':enlevement[0].mode_tarification,
				'vehicule':enlevement[0].vehicule,
				'chauffeur':enlevement[0].chauffeur,
				'poids_vide':enlevement[0].poids_vide,
				'prix_unitaire':enlevement[0].prix_unitaire,
				},
				instance=ot
			)
		
		form.fields['ordretransport'].choices = [(ot.id, ot.commande.client)]
		if [(i['trajet__id'], i['trajet__source__libelle']+' '+ i['trajet__destination__libelle'],) for i in Detailscommande.objects.values('trajet__id', 'trajet__source__libelle', 'trajet__destination__libelle',).filter(commande=ot.commande)]:
			form.fields['trajet'].choices = [(i['trajet__id'], i['trajet__source__libelle']+' '+ i['trajet__destination__libelle'],) for i in Detailscommande.objects.values('trajet__id', 'trajet__source__libelle', 'trajet__destination__libelle',).filter(commande=ot.commande).distinct()]
		
		if [(i['marchandise__id'], i['marchandise__libelle']) for i in Detailscommande.objects.values('marchandise__id', 'marchandise__libelle').filter(commande=ot.commande)]:
			form.fields['marchandise'].choices = [(i['marchandise__id'], i['marchandise__libelle']) for i in Detailscommande.objects.values('marchandise__id', 'marchandise__libelle').filter(commande=ot.commande).distinct()]
	return render(request, 'enlevement/enlevement_creer.html', locals())


def enlevement_modifier(request, pk):
	enlevement = get_object_or_404(Enlevement, pk=pk)
	if request.method == 'POST':
		form = EnlevementForm(request.POST, request.FILES, instance=enlevement)
		print("form errors", form.errors)
		if form.is_valid():
			f = form.save(commit=False)
			f.poids_net = f.poids_net/1000 # conversion en tonne
			f.save()
			return HttpResponseRedirect('/enlevement/enlevement_lister/{0}/'.format(enlevement.ordretransport.id))
		return render(request, 'enlevement/enlevement_modifier.html', locals())	
	form = EnlevementForm(initial={'poids_net':enlevement.poids_net * 1000}, instance=enlevement)
	return render(request, 'enlevement/enlevement_modifier.html', locals())

def enlevement_visualiser(request, pk):
	enlevement = get_object_or_404(Enlevement, pk=pk)
	form = EnlevementForm(instance=enlevement)
	return render(request, 'enlevement/enlevement_visualiser.html', locals())


def enlevement_formset_creer(request, pk):
	ot = get_object_or_404(Ordretransport, pk=pk)
	formSet = inlineformset_factory(Ordretransport, Enlevement, extra=1, can_delete=True, fields=(
    'date_enlevement', 
    'trajet', 
    'marchandise', 
    'vehicule',
    'chauffeur',
    'quantité',
    'prix_unitaire'
    ))
	if request.method == 'POST':
		formset = formSet(request.POST, instance=ot)
		if formset.is_valid():
			for f in formset:
				pass
			return HttpResponseRedirect('/enlevement/enlevement_lister/{0}/'.format(ot.id))
		else:
			return render(request, 'enlevement/enlevement_formset_creer.html', locals())
	else:
		# lecture des details commandes
		details_commande = Detailscommande.objects.filter(commande=ot.commande)
		if details_commande:
			print("oui detail commande")
			pass

		enlevement = Enlevement.objects.filter(Ordretransport=ot)
		if enlevement:
			print("oui enlevement")
			formset = formSet(initial={'enlevement':enlevement[0]}, instance=ot)
	return render(request, 'enlevement/enlevement_formset_creer.html', locals())


def enlevement_delete(request, pk):
    enlevement = get_object_or_404(Enlevement, pk=pk)
    data = dict()
    if request.method == 'POST':
        enlevement.delete()
        return HttpResponseRedirect('/enlevement/enlevement_lister/{0}/'.format(enlevement.ordretransport.id))
    else:
        context = {'enlevement': enlevement}
        data['html_form'] = render_to_string('enlevement/enlevement_delete.html', context, request=request)
    return JsonResponse(data)





