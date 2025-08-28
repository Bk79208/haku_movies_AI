import streamlit as st
import requests
# from tmdbv3api import TMDb, Movie
from src.recommend import fetch_poster
import os
from dotenv import load_dotenv

import pickle
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))

# title = st.text_input('Type the title and press Enter')
# if title:
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# def Movie_search():
#     movie_list = movies['title'].values
#     selected_movie = st.selectbox(
#         "Type or select a movie from the dropdown",
#         movie_list
#     )
#     if st.button('search'):
#         movie_row = movies[movies['title'] == "Avatar"].iloc[0]

# def search_movie(query):
#     url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         st.error("Error fetching data from TMDB API")
#         return {"results": []}
#     return response.json()

# def search_movie(query):
#     url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         st.error(f"TMDB API error: {response.status_code}")
#         return {"results": []}

#     data = response.json()
#     st.write("🔍 Debug API Response:", data)  # 👈 shows full JSON in Streamlit

#     return data

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    return response.json()

def get_movie_credits(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return {"cast": [], "crew": []}
    return response.json()

# Example usage:
def search_movie_detail():
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )
    # if st.button('search'):
    movie_row = movies[movies['title'] == selected_movie].iloc[0]
    movie_id = movie_row['movie_id']
    # data = search_movie(name)
    # if not data["results"]:  # no movie found
    #     st.error("No movie found with that title.")
    #     return
    # first_movie = data["results"][0]
    # movie_id = first_movie["id"]

    details = get_movie_details(movie_id)
    poster = fetch_poster(movie_id)
# credits (cast + crew)
    credits = get_movie_credits(movie_id)
    cast = [c["name"] for c in credits.get("cast", [])[:5]]  # top 5 cast
    directors = [c["name"] for c in credits.get("crew", []) if c["job"] == "Director"]


    # Layout: Poster on left, info on right
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster, use_container_width=True)
    with col2:
        st.subheader(details.get("title", "Unknown Title"))
        st.caption(f"Release Date: {details.get('release_date', 'N/A')}")
        st.write(details.get("overview", "No overview available."))
        st.text(f"Rating: {details.get('vote_average', 'N/A')} ⭐")
        st.text(f"Director: {', '.join(directors) if directors else 'N/A'}")
        st.text(f"Cast: {', '.join(cast) if cast else 'N/A'}")


