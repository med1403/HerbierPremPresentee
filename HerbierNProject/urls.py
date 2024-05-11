"""
URL configuration for HerbierNProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from HerbierNApp.views import *
from HerbierNProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil/<int:id>/<str:libele>', accueil, name="accueil"),  # le paramètre name est util, parce que c'est le name là qu'on doit utiliser dans les liens dans les template
    path('details_cat/<str:category>/<int:id>', details_cat, name="details_cat"),
    path('details/<str:nom_class>', details, name="details"),
    path('modification/<int:id>/<str:nom_class>', modification, name="modification_classe"),
    path('modification_in_cat/<int:id>/<str:category>/<str:nom_class>/', modification_in_cat, name="modification_classe_in_cat"),
    path('supprimer/<str:nom_class>/<int:id>', supprimer_classe, name='supprimer_classe'),
    path('supprimer/<str:nom_class>/<str:category>', supprimer_classe_in_category, name='supprimer_classe'),
    path('',  index, name="index"),
    path('index2/<int:id>',  index2, name="indextwo"),
    path('ajout_classe/<int:id>', formualaire_ajout, name="ajout_classe"),
    path('ajout_classe_in_cat/<int:id>/<str:category>/<str:localite>', formualaire_ajout_in_cat, name="ajout_classe_in_cat"),
    #path('connexion/<int:id>/<str:category>', connexion, name="connexion"),
    path('Deconnexion/<int:id>/<str:category>', deconnexion, name="Deconnexion"),
    path('view_cat_items/<str:category>/<int:localite>',view_cat_items, name="view_cat_items")
    
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
