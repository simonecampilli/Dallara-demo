from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from rest_framework.parsers import JSONParser
from .models import Dipendente, JobRequest
from .serializers import DipendenteSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Dipendente
from .forms import DipendenteForm  # Assumi che ci sia un modulo DipendenteForm
from django.shortcuts import render, redirect
from .forms import DipendenteForm
from django.shortcuts import render
from .models import JobRequest

#index è uguale per tutti
def index(request):
    if not request.user.is_authenticated:
        print(request.user)
        return render(request, "htmls/login.html")
    else:
        print(request.user)

        return render(request,"htmls/homepage.html",{
            "username":Dipendente.objects.get(username=request.user).username,
            "nome":Dipendente.objects.get(username=request.user).nome,
            "cognome": Dipendente.objects.get(username=request.user).cognome,
            "data_nascita": Dipendente.objects.get(username=request.user).data_nascita,
            "tipo_lavoro": Dipendente.objects.get(username=request.user).tipo_lavoro,
            "anzianita": Dipendente.objects.get(username=request.user).anzianita,
            "area_di_lavoro":Dipendente.objects.get(username=request.user).area_di_lavoro,
            "altri_campi":Dipendente.objects.get(username=request.user).altri_campi,
            "lista_attestati":Dipendente.objects.get(username=request.user).formazioni.all(),
            "immagine_profilo":Dipendente.objects.get(username=request.user).immagine_profilo.url,
            'id_dipendente': Dipendente.objects.get(username=request.user).pk

        })
# storico vale per tutti
from .models import Storico
def storico(request):
    if not request.user.is_authenticated:
        return render(request, "htmls/login.html")
    else:
        '''
        return render(request,"htmls/storico.html",{
            "lavori": Dipendente.objects.get(username=request.user).lavori,
            "formazione": Dipendente.objects.get(username=request.user).formazioni,
        })'''
        lavori = Dipendente.objects.get(username=request.user).lavori.all()
        print(lavori)# Recupera tutti i lavori dal database
        context = {'lavori': lavori}
        return render(request, "htmls/storico.html", context)



#proposte vale solo per gli operai
def pag3(request):
    if not request.user.is_authenticated:
        return render(request, "htmls/login.html")
    else:
        tipo_lavoro=Dipendente.objects.get(username=request.user).tipo_lavoro
        if Dipendente.objects.get(username=request.user).amministratore or Dipendente.objects.get(username=request.user).risorse_umane:
            return render(request, "htmls/lista_dipendenti.html")

        else:
            if request.method == 'POST':
                print(request.POST)
                titolo = request.POST.get('titolo')
                print(titolo)
                descrizione = request.POST.get('descrizione')
                print(descrizione)
                oggetto_modello = Dipendente.objects.get(username=request.user)  # Otteniamo l'oggetto del modello (assicurati che ne esista uno)
                if oggetto_modello and titolo!=None:
                    print("ciao")
                    # Creiamo un nuovo oggetto Storico per il nuovo lavoro
                    nuovo_lavoro,creato= Storico.objects.get_or_create(nome=titolo, descrizione=descrizione, premio="Nessuno", data="oggi")
                    # Aggiungiamo il nuovo lavoro al campo ManyToMany
                    oggetto_modello.lavori.add(nuovo_lavoro)
                    return JsonResponse({'message': 'Elemento aggiunto con successo!'})
                else:
                    job_list = JobRequest.objects.all()
                    jobs = []
                    for x in job_list:
                        print(x.descrizione)
                        elementi = x.descrizione.split(',')
                        elementi = [elemento.strip() for elemento in elementi]
                        if Dipendente.objects.get(username=request.user).tipo_lavoro.lower() in elementi:
                            jobs.append(x)
                    # job_desc = job_list.
                    # print(job_desc)
                    return render(request, 'htmls/posizioni_aperte.html', {'job_list': jobs})
            else:

                job_list=JobRequest.objects.all()
                jobs=[]
                for x in job_list:
                    print(x.descrizione)
                    elementi = x.descrizione.split(',')
                    elementi = [elemento.strip() for elemento in elementi]
                    if Dipendente.objects.get(username=request.user).tipo_lavoro.lower() in elementi:
                        jobs.append(x)
                #job_desc = job_list.
                #print(job_desc)
                return render(request, 'htmls/posizioni_aperte.html', {'job_list': jobs})
                #"lavori": JobRequest.objects.filter(descrizione=tipo_lavoro),


def pag4(request):
    if not request.user.is_authenticated:
        return render(request, "htmls/login.html")
    else:
        tipo_lavoro=Dipendente.objects.get(username=request.user).tipo_lavoro
        if Dipendente.objects.get(username=request.user).amministratore:
            return render(request, "htmls/domanda.html")
        elif Dipendente.objects.get(username=request.user).risorse_umane:
            return render(request, "htmls/vuoto.html")
        else:
            return render(request, "htmls/vuoto.html")


