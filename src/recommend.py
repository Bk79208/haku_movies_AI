import pickle
import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()
OMDb_API = os.getenv("OMDb_API")

movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

# def fetch_poster(movie_title):
    # poster = movies["poster_link"]  # <-- Correct key
    # if poster and poster != "N/A":
    #     return poster
    # else:
    #     st.warning(f"No valid poster available for '{movie_title}'")
    #     return None

error_shown = False
def fetch_poster(movie_id):
    global error_shown
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url)
        data.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = data.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.exceptions.ConnectionError:
        if not error_shown:
            st.error("No internet connection at present. Unable to fetch images.")
            error_shown = True  # Set the flag to True after showing the error
        return "https://via.placeholder.com/150"  # Return a placeholder image URL
    except requests.exceptions.RequestException as e:
        if not error_shown:
            st.error(f"An error occurred while fetching the images: {e}")
            error_shown = True  # Set the flag to True after showing the error
        return "https://via.placeholder.com/150"  # Return a placeholder image URL

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    # recommended_movie_tag = []
    recommended_movie_genres = []

    for i in distances[1:6]:
           
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_genres.append(movies.iloc[i[0]].genre)

    return recommended_movie_names,recommended_movie_genres,recommended_movie_posters

def recommendFromGenres(genre):
    index = movies[movies['genres'] == genre].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    # recommended_movie_tag = []
    # recommended_movie_genres = []

    # for i in distances[1:6]:
    for i in random.sample(distances[1:20], 5):
        
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        # recommended_movie_tag.append(movies.iloc[i[0]].tags)
        # recommended_movie_genres.append(movies.iloc[i[0]].genre)
        # recommended_movie_posters.append(fetch_poster(recommended_movie_names))

    return recommended_movie_names,recommended_movie_posters#,recommended_movie_genres

