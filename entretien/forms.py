from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Entretien
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper

class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        exclude = ()
        widgets = {
           'date_entretien_debut' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_entretien_fin' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_entretien_prochain' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),

           'fournisseur': AddAnotherWidgetWrapper(
                forms.Select(),
                reverse_lazy('entretien:add_fournisseur'),
             )

          }

