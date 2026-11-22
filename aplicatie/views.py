from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Primul raspuns")

contor_id = 0
suma = 0

def aduna_numere(request,slug):
    global contor_id, suma
    sir_char = slug
    nb_list = []
    for char in reversed(sir_char):
        if char.isdigit():
            nb_list.append(char)
        else:
            break
    if nb_list:
        valoare = int("".join(reversed(nb_list)))
        suma += valoare
    else:
        return HttpResponse("-eroare")
    contor_id += 1
        
    return HttpResponse(f"numar cereri:{contor_id} suma numere:{suma}")

def afiseaza_liste(request):
    valori_liste = dict(request.GET.lists())

    return render(request, "baza_task_extra.html", {
            "valori_liste": valori_liste
        }
    )