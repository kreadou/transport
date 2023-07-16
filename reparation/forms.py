from django import forms

from parametre.models import Reparation

class ReparationForm(forms.ModelForm):
    class Meta:
        model = Reparation
        exclude = ('couleur', 'etat0', 'etat1', 'etat2', 'etat3', 'etat4', 'etat5',)



