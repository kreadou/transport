from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Chauffeur

class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Chauffeur
        exclude = ()
        widgets = {
           'date_naissance' : DatePickerInput(options={
                         'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_entree' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_sortie' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'piece_date_etablissement' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'piece_date_expiration' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'permis_date_etablissement' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'permis_date_echeance' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),


          } 


