from django import forms

from parametre.models import Alerte, Para

class AlerteForm(forms.ModelForm):
    class Meta:
        model = Alerte
        exclude = ('couleur', 'etat0', 'etat1', 'etat2', 'etat3', 'etat4', 'etat5',)


class ParaForm(forms.ModelForm):
    class Meta:
        model = Para
        fields = ('delai_piece_date_expiration', 'delai_permis_date_echeance', 'delai_carte_acces_echeance',
        'delai_entretien_prochain', 'delai_kilometrage_prochain_entretien', 'delai_echeance_visite', 
        'delai_echeance_assurance', 'delai_echeance_stationnement', 'delai_echeance_patente'
        )
