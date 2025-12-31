import streamlit as st
from datetime import datetime
from applogic.ingestion import Ingestion
import streamlit as st
from PIL import Image, UnidentifiedImageError
from pymongo.errors import PyMongoError
from json import JSONDecodeError

def uploadPage():
    st.title("Upload Grocery List")

    # File uploader widget
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg"]
    )
    #create dropdown
    username = st.selectbox("Who is using the service?", ("Mustafa", "Noman"))
    # If the user uploads an image
    if uploaded_file is not None:
        # Open it with PIL
        try:
            st.write("Loading:")
            image = Image.open(uploaded_file)
            image.save("./image.jpeg")
            NameOfImage = "image.jpeg"
            ingestionObj = Ingestion(NameOfImage, username)
            cleaned = ingestionObj.extract()
            st.subheader("Cleaned Data:")
            st.write(cleaned)
            classified_data = ingestionObj.ClassifyData()
            classified_data+="\n"
            st.subheader("Classified Data:")
            json_data = ingestionObj.StringToJson()
            st.write(json_data)
            ingestionObj.save_to_db()
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