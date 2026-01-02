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
    month_options = ["all", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selectedmonth = st.selectbox("filter by month", month_options)
    collection = connector.fetch_collection(username)
    #adding existing json to dictionary list
    total = 0 #getting total of each json
    fetched_json = connector.get_json_from_collection(collection)
    for json in fetched_json:
        print(json)
        print("\n")
        frame = pd.DataFrame.from_dict(json)
        frame = frame.drop('_id', axis=1)
        frame["date"] = pd.to_datetime(frame["date"], format='%Y-%m-%d')
        frame.sort_values(by="date", inplace=True)
        frame["month"] = frame["date"].dt.month_name()
        if selectedmonth == "all":
            total += json["total"]
        if frame["month"].iloc[0] == selectedmonth:
            total += json["total"]
        dataframes.append(frame)
    
    #combine frames
    if len(dataframes) != 0:
        combinedFrame = pd.concat(dataframes)
        if(selectedmonth == "all"):   
            st.dataframe(combinedFrame)
        else:
            combinedFrame = combinedFrame[combinedFrame["month"] == selectedmonth]
            st.dataframe(combinedFrame)

    return total
