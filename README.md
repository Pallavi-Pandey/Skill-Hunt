# TalentScout - Intelligent Hiring Assistant 🤖

An AI-powered chatbot for automating initial candidate screening in technology recruitment. Built for TalentScout, a fictional recruitment agency specializing in technology placements.

## 🌟 Features

- **Intelligent Candidate Screening**: Automatically collects essential candidate information
- **Dynamic Technical Questions**: Generates personalized technical questions based on candidate's tech stack
- **Experience-Level Awareness**: Adapts question difficulty based on years of experience (Junior/Mid-level/Senior)
- **AI-Powered Evaluation**: Provides real-time feedback on candidate responses using LLMs
- **Interview Summary**: Generates comprehensive hiring recommendations
- **Data Persistence**: Saves interview data in structured JSON format
- **Offline Mode**: Works without LLM with preset questions when API key is not configured

## 🛠️ Technologies Used

- **Python 3.7+**: Core programming language
- **OpenAI API**: Large Language Model integration for dynamic question generation and evaluation
- **python-dotenv**: Environment variable management

## 📋 Prerequisites

- Python 3.7 or higher
- OpenAI API key (optional - chatbot works in offline mode without it)

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Pallavi-Pandey/Skill-Hunt.git
cd Skill-Hunt
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API key** (optional but recommended):
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🎯 Usage

### Running the Chatbot

Simply run the main chatbot script:

```bash
python chatbot.py
```

### Interview Flow

1. **Basic Information Collection**:
   - Full name
   - Email address
   - Phone number
   - Years of professional experience
   - Preferred role

2. **Tech Stack Declaration**:
   - Candidate lists their technical skills
   - System recognizes various technologies across categories:
     - Frontend: React, Angular, Vue.js, etc.
     - Backend: Node.js, Python, Java, etc.
     - Database: MongoDB, PostgreSQL, MySQL, etc.
     - DevOps: Docker, Kubernetes, AWS, etc.
     - Mobile: React Native, Flutter, iOS, Android, etc.
     - Data: TensorFlow, PyTorch, Pandas, etc.

3. **Technical Interview**:
   - 3-5 dynamically generated questions based on tech stack
   - Questions adapted to experience level
   - Real-time AI feedback on responses (when LLM is enabled)

4. **Summary & Evaluation**:
   - AI-generated assessment of candidate's performance
   - Key strengths and areas for improvement
   - Hiring recommendation

5. **Data Storage**:
   - Interview saved to `interviews/` directory
   - JSON format for easy processing

## 📁 Project Structure

```
Skill-Hunt/
├── chatbot.py           # Main chatbot orchestration
├── candidate.py         # Candidate data model
├── llm_service.py       # LLM integration service
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── interviews/         # Saved interview data (created at runtime)
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **MIN_QUESTIONS_PER_STACK**: Minimum questions per interview (default: 3)
- **MAX_QUESTIONS_PER_STACK**: Maximum questions per interview (default: 5)
- **TECH_STACKS**: Add or modify supported technologies
- **DIFFICULTY_LEVELS**: Adjust experience level classifications

Edit `.env` to configure:

- **OPENAI_API_KEY**: Your OpenAI API key
- **OPENAI_MODEL**: Model to use (default: gpt-3.5-turbo)

## 🎓 LLM Integration

The chatbot demonstrates understanding of Large Language Models through:

1. **Prompt Engineering**: Carefully crafted prompts for question generation and evaluation
2. **Context Management**: Maintains conversation context and candidate information
3. **Temperature Control**: Uses appropriate temperature settings for different tasks
4. **Error Handling**: Graceful fallback when LLM is unavailable
5. **Response Processing**: Parses and cleans LLM outputs

### With LLM (Recommended):
- Dynamic, personalized questions
- Real-time response evaluation
- Comprehensive hiring recommendations
- Context-aware follow-up questions

### Without LLM (Offline Mode):
- Preset questions based on tech stack
- Basic data collection
- Manual review required

## 📊 Example Interview

```
   Welcome to TalentScout Hiring Assistant   

Hello! I'm your AI-powered hiring assistant.
I'll help screen your application for technology positions.
Let's get started!

--- Basic Information ---

What's your full name? John Doe
What's your email address? john.doe@email.com
What's your phone number? +1234567890
How many years of professional experience do you have? 4
What role are you applying for? Full Stack Developer

Thank you, John! Let's talk about your technical skills.

--- Technical Skills ---

Enter your tech stack (comma-separated):
> React, Node.js, MongoDB, Docker, AWS

Great! I see you work with: React, Node.js, MongoDB, Docker, AWS
Now I'll ask you some technical questions based on your skills.

--- Technical Interview ---

Based on your 4 years of experience, I'll ask mid-level questions.

Generating personalized questions using AI...

Question 1/3:
Explain how React's Virtual DOM works and why it improves performance...

[Interview continues...]
```

## 🔒 Security & Privacy

- API keys stored in `.env` (not committed to git)
- Interview data stored locally
- No data sent to third parties except OpenAI API (when enabled)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is created for educational purposes as part of an assignment.

## 👥 Author

Developed for TalentScout Recruitment Agency

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Make sure you've created a `.env` file
- Add your API key: `OPENAI_API_KEY=your_key_here`
- The chatbot will still work in offline mode without it

### "Module not found" error
- Run `pip install -r requirements.txt`
- Ensure you're using Python 3.7+

### Questions seem generic
- Ensure your OpenAI API key is properly configured
- Check your API key has available credits
- The chatbot uses fallback questions when LLM is unavailable

## 🚀 Future Enhancements

- Web-based UI interface
- Video interview capabilities
- Integration with ATS (Applicant Tracking Systems)
- Multi-language support
- Advanced analytics dashboard
- Resume parsing integration
