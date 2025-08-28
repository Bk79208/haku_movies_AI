import tensorflow as tf
import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from src.rec_gen import rec_by_genre
import pickle

# Load saved class names
import json
with open("artifacts/class_names.json", "r") as f:
    class_names = json.load(f)

# Cache the model so it's not reloaded every time
@st.cache_resource
def load_my_model():
    return load_model('artifacts/movie_genre_model.h5')
model = load_my_model()

movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))



# Streamlit UI
# st.title("movie genre Prediction")

def image_pre():
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])  

    if uploaded_file is not None:
        image = Image.open(uploaded_file).resize((224, 224))
        st.image(image, caption="Uploaded Image")

        img_array = tf.keras.utils.img_to_array(image.resize((562, 380)))  # width=562, height=380
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # if st.button("Predict"):
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_class = class_names[predicted_index]
        confidence = 100 * predictions[0][predicted_index]

        # st.write("Prediction probabilities:", predictions[0])
        # st.subheader(f"Prediction: {predicted_class} ({confidence:.2f}% confidence)")
        st.subheader(f"Prediction: {predicted_class}")

        genres = movie_genres["genre"].unique()
        selected_genres = [predicted_class]
        for genre in genres:
            if genre.strip().lower() in [g.strip().lower() for g in selected_genres]:
                rec_by_genre(genre)