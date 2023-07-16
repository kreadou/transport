# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.template.loader import render_to_string

from parametre.models import Detailscommande, Commande, Ordretransport, Detailsot
from detailscommande.forms import *
from django.db.models import Sum, F

def detailscommande_lister(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    detailscommande_list = Detailscommande.objects.filter(commande = commande)
    montant_total_commande = detailscommande_list.aggregate(total=Sum(F('quantite') * F('prix_unitaire')))['total']
    return render(request, 'detailscommande/detailscommande_lister.html', locals())


def detailscommande_creer(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = DetailscommandeForm(request.POST, request.FILES)
        if form.is_valid():
            cde=form.save(commit=False)
            cde.commande=commande
            cde.save()
            try:
                ot = Ordretransport.objects.filter(commande=commande)[0]
                Detailsot.objects.create(
                    ot=ot,
                    trajet=cde.trajet,
                    marchandise = cde.marchandise,
                    quantite = cde.quantite,
                    prix_unitaire = cde.prix_unitaire
                )
            except:pass

            if 'enregistrer_ajouter_nouveau' in request.POST:
                form = DetailscommandeForm(initial={
                    #'trajet':cde.trajet,
                    'marchandise':cde.marchandise,
                    'lieu_chargement':cde.lieu_chargement,
                    'lieu_dechargement':cde.lieu_dechargement,
                    'contact_chargement':cde.telephone_chargement,  
                    'contact_dechargement':cde.telephone_dechargement,
                    'adresse_chargement':cde.telephone_chargement,  
                    'adresse_dechargement':cde.telephone_dechargement,
                    'telephone_chargement':cde.telephone_chargement,    
                    'telephone_dechargement':cde.telephone_dechargement,                    
                    'quantite':cde.quantite,
                    'prix_unitaire':cde.prix_unitaire,
                    },
                    instance=commande)
                form.fields['commande'].choices = [(commande.id, commande.client)]
                return render(request, 'detailscommande/detailscommande_creer.html', locals())  
            return HttpResponseRedirect('/detailscommande/detailscommande_lister/{0}/'.format(commande.id)) 
        return render(request, 'detailscommande/detailscommande_creer.html', locals())  
    form = DetailscommandeForm()
    detailscommande_list = Detailscommande.objects.filter(commande = commande)
    if detailscommande_list:
        form = DetailscommandeForm(initial={
                'lieu_chargement':detailscommande_list[0].lieu_chargement,
                'lieu_dechargement':detailscommande_list[0].lieu_dechargement,
                'contact_chargement':detailscommande_list[0].telephone_chargement,  
                'contact_dechargement':detailscommande_list[0].telephone_dechargement,
                'adresse_chargement':detailscommande_list[0].telephone_chargement,  
                'adresse_dechargement':detailscommande_list[0].telephone_dechargement,
                'telephone_chargement':detailscommande_list[0].telephone_chargement,    
                'telephone_dechargement':detailscommande_list[0].telephone_dechargement
                },
                instance=commande)
    form.fields['commande'].choices = [(commande.id, commande.client)]
    return render(request, 'detailscommande/detailscommande_creer.html', locals())


def detailscommande_modifier(request, pk):
    detailscommande = get_object_or_404(Detailscommande, pk=pk)
    if request.method == 'POST':
        form = DetailscommandeForm(request.POST, request.FILES, instance=detailscommande)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/detailscommande/detailscommande_lister/{0}/'.format(detailscommande.commande.id)) 
        return render(request, 'detailscommande/detailscommande_modifier.html', locals())   
    form = DetailscommandeForm(instance=detailscommande)
    return render(request, 'detailscommande/detailscommande_modifier.html', locals())


def detailscommande_visualiser(request, pk):
    detailscommande = get_object_or_404(Detailscommande, pk=pk)
    form = DetailscommandeForm(instance=detailscommande)
    return render(request, 'detailscommande/detailscommande_visualiser.html', locals())


def detailscommande_delete(request, pk):
    detailscommande = get_object_or_404(Detailscommande, pk=pk)
    data = dict()
    if request.method == 'POST':
        detailscommande.delete()
        return HttpResponseRedirect('/detailscommande/accueil/')
    else:
        context = {'detailscommande': detailscommande}
        data['html_form'] = render_to_string('detailscommande/detailscommande_delete.html', context, request=request)
    return JsonResponse(data)


