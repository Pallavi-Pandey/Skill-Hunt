"""
Configuration module for TalentScout Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the chatbot"""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    # Interview Settings
    MIN_QUESTIONS_PER_STACK = 3
    MAX_QUESTIONS_PER_STACK = 5
    
    # Tech Stack Categories
    TECH_STACKS = {
        'frontend': ['React', 'Angular', 'Vue.js', 'HTML/CSS', 'JavaScript', 'TypeScript'],
        'backend': ['Node.js', 'Python', 'Java', 'C#', '.NET', 'Go', 'Ruby', 'PHP'],
        'database': ['MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Cassandra', 'DynamoDB'],
        'devops': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Jenkins', 'GitLab CI/CD'],
        'mobile': ['React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin'],
        'data': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Apache Spark']
    }
    
    # Question Difficulty Levels
    DIFFICULTY_LEVELS = ['junior', 'mid-level', 'senior']
