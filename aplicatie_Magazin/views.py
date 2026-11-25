from datetime import datetime as dt
import locale
import re
from .middleware import get_ip
from collections import Counter

locale.setlocale(locale.LC_TIME, 'ro_RO.UTF-8')
lista_accesari = []

#Lab 1 ex 4
class Accesare:
    contor_id=1
    def __init__(self,ip_client,url,parametri={}):
        self.ip_client=ip_client
        self.id=Accesare.contor_id
        Accesare.contor_id+=1  
        #print(self.id)
        self.url=url
        parametri=dict(url.GET.lists())
        self.parametri=parametri
        data=dt.now()
        self.data=data
    #Lab 1 ex 5    
    def lista_parametri(self):
        #print(self.parametri)
        lista_parametri=[]
        for key,values in self.parametri.items():
            valori_finale=[]
            for elem in values:
                if elem.isdigit():
                    valori_finale.append(int(elem))
                elif elem == "":
                    valori_finale.append(None)
                else:
                    valori_finale.append(elem)
            if len(valori_finale) > 1:
                lista_parametri.append((key,valori_finale))
            else:
                lista_parametri.append((key,valori_finale[0]))
        
        return lista_parametri
    #Lab 1 ex 6
    def string_url(self):
        return self.url.build_absolute_uri()
    #Lab 1 ex 6
    def pagina(self):
        route = self.url.resolver_match.url_name
        if route == 'detalii_accesare':
            id_acc = self.url.resolver_match.kwargs.get('id_acc')
            return f"/accesare{id_acc}"
        elif route == 'info_static' or route == 'info_dinamic':
            route = 'info'
        nume_pagina = "/" if route == "index" else "/" + route
        return nume_pagina
    #Lab 1 ex 7
    def calculeaza_data(self, data=''):
        #Lab 1 ex 10
        if data == "zi":
            format='%e %B %Y'
        elif data == "timp":
            format='%T'
        else:
            format='%A, %e %B %Y %T'
            
        return self.data.strftime(format).title()
    #Lab 1 ex 8
    def __str__(self):
        dictionar_accesare={}
        dictionar_accesare["string_url"] = self.string_url()
        dictionar_accesare["pagina"] = self.pagina()
        dictionar_accesare["calculeaza_data"] = self.calculeaza_data()
        dictionar_accesare["lista_parametri"] = str(self.lista_parametri())
        dictionar_accesare["id_accesare"] = str(self.id)
        dictionar_accesare["ip_client"] = self.ip_client
        string_accesare= "\n".join(f"{k}: '{dictionar_accesare[k]}'" for k in dictionar_accesare) 
        return string_accesare
        
from django.shortcuts import render

from django.http import HttpResponse
#Lab 1 ex 2
def index(request):
    a_index=Accesare(get_ip(request),request)
    lista_accesari.append(a_index)
    #print(a1.string_url())
    #print(a1.pagina())
    print(a_index.__str__())
    titlu_tab = 'Pagina principală'
    titlu_articol = "Pagina principală"
    continut_articol = '<p id="request_text">&nbsp;&nbsp;&nbsp;&nbsp;Proiectul este conceput având ca obiectiv un website pentru un magazin de vânzare de telefoane mobile (smartphones). Acesta permite utilizatorilor să navigheze printr-un catalog de produse în vederea achiziționării. Fiecare telefon este înregistrat cu un număr unic de identificare și are asociată o fișă cu detalii tehnice (tip de telefon, ca de exemplu, smartphone android, iPhone, Huawei), model, marcă, memorie, starea fizică (dacă este nou sau second hand), anul fabricației, accesorii incluse etc.) și prețul propus.<br>&nbsp;&nbsp;&nbsp;&nbsp;De asemenea, aplicația oferă și servicii tehnice de testare, optimizare, curățare a telefonului, precum și de instalare sistem de operare.</p>'
    return render(request, "pagina_principala.html",
        {
            "titlu_tab":titlu_tab,
            "titlu_articol":titlu_articol,
            "continut_articol":continut_articol
        }
        )
