import pickle
import streamlit as st
import pandas as pd
import requests
import re

# ------------------------------
# Helper: Clean Titles
# ------------------------------
def clean_title(title):
    return re.sub(r'\s*\(.*?\)', '', title).strip()

# ------------------------------
# Fetch Poster from OMDb
# ------------------------------
def fetch_poster_by_title(title):
    api_key = 'b1519bc2'  # ✅ Your working OMDb API key
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('Response') == 'True' and data.get('Poster') and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# ------------------------------
# Recommendation Logic
# ------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    
    for i in movies_list:
        title = movies.iloc[i[0]].title
        cleaned_title = clean_title(title)
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster_by_title(cleaned_title))

    return recommended_movies, recommended_posters

# ------------------------------
# Load Data
# ------------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------------------
# UI Setup
# ------------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #00ccff;'>🎥 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    '📽️ Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('🎯 Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"<h5 style='text-align: center;'>{names[idx]}</h5>", unsafe_allow_html=True)

# ------------------------------
# Footer
# ------------------------------
st.markdown(
    "<hr><p style='text-align:center;'>Made with ❤️ by Aditya</p>",
    unsafe_allow_html=True
)
