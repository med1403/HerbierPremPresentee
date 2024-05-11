from django.shortcuts import render, get_object_or_404,redirect
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import matplotlib
from random import choice
from .models import Messure
from .forms import Form_classe, Menace_ClasseForm
matplotlib.use("Agg")
import plotly.express as px
from django.http import HttpResponse
from io import BytesIO
import base64
from .models import Aire_protege, Category,Menace_Classe
from django.db.models import Q
from datetime import datetime


# Create your views here.


# def connexion(request,id,category):
#     if request.method == 'POST':
#         # connexion de l'utilisateur
#         # recuperation des données du formulaire
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('accueil', id=id)
#         else:
#             context = {"ErroMessage": "Login ou mot de passe Incorrect"}
#             return redirect('details_cat',id=id, category=category)
#     return render(request, 'HerbierNApp/category.html', context)


def deconnexion(request,id,category):
    logout(request)
    return redirect('details_cat',category=category,id=id)


# J'AI AJOUTE LE LIBELE DE LA CATEGORIE EN PARAMETRE DE LA VUE D'ACCEUIL QUI RECUPERERA LE LIBELE DE LA CATEGORIE EN PLUS DE L'ID DE L'AIR PROTEGEE
def accueil(request, id, libele):
    #  localities = Menace_Classe.objects.filter(nom_air=id)
    localite = get_object_or_404(Aire_protege, id=id)
    categorie = get_object_or_404(Category, libele=libele)
    categories = Category.objects.all()

    infos = Menace_Classe.objects.filter(category=libele,nom_air=id)
    context = {"localite": localite, "categories": categories, "infos": infos, 'categorie': categorie}
    return render(request, 'HerbierNApp/accueil.html', context)


# J'AI CREER UNE VUE POUR LA PAGE INDEX 2 QUI VA RECUPERER L'ID DE L'AIRE PROTEGEE
def index2(request, id):
    localite = get_object_or_404(Aire_protege, id=id)
    categories = Category.objects.all()
    context = {'categories': categories, 'localite': localite}
    return render(request, "HerbierNApp/index2.html", context)


def details_cat(request, category, id):

    class_cat = Menace_Classe.objects.filter(Q(category=category) & Q(nom_air=id))
    air= get_object_or_404(Aire_protege,id=id)
    image_cat = get_object_or_404(Category, libele=category)
    # Exemple de création d'un graphique avec Matplotlib
    zones = [item.zone for item in class_cat]
    niveaux_impacts = [item.niveau_impact() for item in class_cat]
    userinput = request.GET.get("userinput")
    if userinput:
        class_cat=Menace_Classe.objects.filter(Q(category=category) & Q(habitat__icontains=userinput) & Q(nom_air=id))
        zones = [item.zone for item in class_cat]
        niveaux_impacts = [item.niveau_impact() for item in class_cat]

    plt.plot(zones, niveaux_impacts, marker='o')
    plt.title('Niveaux d\'impacte en fonctionne des zones')
    plt.xlabel('Zone')
    plt.ylabel('Niveau d\'impacte')

    # Sauvegarde le graphique en mémoire
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convertit l'image en base64 pour l'inclure dans le contexte
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    score_risque = [item.score_Risque for item in class_cat]

    plt.plot(zones, score_risque, marker='o')
    plt.title('Score de risque  en fonctionne des zones')
    plt.xlabel('Zone')
    plt.ylabel('Score de Risque')

    # sauvegarde du graphique
    image_stream1 = BytesIO()
    plt.savefig(image_stream1, format='png')
    plt.close()
    image_base641 = base64.b64encode(image_stream1.getvalue()).decode('utf-8')

    context = {"classes": class_cat, "image_cat": image_cat, "image_base64": image_base64, 'image_base641': image_base641, 'category': category, 'localite': id,"air":air}

    #Gestion de la connexion
    if request.method == 'POST':
        # connexion de l'utilisateur
        # recuperation des données du formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('details_cat', id=id,category=category)
        else:
            context = {"ErroMessage": "Login ou mot de passe Incorrect"}
            return redirect('details_cat',id=id, category=category)

    return render(request, 'HerbierNApp/category.html', context)