#Lab 2 ex 5
def afis_istoric(request):
    a_istoric = Accesare(get_ip(request), request)
    lista_accesari.append(a_istoric)
    titlu_tab = 'Istoricul'
    titlu_articol = "Istoricul magazinului nostru"
    continut_articol = '<p id="request_text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Afacerea noastră a pornit în anul 2020 dintr-un mic atelier de reparații GSM din București, având ca pasiune principală tehnologia mobilă și dorința de a oferi clienților dispozitive verificate și de încredere.<br>&nbsp;&nbsp;&nbsp;&nbsp;De-a lungul timpului, ne-am extins activitatea de la simple intervenții hardware la comercializarea unei game variate de telefoane mobile noi și recondiționate, dezvoltând totodată această platformă online pentru a facilita accesul clienților din toată țara la produsele și serviciile noastre.</p>'
    return render(request, "istoric.html",
        {
            "titlu_tab":titlu_tab,
            "titlu_articol":titlu_articol,
            "continut_articol":continut_articol
        }
    )
#Lab 2 ex 5
def afis_despre(request):
    a_despre = Accesare(get_ip(request), request)
    lista_accesari.append(a_despre)
    titlu_tab = 'Despre noi'
    titlu_articol = "Despre noi și echipa noastră"
    continut_articol = '<p id="request_text">&nbsp;&nbsp;&nbsp;&nbsp;Suntem o echipă dedicată de tehnicieni și consultanți specializați în ecosistemele iOS și Android, pregătiți să te ajute să alegi telefonul potrivit nevoilor și bugetului tău.<br>&nbsp;&nbsp;&nbsp;&nbsp;Fiecare dispozitiv second-hand din oferta noastră trece printr-un proces riguros de testare în 30 de puncte înainte de a fi listat pe site, beneficiind de garanție și suport tehnic post-vânzare.</p>'
    return render(request, "despre.html",
        {
            "titlu_tab":titlu_tab,
            "titlu_articol":titlu_articol,
            "continut_articol":continut_articol
        }
    )
#Lab 1 ex 2
def afis_info(request, data=""):
    now=dt.now()
    #now_formated = now.strftime('%A, %e %B %Y').title()
    #Lab 1 ex 3
    a_info=Accesare(get_ip(request),request)
    lista_accesari.append(a_info)
    #print(a3.string_url())
    #print(a3.pagina())
    #print(a3.lista_parametri())
    print(a_info.__str__())
    return render(request,"info.html",
        {
            "titlu_tab":"Informații despre server",
            "titlu_articol":"Informații despre server",
            "continut_articol":"Continut text",
            #"data_ora_articol":f"{now_formated}",
            "data_ora_articol":f"{a_info.calculeaza_data(data)}"
        }
    )

