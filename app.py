import pandas as pd
import streamlit as st
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


API_KEY = "579034084262bc42447e9861942396dd"

def fetch_poster(movie):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie}"
    data = requests.get(url).json()
    poster_path = data["results"][0]["poster_path"]
    return "https://image.tmdb.org/t/p/w500/" + poster_path


# Load dataset
movies = pd.read_csv("movies.csv")

# Clean data
movies['genres'] = movies['genres'].fillna('')
movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

# Vectorization
cv = CountVectorizer()
matrix = cv.fit_transform(movies['genres'])

# Similarity
similarity = cosine_similarity(matrix)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        
    return recommended_movies


# ---------------- UI ---------------- #

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button("Recommend"):
    
    recommendations = recommend(selected_movie)
    
    st.subheader("Recommended Movies:")
    
    for movie in recommendations:
        st.write(movie)
