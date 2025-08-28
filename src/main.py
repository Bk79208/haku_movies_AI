import streamlit as st
# import requests
import pickle

from src.rec_gen import rec_by_genre

# Load movie data from pickle
# movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
# movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

genres = movie_genres["genre"].unique()

def main():
    st.title("🎥 Movies Collection")

    genres = movie_genres["genre"].unique()  # check if column is "genres" not "genre"
    # selected_genres = ['Action', 'Comedy', 'Romance', 'Horror']

    selected_genres = ['Action', 'Comedy']
    for genre in genres:
        if genre in selected_genres:
            # st.subheader(genre)

            rec_by_genre(genre)

