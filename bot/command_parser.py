import spacy
from functools import reduce
from spacy.symbols import nsubj, dobj, VERB

nlp = spacy.load('en_core_web_sm')

def parse_command(text):
    doc = nlp(str(text))
    objs = filter(lambda x: x.dep == dobj and x.head.pos == VERB, doc)
    result_commands = list(map(lambda x: (x.head, x), objs))

    # result_commands = []
    # for possible_object in doc:
    #     if possible_object.dep == dobj and possible_object.head.pos == VERB:
    #         result_commands.append((possible_object.head, possible_object))

    return result_commands
