import argostranslate.translate
from func_model import split_text, show_progress
from classes import StringListIterator
from typing import Any



def translate(text: str, trans_progress_bar : Any, language: str) -> str:
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
        
        if language != "en":
            translated_to_english = argostranslate.translate.translate(sentence, language, "en")

            translated_to_hebrew = argostranslate.translate.translate(translated_to_english, "en", "he")

        else: 
            translated_to_hebrew = argostranslate.translate.translate(sentence, "en", "he")

        # every ten iterations, advance the progerss bar
        i += 1
        if j == 10:
            j = 0
        if i % 10 == 0:
            j += 1
            show_progress(j,"",trans_progress_bar, False)

        final_text += translated_to_hebrew
        

    return final_text
