import streamlit as st
from src.database import get_db_session, Story, User
from src.ai_engine import AIEngine

def elder_tab():
    st.header("Share Your Story")

    title = st.text_input("Story Title")
    story_text = st.text_area("Your Story", height=300)

    if st.button("Submit Story"):
        if title and story_text:
            try:
                with get_db_session() as session:
                    # Get a mock user (or the first user)
                    user = session.query(User).first()
                    if not user:
                        st.error("No user found in the database. Please run the setup script.")
                        return

                    ai_engine = AIEngine()
                    
                    # Generate image from story (optional)
                    image_path = None
                    if ai_engine.is_ready():
                        st.info("Generating thumbnail image...")
                        image_path = ai_engine.generate_image_from_text(story_text)
                    
                    # Create and save the story
                    new_story = Story(
                        title=title,
                        transcript=story_text,
                        author_id=user.id,
                        category="Personal",
                        thumbnail_image_path=image_path
                    )
                    session.add(new_story)
                    session.commit()
                    st.success("Your story has been shared!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide both a title and a story.")
