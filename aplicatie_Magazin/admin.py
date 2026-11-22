from django.contrib import admin
#from .models import Ambalaj, Prajitura
from .models import Brand, Categorie, Magazin, RaionDepozit, ServiciuTehnic, Telefon 

# Register your models here.
#admin.site.register()
# admin.site.register(Brand)
# admin.site.register(Categorie)
# admin.site.register(Magazin)
# admin.site.register(RaionDepozit)
# admin.site.register(ServiciuTehnic)
# admin.site.register(Telefon)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume_brand', 'tara_origine', 'site_oficial')
    search_fields = ('nume_brand', 'tara_origine')


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'ordine_afisare', 'culoare')
    list_editable = ('ordine_afisare',)
    search_fields = ('nume',)


@admin.register(Magazin)
class MagazinAdmin(admin.ModelAdmin):
    list_display = ('nume_sediu', 'adresa', 'telefon_contact')
    search_fields = ('nume_sediu', 'adresa')


@admin.register(RaionDepozit)
class RaionDepozitAdmin(admin.ModelAdmin):
    list_display = ('cod_raion', 'magazin', 'tip_zona', 'capacitate_maxima')
    list_filter = ('magazin', 'tip_zona')
    search_fields = ('cod_raion',)


@admin.register(ServiciuTehnic)
class ServiciuTehnicAdmin(admin.ModelAdmin):
    list_display = ('denumire_serviciu', 'tarif', 'durata_estimata_minute')
    search_fields = ('denumire_serviciu',)


@admin.register(Telefon)
class TelefonAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'categorie', 'pret', 'memorie_ram', 'stocare_interna', 'stare_fizica', 'este_in_stoc')
    list_filter = ('brand', 'categorie', 'stare_fizica', 'este_in_stoc')
    search_fields = ('model', 'brand__nume_brand')