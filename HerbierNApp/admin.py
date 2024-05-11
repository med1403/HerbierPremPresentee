
from django.contrib import admin

from HerbierNApp.models import *


# Register your models here.
@admin.register(Aire_protege)
class Aire_protegeAdmin(admin.ModelAdmin):
    list_display = ['nom_air']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["libele"]


@admin.register(Menace_Classe)
class Menace_Classe(admin.ModelAdmin):
    list_display = ("nom_class", "category", "zone", "save_date", "cordonnees", "habitat", "calendar", "score_Risque", "niveau_impact", "type_mesure")
    list_filter = ('nom_classification1', 'nom_classification2')
    search_fields = ("nom_class", "zone")


@admin.register(Messure)
class MessureAdmin(admin.ModelAdmin):
    list_display = ["mesure"]


@admin.register(S_classification1)
class S_classification1Admin(admin.ModelAdmin):
    list_display = ["nom_classification1"]


@admin.register(S_classification2)
class S_classification2Admin(admin.ModelAdmin):
    list_display = ["nom_classification2"]

