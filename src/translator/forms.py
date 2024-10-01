from django import forms
from .languages import LANGUAGES

class TradutorForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-textarea mt-1 block w-full',
        'placeholder': 'Digite o texto para traduzir...'
    }))
    idioma_destino = forms.ChoiceField(choices=[(key, value) for key, value in LANGUAGES.items()])
