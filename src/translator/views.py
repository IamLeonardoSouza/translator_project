import speech_recognition as sr
from django.shortcuts import render
from .translate import translate_text
from .forms import TradutorForm


def tradutor_view(request):
    resultado = None
    if request.method == 'POST':
        form = TradutorForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            audio = form.cleaned_data.get('audio')
            idioma_destino = form.cleaned_data['idioma_destino']

            if audio:
                recognizer = sr.Recognizer()
                audio_file = sr.AudioFile(audio)
                with audio_file as source:
                    audio_data = recognizer.record(source)
                texto = recognizer.recognize_google(audio_data, language='pt-BR')

            if texto:
                resultado = translate_text(texto, idioma_destino)

    else:
        form = TradutorForm()
    
    return render(request, 'translator.html', {'form': form, 'resultado': resultado})
