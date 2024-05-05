# projects

**project Image_Caption:**

the code sends a request to relativity server to download images, then iterates over them
to get a caption using a model from transformers (https://huggingface.co/Salesforce/blip-image-captioning-large). 
After generating a caption, the text is translated to hebrew by using argostranslate
(https://github.com/argosopentech/argos-translate). Afterwards, the text
is sent to the server to be saved and looked at later.


**project Translator:**

the code sends a request to relativity server to retrieve text. the user can choose which language to 
translate from, english, russian or arabic. for the translation, the model argos translate is used
(https://github.com/argosopentech/argos-translate)



**project OCR:**

sending a request to relativity server to download the files, then iterating over them to perform
OCR. the user can control the dpi, psm, if the image should be rotated and if he wants a fast 
(runs once and rotates only 4 times) or a slow and more indepth run (saves the image with higher
dpi, changing the psm if no text was found, rotating up to 8 times). during the OCR, the text
is also going through a check to see if it's a real text or just gibberish. when the proccess
is done, the results are uploaded to relativity
