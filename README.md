# projects

**project ocr:**

the code pulls files from the data base, saving them as pdf whenever they are pdf or images. 
after saving them locally, iterating through them and converting them to images the code
extracts the text from them. the text is then uploaded to the data base and the files are
deleted locally

**project transcription:**
the code pulls files from the data base, saving them locally and then sending them to another system
for transcription. the code receives the text from the other system, updating the data base with it
and delete the files locally


**project grading files:**

the code gets a list of words from an excel file and search for them in text files. each word have a score which the user decides upon in the excel file.
the end result is an excel file with two tabs, one shows file name, file score, the average of score, amount of words that were found and the 10 most frequent words 
that were found. the second tab shows all the words that appeared, their score, the type of the word (was it global or specific to this case), the amount of times 
the word appeared, and the file it was found at. 


**project networkgraph:**

the code gets an excel file with phone calls detalies. the end result is web which contains a network graph of the phone calls' participants that shows the 
connections between them. each company have a color to help to distinguish from the other companies, each node have the information of the phone call participant
which includes his name and the company he is from. each edge contains how long the conversation last and which one made the call. the web have buttons which allow
the user to change the graph. the user can change the graph based on the caller, receiver, date of the call, type of the graph (whenever it's the normal view or 
girvan_newman one which divides them into communities). the user can also choose another excel file to receieve a graph for it as well, replacing the old one.


**project NER**:

the code iterates through files, searching for NER. the end result is an excel file with the file name, type of the NER and the text of the NER itself. 
