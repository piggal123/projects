from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, ImageFile
from translate_function import translate

# allowing truncated images to be loaded.
ImageFile.LOAD_TRUNCATED_IMAGES = True
# setting the maximum image pixels to 999999999.
Image.MAX_IMAGE_PIXELS = 999999999

class CaptionModel:

    def __init__(self, model_name: str):
        self.processor = BlipProcessor.from_pretrained("C:/projects/ICA_Image_Caption/" +model_name)
        self.model = BlipForConditionalGeneration.from_pretrained("C:/projects/ICA_Image_Caption/" + model_name)

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

        return translate(self.processor.decode(out[0], skip_special_tokens=True))
