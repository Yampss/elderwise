import streamlit as st
import uuid
from datetime import datetime
import time
from st_audiorec import st_audiorec
import speech_recognition as sr
from io import BytesIO
import tempfile
import os

from src.config import Config
from src.data_manager import DataManager
from src.ai_engine import AIEngine
from src.utils import (
    check_ai_availability, show_api_key_setup, get_sample_prompts,
    create_progress_indicator, format_duration, create_user_profile_form
)

def elder_recording_interface():
    """Main interface for elders to record their stories"""
    
    # Check if user has profile
    if 'elder_profile' not in st.session_state:
        st.markdown("## Welcome to ElderWise! 👋")
        st.markdown("Let's start by creating your profile so others can learn about your background.")
        
        profile_data = create_user_profile_form("elder")
        if profile_data:
            # Save profile
            data_manager = DataManager()
            user_id = data_manager.save_user_profile(profile_data)
            profile_data['id'] = user_id
            st.session_state.elder_profile = profile_data
            st.success("Profile created! You can now start sharing your stories.")
            st.rerun()
        return
    
    # Check AI availability
    ai_available = check_ai_availability()
    if not ai_available and 'skip_api_key' not in st.session_state:
        show_api_key_setup()
        return
    
    # Main recording interface
    st.markdown("## 📝 Share Your Wisdom")
    st.markdown("Your stories and experiences are valuable. Let's capture them to inspire and teach others!")
    
    # Create tabs for different recording options
    tab1, tab2, tab3 = st.tabs(["🎤 New Story", "📚 My Stories", "💡 Story Ideas"])
    
    with tab1:
        show_recording_interface()
    
    with tab2:
        show_user_stories()
    
    with tab3:
        show_story_prompts()

def show_recording_interface():
    """Show the story recording interface"""
    config = Config()
    
    # Story setup form
    with st.form("story_setup"):
        st.markdown("### Story Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "What type of story is this?",
                options=list(config.STORY_CATEGORIES.keys()),
                format_func=lambda x: config.STORY_CATEGORIES[x],
                help="Choose the category that best fits your story"
            )
        
        with col2:
            title = st.text_input(
                "Story Title",
                help="Give your story a descriptive title",
                placeholder="e.g., 'How I Started My Business with $50'"
            )
        
        # Story prompt selection
        prompts = get_sample_prompts(category)
        if prompts:
            selected_prompt = st.selectbox(
                "Choose a prompt to guide your story (optional)",
                options=["Custom story"] + prompts,
                help="These prompts can help guide your storytelling"
            )
            
            if selected_prompt != "Custom story":
                st.info(f"💡 Prompt: {selected_prompt}")
        else:
            selected_prompt = "Custom story"
        
        description = st.text_area(
            "Brief description (optional)",
            help="What will people learn from your story?",
            placeholder="This story teaches about...",
            height=80
        )
        
        setup_complete = st.form_submit_button("Start Recording")
    
    if setup_complete and title:
        st.session_state.current_story = {
            "title": title,
            "category": category,
            "description": description,
            "prompt": selected_prompt if selected_prompt != "Custom story" else None,
            "contributor_name": st.session_state.elder_profile.get('name', 'Anonymous'),
            "contributor_id": st.session_state.elder_profile.get('id')
        }
        st.rerun()
    elif setup_complete and not title:
        st.error("Please provide a title for your story.")
    
    # Recording interface
    if 'current_story' in st.session_state:
        show_story_recording()

def show_story_recording():
    """Show the actual recording interface"""
    story_data = st.session_state.current_story
    
    st.markdown("---")
    st.markdown(f"### 🎤 Recording: {story_data['title']}")
    
    if story_data.get('prompt'):
        st.markdown(f"**Prompt:** {story_data['prompt']}")
    
    # Recording options
    recording_method = st.radio(
        "How would you like to record your story?",
        ["🎤 Record directly", "📁 Upload audio file", "⌨️ Type your story"],
        horizontal=True
    )
    
    if recording_method == "🎤 Record directly":
        show_direct_recording()
    elif recording_method == "📁 Upload audio file":
        show_file_upload()
    else:
        show_text_input()

