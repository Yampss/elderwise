import streamlit as st
import os
from PIL import Image
from datetime import datetime
from src.database import get_db_session, Story
import uuid

def share_story_page():
    """Page for users to share their stories with mandatory cover photo upload"""
    
    st.header("✍️ Share Your Story")
    st.write("Share your experiences, wisdom, or creative stories with the community!")

    with st.form("story_form", clear_on_submit=True):
        # Story details
        title = st.text_input(
            "Story Title *", 
            placeholder="Give your story an engaging title...",
            help="This will be the main headline for your story"
        )
        
        story_text = st.text_area(
            "Your Story *",
            placeholder="Write your story here... Share your experiences, lessons learned, adventures, or creative tales!",
            height=300,
            help="Tell your story in your own words. There's no limit to creativity!"
        )
        
        # Category selection
        category = st.selectbox(
            "Story Category *",
            ["Life Lessons", "Travel Adventures", "Career Journey", "Family Stories", 
             "Historical Memories", "Creative Fiction", "Inspirational", "Other"],
            help="Choose the category that best fits your story"
        )
        
        # Mandatory cover photo upload
        st.subheader("📸 Cover Photo")
        st.write("Upload an eye-catching cover photo for your story (Required)")
        
        uploaded_file = st.file_uploader(
            "Choose a cover photo *",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image that represents your story. This will be shown as a thumbnail."
        )
        
        # Preview uploaded image
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Cover Photo Preview", width=300)
        
        submitted = st.form_submit_button("📤 Share Story", type="primary", use_container_width=True)

        if submitted:
            # Validation
            errors = []
            if not title.strip():
                errors.append("Story title is required")
            if not story_text.strip():
                errors.append("Story content is required")
            if uploaded_file is None:
                errors.append("Cover photo is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                return

            try:
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Save uploaded image
                status_text.text("📁 Saving cover photo...")
                progress_bar.progress(33)
                
                # Create unique filename
                file_extension = uploaded_file.name.split('.')[-1]
                unique_filename = f"{uuid.uuid4()}.{file_extension}"
                image_path = os.path.join("data", "images", unique_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                
                # Save the uploaded file
                image = Image.open(uploaded_file)
                # Resize image for better performance (max width 800px)
                if image.width > 800:
                    ratio = 800 / image.width
                    new_height = int(image.height * ratio)
                    image = image.resize((800, new_height), Image.Resampling.LANCZOS)
                
                image.save(image_path, optimize=True, quality=85)

                # Save story to database
                status_text.text("💾 Saving your story...")
                progress_bar.progress(66)

                with get_db_session() as session:
                    new_story = Story(
                        title=title.strip(),
                        transcript=story_text.strip(),
                        category=category.lower().replace(' ', '_'),
                        thumbnail_image_path=image_path,
                        author_id=1,  # Default author for now
                        summary=story_text.strip()[:200] + "..." if len(story_text.strip()) > 200 else story_text.strip()
                    )
                    session.add(new_story)
                    session.commit()

                progress_bar.progress(100)
                status_text.text("✅ Story shared successfully!")
                
                st.success("🎉 Your story has been shared successfully!")
                st.balloons()
                
                # Show success info
                st.info(f"📖 Title: {title}")
                st.info(f"📂 Category: {category}")
                st.info(f"📝 Story length: {len(story_text.strip())} characters")

            except Exception as e:
                st.error(f"❌ Error saving story: {str(e)}")
                # Clean up image file if story save failed
                if 'image_path' in locals() and os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                    except:
                        pass

    # Instructions section
    with st.expander("💡 Tips for Great Stories"):
        st.markdown("""
        **📝 Writing Tips:**
        - Start with an engaging opening
        - Use descriptive language to paint a picture
        - Include dialogue when appropriate
        - End with a meaningful conclusion or lesson
        
        **📸 Photo Tips:**
        - Choose high-quality images
        - Ensure the photo relates to your story
        - Use landscape orientation for best results
        - File size should be under 10MB
        """)
