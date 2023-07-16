from django import forms

from parametre.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ()



