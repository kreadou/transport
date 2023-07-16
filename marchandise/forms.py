from django import forms

from parametre.models import Marchandise

class MarchandiseForm(forms.ModelForm):
    class Meta:
        model = Marchandise
        exclude = ('couleur', 'etat0', 'etat1', 'etat2', 'etat3', 'etat4', 'etat5',)



