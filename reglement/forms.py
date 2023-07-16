from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Reglement

class ReglementForm(forms.ModelForm):
    class Meta:
        model = Reglement
        exclude = ()
        widgets = {
	           'date_reglement' : DatePickerInput(options={
	                          'format': 'DD/MM/YYYY',
	                          'locale': "fr",
	          }),
	    }