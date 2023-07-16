from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Enlevement, Ordretransport

class EnlevementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnlevementForm, self).__init__(*args, **kwargs)
        #for field in self.fields:self.fields[field].label=''    
    class Meta:
        model = Enlevement
        exclude = (
        	'lieu_chargement', 
        	'contact_chargement', 
        	'telephone_chargement', 
        	'lieu_dechargement', 
        	'contact_dechargement', 
        	'telephone_dechargement', 
        	"date_dechargement",
        	'etat_enlevement',
        	'observation'
       	)
        widgets = {
           'date_enlevement' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
            'trajet': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:trajet_add')),

            'marchandise': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:marchandise_add')), 

            'vehicule': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:vehicule_add')), 

            'chauffeur': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:chauffeur_add')), 
            'rubrique': forms.Textarea(attrs={'rows': 3}),
          } 
          
EnlevementFormSet = inlineformset_factory(Ordretransport, Enlevement, extra=0, fields=(
    'date_enlevement', 
    'trajet', 
    'marchandise', 
    'vehicule',
    'chauffeur',
    'quantite',
    'prix_unitaire'
    ))

