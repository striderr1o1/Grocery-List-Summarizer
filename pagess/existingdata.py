import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure
# from jsonfile import StringToJson
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["Grocery"]
collection = database["items_data"]

def ShowExistingData():
    dataframes = []
    #adding existing json to dictionary list
    for json in collection.find():
        frame = pd.DataFrame.from_dict(json)
        dataframes.append(frame)
        frame = frame.drop('_id', axis=1)
        st.write(frame)
    return
