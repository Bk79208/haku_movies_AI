import streamlit as st
# import sqlite3
import mysql.connector
# import requests
from src.main import main
from src.Chat_box2 import chatbox
from src.image_predistion import image_pre
from src.rec_name import rec
from src.search_movie import search_movie_detail
# from src.movie import movie_detail

# Load movie data from pickle
# movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
# movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
# movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

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

st.sidebar.subheader("Input Settings")

input_type = st.sidebar.radio("features", ("Main", "Search", "Image", "Chat assistent", "Recommendation"))
if input_type == "Main":
    
    # Movies Collection Section
    # st.header("🎬 Movies Collection")
    main()

    # st.markdown("---")  # horizontal line separator

    # # Chat Assistant Section
    # st.header("💬 K - Your Movie Assistant")
    # chatbox()
if input_type == "Search":
    
    # title = st.text_input('Type the title and press Enter')
    # if st.button('search'):
    #         search_movie_detail(title)
    search_movie_detail()
            

if input_type == "Image":
    image_pre()

if input_type == "Chat assistent":
    chatbox()

if input_type == "Recommendation":
    rec()