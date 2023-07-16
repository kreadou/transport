# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from bootstrap_datepicker_plus import DatePickerInput
from datetime import date
from django_addanother.widgets import AddAnotherWidgetWrapper

from parametre.models import *


class LoginForm(AuthenticationForm):
  username = forms.CharField(label="User name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
  password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class ProfilForm(ModelForm):
    class Meta:
        model = Profil
        exclude=('user', 'fichier_qrcode')

class ProfilForm2(ModelForm):
    class Meta:
        model = Profil
        exclude=('user', 'fichier_qrcode', 'groupe', 'login', 'compte', 'service', 'mode_reglement', 'type_profil')


class TrajetForm(ModelForm):
  class Meta:
      model = Trajet
      exclude = ()
      widgets = {
          'source': AddAnotherWidgetWrapper(
              forms.Select,
              reverse_lazy('marchandise:source_add')),
          'destination': AddAnotherWidgetWrapper(
              forms.Select,
              reverse_lazy('marchandise:destination_add')),
        }


class CommuneForm(ModelForm):
  class Meta:
      model = Commune
      exclude = ()
      

class ClientForm(ModelForm):
  class Meta:
      model = Client
      exclude = ()

class TarificationtForm(ModelForm):
  class Meta:
      model = Tarification
      exclude = ()


class ChauffeurForm(ModelForm):
  class Meta:
      model = Chauffeur
      exclude = ()


class VehiculeForm(ModelForm):
  class Meta:
      model = Vehicule
      exclude = ()

class CarburantForm(ModelForm):
  class Meta:
    model = Carburant
    exclude = ()


class FacturationForm(ModelForm):
  class Meta:
    model = Facturation
    exclude = ('numero_facture',)


class DepenseForm(ModelForm):
  class Meta:
    model = Depense
    exclude = () 
    widgets = {
           'date_depense' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
          }),
    }


class SocieteForm(ModelForm):
  class Meta:
    model = Societe
    exclude = ()
    widgets = {
           'dateEnvoiEmail' : DatePickerInput(options={
                          'format': 'DD/MM/YYYY',
                          'locale': "fr",
                          }),
          } 

class ParaForm(ModelForm):
  class Meta:
    model = Para
    exclude = ()


class PeriodeForm(forms.Form):
    periode_du = forms.DateField(
      initial=Para.objects.all()[Para.objects.count()-1].date_debut if Para.objects.all() else None, 
      label="Du ",
      required=False,
      widget=forms.widgets.DateInput(
        format=('%Y-%m-%d'), 
        attrs={'type':'date'}))
    
    periode_au = forms.DateField(
      initial= date.today(), 
      label='Au ', 
      required=False,
    widget=forms.widgets.DateInput(
      format=('%Y-%m-%d'), 
      attrs={'type':'date'}
  ))
