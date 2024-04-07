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

