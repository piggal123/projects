import argostranslate.translate
from typing import Any


def translate(text: str) -> str:
    """
    translating the text using argotranslate model
    :param text: str, the file's text
    :return:
    str, the translated text
    """
        
    return(argostranslate.translate.translate(text, "en", "he"))
    