def details(request, nom_class):
    object_classe = get_object_or_404(Menace_Classe, nom_class=nom_class)

    if object_classe.score_Risque == 1:
        score = "Très Faible"
    elif object_classe.score_Risque == 2:
        score = "Faible"
    elif object_classe.score_Risque == 3:
        score = "Elevé"
    else:
        score = "Très Elevé"

    if object_classe.calendar == 1:
        calendrier = "Future"
    elif object_classe.calendar == 2:
        calendrier = "Passé"
    else:
        calendrier = "En cours"

    niveau_impact = object_classe.niveau_impact()

    # Récupérer le type_mesure de l'objet
    type_mesure = object_classe.type_mesure()  # Assure-toi que type_mesure est un champ valide dans Menace_Classe

    # Récupérer une mesure aléatoire avec le même type_mesure
    mesures_associated = Messure.objects.filter(type_mesure=type_mesure)
    if(mesures_associated.exists()):
        mesure_aleatoire = choice(mesures_associated)

    else:
        mesure_aleatoire ="Pas de messure enregistrée pour ce type de mesure"
    context = {"calendrier": calendrier, "score": score, "niveau_impact": niveau_impact,
               "mesure": mesure_aleatoire}

    # Traitement
    return render(request, "HerbierNApp/details.html", context)


def modification(request, id, nom_class):
    classe = get_object_or_404(Menace_Classe, nom_class=nom_class)
    id_localite = id
    if request.method == 'POST':
        form = Menace_ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
        return redirect('details_cat', id=id,nom_class=nom_class)
    else:
        form = Menace_ClasseForm(instance=classe)
    context = {'classe': classe, 'form': form, 'id_localite': id_localite}
    return render(request, 'HerbierNApp/modification.html', context)


def modification_in_cat(request,id,category, nom_class):
    classe = get_object_or_404(Menace_Classe, nom_class=nom_class)
    image_cat = get_object_or_404(Category, libele=category)
    if request.method == 'POST':
        form = Menace_ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            return redirect('details_cat', id=id, category=category)
    else:
        form = Menace_ClasseForm(instance=classe)
    context = {'classe': classe, 'form': form, 'image_cat': image_cat}
    return render(request, 'HerbierNApp/modification_in_cat.html', context)


def index(request):
    localities = Aire_protege.objects.all()
    context = {'localities': localities}
    return render(request, "HerbierNApp/index.html", context)





def supprimer_classe(request, nom_class, id):
    classe = get_object_or_404(Menace_Classe, nom_class=nom_class)
    if request.method == 'POST':
        classe.delete()
        return redirect('accueil', id=id)
    else:  # Redirigez vers la liste des classes après la suppression
        return render(request, 'HerbierNApp/supprime.html', {'classe': classe})


def supprimer_classe_in_category(request, nom_class, category):
    classe = get_object_or_404(Menace_Classe, nom_class=nom_class)
    localite = get_object_or_404(Aire_protege,nom_air=classe.nom_air)
    if request.method == 'POST':
        classe.delete()
        return redirect('details_cat',category,localite.id )
    else:  # Redirigez vers la liste des classes après la suppression
        return render(request, 'HerbierNApp/supprime.html', {'classe': classe})


def formualaire_ajout(request, id):
    if request.method == "POST":
        form = Form_classe(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accueil",id=id)
    else:
        form = Form_classe()

    return render(request, "HerbierNApp/formulaire_ajout.html", {"form": form})


def formualaire_ajout_in_cat(request, id, category,localite):

    if request.method == "POST":
        form = Form_classe(request.POST)
        if form.is_valid():
            # Sauvegarde du formulaire avec la catégorie et le nom_air pré-remplis
            instance = form.save(commit=False)
            # Enregistrement de l'instance mise à jour
            instance.save()

            return redirect("details_cat", id=id, category=category)

        # Création du formulaire avec les champs pré-remplis
    form = Form_classe(initial={'category': category, 'nom_air': "Bero", "save_date":datetime.now()})

    return render(request, "HerbierNApp/formulaire_ajout.html", {"form": form})

def view_cat_items(request, localite, category):
    if request.method == 'POST':
        userinput = request.POST.get("userinput")
        if userinput:
            especes_cat = Menace_Classe.objects.filter(nom_air=localite, category=category, habitat__icontains=userinput)
            context = {"contenu": especes_cat}

        else:
            context = {"contenu": "Aucun enregistrement pour votre recherche"}
        return render(request, "HerbierNApp/view_cat_items.html", context)
    else:
        # Traitement pour la méthode GET (s'il y a lieu)
        return render(request, "HerbierNApp/view_cat_items.html", {'contenu': None})
