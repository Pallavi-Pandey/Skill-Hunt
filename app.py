"""
TalentScout Hiring Assistant Chatbot
A Streamlit-based intelligent chatbot for initial candidate screening.
"""

import streamlit as st
import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

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
        st.session_state.candidate_info = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None
        }
        st.session_state.info_collected = False
        st.session_state.questions_asked = False
        st.session_state.conversation_ended = False
        
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


def extract_candidate_info(conversation_history):
    """
    Use LLM to extract structured candidate information from conversation.
    This is a fallback mechanism to ensure we capture all information.
    """
    extraction_prompt = """Based on the following conversation, extract the candidate information in JSON format.
If information is not provided, use null for that field.

Required fields:
- name (Full Name)
- email (Email Address)
- phone (Phone Number)
- experience (Years of Experience)
- position (Desired Position)
- location (Current Location)
- tech_stack (Technologies, frameworks, languages, tools as a list)

Return ONLY valid JSON, nothing else.

Conversation:
"""
    
    conv_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": extraction_prompt},
                {"role": "user", "content": conv_text}
            ],
            temperature=0.3
        )
        
        extracted = json.loads(response.choices[0].message.content)
        return extracted
    except Exception as e:
        st.error(f"Error extracting information: {str(e)}")
        return None


def get_bot_response(user_message):
    """Get response from the chatbot using OpenAI API."""
    
    # Check if API key is configured
    if not openai.api_key:
        return "⚠️ OpenAI API key is not configured. Please set up your API key in the .env file."
    
    try:
        # Prepare conversation history for API call
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in st.session_state.messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    except openai.error.AuthenticationError:
        return "⚠️ Authentication error. Please check your OpenAI API key."
    except openai.error.RateLimitError:
        return "⚠️ Rate limit reached. Please try again in a moment."
    except openai.error.APIError as e:
        return f"⚠️ OpenAI API error: {str(e)}"
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"


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
            
            # Get bot response
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
        if openai.api_key:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Key Missing")
            st.info("Please configure your OpenAI API key in the .env file.")
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Powered by:** OpenAI GPT")


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
