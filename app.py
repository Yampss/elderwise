import streamlit as st
from src.database import init_database
from src.utils import setup_page_config, setup_directories
from pages.share_story import share_story_page
from pages.read_stories import read_stories_page

def main():
    """Main application entry point"""
    setup_page_config()
    setup_directories()

    # Custom CSS for modern styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .story-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        padding-left: 1rem;
        padding-right: 1rem;
        background-color: #f0f2f6;
        color: #262730;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>📚 StoryShare</h1>
        <p>Share your stories, discover amazing tales from our community</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize database
    init_database()

    # Create tabs for navigation
    tab1, tab2 = st.tabs(["✍️ Share a Story", "📖 Read Stories"])

    with tab1:
        share_story_page()

    with tab2:
        read_stories_page()

if __name__ == "__main__":
    main()
