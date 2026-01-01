# TalentScout - Quick Start Guide

Get up and running with the TalentScout Hiring Assistant in minutes!

## 🚀 Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/Pallavi-Pandey/Skill-Hunt.git
cd Skill-Hunt

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the demo
python demo.py
```

## 💡 Two Modes of Operation

### Mode 1: Offline Mode (No API Key Required)
Perfect for testing and evaluation. Uses preset questions.

```bash
python chatbot.py
```

### Mode 2: AI-Powered Mode (Recommended)
Dynamic questions and real-time evaluation using OpenAI.

```bash
# 1. Set up your API key
cp .env.example .env

# 2. Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# 3. Run the chatbot
python chatbot.py
```

## 📝 First Interview

When you run `python chatbot.py`, you'll be guided through:

1. **Basic Info** (30 seconds)
   - Name, email, phone
   - Years of experience
   - Desired role

2. **Tech Stack** (1 minute)
   - List your technologies
   - Example: "React, Node.js, MongoDB, Docker"

3. **Technical Questions** (5-10 minutes)
   - 3-5 questions based on your stack
   - Questions adapt to your experience level
   - Real-time feedback (with API key)

4. **Summary** (automatic)
   - Interview results saved to `interviews/` folder
   - JSON format for easy integration

## 🎯 Examples & Demos

```bash
# View comprehensive examples
python examples.py

# Run non-interactive demo
python demo.py
```

## ⚙️ Configuration

Edit `config.py` to customize:
- Number of questions (MIN_QUESTIONS_PER_STACK)
- Supported technologies (TECH_STACKS)
- Experience levels (DIFFICULTY_LEVELS)

## 🔧 Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**API key not working?**
- Check `.env` file exists
- Verify key format: `OPENAI_API_KEY=sk-...`
- Ensure you have API credits

**Want to test without API key?**
- Just run `python chatbot.py`
- Works in offline mode automatically

## 📚 Learn More

- Full documentation: `README.md`
- Usage examples: `python examples.py`
- Demo mode: `python demo.py`

## 🎓 Understanding LLM Integration

The chatbot demonstrates LLM capabilities through:

1. **Prompt Engineering**: Crafted prompts for question generation
2. **Context Management**: Maintains interview state
3. **Dynamic Responses**: Adapts to candidate's tech stack
4. **Evaluation**: AI-powered feedback on answers
5. **Graceful Fallback**: Works offline when needed

## 📊 Sample Output

```
   Welcome to TalentScout Hiring Assistant   

--- Technical Interview ---

Question 1/3:
Explain the differences between REST and GraphQL APIs.
Which would you choose for a real-time chat application?

Your answer:
> [Type your response here]

💭 Evaluating your response...

Feedback: Good explanation of the key differences. Your choice
of GraphQL for real-time features shows understanding of
subscriptions. Consider mentioning WebSockets as well.
```

## 🎉 Next Steps

1. ✅ Run the demo: `python demo.py`
2. ✅ Try the examples: `python examples.py`
3. ✅ Start interviewing: `python chatbot.py`
4. ✅ Configure API key for AI features
5. ✅ Customize tech stacks in `config.py`

---

**Need Help?** Check the main README.md for detailed documentation!
