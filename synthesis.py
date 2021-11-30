# import necessary libraries
import tensorflow_hub as hub
from sklearn import svm


def get_training_data():
    f = open('training.csv')
    f.readline()

    reviews, categories = [],[]
    for l in f:
        l = l.strip()
        l = l.split(',')
        reviews.append(''.join(l[3:-1]))
        categories.append(l[-1])

    return reviews, categories

def load_USE_embedder():
    # Load pre-trained universal sentence encoder model
    print('loading...')
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    print('done...')

    return embed

def get_model():
    Rs, Cs = get_training_data()
    embed = load_USE_embedder()

    embeddings = [r.numpy() for r in embed(Rs)]

    clf = svm.SVC()
    clf.fit(embeddings, Cs)

    return clf, embed


