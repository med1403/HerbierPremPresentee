from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Create your models here.
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Case, When


# Create your models here.

# Creation des models

# Création du model pour les Catégories
# Les verbose sont utilisé pour formater l'affichage des noms de catégorie dans la page d'administration
class Aire_protege(models.Model):
    nom_air = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom_air

    class Meta:
        verbose_name = "Aire protegée"
        verbose_name_plural = "Aires protegées"


class Category(models.Model):
    libele = models.CharField(max_length=255, unique=True, primary_key=True)
    image = models.ImageField(upload_to="products_images", blank=True, null=True)

    def __str__(self):
        return f"{self.libele}"

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class S_classification1(models.Model):
    nom_classification1 = models.CharField(max_length=255,blank=True,unique=True)

    def __str__(self):
        return f"{self.nom_classification1}"

    class Meta:
        verbose_name = "Sous-classification 1"
        verbose_name_plural = "Sous-classifications 1"


class S_classification2(models.Model):
    nom_classification2 = models.CharField(max_length=255,unique=True,blank=True)

    def __str__(self):
        return f"{self.nom_classification2}"

    class Meta:
        verbose_name = "Sous-classification 2"
        verbose_name_plural = "Sous-classifications 2"


# Création du model pour les Classes de Menace
class Messure(models.Model):
    mesure = models.TextField(unique=True)
    type_mesure = models.IntegerField(default=1)

    def __str__(self):
        return self.mesure

    class Meta:
        verbose_name = "Mesure d'atténuation"
        verbose_name_plural = "Mesures d'atténuation"


class Menace_Classe(models.Model):
    nom_class = models.CharField(max_length=255, null=True, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_name",to_field="libele")
    save_date = models.DateTimeField(auto_now=False)
    nom_classification1 = models.ForeignKey(S_classification1, on_delete=models.CASCADE, null=True, blank=True)
    nom_classification2 = models.ForeignKey(S_classification2, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.CharField(max_length=255)
    nom_air = models.ForeignKey(Aire_protege, on_delete=models.CASCADE)
    cordonnees = models.CharField(max_length=255)
    habitat = models.CharField(max_length=255)
    description = models.TextField()
    score_Risque = models.IntegerField(default=0)
    calendar = models.IntegerField(default=0)

    def niveau_impact(self, *args, **kwargs):
        niveau = self.score_Risque * self.calendar
        return niveau

    def type_mesure(self):
        if 4 > self.niveau_impact() > 0:
            mesure = 1
        elif 4 <= self.niveau_impact() < 7:
            mesure = 2
        elif 10 > self.niveau_impact() >= 7:
            mesure = 3
        else:
            mesure = 4
        return mesure

    class Meta:
        verbose_name = "Classe de ménace"
        verbose_name_plural = "Classes de ménace"
