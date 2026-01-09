import streamlit as st
from applogic.mongoDB_conn import MongoDBConnector
from applogic.processor import process_grocery_data
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

# Instantiate connector globally or inside the function.
# Keeping it here is fine, or we can move it inside.
connector = MongoDBConnector()
class ExistingPageClass:
    mdb_connector = None
    username = ""
    def __init__(self, connector_to_mdb, username):
        self.mdb_connector = connector_to_mdb
        self.username = username
    def get_user_selection(self):
        """
        Handles the UI for selecting the user and filtering criteria.
            
        Returns:
            tuple: (username, selected_month)
        """
        # username = st.selectbox("Who's data do you wish to see?", ("Mustafa", "Noman"))
        username = self.username
        month_options = ["all", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("filter by month", month_options)
        return username, selected_month

    def get_df_with_checkbox(self, combined_df):

        # Add a boolean column for the checkbox
        combined_df["Select"] = False
        edited_df = st.data_editor(
                combined_df,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select this row",
                        default=False,
                    ),
                    "_id":None #to hide the column, later need
                    # to get the id when checkbox clicked
                },
                disabled=list(set(combined_df.columns) - {"Select"}),  # Disable editing for all columns except 'Select'
                hide_index=True,
                key="data_editor"
        )
        return edited_df
    def converting_json_to_df(self, Json):
        json_df = pd.DataFrame.from_dict(Json)
        return json_df

    def ShowExistingData(self):
        """
        Main controller function to display existing grocery data.
        Orchestrates UI inputs, data fetching, processing, and visualization.
        """
        # 1. UI: Get Filters
        username, selected_month = self.get_user_selection()
        
        # 2. Logic: Fetch Data
        collection = self.mdb_connector.fetch_collection(username)
        json_list = self.mdb_connector.get_json_from_collection(collection)
        
        # 3. Logic: Process and Filter Data (delegated to processor module)
        combined_df, total = process_grocery_data(json_list, selected_month)
        
        # 4. UI: Display Results
        if combined_df is not None and not combined_df.empty:
            
            
            # Display data with a checkbox column
            edited_df = self.get_df_with_checkbox(combined_df)

            # Check for selected rows
            selected_rows = edited_df[edited_df["Select"]]
            
            if not selected_rows.empty:
                # Iterate through selected rows
                for index, row in selected_rows.iterrows():
                    ID = row["_id"]
                    detailed_list_json = self.mdb_connector.get_detailedList_from_id(ID)
                    dataframe_of_list = self.converting_json_to_df(detailed_list_json)
                    st.write(f"Details for ID {ID}:")
                    st.dataframe(dataframe_of_list)
                #get relevant collection from the database
        else:
            st.info("No data found for the selected criteria.")
    
        return total
# dont drop the ids, just hide them, later fetchh grocery data details based on ID
