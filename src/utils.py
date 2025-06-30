import os
import streamlit as st
from pathlib import Path
import json
from datetime import datetime

def setup_page_config():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="StoryShare - Share and Discover Stories",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://github.com/storyshare/help',
            'Report a bug': 'https://github.com/storyshare/issues',
            'About': """
            # StoryShare
            A simple platform for sharing and discovering amazing stories.
            
            **Features:**
            - ✍️ Share your stories with cover photos
            - 📖 Read stories from the community
            - 📂 Organize stories by categories
            - 📱 Mobile-friendly interface
            
            **Version:** 2.0.0
            **Built with:** Streamlit & PostgreSQL
            """
        }
    )

def setup_directories():
    """Create necessary directories for the application"""
    from src.config import Config
    config = Config()
    
    directories = [
        config.DATA_DIR,
        config.STORIES_DIR,
        config.AUDIO_DIR,
        config.TRANSCRIPTS_DIR,
        config.USER_DATA_DIR,
        Path("data/images")  # Add images directory for cover photos
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def format_date(date_string):
    """Format ISO date string to human readable format"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%B %d, %Y at %I:%M %p")
    except:
        return date_string

def validate_audio_file(uploaded_file):
    """Validate uploaded audio file"""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file size (max 50MB)
    if uploaded_file.size > 50 * 1024 * 1024:
        return False, "File too large. Maximum size is 50MB."
    
    # Check file type
    allowed_types = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/m4a', 'audio/ogg']
    if uploaded_file.type not in allowed_types:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
    
    return True, "Valid file"

def save_uploaded_audio(uploaded_file, story_id):
    """Save uploaded audio file and return file path"""
    from src.config import Config
    config = Config()
    
    file_extension = uploaded_file.name.split('.')[-1]
    audio_filename = f"{story_id}.{file_extension}"
    audio_path = config.AUDIO_DIR / audio_filename
    
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(audio_path)

def get_sample_prompts(category):
    """Get sample prompts for a category"""
    from src.config import Config
    config = Config()
    return config.STORY_PROMPTS.get(category, [])

def create_story_card(story, show_full=False):
    """Create a story card component"""
    category_emoji = {
        "life_skills": "🏠",
        "professional": "💼", 
        "cultural": "🌍",
        "historical": "📜",
        "relationships": "❤️",
        "parenting": "👨‍👩‍👧‍👦",
        "cooking": "🍳",
        "crafts": "🎨",
        "travel": "✈️",
        "health": "🏥"
    }
    
    emoji = category_emoji.get(story.get('category', ''), "📚")
    category_name = story.get('category', '').replace('_', ' ').title()
    
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #e1e5e9; 
            border-radius: 10px; 
            padding: 1.5rem; 
            margin: 1rem 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #2c3e50;">{emoji} {story.get('title', 'Untitled Story')}</h4>
                <span style="background: #667eea; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                    {category_name}
                </span>
            </div>
            <p style="color: #555; margin: 0.5rem 0; line-height: 1.6;">
                {story.get('summary', story.get('transcript', '')[:150] + '...' if len(story.get('transcript', '')) > 150 else story.get('transcript', ''))}
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; font-size: 0.9rem; color: #777;">
                <span>👤 {story.get('contributor_name', 'Anonymous')}</span>
                <span>📅 {format_date(story.get('created_at', ''))}</span>
                <span>⏱️ {format_duration(story.get('duration', 0))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_full:
            if story.get('transcript'):
                st.markdown("**Full Story:**")
                st.write(story['transcript'])
            
            if story.get('tags'):
                st.markdown("**Tags:**")
                tags_html = " ".join([f"<span style='background: #e3f2fd; padding: 0.2rem 0.6rem; border-radius: 10px; margin: 0.2rem; font-size: 0.8rem;'>{tag}</span>" for tag in story['tags']])
                st.markdown(tags_html, unsafe_allow_html=True)

def create_user_profile_form(user_type):
    """Create user profile form"""
    st.markdown(f"### Create Your {user_type.title()} Profile")
    
    with st.form(f"{user_type}_profile_form"):
        name = st.text_input("Your Name", help="How would you like to be called?")
        
        if user_type == "elder":
            age = st.number_input("Age", min_value=50, max_value=120, value=65)
            location = st.text_input("Location (Optional)", help="City, State/Country")
            bio = st.text_area("Tell us about yourself", 
                             help="Share your background, experiences, what you'd like to teach others")
            expertise_areas = st.multiselect(
                "Your areas of expertise",
                ["Life Skills", "Professional Experience", "Parenting", "Cooking", 
                 "Crafts & Hobbies", "Historical Knowledge", "Cultural Traditions",
                 "Health & Wellness", "Relationships", "Travel & Adventure"],
                help="Select areas where you have wisdom to share"
            )
            
        else:  # seeker
            age = st.number_input("Age", min_value=13, max_value=80, value=25)
            location = st.text_input("Location (Optional)", help="City, State/Country")
            bio = st.text_area("Tell us about yourself", 
                             help="Share your interests, goals, what you hope to learn")
            interests = st.multiselect(
                "What would you like to learn about?",
                ["Life Skills", "Career Development", "Parenting", "Cooking", 
                 "Crafts & Hobbies", "Historical Events", "Cultural Traditions",
                 "Health & Wellness", "Relationships", "Travel & Adventure"],
                help="Select areas where you'd like guidance"
            )
            goals = st.text_area("Your goals and aspirations", 
                               help="What are you hoping to achieve? What challenges are you facing?")
        
        privacy_level = st.selectbox(
            "Privacy Level",
            ["Public - Anyone can see my profile",
             "Community - Only registered users can see my profile", 
             "Connections - Only my connections can see my full profile"],
            index=1
        )
        
        submitted = st.form_submit_button("Create Profile")
        
        if submitted and name:
            profile_data = {
                "name": name,
                "user_type": user_type,
                "age": age,
                "location": location,
                "bio": bio,
                "privacy_level": privacy_level
            }
            
            if user_type == "elder":
                profile_data["expertise_areas"] = expertise_areas
            else:
                profile_data["interests"] = interests
                profile_data["goals"] = goals
            
            return profile_data
        elif submitted and not name:
            st.error("Please enter your name to continue")
    
    return None

def show_api_key_setup():
    """Show API key setup interface"""
    st.markdown("### 🔑 Setup Required")
    st.markdown("""
    To use ElderWise's AI features (transcription, story analysis, smart matching), 
    you need to provide a Google Gemini API key.
    """)
    
    with st.expander("How to get a Gemini API key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the generated key
        5. Paste it below
        
        The free tier includes generous limits perfect for this project!
        """)
    
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        help="Your API key will be stored securely for this session"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save API Key", disabled=not api_key):
            from src.config import Config
            Config.set_gemini_api_key(api_key)
            st.success("API key saved! AI features are now available.")
            st.rerun()
    
    with col2:
        if st.button("Skip for now"):
            st.session_state.skip_api_key = True
            st.info("You can still use basic features. Add your API key later for AI features.")
            st.rerun()

