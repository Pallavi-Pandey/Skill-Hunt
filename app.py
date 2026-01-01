"""
TalentScout Hiring Assistant Chatbot
A Streamlit-based intelligent chatbot for initial candidate screening.
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Conversation ending keywords
ENDING_KEYWORDS = ["goodbye", "bye", "exit", "quit", "end", "stop", "no thanks", "done"]

# System prompt for the chatbot
SYSTEM_PROMPT = """You are a professional Hiring Assistant chatbot for TalentScout, a recruitment agency specializing in technology placements. Your role is to conduct initial candidate screening by:

1. Greeting candidates warmly and explaining your purpose
2. Gathering essential candidate information:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack (programming languages, frameworks, databases, tools)

3. After collecting all information, generate 3-5 relevant technical questions based on their tech stack to assess proficiency.

4. Maintain professional, friendly, and context-aware conversation flow.

5. If the user provides vague or incomplete information, politely ask for clarification.

6. Do NOT deviate from your hiring assistant purpose. If asked about unrelated topics, politely redirect to the screening process.

7. When the user wants to end the conversation (keywords like "goodbye", "bye", "exit", "quit"), thank them and inform about next steps.

Remember: Stay focused on candidate screening, maintain context, and ensure all required information is collected before asking technical questions."""


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_ended = False
        st.session_state.chat = None
        
        # Initialize Gemini chat if API key is available
        if GEMINI_API_KEY:
            model = genai.GenerativeModel(MODEL, system_instruction=SYSTEM_PROMPT)
            st.session_state.chat = model.start_chat(history=[])
        
        # Add greeting message
        greeting = get_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })


def get_greeting():
    """Generate initial greeting message."""
    return """Hello! 👋 Welcome to TalentScout's Hiring Assistant!

I'm here to help with your initial candidate screening for technology positions. I'll gather some essential information about you and then ask a few technical questions based on your expertise.

This should take about 10-15 minutes. Let's get started!

May I have your full name, please?"""


def check_ending_keyword(user_input):
    """Check if user wants to end the conversation."""
    return any(keyword in user_input.lower() for keyword in ENDING_KEYWORDS)


def get_farewell_message():
    """Generate farewell message."""
    return """Thank you for your time! 🎉

Your information has been recorded. Our recruitment team will review your profile and technical responses. You can expect to hear from us within 3-5 business days via email.

If your profile matches our current openings, we'll reach out to schedule a detailed technical interview.

Best of luck with your job search! Feel free to return anytime if you have additional information to share.

Goodbye! 👋"""


def get_bot_response(user_message):
    """Get response from the chatbot using Gemini API."""
    
    # Check if API key is configured
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API key is not configured. Please set up your API key in the .env file."
    
    try:
        # Use the chat session for multi-turn conversation
        if st.session_state.chat is None:
            model = genai.GenerativeModel(MODEL, system_instruction=SYSTEM_PROMPT)
            st.session_state.chat = model.start_chat(history=[])
        
        # Send message and get response
        response = st.session_state.chat.send_message(
            user_message,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        
        return response.text
    
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API Error: {error_msg}")  # Log for debugging
        if "API_KEY" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper() or "INVALID" in error_msg.upper():
            return " Authentication error. Please check your Gemini API key."
        elif "QUOTA" in error_msg.upper():
            return " Quota exceeded. Please check your API usage limits."
        elif "RESOURCE_EXHAUSTED" in error_msg.upper():
            return " Rate limit reached. Please try again in a moment."
        else:
            return f" Gemini API error: {error_msg}"


def display_chat_interface():
    """Display the chat interface."""
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if not st.session_state.conversation_ended:
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Check for ending keywords
            if check_ending_keyword(prompt):
                farewell = get_farewell_message()
                st.session_state.messages.append({"role": "assistant", "content": farewell})
                st.session_state.conversation_ended = True
                
                with st.chat_message("assistant"):
                    st.markdown(farewell)
                st.rerun()
            else:
                # Get bot response only if not ending conversation
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = get_bot_response(prompt)
                        st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    else:
        st.info("Conversation has ended. Refresh the page to start a new conversation.")


def display_sidebar():
    """Display sidebar with information and options."""
    with st.sidebar:
        st.title("🎯 TalentScout")
        st.subheader("Hiring Assistant")
        
        st.markdown("---")
        
        st.markdown("""
        ### About
        This intelligent chatbot assists with initial candidate screening by:
        
        ✅ Collecting candidate information  
        ✅ Generating technical questions  
        ✅ Assessing tech stack proficiency  
        
        ### Tips
        - Be specific about your tech stack
        - Provide complete contact details
        - You can type 'bye' to end anytime
        """)
        
        st.markdown("---")
        
        # Reset conversation button
        if st.button("🔄 Start New Conversation"):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        
        # API Status indicator
        if GEMINI_API_KEY:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Key Missing")
            st.info("Please configure your Gemini API key in the .env file.")
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Powered by:** Google Gemini")


def main():
    """Main application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="TalentScout - Hiring Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .stChatInput {
        border-radius: 0.5rem;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Main title
    st.title("💼 TalentScout Hiring Assistant")
    st.markdown("*Your AI-powered recruitment companion*")
    st.markdown("---")
    
    # Display sidebar
    display_sidebar()
    
    # Display chat interface
    display_chat_interface()


if __name__ == "__main__":
    main()
