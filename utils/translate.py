""" This module contains functions for translating text using DeepL Translate API. """
import os
import deepl
from .countries import languages_with_flags


def deepl_translate_query(text, input_lang):
    """
    Translates text using DeepL Translate API.

    Args:
        text (str): The text to translate.
        input_lang (str): The language to be translated to.

    Returns:
        str: The translated text.
    """
    auth_key = os.getenv("DEEPL_API_KEY")  # Replace with your key
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text,
        target_lang=languages_with_flags[input_lang].upper()
        if input_lang != "English"
        else "EN-GB",
    )
    return result.text
