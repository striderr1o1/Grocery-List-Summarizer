import streamlit as st
import os
from pagess.uploadlist import uploadPage
from pagess.existingdata import ShowExistingData

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload", "Data"])

if page == "Upload":
    uploadPage()

elif page == "Data":
    st.title("Existing Data")
    ShowExistingData()

#add some module that fetches and displays data from mongodb



    