import speech_recognition as sr
from translate import translate_text  # Importa sua função de tradução
from .languages import LANGUAGES

def record_audio():
    """
    Grava áudio e retorna o texto reconhecido.

    Returns:
        str: Texto reconhecido ou mensagem de erro.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando o microfone... Fale agora!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Reconhecendo...")
        text = recognizer.recognize_google(audio, language='pt-BR')  # Você pode ajustar o idioma aqui
        return text
    except sr.UnknownValueError:
        return "Não consegui entender o áudio"
    except sr.RequestError as e:
        return f"Erro ao se conectar ao serviço de reconhecimento: {e}"

def translate_audio(target_lang):
    """
    Grava um áudio e traduz o texto reconhecido.

    Args:
        target_lang (str): Código do idioma de destino.

    Returns:
        str: Texto traduzido ou mensagem de erro.
    """
    recognized_text = record_audio()
    if "não consegui entender" in recognized_text.lower():
        return recognized_text

    translated_text = translate_text(recognized_text, target_lang)
    return translated_text
