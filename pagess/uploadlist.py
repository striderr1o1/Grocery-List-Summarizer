import streamlit as st
from datetime import datetime
from applogic.ingestion import Ingestion
import streamlit as st
from PIL import Image, UnidentifiedImageError
from pymongo.errors import PyMongoError
from json import JSONDecodeError
import pandas as pd
class ListProcessingPage:
    uploaded_file = None
    ingestionObj = None
    username = ""
    db_connector = None
    def __init__(self, dbconnector, username):
        self.db_connector = dbconnector
        self.username = username
        self.uploadPage()
        

    def Image_Processing(self):
        st.write("Loading:")
        image = Image.open(self.uploaded_file)
        image.save("./image.jpeg")
        NameOfImage = "image.jpeg"
        self.ingestionObj = Ingestion(NameOfImage, self.username, self.db_connector)
        cleaned, JSON = self.ingestionObj.extract()
        st.write(JSON)
        df = self._converting_json_to_df(cleaned)
        st.subheader("Cleaned Data:")
        st.dataframe(df)
        classified_data = self.ingestionObj.ClassifyData()
        classified_data+="\n"
        st.subheader("Classified Data:")
        json_data = self.ingestionObj.StringToJson()
        df_classified = self._converting_json_to_df(json_data)
        st.dataframe(df_classified)
        self.ingestionObj.save_to_db()
        st.write("Saved To Database!")
    
    def _converting_json_to_df(self, Json):
        json_df = pd.DataFrame.from_dict(Json)
        return json_df
    
    def uploadPage(self):
        st.write(f"Welcome, {self.username}")
        st.title("Upload Grocery List")
    
        # File uploader widget
        self.uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg"]
        )
        #create dropdown
        # self.username = st.session_state["username"]
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
