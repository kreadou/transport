from django import forms

from parametre.models import Carburant

class CarburantForm(forms.ModelForm):
    class Meta:
        model = Carburant
        exclude = ()