def afis_log(request):
    a_log = Accesare(get_ip(request),request)
    lista_accesari.append(a_log)
    ultimele = request.GET.get('ultimele')
    istoric_accesari = lista_accesari
    mesaj_eroare=''
    #Lab 2 ex 1
    pagini_accesate = [acc.pagina() for acc in lista_accesari]
    contor_pagini = Counter(pagini_accesate)
    min_accesari = len(lista_accesari) + 1
    max_accesari = 0
    pagina_max = '-'
    pagina_min = '-'
    for pagina, nr_accesari in contor_pagini.items():
        if nr_accesari < min_accesari:
            min_accesari = nr_accesari
            pagina_min = pagina
        if nr_accesari > max_accesari:
            max_accesari = nr_accesari
            pagina_max = pagina
    if len(contor_pagini) < 2:
        pagina_min = '-'
    #print(pagina_min, min_accesari, pagina_max, max_accesari)
    
    if ultimele is not None:
        if ultimele.isdigit():
            n = int(ultimele)
            k = len(lista_accesari)
            
            if n > k:
                istoric_accesari = lista_accesari
                if k == 1:
                    mesaj_eroare = f'Exista doar o singura ({k}) accesare fata de {n} accesari cerute!'
                else:
                    mesaj_eroare = f'Exista doar {k} accesari fata de {n} accesari cerute!'
            elif n == 0:
                istoric_accesari = []
            else:            
                istoric_accesari = lista_accesari[-n:]
        else:
            mesaj_eroare = "Parametrul 'ultimele' trebuie sa aiba o valoare numerica intreaga!"
            istoric_accesari = []
    
    accesari = request.GET.get('accesari')
    #Lab 2 ex 2
    sectiune_suplimentara = (accesari == "nr")
    #Lab 2 ex 3
    sectiune_detalii = (accesari == "detalii")
    #Lab 2 ex 4
    tabel = request.GET.get('tabel')
    coloane_tabel = []
    randuri_tabel = []
    
    if tabel:
        if tabel.strip().lower() == "tot":
            coloane_tabel = ['id', 'url', 'pagina', 'data', 'parametri', 'ip_client']
        else:
            coloane_tabel = [col.strip().lower() for col in tabel.split(',') if col.strip()]

        for item in istoric_accesari:
            valori = {
                'id': item.id,
                'url': item.string_url(),
                'pagina': item.pagina(),
                'data': item.calculeaza_data(),
                'parametri': str(item.lista_parametri()),
                'ip_client': item.ip_client,
            }
            rand = [valori.get(col, "N/A") for col in coloane_tabel]
            randuri_tabel.append(rand)
        
    nume_parametri = list(request.GET.keys())
    nr_parametri = len(nume_parametri)
    #Lab 2 ex 2
    iduri = request.GET.getlist('iduri')
    iduri_dubluri = request.GET.get("dubluri", "false").lower() == 'true'

    if iduri:
        iduri_parsate = []
        for lista in iduri:
            for elem in lista.split(","):                
                if elem.isdigit():
                    #print(int(elem))
                    if iduri_dubluri:
                        iduri_parsate.append(elem)
                    else:
                        if elem in iduri_parsate:
                            continue
                        else:
                            iduri_parsate.append(elem)
        print(",".join( str(elem) for elem in iduri_parsate))
                
    text_final = "\n\n".join([str(elem) for elem in istoric_accesari])
    
    if mesaj_eroare:
        if text_final:
            text_final += f"\n\n{mesaj_eroare}"
        else:
            text_final = mesaj_eroare

    if sectiune_suplimentara:
        text_final += f"\n\n Numarul de accesari de cand a fost pornit serverul (in sesiunea curenta): {len(lista_accesari)}"

    return render(request,"log.html",
        {
            "titlu_tab":"Log accesari",
            "titlu_articol":"Log accesari",
            "continut_articol":text_final,
            "sectiune_detalii": sectiune_detalii,
            "lista_completa_accesari": lista_accesari,
            "nr_parametri": nr_parametri,
            "nume_parametri": nume_parametri,
            "coloane_tabel":coloane_tabel,
            "randuri_tabel":randuri_tabel,
            "pagina_min": pagina_min,
            "pagina_max": pagina_max
        }
    )

def detalii_accesare(request,id_acc):
    accesare_gasita = None
    id_cautat = int(id_acc)

    for item in lista_accesari:
        if item.id == id_cautat:
            accesare_gasita = item
            break
    
    a_curenta = Accesare(get_ip(request), request)
    lista_accesari.append(a_curenta)

    return render(request, "detalii_accesare.html", {
        "accesare": accesare_gasita,
        "id_cautat": id_cautat
    })

def in_lucru(request):
    a_in_lucru = Accesare(get_ip(request), request)
    lista_accesari.append(a_in_lucru)
    return render(request, "in_lucru.html",{
        "continut_articol": "<p>Această secțiune a magazinului nostru online este momentan în curs de dezvoltare. Echipa noastră lucrează la adăugarea funcționalităților și a conținutului dedicat. Te rugăm să revii în curând!</p>"
    })

# def pag1(request):
#     return HttpResponse(2+3)

# l=[]
# def pag2(request):
#     global l
#     a=request.GET.get("a",10)
#     print(request.GET)
#     l.append(a)
#     return HttpResponse(f"<b>Am primit</b>: {l}")

# def functie(request):
#     val_a=request.GET.get("a")
#     val_b=request.GET.get("b",10)
#     #a1=Accesare(123)
#     #a2=Accesare(123)
#     return HttpResponse(f"Al 2-lea raspuns<br>{int(val_a)+int(val_b)}")
#     #return HttpResponse(f"Al 2-lea raspuns<br>{a2.id}")
