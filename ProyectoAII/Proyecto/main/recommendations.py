import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

path = "steam"
ds = pd.read_csv(path+"\\game.csv")

def load():
    tf = TfidfVectorizer()
    df = ds['tagNames']
    tfidf_matrix = tf.fit_transform(df)

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['name'][i]) for i in similar_indices]

        results[row['name']] = similar_items[1:]

    return results