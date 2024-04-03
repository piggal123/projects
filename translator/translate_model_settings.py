from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from func_model import split_text
from classes import StringListIterator
import torch


class Translator:

    def __init__(self, model_name):
        self.model_name = model_name
        local_model_path = model_name + "_model"

        local_model = AutoModelForSeq2SeqLM.from_pretrained(local_model_path)
        local_tokenizer = AutoTokenizer.from_pretrained(local_model_path)

        self.pipe = pipeline("translation", model=local_model, tokenizer=local_tokenizer)

    def translate(self, text: str) -> str:
        """
        splitting the text into iterator by calling the function split_text and creating an
        StringListIterator class instance by using the returned list. translating the
        text by using the model
        :param text: str, the file's text
        :return:
        str, the translated text
        """
        text_iterator = StringListIterator(split_text(text))

        final_text = ""
        for sentence in text_iterator:

            result = self.pipe(sentence)

            if result[0]["translation_text"] == "- Yeah.":
                continue

            final_text += result[0]["translation_text"]

        return final_text

