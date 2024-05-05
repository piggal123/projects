from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


class CaptionModel:

    def __init__(self, model_name: str):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def caption_image(self, file_path: str) -> str:
        """
        generating a caption for the image, using the model
        args:
            :param file_path str: the file path
        return:
        str: the image caption
        """
        raw_image = Image.open(file_path)

        inputs = self.processor(raw_image, return_tensors="pt")

        out = self.model.generate(**inputs)

        return self.processor.decode(out[0], skip_special_tokens=True)
