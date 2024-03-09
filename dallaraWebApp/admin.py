from django.contrib import admin

# Register your models here.
from .models import Dipendente,Formazione, JobRequest, Storico

admin.site.register(Dipendente)
admin.site.register(Formazione)
admin.site.register(JobRequest)
admin.site.register(Storico)