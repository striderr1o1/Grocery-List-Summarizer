"""
Chatbot Page
Interactive chatbot for grocery-related queries

This module provides an AI-powered chatbot interface for users to ask questions
about groceries, recipes, nutrition, meal planning, and shopping tips.
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()


def generate_response(user_input: str, temperature: float = 0.7) -> str:
    """
    Generate a response to user input.
    TODO: Replace this with actual AI model integration (Gemini, Groq, etc.)
    
    This is a placeholder function that provides basic keyword-based responses.
    You should integrate this with your preferred AI model (Google Gemini, Groq, OpenAI, etc.)
    
    Args:
        user_input: The user's message/question
        temperature: Response creativity level (0.0 to 1.0)
                    Higher values = more creative/random responses
    
    Returns:
        AI-generated response string
    """
    # Convert to lowercase for easier keyword matching
    user_input_lower = user_input.lower()
    
    # Simple keyword-based response logic (replace with actual AI)
    if "recipe" in user_input_lower:
        return "I can suggest recipes! To give you the best recommendations, could you tell me what ingredients you have or what type of cuisine you're interested in?"
    elif "nutrition" in user_input_lower or "healthy" in user_input_lower:
        return "I'd be happy to help with nutritional information! Which food items are you curious about?"
    elif "meal plan" in user_input_lower:
        return "Great! I can help you plan your meals. How many days would you like to plan for, and do you have any dietary preferences or restrictions?"
    elif "shopping" in user_input_lower or "buy" in user_input_lower:
        return "I can help with your shopping list! What items are you looking to purchase, or would you like suggestions based on a meal plan?"
    elif "hello" in user_input_lower or "hi" in user_input_lower:
        return "Hello! 👋 How can I assist you with your grocery needs today?"
    elif "thank" in user_input_lower:
        return "You're welcome! Feel free to ask if you need anything else! 😊"
    else:
        return f"I understand you're asking about: '{user_input}'. Could you provide more details so I can assist you better? I specialize in recipes, nutrition, meal planning, and shopping tips!"


def render_chatbot_page():
    """
    Render the chatbot page for grocery assistance
    
    This function creates the complete chatbot interface including:
    - Chat message history display
    - Message input field
    - Sidebar with settings and quick actions
    - Session state management for conversation history
    """
    # Page title and description
    st.title("🤖 Grocery Assistant Chatbot")
    st.markdown("Ask me anything about your groceries, recipes, or nutrition!")
    
    # Sidebar with additional features and controls
    with st.sidebar:
        st.header("💬 Chat Options")
        
        # Button to clear chat history
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []  # Reset messages
            st.rerun()  # Refresh the page
        
        st.divider()
        
        # Information about chatbot capabilities
        st.header("ℹ️ About")
        st.markdown("""
        This chatbot can help you with:
        - **Recipe Ideas**: Get suggestions based on your ingredients
        - **Nutrition Info**: Learn about nutritional values
        - **Meal Planning**: Plan your weekly meals
        - **Shopping Tips**: Smart grocery shopping advice
        """)
        
        st.divider()
        
        # Settings section
        st.header("🔧 Settings")
        temperature = st.slider(
            "Response Creativity", 
            0.0, 1.0, 0.7, 0.1,
            help="Higher values = more creative responses"
        )
        
        st.divider()
        
        # Quick action buttons for common queries
        st.header("⚡ Quick Actions")
        if st.button("💡 Suggest a recipe", use_container_width=True):
            # Store quick prompt in session state to trigger it
            st.session_state.quick_prompt = "Can you suggest a healthy recipe?"
        if st.button("🥗 Meal plan ideas", use_container_width=True):
            st.session_state.quick_prompt = "Help me plan meals for this week"
        if st.button("🛒 Shopping tips", use_container_width=True):
            st.session_state.quick_prompt = "Give me tips for smart grocery shopping"
    
    # Initialize chat history in session state if it doesn't exist
    # Session state persists across reruns of the app
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add a welcome message to start the conversation
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! 👋 I'm your grocery assistant. I can help you with:\n\n- 🍳 Recipe suggestions based on your groceries\n- 🥗 Nutritional information\n- 📅 Meal planning ideas\n- 🛒 Shopping tips\n\nWhat would you like to know?",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    # Display all chat messages from history
    for message in st.session_state.messages:
        # Create a chat message bubble (user or assistant)
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Show timestamp if available
            if "timestamp" in message:
                st.caption(f"🕐 {message['timestamp']}")
    
    # Handle quick prompts from sidebar buttons
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt  # Remove after using
        
        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Generate and add assistant response
        response = generate_response(prompt, temperature)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        # Rerun to display the new messages
        st.rerun()
    
    # Chat input field at the bottom of the page
    if prompt := st.chat_input("Ask me about groceries..."):
        # Add user message to chat history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕐 {timestamp}")
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Call the response generation function
                response = generate_response(prompt, temperature)
                st.markdown(response)
                response_time = datetime.now().strftime("%H:%M")
                st.caption(f"🕐 {response_time}")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": response_time
        })
        
        # Rerun to update the display
        st.rerun()
    
    # Show example prompts if chat is empty (only welcome message exists)
    if len(st.session_state.messages) <= 1:
        st.markdown("### 💭 Try asking:")
        col1, col2, col3 = st.columns(3)
        
        # Display example questions in three columns
        with col1:
            st.info("🍝 What can I make with pasta and tomatoes?")
        with col2:
            st.info("🥑 Is avocado healthy?")
        with col3:
            st.info("📋 Help me plan a week of meals")
