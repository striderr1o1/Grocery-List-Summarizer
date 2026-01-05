import streamlit as st
import os
from applogic.mongoDB_conn import MongoDBConnector
from pagess.existingdata import ExistingPageClass
from pagess.uploadlist import ListProcessingPage
import streamlit as st
from pagess.authpage import require_auth

database_connector = MongoDBConnector()
st.session_state["auth"] = False
st.set_page_config(layout="wide")
# so that it shows the login page before adding other parts of the page
if(st.session_state["auth"]==False):
        require_auth(database_connector)

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload", "Data"])

if page == "Upload":
    if(st.session_state["auth"]==False):
        require_auth(database_connector)
    list_Processing_page = ListProcessingPage(database_connector, st.session_state.user["username"])

elif page == "Data":
    if(st.session_state["auth"]==False):
        require_auth(database_connector)
    st.title("Existing Data")
    existingpage = ExistingPageClass(database_connector, st.session_state.user["username"])
    total = existingpage.ShowExistingData()
    st.write("Approximate Total: ", total)