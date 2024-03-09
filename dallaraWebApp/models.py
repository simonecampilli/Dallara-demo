from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Dipendente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    data_nascita = models.DateField()
    anzianita = models.IntegerField()  # Anni di anzianità all'interno dell'azienda
    amministratore = models.BooleanField(default=False)
    formazioni = models.ManyToManyField('Formazione', blank=True)
    lavori = models.ManyToManyField('Storico', blank=True)
    accesso_area = models.BooleanField(default=False)
    tipo_lavoro = models.CharField(max_length=100)
    area_di_lavoro = models.CharField(max_length=100)
    altri_campi = models.TextField(blank=True)
    risorse_umane = models.BooleanField(default=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    immagine_profilo = models.ImageField(upload_to='immagini_profilo/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"

class Formazione(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    #flag_conseguito = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class JobRequest(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    flag_conseguito = models.BooleanField(default=False)

    def __str__(self):
        return self.nome



class Storico(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    premio = models.CharField(max_length=100, default=False)
    data = models.CharField(max_length=100)
    def __str__(self):
        return self.nome




