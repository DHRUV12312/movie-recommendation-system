import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
