"""
Configuration module for TalentScout Hiring Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the chatbot"""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
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
