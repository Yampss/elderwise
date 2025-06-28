import streamlit as st
import os
from datetime import datetime
import json
from pathlib import Path

# Import our custom modules
from src.config import Config
from src.ai_engine import AIEngine
from src.data_manager import DataManager
from src.utils import setup_directories

# Import page modules
from pages.elder_interface import elder_recording_interface
from pages.discovery_portal import wisdom_discovery_portal
from pages.community import community_features
from pages.admin_dashboard import admin_dashboard

def main():
    """Main ElderWise application"""
    
    # Page configuration
    st.set_page_config(
        page_title="ElderWise - Connecting Generations Through Stories",
        page_icon="👴",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Setup directories and initialize data manager
    setup_directories()
    
    # Initialize session state
    if 'current_user_type' not in st.session_state:
        st.session_state.current_user_type = None
    if 'current_user_name' not in st.session_state:
        st.session_state.current_user_name = None
        
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .user-type-card {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        background: white;
        border: 2px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    .user-type-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    .elder-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    }
    .seeker-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    .big-button {
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌟 ElderWise</h1>
        <h3>Where Wisdom Meets Wonder - Connecting Generations Through Stories</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user has selected their type
    if st.session_state.current_user_type is None:
        show_user_selection()
    else:
        show_main_app()

def show_user_selection():
    """Show user type selection screen"""
    st.markdown("## Welcome to ElderWise! 👋")
    st.markdown("Please choose how you'd like to use our platform:")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Elder option
        st.markdown("""
        <div class="user-type-card elder-card">
            <h3>👴 I'm a Senior</h3>
            <p>Share your life experiences, wisdom, and stories with younger generations. Your knowledge is invaluable!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue as Senior", key="elder_btn", help="Share your wisdom and stories", use_container_width=True):
            st.session_state.current_user_type = "elder"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Young person option
        st.markdown("""
        <div class="user-type-card seeker-card">
            <h3>🧑 I'm Seeking Wisdom</h3>
            <p>Learn from the experiences of seniors, discover amazing stories, and connect with mentors who can guide you.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue as Wisdom Seeker", key="seeker_btn", help="Learn from senior wisdom", use_container_width=True):
            st.session_state.current_user_type = "seeker"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Admin option
        if st.button("Admin Dashboard", key="admin_btn", help="Platform administration", use_container_width=True):
            st.session_state.current_user_type = "admin"
            st.rerun()

def show_main_app():
    """Show the main application interface"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.current_user_type.title()}! 👋")
        
        if st.button("🔄 Switch User Type", use_container_width=True):
            st.session_state.current_user_type = None
            st.session_state.current_user_name = None
            st.rerun()
        
        st.markdown("---")
        
        # Navigation based on user type
        if st.session_state.current_user_type == "elder":
            page = st.selectbox(
                "Navigation",
                ["📝 Record Stories", "🌟 My Impact", "🤝 Community"],
                help="Choose what you'd like to do"
            )
        elif st.session_state.current_user_type == "seeker":
            page = st.selectbox(
                "Navigation", 
                ["🔍 Discover Wisdom", "🤝 My Connections", "📚 Learning Paths"],
                help="Explore and learn from senior wisdom"
            )
        else:  # admin
            page = st.selectbox(
                "Navigation",
                ["📊 Dashboard", "📝 Content Review", "👥 Community Management"],
                help="Platform administration"
            )
        
        # Quick stats
        show_quick_stats()
    
    # Main content area
    if st.session_state.current_user_type == "elder":
        if "Record Stories" in page:
            elder_recording_interface()
        elif "Impact" in page:
            show_elder_impact()
        elif "Community" in page:
            community_features("elder")
            
    elif st.session_state.current_user_type == "seeker":
        if "Discover" in page:
            wisdom_discovery_portal()
        elif "Connections" in page:
            community_features("seeker")
        elif "Learning" in page:
            show_learning_paths()
            
    else:  # admin
        admin_dashboard()

def show_quick_stats():
    """Show quick statistics in sidebar"""
    st.markdown("### 📊 Quick Stats")
    
    data_manager = DataManager()
    stats = data_manager.get_platform_stats()
    
    st.markdown(f"""
    <div class="stat-card">
        <h4>📚 {stats.get('total_stories', 0)}</h4>
        <p>Stories Shared</p>
    </div>
    <div class="stat-card">
        <h4>👥 {stats.get('active_contributors', 0)}</h4>
        <p>Active Contributors</p>
    </div>
    <div class="stat-card">
        <h4>🤝 {stats.get('connections_made', 0)}</h4>
        <p>Connections Made</p>
    </div>
    """, unsafe_allow_html=True)

def show_elder_impact():
    """Show impact metrics for elders"""
    st.markdown("## 🌟 Your Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Stories Recorded", "12", "+2 this week")
    with col2:
        st.metric("People Helped", "47", "+5 this week")
    with col3:
        st.metric("Hours of Wisdom", "8.5", "+1.2 this week")
    
    st.markdown("### Recent Activity")
    st.info("📚 Your story 'Starting a Business with $50' was featured yesterday!")
    st.success("🎯 Someone found your parenting advice helpful!")
    st.info("💬 You have 3 new questions from wisdom seekers")

def show_learning_paths():
    """Show curated learning paths for seekers"""
    st.markdown("## 📚 Learning Paths")
    
    paths = [
        {
            "title": "🏢 Starting Your Career",
            "description": "Essential wisdom for career beginners",
            "stories": 15,
            "duration": "2 hours"
        },
        {
            "title": "💰 Financial Wisdom",
            "description": "Money management through the decades",
            "stories": 23,
            "duration": "3.5 hours"
        },
        {
            "title": "❤️ Relationship Advice",
            "description": "Building lasting relationships",
            "stories": 18,
            "duration": "2.5 hours"
        }
    ]
    
    for path in paths:
        with st.expander(f"{path['title']} - {path['stories']} stories"):
            st.write(path['description'])
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📖 {path['stories']} stories")
            with col2:
                st.write(f"⏱️ {path['duration']}")
            st.button(f"Start Learning Path", key=f"path_{path['title']}")

if __name__ == "__main__":
    main()
