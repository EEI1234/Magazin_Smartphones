def get_ip(request):
        req_headers = request.META
        str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if str_lista_ip:
            return str_lista_ip.split(',')[-1].strip()
        else:
            return request.META.get('REMOTE_ADDR')

#nr_total_accesari = 0
#Lab 1 ex 8 + #Lab 2 task 2 ex 6
class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # global nr_total_accesari
        # nr_total_accesari += 1
        # cod de procesare a cererii ....      
        #putem trimite date către funcția de vizualizare; le setăm ca proprietăți în obiectul request     
        request.proprietate_noua=17       
        # se apelează indirect funcția de vizualizare (din views.py)
        response = self.get_response(request)      

        # putem adauga un header HTTP pentru toate răspunsurile
        response['header_nou'] = 'valoare'
        #verificăm tipul de conținut folosind headerul HTTP Content-Type
        # putem transmite divere resurse (imagini, css etc.), nu doar html-uri
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            # obținem conținutul raspunsului
            # (response.content este memorat sub forma de bytes -> transformăm în string
            content = response.content.decode('utf-8')
            # Modificăm conținutul raspunsului generat din views
            new_content = content.replace(
                '</footer>',
                f'<div>IP-ul tău este: <strong>{get_ip(request)}</strong></div></footer>'
            )
            # Suprascriem conținutul răspunsului (in obiectul response)
            response.content = new_content.encode('utf-8')
            # Actualizăm lungimea conținutului -> obligatoriu pentru headerele HTTP
            response['Content-Length'] = len(response.content)
        return response