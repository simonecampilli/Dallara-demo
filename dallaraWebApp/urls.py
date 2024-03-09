from django.contrib import admin
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path('dipendente/<int:dipendente_id>/', views.visualizza_dipendente, name='visualizza_dipendente'),
    path('ricerca_dipendenti/', views.ricerca_dipendenti, name='ricerca_dipendenti'),
    path('api/dipendenti/', views.dipendente_list, name='dipendenti-list-create'),
    path('api/dipendenti/<int:pk>/', views.dipendente_detail, name='dipendente-detail'),
    path('domanda', views.domanda, name='domanda'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('storico/',views.storico,name='storico'),
    path('proposte/',views.pag3,name='pag3'),
    path('pag4/',views.pag4,name='pag4'),

    path('proposte2/',views.proposte, name='proposte'),

    path('logout', views.custom_logout, name='logout'),
    path('dipendente/<int:pk>/modifica/', views.modifica_dipendente, name='modifica_dipendente'),
    path('dipendente/nuovo', views.aggiungi_dipendente, name='aggiungi_dipendente')

]
