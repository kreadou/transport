# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import modelformset_factory
from parametre.models import * 
from parametre.forms import *

import random
from datetime import *

from Utilitaire import *
#from django.core.serializers import serialize
from django.contrib.auth.models import Group


@login_required(login_url="login/")
def accueil(request):
    return render(request, "accueil.html")


@login_required(login_url="login/")
def index(request):
    return render(request, "parametre/index.html")

class ChauffeurList(ListView): 
    model = Chauffeur
    template_name = 'parametre/chauffeur_list.html'


class ChauffeurDetail(DetailView): 
    model = Chauffeur
    template_name = 'parametre/chauffeur_detail.html'
    context_object_name = 'post'


class ChauffeurCreate(CreateView): 
    model = Chauffeur
    fields = '__all__'
    success_url = '/parametre/chauffeur_list'


class ChauffeurUpdate(UpdateView): 
    model = Chauffeur
    fields = '__all__'
    success_url = '/parametre/chauffeur_list'


class ChauffeurDelete(DeleteView): 
    model = Chauffeur
    success_url = '/parametre/chauffeur_list'

class DepenseList(ListView): 
    model = Depense
    template_name = 'parametre/depense_list.html'


class DepenseDetail(DetailView): 
    model = Depense
    template_name = 'parametre/depense_detail.html'
    context_object_name = 'post'


class DepenseCreate(CreateView): 
    model = Depense
    fields = '__all__'
    success_url = '/parametre/depense_list'


class DepenseUpdate(UpdateView): 
    model = Depense
    fields = '__all__'
    success_url = '/parametre/depense_list'


class DepenseDelete(DeleteView): 
    model = Depense
    success_url = '/parametre/depense_list'


def profil_utilisateur(request):
    profilFormSet = modelformset_factory(Profil, extra=3, exclude=())
    formset = profilFormSet(queryset=Profil.objects.order_by())
    for i in formset:
        i.fields['telephone'].widget.attrs.update(size='10%')
        i.fields['cellulaire'].widget.attrs.update(size='10%')
    if request.method=='POST':
        formset = profilFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed()), formset):
                i.save()
            formset = profilFormSet(queryset=Profil.objects.order_by())
            for i in formset:
                i.fields['telephone'].widget.attrs.update(size='10%')
                i.fields['cellulaire'].widget.attrs.update(size='10%')
            return render(request, 'parametre/profil.html', locals())
    return render(request, 'parametre/profil.html', locals())


