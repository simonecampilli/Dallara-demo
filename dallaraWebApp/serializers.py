from rest_framework import serializers
from .models import Dipendente

from rest_framework import serializers
from .models import Dipendente, Formazione, Storico

class FormazioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formazione
        fields = ['id', 'nome', 'descrizione']

class StoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storico
        fields = ['id', 'nome', 'descrizione']

class DipendenteSerializer(serializers.ModelSerializer):
    formazioni = FormazioneSerializer(many=True, read_only=True)
    lavori = StoricoSerializer(many=True, read_only=True)

    class Meta:
        model = Dipendente
        fields = ['id', 'nome', 'cognome', 'data_nascita', 'anzianita', 'amministratore',
                  'formazioni', 'lavori', 'accesso_area', 'tipo_lavoro', 'area_di_lavoro',
                  'altri_campi', 'risorse_umane']
