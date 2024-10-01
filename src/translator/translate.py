from googletrans import Translator
from .languages import LANGUAGES

def translate_text(text, target_lang):
    """
    Translates text into the specified target language.

    Args:
        text (str): The text to be translated.
        target_lang (str): The target language code (e.g., 'en', 'pt').

    Returns:
        str: Translated text or error message.
    """
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Error during translation: {str(e)}"