def continent(request):
    continentFormSet = modelformset_factory(Continent, extra=3, exclude=())
    formset = continentFormSet(queryset=Continent.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = continentFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = continentFormSet(queryset=Continent.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['abrege'].widget.attrs.update(size='40%')
            return render(request, 'parametre/continent.html', locals())
    return render(request, 'parametre/continent.html', locals())


def pays(request):
    paysFormSet = modelformset_factory(Pays, extra=3, exclude=())
    formset = paysFormSet(queryset=Pays.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = paysFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = paysFormSet(queryset=Pays.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'parametre/pays.html', locals())
    return render(request, 'parametre/pays.html', locals())


def region(request):
    regionFormSet = modelformset_factory(Region, extra=3, exclude=())
    formset = regionFormSet(queryset=Region.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = regionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = regionFormSet(queryset=Region.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'parametre/region.html', locals())
    return render(request, 'parametre/region.html', locals())


def departement(request):
    departementFormSet = modelformset_factory(Departement, extra=3, exclude=())
    formset = departementFormSet(queryset=Departement.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = departementFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = departementFormSet(queryset=Departement.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'parametre/departement.html', locals())
    return render(request, 'parametre/departement.html', locals())


def ville(request):
    villeFormSet = modelformset_factory(Ville, extra=3, exclude=())
    formset = villeFormSet(queryset=Ville.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = villeFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = villeFormSet(queryset=Ville.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['abrege'].widget.attrs.update(size='30%')
            return render(request, 'parametre/ville.html', locals())
    return render(request, 'parametre/ville.html', locals())


def commune(request):
    communeFormSet = modelformset_factory(Commune, extra=3, exclude=())
    formset = communeFormSet(queryset=Commune.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
 
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='70%')
        #i.fields['abrege'].widget.attrs.update(size='30%')
    if request.method=='POST':
        formset = communeFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = communeFormSet(queryset=Commune.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 

            return render(request, 'parametre/commune.html', locals())
    return render(request, 'parametre/commune.html', locals())


def civilite(request):
    civiliteFormSet = modelformset_factory(Civilite, extra=3, exclude=())
    formset = civiliteFormSet(queryset=Civilite.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = civiliteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = civiliteFormSet(queryset=Civilite.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='80%')
                i.fields['abrege'].widget.attrs.update(size='40%')
            return render(request, 'parametre/civilite.html', locals())
    return render(request, 'parametre/civilite.html', locals())


def fonction(request):
    fonctionFormSet = modelformset_factory(Fonction, extra=3, exclude=())
    formset = fonctionFormSet(queryset=Fonction.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label=''
        #i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = fonctionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = fonctionFormSet(queryset=Fonction.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label=''
            return render(request, 'parametre/fonction.html', locals())
    return render(request, 'parametre/fonction.html', locals())


def profession(request):
    professionFormSet = modelformset_factory(Profession, extra=3, exclude=())
    formset = professionFormSet(queryset=Profession.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label=''
        
    if request.method=='POST':
        formset = professionFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = professionFormSet(queryset=Profession.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label=''
            return render(request, 'parametre/profession.html', locals())
    return render(request, 'parametre/profession.html', locals())


def service(request):
    serviceFormSet = modelformset_factory(Service, extra=3, exclude=())
    formset = serviceFormSet(queryset=Service.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = serviceFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = serviceFormSet(queryset=Service.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='80%')
                i.fields['abrege'].widget.attrs.update(size='40%')
            return render(request, 'parametre/service.html', locals())
    return render(request, 'parametre/service.html', locals())


def marque(request):
    marqueFormSet = modelformset_factory(Marque, extra=3, exclude=())
    formset = marqueFormSet(queryset=Marque.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
            
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        #i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = marqueFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = marqueFormSet(queryset=Marque.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label=''

            return render(request, 'parametre/marque.html', locals())
    return render(request, 'parametre/marque.html', locals())


def typeActivite(request):
    type_activiteFormSet = modelformset_factory(TypeActivite, extra=3, exclude=())
    formset = type_activiteFormSet(queryset=TypeActivite.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='80%')
        i.fields['abrege'].widget.attrs.update(size='40%')
    if request.method=='POST':
        formset = type_activiteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = type_activiteFormSet(queryset=TypeActivite.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='80%')
                i.fields['abrege'].widget.attrs.update(size='40%')
            return render(request, 'parametre/type_activite.html', locals())
    return render(request, 'parametre/type_activite.html', locals())


def activite(request):
    activiteFormSet = modelformset_factory(Activite, extra=3, exclude=())
    formset = activiteFormSet(queryset=Activite.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='60%')
        i.fields['abrege'].widget.attrs.update(size='10%')
    if request.method=='POST':
        formset = activiteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = activiteFormSet(queryset=Activite.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='60%')
                i.fields['abrege'].widget.attrs.update(size='10%')
            return render(request, 'parametre/activite.html', locals())
    return render(request, 'parametre/activite.html', locals())


def taux(request):
    tauxFormSet = modelformset_factory(Taux, extra=3, exclude=())
    formset = tauxFormSet(queryset=Taux.objects.order_by('libelle'))
    for i in formset:
        i.fields['libelle'].widget.attrs.update(size='60%')
        i.fields['abrege'].widget.attrs.update(size='30%')
        i.fields['taux'].widget.attrs.update(size='10%',)
    if request.method=='POST':
        formset = tauxFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = tauxFormSet(queryset=Taux.objects.order_by('libelle'))
            for i in formset:
                i.fields['libelle'].widget.attrs.update(size='60%')
                i.fields['abrege'].widget.attrs.update(size='30%')
                i.fields['taux'].widget.attrs.update(size='10%',)
            return render(request, 'parametre/taux.html', locals())
    return render(request, 'parametre/taux.html', locals())


def trajet(request):
    trajetFormSet = modelformset_factory(Trajet, extra=3, exclude=())
    if request.method=="POST" and request.POST.get("submit")=="ligne":
        if request.POST.get("ligne"):
            nombre_ligne = request.POST.get("ligne")
            #print("nombre de ligne = ", request.POST.get("ligne"))
            trajetFormSet = modelformset_factory(Trajet, extra=int(nombre_ligne), exclude=())
    formset = trajetFormSet(queryset=Trajet.objects.order_by('source'))
    for form in formset:
        for field in form.fields:form.fields[field].label=''

    if request.method=='POST':
        formset = trajetFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['source']), formset):
                i.save()
            formset =trajetFormSet(queryset=Trajet.objects.order_by('source'))
            for form in formset:
                for field in form.fields:form.fields[field].label=''
    return render(request, 'parametre/trajet.html', locals())


def marchandise(request):
    marchandiseFormSet = modelformset_factory(Marchandise, extra=3, exclude=())
    formset = marchandiseFormSet(queryset=Marchandise.objects.order_by('libelle'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 

    if request.method=='POST':
        formset = marchandiseFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['libelle']), formset):
                i.save()
            formset = marchandiseFormSet(queryset=Marchandise.objects.order_by('libelle'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
        
            return render(request, 'parametre/marchandise.html', locals())
    return render(request, 'parametre/marchandise.html', locals())



def alerte(request):
    alerteFormSet = modelformset_factory(Alerte, extra=3, exclude=())
    formset = alerteFormSet(queryset=Alerte.objects.order_by('type_alerte'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['delai'].widget.attrs.update(size='2%')
    if request.method=='POST':
        formset = alerteFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['type_alerte']), formset):
                i.save()
            formset = alerteFormSet(queryset=Alerte.objects.order_by('type_alerte'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['delai'].widget.attrs.update(size='2%')
            return render(request, 'parametre/alerte.html', locals())
    return render(request, 'parametre/alerte.html', locals())


def fournisseur(request):
    fournisseurFormSet = modelformset_factory(Fournisseur, extra=3, exclude=())
    formset = fournisseurFormSet(queryset=Fournisseur.objects.order_by('raison_sociale'))
    for form in formset:
        for field in form.fields:form.fields[field].label='' 
        #i.fields['delai'].widget.attrs.update(size='2%')
    if request.method=='POST':
        formset = fournisseurFormSet(request.POST)
        if formset.is_valid():
            for i in filter(lambda x : (x.is_valid() and x.has_changed() and x.cleaned_data['raison_sociale']), formset):
                i.save()
            formset = fournisseurFormSet(queryset=Fournisseur.objects.order_by('raison_sociale'))
            for form in formset:
                for field in form.fields:form.fields[field].label='' 
                #i.fields['delai'].widget.attrs.update(size='2%')
            return render(request, 'parametre/fournisseur.html', locals())
    return render(request, 'parametre/fournisseur.html', locals())


def societe(request):
    try:
        societe = get_object_or_404(Societe, pk=1)
    except:
        Societe.objects.create(raisonSociale='COCO INTER').save()
        societe = get_object_or_404(Societe, pk=1)  
    form = SocieteForm(instance=societe)
    if request.method=='POST':
        form = SocieteForm(request.POST, instance=societe)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("parametre/index")    
    return render(request, 'parametre/societe.html', locals())


@login_required(login_url="login/")
def profil_lister(request):
    profil_list = Profil.objects.order_by('nom', 'prenoms')
    return render(request, 'parametre/profil_lister.html', locals())


@login_required(login_url="login/")
def profil_creer(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            UserModel = get_user_model()
            if not UserModel.objects.filter(username=form.cleaned_data['login']).exists():
                user = UserModel.objects.create_user(username=form.cleaned_data['login'], password=form.cleaned_data['mdp'])
                if form.cleaned_data['groupe']=="Administrateur":
                    user.is_superuser=True
                    user.is_staff=True
                user.save()
                user.last_name = form.cleaned_data['nom']
                user.first_name = form.cleaned_data['prenoms']
                if not user.is_superuser:
                    group = Group.objects.get(name=form.cleaned_data.get('groupe')) 
                    group.user_set.add(user)
                profil=form.save(commit=False)
                profil.user = user
                profil.save()
                #profil = sauvegarde_qrcode(profil)
                #profil.save()
                return HttpResponseRedirect("/parametre/profil_lister/")
            else:
                print('exists deja') 
                return render(request, 'parametre/profil_creer.html', locals())   
        else:
            print('non valide exists deja')   
            return render(request, 'parametre/profil_creer.html', locals())
    else:   
        form = ProfilForm()
        profil_list = Profil.objects.all()
        return render(request, 'parametre/profil_creer.html', locals())


@login_required(login_url="login/")
def profil_modifier(request, pk):
    profil = Profil.objects.get(id=pk)
    form = ProfilForm2(instance=profil)    
    if request.method == 'POST':
        form = ProfilForm2(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            #request.user.set_password(form.cleaned_data['mdp'])
            #request.user.save()
            return HttpResponseRedirect("/parametre/profil_lister/")
        return render(request, 'parametre/profil_modifier.html', locals())
    return render(request, 'parametre/profil_modifier.html', locals())
 

def sauvegarde_qrcode(profil):
    try:
        t=[
           str(algo()).zfill(10)
        ]
        fichier= "qrcode" + '{0}'.format(str(profil.id))+str(random.randint(1,10000)).zfill(5)+'.png'
        print("OOOOOOOOOOOOOOOOOOOOOOOO")
        qrcode_text = qrcode.make(t)
        print("AAAAAAAAAAAAAAAAAAAAA")
        qrcode_text.save(settings.MEDIA_ROOT + '\\qrcode\\' + '{0}'.format(fichier))
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        
        profil.fichier_qrcode = '{0}'.format(fichier)
        print("CCCCCCCCCCCCCCCCCCCCCCCCCCCC")
        return profil 
    except:
        print("erreur qr code")  
        return profil  