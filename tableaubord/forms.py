from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Commande, Vehicule, Chauffeur, Marchandise, Trajet, Para, Client
from datetime import datetime
from multipleselectionfield import MultipleSelectionField


class FilterForm(forms.Form):#datetime(2022,1,1),
    periode_du = forms.DateField(initial=Para.objects.all()[Para.objects.count()-1].date_debut if Para.objects.all() else None, 
      label="Période du ", 
      required=False,
      widget=forms.widgets.DateInput(
        format=('%Y-%m-%d'), 
        attrs={'type':'date'}))

    periode_au = forms.DateField(
      initial=datetime.today, 
      label="Période au ", 
      required=False,
      widget=forms.widgets.DateInput(
        format=('%Y-%m-%d'), 
        attrs={'type':'date'}))

    dossiers = forms.ChoiceField(widget=CheckboxSelectMultiple(
      attrs={
      "checked":"checked",
    }), 

    choices=[(i.id, i.numero_dossier+' - '+i.client.raison_sociale) for i in Commande.objects.all()], 

    initial=[i.id for i in Commande.objects.all()],
    label='liste des dossiers')
    clients = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked"}), choices=[(i.id, i.raison_sociale) for i in Client.objects.all()], label='liste des Clients')
    vehicules = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked"}), choices=[(i.id, i.immatriculation+' - '+i.marque.libelle) for i in Vehicule.objects.all()], label='liste des véhicules')
    chauffeurs = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked"}), choices=[(i.id, i.matricule +' - '+i.nom.title() +' '+i.prenoms[:1]) for i in Chauffeur.objects.all()], label='Liste des chauffeurs')
    marchandises = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked"}), choices=[(i.id, i.libelle) for i in Marchandise.objects.all()], label='liste des marchandises')
    trajets = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked"}), choices=[(i.id, i.source.libelle +' - ' +i.destination.libelle) for i in Trajet.objects.all()], label='Liste des trajets')
    """
    marchandises = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked",

    'onchange': "$(this).attr('checked') ? alert('Checked') : alert('Unchecked');"}), choices=[(i.id, i.libelle) for i in Marchandise.objects.all()], label='liste des marchandises')
    
    trajets = forms.ChoiceField(widget=CheckboxSelectMultiple(attrs={"checked":"checked",

    'onchange': "alert($(this).val());"}), choices=[(i.id, i.source.libelle +' - ' +i.destination.libelle) for i in Trajet.objects.all()], label='Liste des trajets')

    #alert($('input[type=checkbox][name=trajets]:checked').val());

    #$("#checkkBoxId").attr("checked") ? alert("Checked") : alert("Unchecked");
    
    #initial = [c[0] for c in MY_CHOICES]
    """
    class Meta:
        widgets = {
               'periode_du' : DatePickerInput(options={
                              'format': 'DD/MM/YYYY',
                              'locale': "fr",
              }),
               'periode_au' : DatePickerInput(options={
                              'format': 'DD/MM/YYYY',
                              'locale': "fr",
              }),
        }