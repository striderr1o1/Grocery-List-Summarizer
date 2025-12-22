import streamlit as st
import os
from pages.uploadlist import uploadPage
from pages.existingdata import ShowExistingData

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload", "Data"])

if page == "Upload":
    uploadPage()

elif page == "Data":
    st.title("Existing Data")
    ShowExistingData()
    

    