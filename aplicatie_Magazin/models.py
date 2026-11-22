from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator

# Create your models here.
class Brand(models.Model):
    nume_brand = models.CharField(
        max_length=50,
        unique=True, # [5%] Câmp unic (altul decât id-ul)
        error_messages={ # [10%] Mesaj de eroare personalizat (1/5)
            'unique': 'Există deja un brand înregistrat cu acest nume!',
            'max_length': 'Numele bradului nu poate depăși 50 de caractere.'
        }
    )
    tara_origine = models.CharField(
        max_length=50,
        null=True, # [5%] Câmp care admite null (1/5)
        blank=True,
        help_text='Țara în care se află sediul central al producătorului.' # [5%] help_text (1/5)
    )
    site_oficial = models.URLField( # [5%] Câmp ales dintre EmailField, URLField, SlugField
        max_length=200,
        null=True, # [5%] Câmp care admite null (2/5)
        blank=True,
        error_messages={ # [10%] Mesaj de eroare personalizat (2/5)
            'invalid': 'Introduceți un URL valid (ex: https://www.samsung.com).'
        }
    )
    
    class Meta:
        ordering = ['nume_brand'] # [5%] Ordonare implicită (Model 1/2)
        verbose_name_plural = 'Branduri'
        
    def __str__(self):
        return self.nume_brand
    
class Categorie(models.Model):
    nume = models.CharField(
        max_length=50,
        unique=True,
        error_messages={ # [10%] Mesaj de eroare personalizat (3/5)
            'unique': 'Această categorie există deja în baza de date!'
        }
    )
    descriere = models.TextField(
        null=True, # [5%] Câmp care admite null (3/5)
        blank=True
    )
    culoare = models.CharField(
        max_length=7,
        default="#007BFF", # [10%] Valoare default (1/4)
        help_text = "Cod hexazecimal pentru culoarea etichetei în interfață (ex: #FF5733)."  # [5%] help_text (2/5)
    )
    sigla = models.ImageField( # [5%] Câmp de tip ImageField
        upload_to='sigle_categorii/',
        null=True, # [5%] Câmp care admite null (4/5)
        blank=True,
        help_text= "Încărcați o pictogramă reprezentativă pentru categorie." # [5%] help_text (3/5)
    )
    ordine_afisare = models.PositiveBigIntegerField(
        default=1 # [10%] Valoare default (2/4)
    )
    
    class Meta:
        ordering = ['ordine_afisare','nume'] # [5%] Ordonare implicită (Model 2/2)
        verbose_name_plural = "Categorii"
        
    def __str__(self):
        return self.nume
    
class Magazin(models.Model):
    nume_sediu = models.CharField(max_length=100)
    adresa = models.CharField(max_length=255)
    telefon_contact = models.CharField(
        max_length=15,
        default='', # [10%] Valoare default care admite loc liber în admin (3/4)
        blank=True,
        help_text= "Numărul de telefon al recepției acestui punct de lucru."  # [5%] help_text (4/5)
    )
    
    class Meta:
        verbose_name_plural = 'Magazine'
        
    def __str__(self):
        return self.nume_sediu

class RaionDepozit(models.Model):
    TIPURI_ZONA = [
        ('Vitrina', 'Vitrină Expunere'),
        ('Depozit', 'Depozit Securizat'),
        ('Service', 'Zonă Service'),
    ]
    
    magazin = models.ForeignKey(
        Magazin,
        on_delete=models.CASCADE,
        related_name='raioane'
    )
    cod_raion = models.CharField(
        max_length=20,
        error_messages={ # [10%] Mesaj de eroare personalizat (4/5)
            'max_length': 'Codul raionului este prea lung (maxim 20 caractere).'
        }
    )
    tip_zona = models.CharField(
        max_length=20,
        choices=TIPURI_ZONA, # [10%] Câmp cu choices (1/2)
        default='Vitrina' # [10%] Valoare default (4/4)
    )
    capacitate_maxima = models.PositiveIntegerField(default=50)
    
    class Meta:
        # Impune unicitatea combinației (magazin, cod_raion) specifică entității slabe
        unique_together = ('magazin', 'cod_raion')
        verbose_name_plural = "Raioane Depozit"
        constraints = [
            # [25%] Constrângere Q (1/5): Capacitatea trebuie să fie cel puțin 5 unități
            models.CheckConstraint(
                condition=Q(capacitate_maxima__gte=5),
                name='capacitate_minima_raion',
                violation_error_message="Capacitatea unui raion trebuie să fie de minim 5 dispozitive."
            ),
            # [25%] Constrângere Q (2/5): Dacă zona este 'Vitrina', capacitatea maximă nu poate depăși 100
            models.CheckConstraint(
                condition=~Q(tip_zona='Vitrina') | Q(capacitate_maxima__lte=100),
                name='capacitate_maxima_vitrina',
                violation_error_message='O vitrină de expunere nu poate avea o capacitate mai mare de 100 de telefoane.' 
            ),
        ]
        
    def __str__(self):
        return f"{self.magazin.nume_sediu} - {self.cod_raion} ({self.tip_zona})"
    
