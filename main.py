# Add current date to the JSON data
from datetime import datetime
from classify import ClassifyData
from extraction import extract
from jsonfile import StringToJson
from mongoDB_conn import InsertJson
import streamlit as st
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from pymongo.errors import PyMongoError
from json import JSONDecodeError

import os
# Title of the app
st.title("🖼️ Image Upload Demo")

# File uploader widget
uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg"]
)

# If the user uploads an image
if uploaded_file is not None:
    # Open it with PIL
    try:
        st.write("Loading:")
        image = Image.open(uploaded_file)
        image.save("./image.jpeg")
        NameOfImage = "image.jpeg"
        cleaned = extract(NameOfImage)
        st.subheader("Cleaned Data:")
        st.write(cleaned)
        classified_data = ClassifyData(cleaned)
        classified_data+="\n"
        st.subheader("Classified Data:")
        json_data = StringToJson(classified_data)
        
        json_data["date"] = datetime.now().strftime("%Y-%m-%d")
        
        st.write(json_data)
        InsertJson(json_data)
        st.write("Saved To Database!")
        
    except UnidentifiedImageError:
        st.error("Error: The uploaded file is not a valid image.")
    except JSONDecodeError:
        st.error("Error: Failed to parse the classified data into JSON.")
    except PyMongoError as e:
        st.error(f"Database Error: {e}")
    except Exception as e:
        print("Exception: :", e)
        st.error(f"An unexpected error occurred: {e}")
    