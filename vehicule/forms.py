from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        exclude = ()
        widgets = {
           'date_mise_en_circulation' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_effet' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_echeance_visite' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_echeance_assurance' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_echeance_stationnement' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
           'date_echeance_patente' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
          }
