import requests
import streamlit as st
import os
from dotenv import load_dotenv
import pickle

load_dotenv()
OMDb_API = os.getenv("OMDb_API")

movies = pickle.load(open('models/movie_list.pkl','rb'))
movies['genre'] = movies['genre'].apply(lambda x: x.replace(' ', ', '))
similarity = pickle.load(open('models/similarity.pkl','rb'))
movie_genres = pickle.load(open('models/genres_list.pkl','rb'))

def fetch_poster(movie_title):
    try:
        poster = movies["poster_link"]  # <-- Correct key
        if poster and poster != "N/A":
            return poster
        else:
            st.warning(f"No valid poster available for '{movie_title}'")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error while fetching poster: {e}")
        return None
