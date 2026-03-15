import pandas as pd
import streamlit as st
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "579034084262bc42447e9861942396dd"

movies = pd.read_csv("movies.csv")

movies['genres'] = movies['genres'].fillna('')
movies['genres'] = movies['genres'].str.replace('|', ' ')

cv = CountVectorizer()
matrix = cv.fit_transform(movies['genres'])

similarity = cosine_similarity(matrix)

def fetch_poster(movie):
url = "https://api.themoviedb.org/3/search/movie"
params = {
"api_key": API_KEY,
"query": movie
}

```
data = requests.get(url, params=params).json()

if len(data["results"]) == 0:
    return "https://via.placeholder.com/300x450"

poster_path = data["results"][0]["poster_path"]

if poster_path is None:
    return "https://via.placeholder.com/300x450"

return "https://image.tmdb.org/t/p/w500/" + poster_path
```

def recommend(movie):

```
index = movies[movies['title'] == movie].index[0]
distances = similarity[index]

movies_list = sorted(
    list(enumerate(distances)),
    reverse=True,
    key=lambda x: x[1]
)[1:6]

recommended_movies = []
posters = []

for i in movies_list:
    movie_title = movies.iloc[i[0]].title
    recommended_movies.append(movie_title)
    posters.append(fetch_poster(movie_title))

return recommended_movies, posters
```

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
"Choose a movie",
movies['title'].values
)

if st.button("Recommend"):

```
names, posters = recommend(selected_movie)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image(posters[0])
    st.write(names[0])

with col2:
    st.image(posters[1])
    st.write(names[1])

with col3:
    st.image(posters[2])
    st.write(names[2])

with col4:
    st.image(posters[3])
    st.write(names[3])

with col5:
    st.image(posters[4])
    st.write(names[4])
```
