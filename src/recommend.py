import pickle
import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()
OMDb_API = os.getenv("OMDb_API")

# @st.cache_resource
# def load_pickle_file(path):
#     with open(path, 'rb') as f:
#         data = pickle.load(f)
#     return data

# similarity = load_pickle_file("artifacts/similarity.pkl")

movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))
# movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

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
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2fdff14628e91a72e96c485e68560394&language=en-US"
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
    rec_names = []
    rec_posters = []
    # rec_tag = []
    rec_genres = []

    for i in distances[1:6]:
           
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        rec_names.append(movies.iloc[i[0]].title)
        rec_posters.append(fetch_poster(movie_id))
        rec_genres.append(movies.iloc[i[0]].genres)

    return rec_names,rec_posters,rec_genres

def recommendFromGenres(genre):
    index = movies[movies['genres'] == genre].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    rec_ids = []
    rec_names = []
    rec_posters = []
    # rec_tag = []
    # rec_genres = []

    # for i in distances[1:6]:
    for i in random.sample(distances[1:20], 5):
        
        movie_id = movies.iloc[i[0]].movie_id
        rec_ids.append(movies.iloc[i[0]].movie_id)
        rec_posters.append(fetch_poster(movie_id))
        rec_names.append(movies.iloc[i[0]].title)
        
        # rec_tag.append(movies.iloc[i[0]].tags)
        # rec_genres.append(movies.iloc[i[0]].genre)
        # rec_posters.append(fetch_poster(rec_names))

    return rec_ids, rec_names, rec_posters#,rec_genres

