
import streamlit as st
from src.database import get_db_session, Story

def seeker_tab():
    st.header("Discover Stories")

    with get_db_session() as session:
        stories = session.query(Story).order_by(Story.created_at.desc()).all()

    if not stories:
        st.info("No stories have been shared yet.")
        return

    for story in stories:
        st.subheader(story.title)
        if story.thumbnail_image_path:
            try:
                st.image(story.thumbnail_image_path, width=200)
            except Exception as e:
                st.warning(f"Could not load thumbnail: {e}")
        with st.expander("Read Story"):
            st.write(story.transcript)
        st.markdown("---")
