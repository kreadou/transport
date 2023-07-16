from django import forms

from parametre.models import Planning

class PlanningForm(forms.ModelForm):
    class Meta:
        model = Planning
        exclude = ('couleur', 'etat0', 'etat1', 'etat2', 'etat3', 'etat4', 'etat5',)



