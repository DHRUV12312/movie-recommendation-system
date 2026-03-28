import pandas as pd
import streamlit as st
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")

movies['genres'] = movies['genres'].fillna('')
movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

cv = CountVectorizer()
matrix = cv.fit_transform(movies['genres'])
similarity = cosine_similarity(matrix)

API_KEY = "579034084262bc42447e9861942396dd"

def fetch_poster(movie):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie}"
    data = requests.get(url).json()
    poster_path = data["results"][0]["poster_path"]
    return "https://image.tmdb.org/t/p/w500/" + poster_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Choose a movie", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    cols = st.columns(5)
    
    for i, movie in enumerate(recommendations):
        with cols[i]:
            poster = fetch_poster(movie)
            st.image(poster)
            st.caption(movie)
