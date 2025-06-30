import streamlit as st
import os
from PIL import Image
from datetime import datetime
from src.database import get_db_session, Story

def read_stories_page():
    """Page to display all shared stories with their cover photos"""
    
    st.header("� Read Amazing Stories")
    st.write("Discover inspiring stories shared by our community members!")

    try:
        with get_db_session() as session:
            # Fetch all stories, newest first
            stories = session.query(Story).order_by(Story.created_at.desc()).all()

        if not stories:
            st.info("📚 No stories have been shared yet. Be the first to share your story!")
            return

        # Create a grid layout for stories
        st.subheader(f"📚 {len(stories)} Stories Available")
        
        # Add filters
        col1, col2 = st.columns([1, 3])
        with col1:
            # Category filter
            all_categories = list(set([story.category.replace('_', ' ').title() for story in stories if story.category]))
            selected_category = st.selectbox(
                "Filter by Category:",
                ["All Categories"] + sorted(all_categories),
                key="category_filter"
            )
        
        # Filter stories based on selection
        filtered_stories = stories
        if selected_category != "All Categories":
            filtered_stories = [s for s in stories if s.category and s.category.replace('_', ' ').title() == selected_category]

        # Display stories in a grid
        for i, story in enumerate(filtered_stories):
            with st.container():
                # Create columns for layout
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display cover photo
                    if story.thumbnail_image_path and os.path.exists(story.thumbnail_image_path):
                        try:
                            image = Image.open(story.thumbnail_image_path)
                            st.image(image, caption="Story Cover", use_column_width=True)
                        except Exception as e:
                            st.error("🖼️ Cover photo unavailable")
                    else:
                        # Placeholder if no image
                        st.info("📷 No cover photo available")
                
                with col2:
                    # Story details
                    st.subheader(story.title)
                    
                    # Category badge
                    if story.category:
                        category_display = story.category.replace('_', ' ').title()
                        st.badge(category_display)
                    
                    # Story preview
                    preview_text = story.transcript[:150] + "..." if len(story.transcript) > 150 else story.transcript
                    st.write(preview_text)
                    
                    # Story metadata
                    story_date = story.created_at.strftime("%B %d, %Y") if story.created_at else "Unknown date"
                    st.caption(f"📅 Shared on {story_date}")
                    
                    # Read full story button
                    if st.button(f"📖 Read Full Story", key=f"read_{story.id}", type="secondary"):
                        st.session_state[f"show_story_{story.id}"] = True
                
                # Show full story if button was clicked
                if st.session_state.get(f"show_story_{story.id}", False):
                    st.markdown("---")
                    st.subheader(f"📖 {story.title}")
                    
                    # Show full cover photo
                    if story.thumbnail_image_path and os.path.exists(story.thumbnail_image_path):
                        try:
                            image = Image.open(story.thumbnail_image_path)
                            st.image(image, caption="Story Cover", width=400)
                        except:
                            pass
                    
                    # Full story text
                    st.write(story.transcript)
                    
                    # Close button
                    if st.button(f"❌ Close", key=f"close_{story.id}"):
                        st.session_state[f"show_story_{story.id}"] = False
                        st.rerun()
                
                st.markdown("---")

    except Exception as e:
        st.error(f"❌ Error loading stories: {str(e)}")
        st.write("Please check your database connection and try again.")

    # Footer information
    st.markdown("---")
    with st.expander("ℹ️ About StoryShare"):
        st.markdown("""
        **Welcome to StoryShare!** 
        
        This is a community platform where people can share their life experiences, 
        wisdom, adventures, and creative stories. Each story comes with a beautiful 
        cover photo chosen by the author.
        
        **Features:**
        - 📝 Easy story sharing with cover photos
        - 📂 Category organization
        - 🔍 Story filtering and discovery
        - 📱 Mobile-friendly interface
        """)
