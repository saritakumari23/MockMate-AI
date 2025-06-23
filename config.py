import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the AI Interview Coach application."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4'
    OPENAI_MAX_TOKENS = 1000
    OPENAI_TEMPERATURE = 0.7
    
    # Application Configuration
    MAX_QUESTIONS_PER_SESSION = 10
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Interview Categories
    INTERVIEW_CATEGORIES = [
        'behavioral',
        'technical',
        'situational',
        'strengths_weaknesses',
        'career_goals',
        'teamwork',
        'leadership',
        'problem_solving'
    ]
    
    # Difficulty Levels
    DIFFICULTY_LEVELS = ['beginner', 'intermediate', 'advanced']
    
    # Career Fields
    CAREER_FIELDS = [
        'software_engineering',
        'data_science',
        'product_management',
        'marketing',
        'sales',
        'finance',
        'consulting',
        'design',
        'human_resources',
        'operations'
    ] 