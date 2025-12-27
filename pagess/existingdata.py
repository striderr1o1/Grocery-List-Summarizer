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
database = client["lists"]

def GetCollection(username):
    if(username == "Noman"):
        collection = database["baba"]
    else:
        collection = database["mustafa"]
    return collection

def ShowExistingData():
    dataframes = []
    username = st.selectbox("Who's data do you wish to see?", ("Mustafa", "Noman"))
    collection = GetCollection(username)
    #adding existing json to dictionary list
    total = 0 #getting total of each json
    for json in collection.find():
        total += json["total"]
        print(json)
        print("\n")
        frame = pd.DataFrame.from_dict(json)
        frame = frame.drop('_id', axis=1)
        dataframes.append(frame)
        # st.write(frame["date"])
        # st.write(frame)
    
    #combine frames
    if len(dataframes) != 0:
        combinedFrame = pd.concat(dataframes)
        st.dataframe(combinedFrame)
                
    return total
