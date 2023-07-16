from django import forms
from django.urls import reverse_lazy
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper
from parametre.models import Detailscommande

class DetailscommandeForm(forms.ModelForm):
    class Meta:
        model = Detailscommande
        exclude = ()
        widgets = {
            'marchandise': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:marchandise_add')),
            'trajet': AddAnotherWidgetWrapper(
                forms.Select,
                reverse_lazy('marchandise:trajet_add')),
        }
# COMMENT APPELER UNE FONCTION admin
#admin:{{ app_label }}_{{ model_name }}_changelist

### appel de admin    reverse_lazy('admin:parametre_trajet_add')),



