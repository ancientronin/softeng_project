from sqlite3 import connect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
from spacy import displacy

#print('downloading...')
#nltk.download()
#print('done')

nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))


'''
('sqlite_sequence',)
('OneStarReviews',)
('Events',)
('EventPairs',)
('ManualLabels',)
'''

KEY_PHRASES = ['after', 'as soon as', 'before', 'every time', 'then', 'until', 'when', 'whenever', 'while']


def contains_key_phrase(sentence):
    for phrase in KEY_PHRASES:
        if phrase in sentence:
            return True
    return False


def get_table_names():
    conn = connect('data.db')
    cursor = conn.cursor()

    q = "select name from sqlite_master where type='table'"
    cursor.execute(q)

    X = cursor.fetchall()
    for x in X:
        print(x)

    conn.close()


def get_reviews(cursor):
    q = 'select * from OneStarReviews'
    cursor.execute(q)

    while True:
        x = cursor.fetchone()
        Y = sent_tokenize(x[4])
        # print(Y)
        
        last = ''
        for y in range(len(Y)):
            i = Y[y]

            if not contains_key_phrase(i):
                last = i
                continue
            
            X = [last, i, '']
            if y < len(Y) - 1:
                X[2] = Y[y+1]

            print(X)
            
            for x in X:
                wordsList = nltk.word_tokenize(x)
                wordsList = [w for w in wordsList if not w in stop_words]
                tagged = nltk.pos_tag(wordsList)
                # print(tagged)

                parsed = nlp(x)
                # print('parsed')
                # print(parsed)

                for token in parsed:
                    if str(token.dep_) in ['ROOT', 'advcl']:
                        print ("{:<15} | {:<8} | {:<15} | {:<20}".format(str(token.text), str(token.dep_), str(token.head.text), str([child for child in token.children])))
                
            last = i 

        input()


conn = connect('data.db')
try:
    cursor = conn.cursor()
    get_reviews(cursor)
    conn.close()
except Exception as e:
    print('Something went wrong...\n\n{}'.format(e))
    conn.close()



print('hello world')

