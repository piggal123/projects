# projects

**project Image_Caption:**

the code sends a request to relativity server to download images, then iterates over them
to get a caption using a model from transformers (https://huggingface.co/Salesforce/blip-image-captioning-large). 
After generating a caption, the text is translated to hebrew by using another model from
transformers (https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-he-en). Afterwards, the text
is sent to the server to be saved and looked at later.


**project Translator:**

the code sends a request to relativity server to retrieve text. The code is using two translate
models, a russian to hebrew one (https://huggingface.co/Helsinki-NLP/opus-mt-ru-he) and arabic to
hebrew one (https://huggingface.co/Helsinki-NLP/opus-mt-ar-he)


**project OCR:**

sending a request to relativity server to download the files, then iterating over them to perform
OCR. the user can control the dpi, psm, if the image should be rotated and if he wants a fast 
(runs once and rotates only 4 times) or a slow and more indepth run (saves the image with higher
dpi, changing the psm if no text was found, rotating up to 8 times). during the OCR, the text
is also going through a check to see if it's a real text or just gibberish. when the proccess
is done, the results are uploaded to relativity
