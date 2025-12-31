import streamlit as st
from applogic.mongoDB_conn import MongoDBConnector
# from jsonfile import StringToJson
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

connector = MongoDBConnector()
def ShowExistingData():
    dataframes = []
    username = st.selectbox("Who's data do you wish to see?", ("Mustafa", "Noman"))
    collection = connector.fetch_collection(username)
    #adding existing json to dictionary list
    total = 0 #getting total of each json
    for json in collection.find():
        total += json["total"]
        print(json)
        print("\n")
        frame = pd.DataFrame.from_dict(json)
        frame = frame.drop('_id', axis=1)
        frame["date"] = pd.to_datetime(frame["date"], format='%Y-%m-%d')
        frame.sort_values(by="date", inplace=True)
        frame["month"] = frame["date"].dt.month_name()

        
        dataframes.append(frame)
        # st.write(frame["date"])
        # st.write(frame)
    
    #combine frames
    if len(dataframes) != 0:
        combinedFrame = pd.concat(dataframes)
        # combinedFrame["date"] = pd.to_datetime(combinedFrame["date"], format='%Y-%m-%d').dt.date
        # combinedFrame.sort_values(by="date", inplace=True)
        st.dataframe(combinedFrame)

    return total
