import argostranslate.translate
from func_model import split_text, show_progress
from classes import StringListIterator
from typing import Any


def advance_progress_bar(i: int, j: int, translate_progress_bar: Any) -> None:
    """_summary_
    advancing the progress bar every ten iterations
    Args:
        i (int): keeps track of the iterations
        j (int): the value the progress bar should show, resets every 100 iterations
    """
    
    i += 1
    if j == 10:
        j = 0
    if i % 10 == 0:
        j += 1
        show_progress(j,"",translate_progress_bar, False)


def translate(sentence: str, language: str) -> str:
    """_summary_
    calls the argostranslate model to translate the text
    Args:
        sentence (str): the text that will be translated
        language (str): which language the text is

    Returns:
        str: the translated text
    """
    
    if language != "en":
        sentence = argostranslate.translate.translate(sentence, language, "en")


    return (argostranslate.translate.translate(sentence, "en", "he"))

def middleman(text: str, translate_progress_bar : Any, language: str) -> str:
    """
    splitting the text into iterator by calling the function split_text and creating an
    StringListIterator class instance by using the returned list. translating the
    text by using the model
    :param text: str, the file's text
    :return:
    str, the translated text
    """
    
    text_iterator = StringListIterator(split_text(text, 600))
    i = 0
    j = 0
    final_text = ""
    
    for sentence in text_iterator:
        
        final_text += mini_translate(sentence, language)

        advance_progress_bar(i,j, translate_progress_bar)
        
    return final_text