def show_connection_request_form(elder_id, elder_name):
    """Show form to request connection with an elder"""
    st.markdown(f"### Connect with {elder_name}")
    
    with st.form("connection_request"):
        message = st.text_area(
            "Introduce yourself and explain why you'd like to connect",
            help="Share what you hope to learn and why this elder's expertise interests you",
            height=120
        )
        
        topics = st.multiselect(
            "What topics would you like to discuss?",
            ["Career advice", "Life lessons", "Specific skills", "Historical perspectives",
             "Personal challenges", "Family matters", "Health & wellness", "Other"]
        )
        
        preferred_contact = st.selectbox(
            "Preferred way to connect",
            ["Video call", "Voice call", "Written messages", "Any method is fine"]
        )
        
        submitted = st.form_submit_button("Send Connection Request")
        
        if submitted and message:
            return {
                "elder_id": elder_id,
                "message": message,
                "topics": topics,
                "preferred_contact": preferred_contact
            }
        elif submitted and not message:
            st.error("Please write a message to introduce yourself")
    
    return None

def display_impact_metrics(user_data, user_type):
    """Display user impact metrics"""
    from src.data_manager import DataManager
    
    data_manager = DataManager()
    activity = data_manager.get_user_activity(user_data.get('id', ''), user_type)
    
    col1, col2, col3, col4 = st.columns(4)
    
    if user_type == "elder":
        with col1:
            st.metric("Stories Shared", activity['stories_contributed'])
        with col2:
            st.metric("People Helped", f"~{activity['stories_contributed'] * 3}")
        with col3:
            st.metric("Connections", activity['connections_made'])
        with col4:
            st.metric("Questions Answered", activity['questions_answered'])
    else:
        with col1:
            st.metric("Stories Discovered", activity['stories_listened'])
        with col2:
            st.metric("Mentors Connected", activity['connections_made'])
        with col3:
            st.metric("Questions Asked", activity['questions_asked'])
        with col4:
            st.metric("Learning Hours", f"{activity['stories_listened'] * 0.1:.1f}")

def create_featured_story_carousel():
    """Create a carousel of featured stories"""
    from src.data_manager import DataManager
    
    data_manager = DataManager()
    featured_stories = data_manager.get_featured_stories(limit=3)
    
    if not featured_stories:
        st.info("No featured stories yet. Be the first to share your wisdom!")
        return
    
    st.markdown("### ⭐ Featured Stories")
    
    cols = st.columns(len(featured_stories))
    
    for idx, story in enumerate(featured_stories):
        with cols[idx]:
            create_story_card(story)
            if st.button(f"Listen to Story", key=f"featured_{idx}"):
                st.session_state.selected_story = story['id']

def safe_json_loads(json_string, default=None):
    """Safely load JSON with fallback"""
    try:
        return json.loads(json_string)
    except:
        return default if default is not None else {}

def truncate_text(text, max_length=100):
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def create_progress_indicator(current_step, total_steps, step_names=None):
    """Create a visual progress indicator"""
    progress_percentage = current_step / total_steps
    
    st.progress(progress_percentage)
    
    if step_names:
        st.write(f"Step {current_step} of {total_steps}: {step_names[current_step-1]}")
    else:
        st.write(f"Step {current_step} of {total_steps}")

def create_category_filter():
    """Create category filter widget"""
    from src.config import Config
    config = Config()
    
    categories = ["All Categories"] + list(config.STORY_CATEGORIES.values())
    selected = st.selectbox("Filter by Category", categories)
    
    if selected == "All Categories":
        return None
    else:
        # Find the key for this category value
        for key, value in config.STORY_CATEGORIES.items():
            if value == selected:
                return key
        return None
