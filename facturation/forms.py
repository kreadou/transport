from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from parametre.models import Facturation, Para
from datetime import datetime


class MyDatePickerInput(DatePickerInput):
    pass
    #template_name = 'facturation/date-picker.html'


class ToDoForm(forms.Form):
    date = forms.DateField(
        widget=MyDatePickerInput(format='%m/%d/%Y')
    )


class FacturationForm(forms.ModelForm):
    class Meta:
        model = Facturation
        exclude = ('numero_facture',)
        widgets = {
               'date_facture' : DatePickerInput(options={
                              'format': 'DD/MM/YYYY',
                              'locale': "fr",
              }),
        }

class PeriodeForm(forms.Form):#datetime(2022,1,1),
    periode_du = forms.DateField(
      initial=Para.objects.all()[Para.objects.count()-1].date_debut if Para.objects.all() else None, 
      label="Période du",
      required=False,
      widget=forms.widgets.DateInput(
        format=('%Y-%m-%d'), 
        attrs={'type':'date'}))
    
    periode_au = forms.DateField(
      initial=datetime.today, 
      label='Période au', 
      required=False,
    widget=forms.widgets.DateInput(
      format=('%Y-%m-%d'), 
      attrs={'type':'date'}
  ))