class ServiciuTehnic(models.Model):
    denumire_serviciu = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=7, decimal_places=2)
    durata_estimata_minute = models.PositiveIntegerField(default=30)
    
    class Meta:
        verbose_name_plural = 'Servicii Tehnice'
        constraints = [
            # [25%] Constrângere Q (3/5): Tariful trebuie să fie strict pozitiv și durata minim 5 minute
            models.CheckConstraint(
                condition=Q(tarif__gt=0) & Q(durata_estimata_minute__gte=5),
                name='tarif_si_durata_valide',
                violation_error_message="Tariful trebuie să fie > 0 și durata estimată de minim 5 minute."
            )
        ]
    def __str__(self):
        return f"{self.denumire_serviciu} ({self.tarif} RON)"
    
class Telefon(models.Model):
    STARE_CHOICES = [
        ('Nou', 'Nou (Sigilat)'),
        ('Resigilat', 'Resigilat'),
        ('SH', 'Second-Hand'),
    ]
    
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='telefoane')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='telefoane')
    raion = models.ForeignKey(
        RaionDepozit,
        on_delete=models.SET_NULL,
        null=True, # [5%] Câmp care admite null (5/5)
        blank=True,
        related_name='telefoane'
    )
    servicii_compatibile = models.ManyToManyField(ServiciuTehnic, blank=True, related_name='telefoane')
    model = models.CharField(
        max_length=100,
        error_messages={ # [10%] Mesaj de eroare personalizat (5/5)
            'blank': 'Numele modelului este obligatoriu!'
        }
    )
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    memorie_ram = models.PositiveIntegerField(help_text="Capacitatea memoriei RAM în GB.") # [5%] help_text (5/5)
    stocare_interna = models.PositiveIntegerField()
    stare_fizica = models.CharField(
        max_length=15,
        choices=STARE_CHOICES, # [10%] Câmp cu choices (2/2)
        default='Nou'
    )
    este_in_stoc = models.BooleanField(default=True)
    data_lansare = models.DateField(null=True, blank=True)
    data_adaugare = models.DateTimeField(
        auto_now_add=True # [5%] Câmp datetime cu valoare implicită data adăugării
    )
    accesorii_incluse = models.JSONField(
        default=list,
        blank=True,
        help_text="Listă JSON cu accesoriile din cutie, ex: [\"Cablu USB-C\", \"Cheiță SIM\"]"
    )
    
    class Meta:
        verbose_name_plural = 'Telefoane'
        # [10%] Minim 4 câmpuri indexate (1. model, 2. pret, 3. stare_fizica, 4. este_in_stoc)
        indexes = [
            models.Index(fields=['model']),
            models.Index(fields=['pret']),
            models.Index(fields=['stare_fizica', 'este_in_stoc']),
        ]
        constraints = [
            # [25%] Constrângere Q (4/5): Prețul unui telefon trebuie să fie mai mare de 50 RON
            models.CheckConstraint(
                condition=Q(pret__gt=50),
                name='pret_minim_telefon',
                violation_error_message="Prețul unui telefon trebuie să fie mai mare de 50 RON."
            ),
            # [25%] Constrângere Q (5/5): Stocarea internă trebuie să fie mai mare sau egală cu memoria RAM
            models.CheckConstraint(
                condition=Q(stocare_interna__gte=F('memorie_ram')),
                name='stocare_mai_mare_ca_ram',
                violation_error_message="Capacitatea de stocare internă nu poate fi mai mică decât memoria RAM."
            ),
        ]
        
    def __str__(self):
        return f'{self.brand.nume_brand} {self.model} ({self.stocare_interna}GB)'
    