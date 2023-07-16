from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper

from parametre.models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        exclude = ('etat_commande', 'numero_dossier', 'marchandises', 'valide', 'tonnage_estime', 'volume_estime')
        widgets = {
            
           'description': forms.Textarea(attrs={"rows":1, "cols":3}),

           'client': AddAnotherWidgetWrapper(
                forms.Select(),
                reverse_lazy('commande:add_client'),
          ),
           'date_bon_commande' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_commande' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
          } 

