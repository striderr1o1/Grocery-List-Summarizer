"""
Upload List Image Page
Handles image upload, OCR extraction, classification, and database storage

This module provides the UI and logic for uploading grocery list images,
extracting text using AI, classifying items, and storing them in the database.
"""

from datetime import datetime
from classify import ClassifyData
from extraction import extract
from jsonfile import StringToJson
from mongoDB_conn import InsertJson
import streamlit as st
from PIL import Image, UnidentifiedImageError
from pymongo.errors import PyMongoError
from json import JSONDecodeError


def render_upload_page():
    """
    Render the upload image page for grocery list extraction
    
    This function creates the UI for:
    - Uploading grocery receipt/list images
    - Displaying the uploaded image
    - Extracting text from the image using AI
    - Classifying grocery items
    - Saving data to MongoDB
    - Showing processing results and summaries
    """
    # Page title and description
    st.title("🖼️ Upload Grocery List Image")
    st.markdown("Upload a grocery receipt or list image to extract and classify items automatically.")
    
    # File uploader widget - accepts common image formats
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"],  # Supported image formats
        help="Upload a clear image of your grocery receipt or list"
    )
    
    # Process the uploaded image
    if uploaded_file is not None:
        # Create two columns for side-by-side display
        # col1: Display uploaded image
        # col2: Show processing status and results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📷 Uploaded Image")
            # Open and display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("🔄 Processing")
            
            # Wrap processing in try-except for error handling
            try:
                # Step 1: Extract text from image using AI
                with st.spinner("Extracting text from image..."):
                    # Save the image temporarily for processing
                    image.save("./image.jpeg")
                    NameOfImage = "image.jpeg"
                    
                    # Call extraction function (uses AI/OCR)
                    cleaned = extract(NameOfImage)
                
                st.success("✅ Text extracted successfully!")
                
                # Show extracted text in an expandable section
                with st.expander("📝 Extracted Text", expanded=True):
                    st.text(cleaned)
                
                # Step 2: Classify the extracted data into structured format
                with st.spinner("Classifying grocery items..."):
                    # Classify the data using AI
                    classified_data = ClassifyData(cleaned)
                    classified_data += "\n"
                    
                    # Convert classified string to JSON format
                    json_data = StringToJson(classified_data)
                    
                    # Add current date to the JSON data
                    json_data["date"] = datetime.now().strftime("%Y-%m-%d")
                
                st.success("✅ Items classified successfully!")
                
                # Display the classified data as formatted JSON
                with st.expander("📊 Classified Data", expanded=True):
                    st.json(json_data)
                
                # Step 3: Save to database
                with st.spinner("Saving to database..."):
                    InsertJson(json_data)
                
                st.success("✅ Data saved to database successfully!")
                
                # Step 4: Show summary statistics
                st.subheader("📈 Summary")
                # Display total number of items if available
                if "items" in json_data:
                    st.metric("Total Items", len(json_data["items"]))
                # Display the date
                st.info(f"📅 Date: {json_data.get('date', 'N/A')}")
                
            # Error handling for various exceptions
            except UnidentifiedImageError:
                # Handle invalid image files
                st.error("❌ Error: The uploaded file is not a valid image.")
            except JSONDecodeError:
                # Handle JSON parsing errors
                st.error("❌ Error: Failed to parse the classified data into JSON.")
            except PyMongoError as e:
                # Handle database connection/insertion errors
                st.error(f"❌ Database Error: {e}")
            except Exception as e:
                # Catch-all for unexpected errors
                print("Exception:", e)
                st.error(f"❌ An unexpected error occurred: {e}")
    else:
        # Show instructions when no file is uploaded
        st.info("👆 Please upload an image to get started")
        
        # Provide helpful information about how the process works
        with st.expander("ℹ️ How it works"):
            st.markdown("""
            1. **Upload** a clear image of your grocery receipt or list
            2. **Extract** text using AI Image Extraction
            3. **Classify** items into categories
            4. **Save** the data to your database
            5. **View** your grocery history and insights
            """)
