"""
Main Streamlit Application
Grocery Tracker and Assistant

This is the entry point for the multi-page Streamlit app.
It handles navigation between different pages and renders the appropriate page based on user selection.
"""

import streamlit as st
from pages.upload_image import render_upload_page
from pages.chatbot_page import render_chatbot_page


# Configure the page settings - must be the first Streamlit command
st.set_page_config(
    page_title="Grocery Tracker & Assistant",  # Browser tab title
    page_icon="🛒",  # Browser tab icon
    layout="wide",  # Use full width of the browser
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# Custom CSS for better styling and visual enhancements
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """
    Main application entry point with page navigation
    
    This function creates a sidebar navigation menu and routes to the appropriate
    page based on user selection. It acts as a router for the multi-page app.
    """
    # Sidebar navigation - contains page selection and app information
    with st.sidebar:
        # App title in sidebar
        st.markdown("# 🛒 Grocery App")
        st.markdown("---")
        
        # Page selection radio buttons
        # User can choose between Upload Image or Chatbot pages
        page = st.radio(
            "Navigation",
            ["📤 Upload List Image", "🤖 Chatbot Assistant"],
            label_visibility="collapsed"  # Hide the "Navigation" label
        )
        
        st.markdown("---")
        
        # App information section - collapsible expander
        with st.expander("ℹ️ About This App"):
            st.markdown("""
            **Grocery Tracker & Assistant** helps you:
            
            - 📸 Extract grocery items from images
            - 🏷️ Classify and organize items
            - 💾 Store data in database
            - 💬 Get AI-powered grocery assistance
            
            Built with Streamlit, OCR, and AI
            """)
        
        st.markdown("---")
        st.caption("© 2025 Grocery Tracker")
    
    # Route to the selected page by calling the appropriate render function
    # Each page is a separate module with its own render function
    if page == "📤 Upload List Image":
        render_upload_page()  # Render the image upload and processing page
    elif page == "🤖 Chatbot Assistant":
        render_chatbot_page()  # Render the chatbot interface page


# Entry point - runs when script is executed directly
if __name__ == "__main__":
    main()