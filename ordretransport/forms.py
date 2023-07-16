from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory, inlineformset_factory
from bootstrap_datepicker_plus import DatePickerInput
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper

from parametre.models import Ordretransport, Detailsot


class OrdretransportForm(forms.ModelForm):
    class Meta:
        model = Ordretransport
        exclude = ('valide',)
        widgets = {
           'date_ot' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
    } 



class DetailsotForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(DetailsotForm, self).__init__(*args, **kwargs)
    for field in self.fields:self.fields[field].label=''  
   
  class Meta:
    model = Detailsot
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
   } 

OtFormSet = modelformset_factory(Detailsot, form=DetailsotForm, extra=5, can_delete=True,
  fields=('trajet', 'marchandise', 'quantite', 'prix_unitaire'))

