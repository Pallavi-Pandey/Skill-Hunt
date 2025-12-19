# 🎯 TalentScout - Intelligent Hiring Assistant Chatbot

An AI-powered chatbot for initial candidate screening and technical assessment, designed for technology recruitment agencies.

## 📋 Project Overview

TalentScout is an intelligent hiring assistant that streamlines the initial candidate screening process by:

- **Gathering Essential Information**: Collects candidate details including name, contact information, experience, desired positions, location, and tech stack
- **Generating Technical Questions**: Creates 3-5 relevant technical questions tailored to each candidate's declared tech stack
- **Maintaining Context**: Ensures coherent and professional conversation flow throughout the screening process
- **Smart Fallback Handling**: Provides meaningful responses to unexpected inputs while staying focused on recruitment tasks
- **Graceful Conversation Ending**: Concludes interactions professionally and informs candidates about next steps

## ✨ Features

### Core Functionality
- ✅ **Professional Greeting**: Welcomes candidates and explains the screening process
- ✅ **Information Collection**: Systematically gathers all required candidate details
- ✅ **Tech Stack Analysis**: Understands diverse technology stacks (languages, frameworks, databases, tools)
- ✅ **Dynamic Question Generation**: Creates relevant technical questions based on candidate's expertise
- ✅ **Context-Aware Responses**: Maintains conversation history and context
- ✅ **Conversation Control**: Recognizes ending keywords (goodbye, bye, exit, quit, etc.)
- ✅ **Professional Exit**: Thanks candidates and explains next steps
- ✅ **Focused Interaction**: Redirects off-topic queries back to screening process

### User Interface
- 🎨 Clean and intuitive Streamlit interface
- 💬 Real-time chat interaction
- 🔄 Easy conversation reset
- 📊 API status indicator
- 📱 Responsive design

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **Frontend Framework**: Streamlit
- **LLM Integration**: OpenAI GPT-3.5-turbo/GPT-4
- **Environment Management**: python-dotenv
- **API**: OpenAI API

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Pallavi-Pandey/Skill-Hunt.git
   cd Skill-Hunt
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   
   Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## 🚀 Usage Guide

### Starting a Conversation

1. Launch the application using `streamlit run app.py`
2. The chatbot will greet you and explain its purpose
3. Follow the prompts to provide your information:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack

### Providing Tech Stack Information

Be specific when listing your technologies. Examples:
- **Programming Languages**: Python, JavaScript, Java, Go
- **Frameworks**: Django, React, Spring Boot, FastAPI
- **Databases**: PostgreSQL, MongoDB, Redis, MySQL
- **Tools**: Docker, Kubernetes, Git, Jenkins

### Answering Technical Questions

After providing all information, the chatbot will generate 3-5 technical questions tailored to your tech stack. Answer them to demonstrate your proficiency.

### Ending the Conversation

You can end the conversation at any time by typing:
- "goodbye"
- "bye"
- "exit"
- "quit"
- "done"
- "no thanks"

The chatbot will thank you and explain the next steps in the recruitment process.

## 🧠 Prompt Engineering

### System Prompt Design

The chatbot uses a carefully crafted system prompt that:

1. **Defines Role & Purpose**: Establishes the bot as a professional hiring assistant for TalentScout
2. **Lists Responsibilities**: Clearly outlines information gathering and question generation tasks
3. **Sets Behavioral Guidelines**: 
   - Maintain professional and friendly tone
   - Stay focused on recruitment
   - Handle incomplete information gracefully
   - Recognize conversation ending signals
4. **Provides Context Management**: Instructs the model to maintain conversation flow

### Prompt Optimization Strategies

- **Clear Instructions**: Specific, actionable directives for the LLM
- **Structured Data Collection**: Systematic approach to gathering information
- **Context Preservation**: Full conversation history sent with each request
- **Temperature Control**: Set to 0.7 for balanced creativity and consistency
- **Token Management**: Limited to 500 tokens per response for concise answers
- **Error Handling**: Graceful degradation when API issues occur

### Tech Stack Question Generation

The prompt instructs the model to:
- Analyze the candidate's declared tech stack
- Generate 3-5 relevant questions per technology
- Ensure questions are appropriately challenging
- Cover both theoretical knowledge and practical application
- Adapt difficulty based on years of experience

## 🏗️ Architecture

### Application Structure

