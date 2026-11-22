from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    # path("pagina",views.functie,name="pagina"),
    path("istoric",views.afis_istoric,name="istoric"),
    path("despre",views.afis_despre,name="despre"),
    path("info",views.afis_info,name="info_static"),
    path("info/<str:data>",views.afis_info,name="info_dinamic"),
    # path('exemplu_template', views.afis_template, name="exemplu_template"),
    # path('exemplu_template2', views.afis_template, name="exemplu_template2"),
    path('log',views.afis_log,name="log"),
    path('produse', views.in_lucru, name="produse"),
    path('servicii', views.in_lucru, name="servicii"),
    path('accesorii', views.in_lucru, name="accesorii"),
    path('cos_virtual', views.in_lucru, name="cos_virtual"),
    path('contact', views.in_lucru, name="contact"),
    re_path(r'^accesare(?P<id_acc>\d+)/?$', views.detalii_accesare, name='detalii_accesare'),
]
