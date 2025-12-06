# Grocery Tracker App - Structure Overview

## 📁 Project Structure

```
FinanceProject/
├── main.py                    # Main entry point with navigation
├── pages/                     # Page modules folder
│   ├── __init__.py           # Makes pages a Python package
│   ├── upload_image.py       # Upload & process grocery images
│   └── chatbot_page.py       # AI chatbot interface
├── classify.py               # Classification logic
├── extraction.py             # Text extraction from images
├── jsonfile.py              # JSON conversion utilities
├── mongoDB_conn.py          # Database connection
└── requirements.txt         # Python dependencies
```

## 🎯 How It Works

### Main Application (`main.py`)
- **Purpose**: Entry point for the multi-page Streamlit app
- **Features**:
  - Sidebar navigation between pages
  - Page routing system
  - App information and branding
- **Key Function**: `main()` - Handles navigation and renders selected page

### Upload Image Page (`pages/upload_image.py`)
- **Purpose**: Upload and process grocery list images
- **Features**:
  - Image upload widget (JPG, JPEG, PNG)
  - Side-by-side display of image and results
  - AI-powered text extraction
  - Item classification
  - MongoDB storage
  - Summary statistics
- **Key Function**: `render_upload_page()` - Renders the complete upload interface
- **Process Flow**:
  1. User uploads image
  2. Extract text using AI (via `extract()`)
  3. Classify items (via `ClassifyData()`)
  4. Convert to JSON (via `StringToJson()`)
  5. Save to database (via `InsertJson()`)
  6. Display results and summary

### Chatbot Page (`pages/chatbot_page.py`)
- **Purpose**: Interactive AI chatbot for grocery assistance
- **Features**:
  - Chat interface with message history
  - Session state management
  - Timestamps for messages
  - Sidebar with settings and quick actions
  - Response creativity slider
  - Example prompts
- **Key Functions**:
  - `render_chatbot_page()` - Renders the chatbot interface
  - `generate_response()` - Generates AI responses (placeholder - needs AI integration)
- **Session State**:
  - `st.session_state.messages` - Stores chat history
  - `st.session_state.quick_prompt` - Handles quick action buttons

## 🔧 Key Features

### Navigation System
- Radio buttons in sidebar for page selection
- Clean routing with exportable render functions
- Consistent branding across pages

### Upload Page Highlights
- **Error Handling**: Comprehensive try-except blocks for:
  - Invalid images
  - JSON parsing errors
  - Database errors
  - Unexpected exceptions
- **UI Components**:
  - Two-column layout
  - Expandable sections for results
  - Progress spinners
  - Success/error messages
  - Metrics and summaries

### Chatbot Highlights
- **Quick Actions**: Pre-defined prompts for common queries
- **Settings**: Adjustable response creativity
- **Chat Features**:
  - Message timestamps
  - Clear history button
  - Example prompts for new users
- **TODO**: Replace `generate_response()` with actual AI model (Gemini, Groq, etc.)

## 🚀 Running the App

```bash
streamlit run main.py
```

## 📝 Next Steps

1. **Integrate AI Model**: Replace placeholder in `chatbot_page.py` with actual AI (Gemini/Groq)
2. **Enhance Chatbot**: Add context awareness, conversation memory
3. **Add More Pages**: Consider adding:
   - Dashboard/Analytics page
   - History/Database viewer
   - Settings page
4. **Improve UI**: Add more styling, animations, or themes
5. **Error Logging**: Implement proper logging system

## 💡 Tips for Development

- Each page is self-contained with its own `render_*()` function
- Session state is used for maintaining state across reruns
- All pages follow consistent styling and error handling patterns
- Comments explain the "why" not just the "what"
