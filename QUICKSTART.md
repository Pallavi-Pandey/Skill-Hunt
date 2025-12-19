# Quick Start Guide

Get TalentScout Hiring Assistant up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation (3 steps)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Pallavi-Pandey/Skill-Hunt.git
cd Skill-Hunt

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# On macOS/Linux:
nano .env
# On Windows:
notepad .env

# Add your key:
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## First Conversation

1. **Start:** The chatbot will greet you and ask for your name
2. **Provide Info:** Answer questions about:
   - Name
   - Email
   - Phone
   - Experience
   - Desired position
   - Location
   - Tech stack (e.g., "Python, Django, React, PostgreSQL, Docker")
3. **Answer Questions:** The bot will generate technical questions based on your tech stack
4. **End:** Type "goodbye" or "bye" when done

## Example Tech Stack Formats

```
"Python, Django, PostgreSQL, Redis, Docker, AWS"
"JavaScript, TypeScript, React, Node.js, MongoDB, Docker"
"Java, Spring Boot, MySQL, Kafka, Kubernetes, Jenkins"
"Go, Gin, PostgreSQL, RabbitMQ, Docker, AWS"
```

## Common Commands

```bash
# Start the app
streamlit run app.py

# Start on different port
streamlit run app.py --server.port=8502

# Stop the app
Ctrl + C (in terminal)

# Update dependencies
pip install -r requirements.txt --upgrade

# Check Python version
python --version

# Check installed packages
pip list | grep -E "streamlit|openai"
```

## Troubleshooting

### "API key is not configured"
- Check that `.env` file exists
- Verify `OPENAI_API_KEY` is set in `.env`
- Restart the application

### "command not found: streamlit"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall streamlit
pip install streamlit
```

### Port already in use
```bash
# Use a different port
streamlit run app.py --server.port=8502
```

### More issues?
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Next Steps

- Read [README.md](README.md) for complete documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for conversation examples
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## Quick Tips

✅ **DO:**
- Be specific about your tech stack
- Provide complete contact information
- Answer technical questions thoroughly
- Use "goodbye" to end conversation gracefully

❌ **DON'T:**
- Share real personal information for testing
- Commit your `.env` file to version control
- Use production API keys for development
- Expect instant responses (API calls take 2-5 seconds)

## Features at a Glance

| Feature | Status |
|---------|--------|
| Information Gathering | ✅ |
| Tech Stack Analysis | ✅ |
| Question Generation | ✅ |
| Context Awareness | ✅ |
| Graceful Exit | ✅ |
| Error Handling | ✅ |
| Clean UI | ✅ |
| Secure Configuration | ✅ |

## Support

Need help?
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [README.md](README.md)
3. Open a GitHub issue

---

**Happy Recruiting! 🎯**
