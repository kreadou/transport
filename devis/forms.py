from django import forms
from django.forms import modelformset_factory
from bootstrap_datepicker_plus import DatePickerInput
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper
from django.forms.widgets import Textarea
from parametre.models import Devis, Detailsdevis

class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        exclude = ('valide',)
        widgets = {
            'client': AddAnotherWidgetWrapper(
                forms.Select(),
                reverse_lazy('commande:add_client'),
        ),
           'date_devis' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
            }),
        'condition_vente': Textarea(attrs={'cols': 80, 'rows': 3}),
      }


class DetailsdevisForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(DetailsdevisForm, self).__init__(*args, **kwargs)
    for field in self.fields:self.fields[field].label=''  
   
  class Meta:
    model = Detailsdevis
    exclude = ()
    widgets = {
            'marchandise': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('commande:add_marchandise'),
        ),

            'trajet': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('commande:add_trajet'),
      ),

            'rubrique': Textarea(attrs={'cols': 80, 'rows': 1}),

   } 

DevisFormSet = modelformset_factory(Detailsdevis, form=DetailsdevisForm, extra=5, can_delete=True,
  fields=('trajet', 'marchandise', 'quantite', 'prix_unitaire', 'rubrique'))

