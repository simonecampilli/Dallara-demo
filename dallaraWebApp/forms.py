from django import forms
from .models import Dipendente

class DipendenteForm(forms.ModelForm):
    class Meta:
        model = Dipendente
        fields = ['nome', 'cognome', 'data_nascita', 'anzianita', 'formazioni', 'lavori', 'tipo_lavoro', 'area_di_lavoro', 'altri_campi', 'risorse_umane', 'username', ]