```
Skill-Hunt/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── .env                  # Your API keys (not in git)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Key Components

1. **Session State Management**: Tracks conversation history and candidate information
2. **LLM Integration**: OpenAI API for natural language understanding and generation
3. **Prompt Engineering**: System prompts guide the model's behavior
4. **UI Layer**: Streamlit provides the interactive chat interface
5. **Error Handling**: Comprehensive error catching and user-friendly messages

### Data Flow

```
User Input → Streamlit Interface → Session State → OpenAI API
                                                        ↓
User Display ← Streamlit Interface ← Response Processing ← GPT Model
```

## 🔒 Security & Privacy

### Data Handling
- **No Persistent Storage**: Candidate data exists only in session state
- **Session Isolation**: Each conversation is independent
- **API Security**: API keys stored in environment variables, never in code
- **GDPR Compliance**: No data is permanently stored or shared

### Best Practices
- Never commit `.env` file to version control
- Use environment variables for sensitive configuration
- Implement proper API key rotation
- Consider rate limiting for production use

## 🧪 Testing Recommendations

While this implementation focuses on core functionality, here are testing approaches:

### Manual Testing Checklist
- [ ] Greeting message displays correctly
- [ ] All information fields are collected
- [ ] Various tech stacks generate appropriate questions
- [ ] Ending keywords trigger farewell message
- [ ] Off-topic queries are redirected
- [ ] API errors are handled gracefully
- [ ] UI is responsive and intuitive

### Example Test Cases
1. **Happy Path**: Complete flow from greeting to technical questions
2. **Incomplete Information**: Provide partial details, verify prompts
3. **Diverse Tech Stacks**: Test with Python, Java, JavaScript, Go, etc.
4. **Early Exit**: End conversation before completing all fields
5. **Invalid Inputs**: Random characters, very long messages
6. **API Failures**: Test with invalid API key

## 🚧 Challenges & Solutions

### Challenge 1: Context Management
**Problem**: Maintaining conversation context across multiple exchanges  
**Solution**: 
- Store complete message history in session state
- Send full conversation to API with each request
- Use structured system prompt to guide context awareness

### Challenge 2: Information Extraction
**Problem**: Ensuring all required information is collected  
**Solution**:
- Clear system prompt with explicit checklist
- Sequential information gathering
- Polite follow-up questions for missing data

### Challenge 3: Tech Stack Diversity
**Problem**: Handling wide variety of technologies and frameworks  
**Solution**:
- Open-ended tech stack question
- LLM's broad knowledge base
- Dynamic question generation based on specific technologies mentioned

### Challenge 4: Conversation Control
**Problem**: Knowing when to end the conversation  
**Solution**:
- Predefined ending keywords list
- Check user input before processing
- Graceful farewell message with clear next steps

### Challenge 5: API Reliability
**Problem**: Handling API errors and rate limits  
**Solution**:
- Comprehensive exception handling
- User-friendly error messages
- API status indicator in sidebar

## 🎨 UI/UX Design Decisions

### Color Scheme
- Professional blue tones for trust and authority
- Clear visual hierarchy
- Readable font sizes and spacing

### Layout
- Wide layout for comfortable reading
- Sidebar for controls and information
- Chat interface in main area
- Persistent input at bottom

### User Feedback
- Loading spinner during API calls
- Status indicators for API connection
- Clear visual distinction between user and bot messages

## 📈 Performance Considerations

- **Response Time**: Typically 2-5 seconds per message (depends on OpenAI API)
- **Token Efficiency**: Limited response length to 500 tokens
- **Session Management**: Lightweight state storage
- **Scalability**: Stateless design allows horizontal scaling

## 🔮 Future Enhancements

### Potential Features
- 📊 **Sentiment Analysis**: Gauge candidate emotions during conversation
- 🌍 **Multilingual Support**: Interact in multiple languages
- 💾 **Database Integration**: Store candidate profiles persistently
- 📧 **Email Integration**: Automatic follow-up emails
- 📊 **Analytics Dashboard**: Track screening metrics
- 🎯 **Custom Question Banks**: Pre-defined questions per technology
- 🤖 **Multiple LLM Support**: Support for Llama, Claude, etc.
- 🔐 **Enhanced Security**: OAuth integration, encrypted storage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is created for educational and demonstration purposes.

## 👥 Authors

- **TalentScout Team** - Initial work

## 🙏 Acknowledgments

- OpenAI for GPT API
- Streamlit for the amazing framework
- The open-source community

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check documentation above
- Review OpenAI API documentation

---

**Made with ❤️ for better recruitment experiences**
