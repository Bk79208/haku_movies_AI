import pickle
import streamlit as st
import requests
import random

from src.recommend import recommend, recommendFromGenres
from src.rec_gen import rec_by_genre

error_shown = False

movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

def switch_case(value):
    
    if value == "Movies":
        
        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            rec_names,rec_posters,rec_genres = recommend(selected_movie)
            
            if len(rec_names) == 0:
                    st.info("No movies found in this genre.")
                    
            cols = st.columns(len(rec_names))

            for idx, (name, poster) in enumerate(zip(rec_names, rec_posters)):
                with cols[idx]:
                    st.image(poster, caption=name, use_container_width=True)      
                    st.text(rec_genres[4])

    elif value == "Genres":
        
            genres_list = movie_genres['genre'].values
            # genres_list = movie_genres.get('genres', [movie_genres['genre']])
            selected_genre = st.selectbox(
                "Type or select a genre from the dropdown",
                genres_list
            )

            if st.button('Show Recommendation'):
                
                rec_by_genre(selected_genre)
                # st.rerun()
                     


# Handling the selection
def rec():
    value = st.selectbox(
        "Recommendation form Movies or Genres",
        ['Movies', 'Genres']
    )
    result = switch_case(value)
    st.write(result)



