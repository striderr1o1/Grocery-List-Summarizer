import streamlit as st
from datetime import datetime
from applogic.ingestion import Ingestion
import streamlit as st
from PIL import Image, UnidentifiedImageError
from pymongo.errors import PyMongoError
from json import JSONDecodeError

class ListProcessingPage:
    uploaded_file = None
    ingestionObj = None
    username = ""
    db_connector = None
    def __init__(self, dbconnector):
        self.db_connector = dbconnector
        self.uploadPage()
        
        

    def Image_Processing(self):
        st.write("Loading:")
        image = Image.open(self.uploaded_file)
        image.save("./image.jpeg")
        NameOfImage = "image.jpeg"
        self.ingestionObj = Ingestion(NameOfImage, self.username, self.db_connector)
        cleaned = self.ingestionObj.extract()
        st.subheader("Cleaned Data:")
        st.write(cleaned)
        classified_data = self.ingestionObj.ClassifyData()
        classified_data+="\n"
        st.subheader("Classified Data:")
        json_data = self.ingestionObj.StringToJson()
        st.write(json_data)
        self.ingestionObj.save_to_db()
        st.write("Saved To Database!")
    
    
    def uploadPage(self):
        st.title("Upload Grocery List")
    
        # File uploader widget
        self.uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg"]
        )
        #create dropdown
        self.username = st.selectbox("Who is using the service?", ("Mustafa", "Noman"))
        # If the user uploads an image
        if self.uploaded_file is not None:
            # Open it with PIL
            try:
                self.Image_Processing()
                
            except UnidentifiedImageError:
                st.error("Error: The uploaded file is not a valid image.")
            except JSONDecodeError:
                st.error("Error: Failed to parse the classified data into JSON.")
            except PyMongoError as e:
                st.error(f"Database Error: {e}")
            except Exception as e:
                print("Exception: :", e)
                st.error(f"An unexpected error occurred: {e}")