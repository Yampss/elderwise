"""
Configuration settings for ElderWise application
"""

import os
from pathlib import Path
import streamlit as st

class Config:
    """Configuration settings for ElderWise application"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    AUDIO_DIR = DATA_DIR / "audio"
    STORIES_DIR = DATA_DIR / "stories"
    TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
    THUMBNAILS_DIR = DATA_DIR / "thumbnails"
    USER_DATA_DIR = DATA_DIR / "users"
    
    # Application settings
    APP_NAME = "ElderWise"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Connecting Generations Through Stories and Wisdom"
    
    # File upload settings
    MAX_UPLOAD_SIZE_MB = int(os.getenv('MAX_UPLOAD_SIZE_MB', '50'))
    ALLOWED_AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg']
    
    # Database Configuration
    @staticmethod
    def get_database_url():
        """Get database URL from environment or default to SQLite"""
        # For production (Heroku, Railway, Render, etc.)
        if os.getenv('DATABASE_URL'):
            db_url = os.getenv('DATABASE_URL')
            # Fix for SQLAlchemy 1.4+ with PostgreSQL (Heroku compatibility)
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
            return db_url
        
        # For custom PostgreSQL setup
        if os.getenv('POSTGRES_URL'):
            return os.getenv('POSTGRES_URL')
            
        # For local PostgreSQL development
        if os.getenv('USE_POSTGRESQL') == 'true':
            user = os.getenv('DB_USER', 'postgres')
            password = os.getenv('DB_PASSWORD', 'password')
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'elderwise')
            return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        
        # Default SQLite for development
        db_path = Config.DATA_DIR / "elderwise.db"
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"
    
    @staticmethod
    def is_production():
        """Check if running in production environment"""
        return os.getenv('DATABASE_URL') is not None or os.getenv('POSTGRES_URL') is not None
    
    # AI Configuration
    GEMINI_MODEL = "gemini-pro"
    
    @staticmethod
    def get_gemini_api_key():
        """Get Gemini API key from environment or session state"""
        # Try environment variable first
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            return api_key
        
        # Try session state
        if hasattr(st, 'session_state') and 'gemini_api_key' in st.session_state:
            return st.session_state.gemini_api_key
        
        return None
    
    @staticmethod
    def set_gemini_api_key(api_key):
        """Set Gemini API key in session state"""
        st.session_state.gemini_api_key = api_key
    
    # Navigation options
    MAIN_PAGES = {
        "🏠 Home": "home",
        "📝 Share Your Story": "share_story", 
        "🔍 Discover Stories": "discover_stories"
    }
    
    # Story categories
    STORY_CATEGORIES = {
        "life_skills": "Life Skills & Practical Wisdom",
        "professional": "Professional & Career Advice", 
        "cultural": "Cultural Traditions & Heritage",
        "historical": "Historical Perspectives & Events",
        "relationships": "Relationships & Family",
        "parenting": "Parenting & Child-rearing",
        "cooking": "Cooking & Recipes",
        "crafts": "Crafts & Hobbies",
        "travel": "Travel & Adventure",
        "health": "Health & Wellness",
        "technology": "Technology & Digital Life",
        "finance": "Finance & Money Management"
    }
    
    # Story prompts for each category
    STORY_PROMPTS = {
        "life_skills": [
            "Share a time when you learned an important life lesson the hard way",
            "What's the most valuable skill you wish you'd learned earlier?",
            "Tell about a challenge that taught you resilience",
        ],
        "professional": [
            "Describe your first job and what it taught you",
            "Share advice about changing careers or finding purpose in work",
            "What's the biggest mistake you made in your career and what you learned?",
        ],
        "cultural": [
            "What cultural traditions were important in your family?",
            "How did your heritage influence your values and beliefs?",
            "Share a story about a cultural celebration or event",
        ],
        "historical": [
            "What historical events had the most impact on your life?",
            "How did you experience major historical events as a young person?",
            "What lessons from history do you think are most important today?",
        ],
        "relationships": [
            "How did your parents or guardians show love and support?",
            "What was the best piece of relationship advice you received?",
            "Describe a friendship that significantly impacted your life",
        ],
        "parenting": [
            "What was your approach to discipline and setting boundaries?",
            "How did you handle conflicts or challenges with your children?",
            "What are you most proud of teaching your children?",
        ],
        "cooking": [
            "What role did cooking play in your family life?",
            "How did you learn to cook the dishes you love?",
            "Share a memorable cooking experience or disaster",
        ],
        "crafts": [
            "What crafts or hobbies have you enjoyed throughout your life?",
            "How did you learn the skills for your favorite craft?",
            "Describe a project that you are particularly proud of",
        ],
        "travel": [
            "What inspired your love of travel?",
            "Share a travel experience that changed your perspective",
            "How did you prepare for trips in the past compared to now?",
        ],
        "health": [
            "What were common health practices in your family?",
            "How did you stay active and healthy without modern conveniences?",
            "What advice would you give about maintaining health and wellness?",
        ],
        "technology": [
            "How has technology changed during your lifetime?",
            "What was life like before smartphones and the internet?",
            "How did you adapt to new technologies over the years?",
        ],
        "finance": [
            "What financial lessons did you learn from your parents?",
            "How did you handle money differently in your younger years?",
            "What's the best financial advice you can give?",
        ]
    }
    
    # UI Styling
    CUSTOM_CSS = """
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .welcome-section {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        margin: 2rem 0;
    }
    .feature-card {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        background: white;
        border: 2px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    .story-card {
        background: white;
        border: 1px solid #e1e5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .story-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .category-tag {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    </style>
    """
