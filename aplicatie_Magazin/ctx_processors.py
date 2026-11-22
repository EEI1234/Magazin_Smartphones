from django.conf import settings

def procesare(request):
    return {
        'optiuni_meniu':["acasa","despre","produse"],
        #'parametru_calculat': calculeaza(request),
        'copyright': f'© {settings.DATE_FIRMA['an_infiintare']} - 2026 Magazin Smartphones. Toate drepturile rezervate.',
        'date_firma':settings.DATE_FIRMA
    }
