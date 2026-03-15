import streamlit as st
import requests

# TMDB API key
API_KEY = "YOUR_API_KEY"

# sample movie list
movies = [
    "Avatar",
    "Titanic",
    "The Dark Knight",
    "Avengers",
    "Inception",
    "Interstellar",
    "Joker",
    "Frozen",
    "Spider-Man",
    "Iron Man"
]


# function to fetch movie poster
def fetch_poster(movie):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie
    }

    data = requests.get(url, params=params).json()

    if data["results"]:
        poster_path = data["results"][0]["poster_path"]
        return "https://image.tmdb.org/t/p/w500/" + poster_path

    return None


# recommend movies
def recommend(movie):

    recommendations = []

    for m in movies:
        if m != movie:
            recommendations.append(m)

    return recommendations[:5]


# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Choose a movie", movies)

if st.button("Recommend"):

    names = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(len(names)):

        with cols[i]:

            poster = fetch_poster(names[i])

            if poster:
                st.image(poster)

            st.write(names[i])
