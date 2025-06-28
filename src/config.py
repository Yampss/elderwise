import os
from pathlib import Path

class Config:
    """Configuration settings for ElderWise application"""
    
    # Application settings
    APP_NAME = "ElderWise"
    VERSION = "1.0.0"
    
    # Data directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    STORIES_DIR = DATA_DIR / "stories"
    AUDIO_DIR = DATA_DIR / "audio"
    TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
    USER_DATA_DIR = DATA_DIR / "users"
    
    # AI settings
    GEMINI_MODEL = "gemini-pro"
    GEMINI_AUDIO_MODEL = "gemini-pro"
    MAX_STORY_LENGTH = 300  # seconds
    
    # Story categories
    STORY_CATEGORIES = {
        "life_skills": "🏠 Life Skills",
        "professional": "💼 Professional Wisdom", 
        "cultural": "🌍 Cultural Heritage",
        "historical": "📜 Historical Perspectives",
        "relationships": "❤️ Relationships",
        "parenting": "👨‍👩‍👧‍👦 Parenting",
        "cooking": "🍳 Cooking & Recipes",
        "crafts": "🎨 Crafts & Hobbies",
        "travel": "✈️ Travel & Adventure",
        "health": "🏥 Health & Wellness"
    }
    
    # Story prompts for each category
    STORY_PROMPTS = {
        "life_skills": [
            "Tell me about a recipe that's been in your family for generations",
            "How did you manage household finances during tough times?",
            "What's the most important life skill you learned the hard way?",
            "How did you maintain a home without modern conveniences?",
            "What's a tradition you hope will never be forgotten?"
        ],
        "professional": [
            "What's the most important lesson you learned at work?",
            "Tell me about a time you had to adapt to major workplace changes",
            "What advice would you give someone starting their career?",
            "How did you balance work and family life?",
            "What's the secret to working well with difficult people?"
        ],
        "cultural": [
            "Tell me about a tradition from your childhood",
            "What was it like growing up in your community?",
            "How did your family celebrate special occasions?",
            "What languages or dialects did you grow up speaking?",
            "What stories did your grandparents tell you?"
        ],
        "historical": [
            "What major historical event do you remember most clearly?",
            "How did technology change during your lifetime?",
            "What was daily life like when you were young?",
            "How did your community handle difficult times?",
            "What's something about the past that young people should know?"
        ],
        "relationships": [
            "What's the secret to a long, happy relationship?",
            "How did you meet your spouse or best friend?",
            "What's the best relationship advice you ever received?",
            "How do you maintain friendships over decades?",
            "What did you learn about love from your parents?"
        ],
        "parenting": [
            "What's the most challenging part of raising children?",
            "How did you discipline your children effectively?",
            "What values did you try to instill in your kids?",
            "How did you handle teenage problems?",
            "What's your proudest moment as a parent?"
        ],
        "cooking": [
            "What's a recipe you learned from your mother or grandmother?",
            "How did you cook for a large family on a budget?",
            "What's the biggest cooking disaster you learned from?",
            "How did you preserve food before modern refrigeration?",
            "What's a dish that always brings back memories?"
        ],
        "crafts": [
            "What hobbies or crafts did you enjoy throughout your life?",
            "How did you learn your favorite skill or craft?",
            "What project are you most proud of creating?",
            "How did people entertain themselves before TV and internet?",
            "What creative skills do you wish more young people would learn?"
        ],
        "travel": [
            "What's the most memorable trip you ever took?",
            "How was traveling different when you were young?",
            "What's the most beautiful place you've ever seen?",
            "Tell me about a time you got lost or had an adventure",
            "What did you learn from visiting different places?"
        ],
        "health": [
            "What health remedies did your family use?",
            "How did you stay healthy without modern medicine?",
            "What's the most important health lesson you've learned?",
            "How did you handle illness or injury in your family?",
            "What advice do you have for aging gracefully?"
        ]
    }
    
    # UI settings
    LARGE_BUTTON_STYLE = """
        font-size: 1.5rem !important;
        padding: 1rem 2rem !important;
        margin: 1rem 0 !important;
        border-radius: 15px !important;
        min-height: 4rem !important;
    """
    
    # Audio settings
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_CHANNELS = 1
    AUDIO_FORMAT = "wav"
    
    @classmethod
    def get_gemini_api_key(cls):
        """Get Gemini API key from environment or session state"""
        import streamlit as st
        
        # Try to get from environment first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
            
        # If not in environment, try session state
        if hasattr(st, 'session_state') and 'gemini_api_key' in st.session_state:
            return st.session_state.gemini_api_key
            
        return None
    
    @classmethod
    def set_gemini_api_key(cls, api_key):
        """Set Gemini API key in session state"""
        import streamlit as st
        st.session_state.gemini_api_key = api_key
