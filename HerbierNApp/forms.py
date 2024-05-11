from django import forms
from .models import Menace_Classe,Aire_protege
from django import forms



class Form_classe(forms.ModelForm):
    
    class Meta:
        model = Menace_Classe
        fields = '__all__'
    
        
class Menace_ClasseForm(forms.ModelForm):
    class Meta:
        model = Menace_Classe
        fields = ["nom_class", "zone", "save_date", "cordonnees", "habitat", "description", "score_Risque", "calendar"]
        widgets = {
            'nom_class': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.TextInput(attrs={'class': 'form-control'}),
            'save_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'cordonnees': forms.TextInput(attrs={'class': 'form-control'}),
            'habitat': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'score_Risque': forms.NumberInput(attrs={'class': 'form-control'}),
            'calendar': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    