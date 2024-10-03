from django.shortcuts import render
from .forms import AudioUploadForm, AudioRecordForm
import base64
import io
from pydub import AudioSegment
import speech_recognition as sr
from googletrans import Translator
import os
from django.conf import settings 


def translate_audio_view(request):
    upload_form = AudioUploadForm()
    record_form = AudioRecordForm()

    if request.method == 'POST':
        if 'upload_audio' in request.POST:
            upload_form = AudioUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                audio_file = request.FILES['audio_file']
                # Processar o áudio
                translated_text = process_audio_for_translation(audio_file)
                return render(request, 'translator_audio/translator_audio.html', {
                    'upload_form': upload_form,
                    'record_form': record_form,
                    'translated_text': translated_text,
                })

        elif 'record_audio' in request.POST:
            record_form = AudioRecordForm(request.POST)
            if record_form.is_valid():
                recorded_audio = request.POST['recorded_audio']
                # Aqui você pode processar o áudio gravado (que está em Base64)
                translated_text = process_audio_for_translation(recorded_audio)
                return render(request, 'translator_audio/translator_audio.html', {
                    'upload_form': upload_form,
                    'record_form': record_form,
                    'translated_text': translated_text,
                })

    return render(request, 'translator_audio/translator_audio.html', {
        'upload_form': upload_form,
        'record_form': record_form
    })

def process_audio_for_translation(audio_file):
    # Salvar o arquivo de áudio em disco
    audio_path = os.path.join(settings.MEDIA_ROOT, 'media', audio_file.name)
    
    with open(audio_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Converter o conteúdo do áudio em um formato que o SpeechRecognition pode processar
    text = audio_to_text(audio_path)
    
    # Deletar o arquivo após processamento
    os.remove(audio_path)

    if text:
        # Traduzir o texto para o idioma desejado (por exemplo, inglês)
        translated_text = translate_text(text, target_language='en')
        return translated_text
    else:
        return "Não foi possível transcrever o áudio."

def audio_to_text(audio_file):
    # Inicializar o reconhecedor
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # ler o áudio

    try:
        # Usar o Google Web Speech API para reconhecimento
        text = recognizer.recognize_google(audio, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return f"Erro ao se conectar ao serviço de reconhecimento: {e}"

def translate_text(text, target_language='en'):
    # Inicializar o tradutor
    translator = Translator()
    
    # Traduzir o texto
    translated = translator.translate(text, dest=target_language)
    
    return translated.text