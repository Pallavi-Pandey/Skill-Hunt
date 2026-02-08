"""
TalentScout Hiring Assistant Chatbot
A Streamlit-based intelligent chatbot for initial candidate screening.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from llm_service import LLMService
from utils import get_tech_stack_note, save_interview, is_exit_keyword

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

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


def get_client():
    """Get Gemini client."""
    if GEMINI_API_KEY:
        return genai.Client(api_key=GEMINI_API_KEY)
    return None


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation_ended = False
        st.session_state.provider = "gemini"
        
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
    """Get response from the chatbot using specified LLM provider."""
    
    llm_service = LLMService(provider=st.session_state.provider)
    
    if not llm_service.is_available():
        return f"⚠️ {st.session_state.provider.capitalize()} API key is not configured. Please check your .env file."
    
    try:
        # Tech stack steering
        system_note = get_tech_stack_note(user_message)
        
        # Prepare context
        context = []
        for msg in st.session_state.messages:
            context.append({"role": msg["role"], "content": msg["content"]})
        
        if system_note:
            context.append({"role": "system", "content": system_note})
            
        if st.session_state.provider == "gemini":
            from google.genai import types
            client = llm_service.gemini_client
            contents = []
            for msg in context:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))
            
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=500
                )
            )
            return response.text
        else: # groq
            from config import Config
            client = llm_service.groq_client
            messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + context
            
            completion = client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=messages_payload,
                temperature=0.7,
                max_tokens=500,
            )
            return completion.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        return f"⚠️ API error: {error_msg}"


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
            if is_exit_keyword(prompt):
                farewell = get_farewell_message()
                st.session_state.messages.append({"role": "assistant", "content": farewell})
                st.session_state.conversation_ended = True
                
                # Auto-save interview
                save_interview(st.session_state.messages)
                
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
        
        # LLM Provider Selection
        st.session_state.provider = st.selectbox(
            "Select LLM Provider",
            options=["gemini", "groq"],
            index=0 if st.session_state.provider == "gemini" else 1
        )
        
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
        
        # Controls
        st.subheader("Controls")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.conversation_ended = False
            # Re-add greeting
            greeting = get_greeting()
            st.session_state.messages.append({
                "role": "assistant",
                "content": greeting
            })
            st.rerun()
            
        if st.button("💾 Download Transcript"):
            if st.session_state.messages:
                filename = save_interview(st.session_state.messages)
                st.success(f"Saved transcript!")
                with open(filename, "r") as f:
                    st.download_button(
                        label="📥 Click to Download JSON",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="application/json"
                    )
            else:
                st.warning("No chat history to save.")
        
        st.markdown("---")
        
        # API Status indicator
        from config import Config
        if st.session_state.provider == "gemini":
            if Config.GEMINI_API_KEY:
                st.success("✅ Gemini Connected")
            else:
                st.error("❌ Gemini Key Missing")
        else: # groq
            if Config.GROQ_API_KEY:
                st.success("✅ Groq Connected")
            else:
                st.error("❌ Groq Key Missing")
        
        st.markdown("---")
        st.markdown(f"**Model:** `{Config.GEMINI_MODEL if st.session_state.provider == 'gemini' else Config.GROQ_MODEL}`")
        st.markdown(f"**Powered by:** {st.session_state.provider.capitalize()}")


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
