# Troubleshooting Guide

This guide helps you resolve common issues with the TalentScout Hiring Assistant.

## Installation Issues

### Problem: `pip install -r requirements.txt` fails

**Solution 1: Update pip**
```bash
pip install --upgrade pip
```

**Solution 2: Use Python 3.8+**
```bash
python --version  # Check version
# If less than 3.8, install Python 3.8 or higher
```

**Solution 3: Install in virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

### Problem: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Make sure you're in the correct directory
cd Skill-Hunt

# Activate virtual environment if using one
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## API Configuration Issues

### Problem: "OpenAI API key is not configured"

**Symptom:** Sidebar shows "❌ API Key Missing"

**Solution:**
1. Create a `.env` file in the project root (if it doesn't exist):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. Restart the Streamlit application

**Note:** Never commit your `.env` file with actual API keys to version control!

### Problem: "Authentication error. Please check your OpenAI API key"

**Causes:**
- Invalid API key
- Expired API key
- API key doesn't have proper permissions

**Solution:**
1. Verify your API key at https://platform.openai.com/api-keys
2. Generate a new API key if needed
3. Update your `.env` file
4. Restart the application

### Problem: "Rate limit reached"

**Symptom:** "⚠️ Rate limit reached. Please try again in a moment."

**Solution:**
1. Wait a few moments before continuing the conversation
2. If problem persists, check your OpenAI account usage limits
3. Consider upgrading your OpenAI plan if needed

## Application Startup Issues

### Problem: Streamlit command not found

**Error:**
```bash
streamlit: command not found
```

**Solution:**
```bash
# Ensure streamlit is installed
pip install streamlit

# If using virtual environment, make sure it's activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Problem: Port already in use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution 1: Use different port**
```bash
streamlit run app.py --server.port=8502
```

**Solution 2: Kill process using port 8501**
```bash
# On macOS/Linux
lsof -ti:8501 | xargs kill -9

# On Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Problem: Application doesn't open in browser

**Solution:**
```bash
# Manually open the URL shown in terminal
# Usually: http://localhost:8501

# Or specify browser explicitly
streamlit run app.py --browser.serverAddress=localhost
```

## Runtime Issues

### Problem: Chat input not responding

**Solution:**
1. Check browser console for JavaScript errors (F12)
2. Clear browser cache and reload
3. Try a different browser (Chrome, Firefox, Safari)
4. Restart the Streamlit application

### Problem: Conversation gets stuck in "Thinking..." state

**Possible Causes:**
- API timeout
- Network issues
- Invalid API response

**Solution:**
1. Refresh the page
2. Check your internet connection
3. Verify OpenAI API status at https://status.openai.com/
4. Check terminal for error messages

### Problem: Farewell message not appearing

**Solution:**
Make sure you're using one of the ending keywords:
- goodbye
- bye
- exit
- quit
- done
- no thanks
- stop
- end

Keywords are case-insensitive.

### Problem: Responses are slow

**Causes:**
- Network latency
- OpenAI API response time
- Model processing time

**Solutions:**
1. Use a faster model by changing `OPENAI_MODEL` in `.env`:
   ```
   OPENAI_MODEL=gpt-3.5-turbo  # Faster
   ```
2. Check your internet connection
3. Consider using a CDN or closer server region

## Data and Privacy Issues

### Problem: Conversation history persists unexpectedly

**Solution:**
- Click "🔄 Start New Conversation" in the sidebar
- Or refresh the browser page
- Session data is stored in browser memory only

### Problem: Want to clear all data

**Solution:**
1. Click "Start New Conversation" button
2. Clear browser cache for localhost:8501
3. Restart browser

## Development and Debugging

### Problem: Changes not reflecting

**Solution:**
1. Streamlit has auto-reload, but you can force reload:
   - Click "Always rerun" in the top-right menu, or
   - Press `R` to rerun, or
   - Ctrl+C in terminal and restart

### Problem: Want to see detailed errors

**Solution:**
Add to `.streamlit/config.toml`:
```toml
[runner]
fastReruns = false

[logger]
level = "debug"
```

### Problem: Testing without API key

**Symptom:** Want to test UI without making API calls

**Workaround:**
The application will show appropriate error messages when API key is invalid or missing, allowing you to test the UI and conversation flow.

## Environment-Specific Issues

### macOS: SSL Certificate Error

**Error:**
```
[SSL: CERTIFICATE_VERIFY_FAILED]
```

**Solution:**
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Windows: Path issues

**Solution:**
Use forward slashes or raw strings:
```python
# Good
path = "C:/Users/name/project"
path = r"C:\Users\name\project"

# Bad
path = "C:\Users\name\project"
```

### Linux: Permission denied

**Solution:**
```bash
# Make sure you have write permissions
chmod +x app.py
chmod 644 requirements.txt

# Or run with appropriate user permissions
```

## Getting Help

If you've tried all solutions and still have issues:

1. **Check logs:** Look at terminal output for error messages
2. **Search issues:** Check if someone else had the same problem
3. **System info:** Note your:
   - Operating system
   - Python version (`python --version`)
   - Streamlit version (`streamlit version`)
   - OpenAI library version (`pip show openai`)
4. **Error details:** Copy the full error message
5. **Create issue:** Open a GitHub issue with all details above

## Quick Diagnostic

Run this to check your setup:
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "streamlit|openai|python-dotenv"

# Check if .env exists
ls -la .env

# Test Python imports
python -c "import streamlit; import openai; print('All imports OK')"

# Verify syntax
python -m py_compile app.py
```

## Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `APIConnectionError` | Can't connect to OpenAI | Check internet, API status |
| `AuthenticationError` | Invalid API key | Verify API key in `.env` |
| `RateLimitError` | Too many requests | Wait, or upgrade plan |
| `AttributeError: module 'openai' has no attribute...` | Wrong OpenAI version | Update: `pip install --upgrade openai` |
| `StreamlitAPIException` | Streamlit internal error | Restart app, clear cache |

## Performance Optimization

If the app is slow:

1. **Reduce token limit** in `app.py`:
   ```python
   max_tokens=300  # Instead of 500
   ```

2. **Use faster model**:
   ```
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Limit conversation history** (optional enhancement)

4. **Check system resources**: CPU, memory, network

## Still Need Help?

- **Documentation:** Check README.md and USAGE_EXAMPLES.md
- **OpenAI Docs:** https://platform.openai.com/docs
- **Streamlit Docs:** https://docs.streamlit.io/
- **GitHub Issues:** Open an issue with detailed information
