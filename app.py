import streamlit as st
# import sqlite3
import mysql.connector
# import requests
import pickle

from src.recommend import recommendFromGenres
from src.main import main
from src.Chat_box2 import chatbox

# Load movie data from pickle
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

# Clean the column names
# movies.columns = movies.columns.str.strip().str.lower()

# Print to debug
# st.write("Columns:", movies.columns.tolist())

# Should now work
# genres = movie_genres["genre"].unique()



# Connect to MySQL
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",      # or 127.0.0.1
#         user="root",           # your MySQL username
#         password="123456",  # your MySQL password
#         database="users"   # your database name
#     )

# def validate_user(username, password):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE username=%s AND passwords=%s", (username, password))
#     result = cursor.fetchone()
#     conn.close()
#     return result is not None


# # def get_movies_by_genre(genre):
# #     return movies[movies["genre"] == genre].to_dict(orient="records")
# # def get_movies_by_genre(genre):
# #     return movies[movies["genre"].apply(lambda g: genre in g)].to_dict(orient="records")

# # --- LOGIN PAGE ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     st.title("🎬 Movie Login")
#     user = st.text_input("Username")
#     pwd = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if validate_user(user, pwd):
#             st.session_state.logged_in = True
#             st.success("Login successful")
#             st.rerun()
#         else:
#             st.error("Invalid login")
# else:
#     # --- MAIN PAGE ---
    # main()

    # chatbox()

tab1, tab2 = st.tabs(["🎬 Movies Collection", "💬 Chat Assistant"])

with tab1:
    main()

with tab2:
    chatbox()