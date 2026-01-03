import streamlit as st
import os
from applogic.mongoDB_conn import MongoDBConnector
from pagess.existingdata import ExistingPageClass
from pagess.uploadlist import ListProcessingPage
import streamlit as st

database_connector = MongoDBConnector()

st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload", "Data"])

if page == "Upload":
    list_Processing_page = ListProcessingPage(database_connector)

elif page == "Data":
    st.title("Existing Data")
    existingpage = ExistingPageClass(database_connector)
    total = existingpage.ShowExistingData()
    st.write("Approximate Total: ", total)


# one db connector that is being passed to both pages and their classes, and the classes
# within those classes