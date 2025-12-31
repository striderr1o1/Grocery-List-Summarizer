import streamlit as st
import os
from pagess.uploadlist import uploadPage
from pagess.existingdata import ShowExistingData

import streamlit as st
st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Upload", "Data"])

if page == "Upload":
    uploadPage()

elif page == "Data":
    st.title("Existing Data")
    total = ShowExistingData()
    st.write("Approximate Total: ", total)




    