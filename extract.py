from sqlite3 import connect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
from synthesis import get_model
from spacy import displacy

clf, embed = get_model()

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

def get_phrase(token):
    ans = ''
    for child in token.lefts:
        ans = ans + get_phrase(child) + ' '
    ans = ans + token.text + ' '
    for child in token.rights:
        ans = ans + get_phrase(child) + ' '
    return ans[:-1]

def get_reviews(cursor, verb=False):
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
                X[2] = Y[y + 1]

            #print(X)
            Us, As = [],[]
            for x in X:
                wordsList = nltk.word_tokenize(x)
                wordsList = [w for w in wordsList if not w in stop_words]

                parsed = nlp(x)

                for token in parsed:
                    if str(token.dep_) in ['ROOT', 'advcl']:
                        C = get_phrase(token)
                        x = embed([C])
                        y = clf.predict(x)
                        if y[0] != '0':
                            if y[0] == '1':
                                Us.append(C)
                            else:
                                As.append(C)
                            if verb == True:
                                print("{:<15} | {:<8} | {:<15} | {:<20}".format(str(token.text), str(token.dep_),
                                                                            str(token.head.text),
                                                                            str([child for child in token.children])))
                                print(C)
                                print(y)
                                input()
            if len(Us) > 0 and len(As) > 0:
                print(Us)
                print(As)
                input()
            last = i

        #input()



