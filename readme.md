# 🛒 Grocery List Summarizer

A Python-based smart Streamlit web application that extracts, classifies, and summarizes grocery lists from images using Gemini-AI and AI-powered categorization. Built with Python, MongoDB, Groq and Gemini AI.

---

## Features

- **📸 Image Upload & AI-Powered Extraction**: Upload grocery list images (JPG/JPEG) and extract text using Gemini AI
- **🤖 AI-Powered Classification**: Automatically categorizes items into predefined categories using Groq-inference.
- **💾 MongoDB Integration**: Stores classified grocery data with total and date in the database for two users for the time being(Me and my father).
- **📊 Data Visualization**: View and analyze historical grocery data in an interactive, wide-layout DataFrame
- **👥 Multi-User Support**: Separate data tracking for different users (Me and my father at the moment)
- **💰 Automatic Total Calculation**: Computes approximate totals for each user

---

## Project Structure

```
Grocery-List-Summarizer/
├── main.py                    # Main Streamlit application entry point
├── pagess/
│   ├── uploadlist.py         # Upload page logic and image processing
│   └── existingdata.py       # Data retrieval and display functionality + some other stuff
├── uploadingFiles/
│   ├── classify.py           # Groq-based item classification
│   ├── extraction.py         # Gemini AI text extraction
│   ├── jsonfile.py           # JSON related functions
│   └── mongoDB_conn.py       # MongoDB connection and operations
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (MongoDB credentials)
└── sample.json              # Sample data format
```

---

## Technologies Used

- **Frontend**: Streamlit
- **Image Extraction**: Gemini AI
- **Classification/Categorization**: Groq
- **Database**: MongoDB Atlas

---

## Prerequisites

Before running this project, ensure you have:

- MongoDB Atlas account (or local MongoDB instance)
- Google AI API key (for Generative AI)
- Groq API key (for AI-powered categorization)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/striderr1o1/Grocery-List-Summarizer.git
   cd Grocery-List-Summarizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   MONGO_USERNAME=your_mongodb_username
   MONGO_PASSWORD=your_mongodb_password
   GOOGLE_AI_API_KEY=your_google_ai_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Configure MongoDB**
   
   Setup your mongodb atlas account and update the connection string in the .env file. Also change the url and the database and collection names in the main.py file according to your needs.

---

## Usage

1. **Run the application**
   ```bash
   streamlit run main.py
   ```

2. **Navigate the app**
   - **Upload Page**: Upload grocery list images, select user, and process the data
   - **Data Page**: View historical grocery data with approximate totals

3. **Upload Process**
   - Select a user from the dropdown
   - Upload a JPG/JPEG image of your grocery list
   - The app will:
     - Extract text using Gemini AI
     - Classify items into categories using Groq
     - Calculate totals
     - Save to MongoDB

---

## Data Categories

The application classifies grocery items into the following categories:

- 🌶️ **Spices & Seasonings**
- 🍚 **Food Staples**
- 🥜 **Dry Fruits & Seeds**
- 🧴 **Oils, Sauces & Condiments**
- 🧹 **Cleaning & Household**
- 🧴 **Personal Care**

---

## Future Enhancements

> **Note**: This project is actively under development.

---

## License

This project is currently unlicensed. Please contact the repository owner for usage permissions.

---

## Author

**striderr1o1**

- GitHub: [@striderr1o1](https://github.com/striderr1o1)
- Repository: [Grocery-List-Summarizer](https://github.com/striderr1o1/Grocery-List-Summarizer)

---

## Known Issues

- Duplicate date entries in DataFrame display (currently being addressed)
- Limited to JPG/JPEG formats only
- Requires manual user selection (no authentication yet)

---