def show_direct_recording():
    """Show direct audio recording interface"""
    st.markdown("#### 🎤 Direct Recording")
    st.markdown("Click the record button below and start telling your story. Speak clearly and take your time!")
    
    # Large, prominent recording button
    st.markdown("""
    <style>
    .record-button {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 2rem;
        border-radius: 50%;
        text-align: center;
        margin: 2rem auto;
        width: 150px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    .record-button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Audio recorder component
    audio_bytes = st_audiorec()
    
    if audio_bytes:
        st.success("Great recording! Let's process your story.")
        
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            audio_file_path = tmp_file.name
        
        # Process the recording
        process_audio_recording(audio_file_path, audio_bytes)
        
        # Clean up
        try:
            os.unlink(audio_file_path)
        except:
            pass

def show_file_upload():
    """Show file upload interface"""
    st.markdown("#### 📁 Upload Audio File")
    st.markdown("Upload an audio file of your story (WAV, MP3, M4A formats supported)")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'm4a', 'ogg'],
        help="Maximum file size: 50MB"
    )
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("Process Audio", type="primary"):
            with st.spinner("Processing your audio file..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    audio_file_path = tmp_file.name
                
                # Process the audio
                process_audio_recording(audio_file_path, uploaded_file.getbuffer())
                
                # Clean up
                try:
                    os.unlink(audio_file_path)
                except:
                    pass

def show_text_input():
    """Show text input interface"""
    st.markdown("#### ⌨️ Type Your Story")
    st.markdown("Write your story in the text area below. Don't worry about perfect grammar - just share your wisdom!")
    
    story_text = st.text_area(
        "Tell your story",
        height=300,
        placeholder="Once upon a time...",
        help="Take your time and share as much detail as you'd like"
    )
    
    if story_text and len(story_text) > 50:
        if st.button("Save Story", type="primary"):
            process_text_story(story_text)

def process_audio_recording(audio_file_path, audio_bytes):
    """Process audio recording and create story"""
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Transcribe audio
        status_text.text("🎯 Converting speech to text...")
        progress_bar.progress(25)
        
        transcript = transcribe_audio(audio_file_path)
        
        if not transcript:
            st.error("Could not transcribe the audio. Please try recording again or type your story instead.")
            return
        
        # Step 2: Clean up transcript with AI
        status_text.text("✨ Improving transcription quality...")
        progress_bar.progress(50)
        
        ai_engine = AIEngine()
        if ai_engine.is_ready():
            cleaned_transcript = ai_engine.transcribe_audio_text(transcript)
        else:
            cleaned_transcript = transcript
        
        # Step 3: Generate story metadata
        status_text.text("🏷️ Analyzing story content...")
        progress_bar.progress(75)
        
        story_metadata = generate_story_metadata(cleaned_transcript)
        
        # Step 4: Save story
        status_text.text("💾 Saving your story...")
        progress_bar.progress(100)
        
        save_complete_story(cleaned_transcript, story_metadata, audio_bytes)
        
        status_text.text("✅ Story saved successfully!")
        st.success("🎉 Your story has been saved and is now available for others to discover!")
        
        # Clear current story
        if 'current_story' in st.session_state:
            del st.session_state.current_story
        
        time.sleep(2)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def process_text_story(story_text):
    """Process typed story and create story record"""
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Generate story metadata
        status_text.text("🏷️ Analyzing story content...")
        progress_bar.progress(50)
        
        story_metadata = generate_story_metadata(story_text)
        
        # Step 2: Save story
        status_text.text("💾 Saving your story...")
        progress_bar.progress(100)
        
        save_complete_story(story_text, story_metadata)
        
        status_text.text("✅ Story saved successfully!")
        st.success("🎉 Your story has been saved and is now available for others to discover!")
        
        # Clear current story
        if 'current_story' in st.session_state:
            del st.session_state.current_story
        
        time.sleep(2)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error saving story: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def transcribe_audio(audio_file_path):
    """Transcribe audio file to text"""
    try:
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(audio_file_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)
        
        # Try to recognize speech
        transcript = recognizer.recognize_google(audio)
        return transcript
        
    except sr.UnknownValueError:
        st.warning("Could not understand the audio clearly. Please try speaking more clearly.")
        return None
    except sr.RequestError as e:
        st.error(f"Error with speech recognition service: {e}")
        return None
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
        return None

def generate_story_metadata(transcript):
    """Generate metadata for the story using AI"""
    ai_engine = AIEngine()
    story_data = st.session_state.current_story
    
    metadata = {
        "summary": "",
        "tags": [],
        "topics": [],
        "skills": [],
        "emotional_tone": {},
        "follow_up_questions": []
    }
    
    if ai_engine.is_ready():
        try:
            # Generate summary
            metadata["summary"] = ai_engine.generate_story_summary(transcript)
            
            # Extract tags and topics
            tag_data = ai_engine.extract_tags_and_topics(transcript, story_data["title"])
            metadata.update(tag_data)
            
            # Analyze emotional tone
            metadata["emotional_tone"] = ai_engine.analyze_emotional_tone(transcript)
            
            # Generate follow-up questions
            metadata["follow_up_questions"] = ai_engine.suggest_follow_up_questions(
                transcript, story_data["category"]
            )
            
        except Exception as e:
            st.warning(f"AI analysis failed, using basic metadata: {e}")
    
    # Fallback metadata
    if not metadata["summary"]:
        metadata["summary"] = transcript[:150] + "..." if len(transcript) > 150 else transcript
    
    return metadata

def save_complete_story(transcript, metadata, audio_bytes=None):
    """Save the complete story with all metadata"""
    story_data = st.session_state.current_story.copy()
    
    # Add transcript and metadata
    story_data.update({
        "transcript": transcript,
        "duration": len(transcript.split()) * 0.5,  # Rough estimate: 0.5 seconds per word
        **metadata
    })
    
    # Save to data manager
    data_manager = DataManager()
    story_id = data_manager.save_story(story_data)
    
    # Save audio file if provided
    if audio_bytes:
        config = Config()
        audio_filename = f"{story_id}.wav"
        audio_path = config.AUDIO_DIR / audio_filename
        
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        
        story_data["audio_file"] = str(audio_path)
        # Update story with audio file path
        data_manager.save_story(story_data)

def show_user_stories():
    """Show stories created by the current user"""
    st.markdown("### 📚 Your Stories")
    
    if 'elder_profile' not in st.session_state:
        st.warning("Please create your profile first.")
        return
    
    data_manager = DataManager()
    user_stories = data_manager.get_all_stories(
        contributor=st.session_state.elder_profile.get('name')
    )
    
    if not user_stories:
        st.info("You haven't recorded any stories yet. Click 'New Story' to get started!")
        return
    
    st.markdown(f"You have shared **{len(user_stories)}** stories with the community! 🎉")
    
    # Display stories
    for idx, story in enumerate(user_stories):
        with st.expander(f"📖 {story.get('title', 'Untitled Story')} - {story.get('category', '').replace('_', ' ').title()}"):
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Summary:** {story.get('summary', 'No summary available')}")
                st.write(f"**Created:** {story.get('created_at', 'Unknown')}")
                
                if story.get('tags'):
                    tags_html = " ".join([
                        f"<span style='background: #e3f2fd; padding: 0.2rem 0.6rem; border-radius: 10px; margin: 0.2rem; font-size: 0.8rem;'>{tag}</span>" 
                        for tag in story['tags']
                    ])
                    st.markdown("**Tags:** " + tags_html, unsafe_allow_html=True)
            
            with col2:
                st.metric("Duration", format_duration(story.get('duration', 0)))
                
                # Show emotional tone if available
                tone_data = story.get('emotional_tone', {})
                if tone_data.get('tone'):
                    st.write(f"**Tone:** {tone_data['tone'].title()}")
            
            # Show full transcript
            if st.button(f"View Full Story", key=f"view_story_{idx}"):
                st.markdown("**Full Story:**")
                st.write(story.get('transcript', 'No transcript available'))

def show_story_prompts():
    """Show story prompts and ideas for inspiration"""
    st.markdown("### 💡 Story Ideas & Prompts")
    st.markdown("Need inspiration? Here are some prompts to help you share your wisdom!")
    
    config = Config()
    
    # Category selector
    selected_category = st.selectbox(
        "Choose a topic area",
        options=list(config.STORY_CATEGORIES.keys()),
        format_func=lambda x: config.STORY_CATEGORIES[x]
    )
    
    prompts = get_sample_prompts(selected_category)
    
    if prompts:
        st.markdown(f"#### {config.STORY_CATEGORIES[selected_category]} Prompts")
        
        for idx, prompt in enumerate(prompts):
            with st.container():
                st.markdown(f"""
                <div style="
                    border-left: 4px solid #667eea;
                    padding: 1rem;
                    margin: 1rem 0;
                    background: #f8f9fa;
                    border-radius: 0 8px 8px 0;
                ">
                    <p style="margin: 0; font-style: italic; color: #2c3e50;">"{prompt}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Use This Prompt", key=f"prompt_{selected_category}_{idx}"):
                        # Set up story with this prompt
                        st.session_state.current_story = {
                            "title": "",
                            "category": selected_category,
                            "description": "",
                            "prompt": prompt,
                            "contributor_name": st.session_state.elder_profile.get('name', 'Anonymous'),
                            "contributor_id": st.session_state.elder_profile.get('id')
                        }
                        st.success(f"Prompt selected! Go to 'New Story' tab to start recording.")
    else:
        st.info("No prompts available for this category yet. Feel free to share any story from this topic!")
    
    # Tips for good storytelling
    with st.expander("📝 Tips for Great Storytelling"):
        st.markdown("""
        **Make your stories memorable:**
        
        - **Be specific:** Include details about time, place, and people
        - **Share emotions:** How did you feel? What did you learn?
        - **Include the lesson:** What wisdom can others take from your experience?
        - **Use simple language:** Speak as if talking to a friend
        - **Take your time:** Don't rush - pauses are okay!
        - **Be authentic:** Share both successes and challenges
        
        **Remember:** Every experience you've had is valuable to someone who hasn't lived it yet!
        """)
