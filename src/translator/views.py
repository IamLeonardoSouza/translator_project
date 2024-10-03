import speech_recognition as sr
from django.shortcuts import render
from .translate import translate_text
from .forms import TradutorForm


def translator_text_view(request):
    resultado = None
    if request.method == 'POST':
        form = TradutorForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            idioma_destino = form.cleaned_data['idioma_destino']

            if texto:
                resultado = translate_text(texto, idioma_destino)

    else:
        form = TradutorForm()
    
    return render(request, 'translator_text/translator_text.html', {'form': form, 'resultado': resultado})
