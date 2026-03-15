import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# load dataset
movies = pd.read_csv("movies.csv")

# combine important features
movies['tags'] = movies['title']

# convert text to vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# compute similarity
similarity = cosine_similarity(vectors)

# save similarity matrix
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("similarity.pkl created successfully")