#login lo hanno tutti
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if username in ["michele"]:
                return HttpResponseRedirect(reverse("homepage"))
            else:
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "htmls/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "htmls/login.html")


def invio_in_bacheca(request):
    if not request.user.is_authenticated:
        return render(request, "htmls/login.html")
    else:
        tipo_lavoro=Dipendente.objects.get(username=request.user).tipo_lavoro

        return render(request, "htmls/storico.html", {
            "lavori": JobRequest.objects.filter(descrizione=tipo_lavoro),
        })
def visualizza_dipendente(request, dipendente_id):
    dipendente = Dipendente.objects.get(id=dipendente_id)

    context = {
        'dipendente': dipendente
    }

    return render(request, 'htmls/visualizza_dipendente.html', context)

def ricerca_dipendenti(request):
    if request.method == 'GET':

        nome = request.GET.get('nome')
        cognome = request.GET.get('cognome')
        tipo_lavoro = request.GET.get('tipo_lavoro')
        # Aggiungi altri campi di ricerca secondo necessità

        query = Dipendente.objects.all()

        if nome:
            query = query.filter(nome__icontains=nome)
        if cognome:
            query = query.filter(cognome__icontains=cognome)
        if tipo_lavoro:
            query = query.filter(tipo_lavoro__icontains=tipo_lavoro)
        # Aggiungi altri filtri secondo necessità

        dipendenti = query

        context = {
            'dipendenti': dipendenti
        }

        return render(request, 'htmls/lista_dipendenti.html', context)



@csrf_exempt
def dipendente_list(request):
    """
    List all employees, or create a new employee.
    """
    if request.method == 'GET':
        dipendenti = Dipendente.objects.all()
        serializer = DipendenteSerializer(dipendenti, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DipendenteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def dipendente_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        dipendente =Dipendente.objects.get(pk=pk)
    except Dipendente.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DipendenteSerializer(dipendente)
        return JsonResponse(serializer.data)



def domanda(request):
    return render(request, 'htmls/domanda.html')


def chatbot(request):

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_message = request.POST.get('user_message', '')
        #title=request.POST.get('title','')
        user_message+=". Vorrei che mi rispondessi in modo che tu mi possa elencare i ruoli, come se fosse un file csv. Senza ulteriori informazioni, solo elenco dei ruoli. mi raccomando le virgole. non ci devono essere numeri. come risposta voglio solo l'elenco dei ruoli. Senza spazi e senza punti solo virgole che alternano le parole. tutto in minuscolo."
        client = OpenAI(api_key='')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "tu sei l'assistente chatbot per un gestionale."},
                {"role": "user", "content": user_message}
            ]
        )
        print(completion.choices[0].message.content)
        response = str(completion.choices[0].message.content)  # Converti in stringa
        response2=response.replace(".","")
        print(response2)
        response2.replace(" ","")
        #array_of_jobs=response.split(",")
        #print(array_of_jobs)
        new_job_request=JobRequest(nome="Nuovo Lavoro",descrizione=response2,flag_conseguito=False)
        new_job_request.save()



        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'})


def dashboard(request):
    return render(request, 'htmls/dashboard.html')


from django.shortcuts import render
from .models import JobRequest

def proposte(request):
    if not request.user.is_authenticated:
        return render(request, "htmls/login.html")
    else:
        job_list = JobRequest.objects.all()
        print("ciao")
        return render(request, 'htmls/proposte.html', {'job_list': job_list})


def custom_logout(request):
    logout(request)
    # Reindirizza l'utente alla pagina desiderata dopo il logout
    return redirect('login_view')





def modifica_dipendente(request, pk):
    dipendente = get_object_or_404(Dipendente, pk=pk)

    if request.method == 'POST':
        form = DipendenteForm(request.POST, instance=dipendente)
        if form.is_valid():
            form.save()
            # Redirect alla vista che mostra la lista dei dipendenti
            return redirect('ricerca_dipendenti')
    else:
        form = DipendenteForm(instance=dipendente)

    return render(request, 'htmls/modifica_dipendente.html', {'form': form})


def aggiungi_dipendente(request):
    if Dipendente.objects.get(username=request.user).amministratore or Dipendente.objects.get(username=request.user).risorse_umane:
        if request.method == 'POST':
            form = DipendenteForm(request.POST)
            if form.is_valid():
                dipendente = form.save(commit=False)
                # Assicurati che l'utente sia autenticato come amministratore prima di aggiungere un dipendente
                if request.user.is_authenticated and request.user.is_superuser:
                    dipendente.save()
                    return redirect('ricerca_dipendenti')
                else:
                    return render(request, 'errore_permessi.html')
        else:
            form = DipendenteForm()
        return render(request, 'htmls/aggiungi_dipendente.html', {'form': form})
    else :
        return render(request, "htmls/vuoto.html")
