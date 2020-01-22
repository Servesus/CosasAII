import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def load():
    path = "steam"
    ds = pd.read_csv(path+"\\game.csv")
    tf = TfidfVectorizer()
    df = ds['tagNames']
    tfidf_matrix = tf.fit_transform(df)

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    results = {}

    count = 0

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['name'][i]) for i in similar_indices]

        results[row['name']] = similar_items[1:]
        count = count + 1
        print("Iteration " + str(count) + " of " + "27077")

    return results