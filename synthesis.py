print('hello world')
import spacy
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('universal_sentence_encoder')
