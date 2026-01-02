import streamlit as st
from applogic.mongoDB_conn import MongoDBConnector
from applogic.processor import process_grocery_data
from dotenv import load_dotenv
import os

load_dotenv()

# Instantiate connector globally or inside the function.
# Keeping it here is fine, or we can move it inside.
connector = MongoDBConnector()

def get_user_selection():
    """
    Handles the UI for selecting the user and filtering criteria.
        
    Returns:
        tuple: (username, selected_month)
    """
    username = st.selectbox("Who's data do you wish to see?", ("Mustafa", "Noman"))
    month_options = ["all", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("filter by month", month_options)
    return username, selected_month

def ShowExistingData():
    """
    Main controller function to display existing grocery data.
    Orchestrates UI inputs, data fetching, processing, and visualization.
    """
    # 1. UI: Get Filters
    username, selected_month = get_user_selection()
    
    # 2. Logic: Fetch Data
    collection = connector.fetch_collection(username)
    json_list = connector.get_json_from_collection(collection)
    
    # 3. Logic: Process and Filter Data (delegated to processor module)
    combined_df, total = process_grocery_data(json_list, selected_month)
    
    # 4. UI: Display Results
    if combined_df is not None and not combined_df.empty:
        st.dataframe(combined_df)
    else:
        st.info("No data found for the selected criteria.")

    return total
