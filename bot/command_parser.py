import spacy
from spacy.symbols import nsubj, dobj, VERB

nlp = spacy.load('en_core_web_sm')

def parse_command(text):
    
    result_commands = []
    
    doc = nlp(str(text))

    for possible_object in doc:
        if possible_object.dep == dobj and possible_object.head.pos == VERB:
            result_commands.append((possible_object.head, possible_object))

    return result_commands