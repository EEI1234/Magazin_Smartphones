from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',views.index, name='index_task_extra'),
    path('pag',views.index, name="pag"),
    path('pag/<slug:slug>',views.aduna_numere, name="pag_dinamic"),
    path('liste',views.afiseaza_liste, name="liste")
]
