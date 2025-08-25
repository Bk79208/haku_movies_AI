import streamlit as st
# import requests
import pickle

from src.recommend import recommendFromGenres

# Load movie data from pickle
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

genres = movie_genres["genre"].unique()

def main():
    st.title("🎥 Movies Collection")

    genres = movie_genres["genre"].unique()  # check if column is "genres" not "genre"
    # selected_genres = ['Action', 'Comedy', 'Romance', 'Horror']

    selected_genres = ['Action']
    for genre in genres:
        if genre in selected_genres:
            st.subheader(genre)

            rec_names, rec_posters = recommendFromGenres(genre)

            if len(rec_names) == 0:
                st.info("No movies found in this genre.")
                continue

            cols = st.columns(len(rec_names))

            for idx, (name, poster) in enumerate(zip(rec_names, rec_posters)):
                with cols[idx]:
                    st.image(poster, caption=name, use_container_width=True)

