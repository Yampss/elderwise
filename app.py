import streamlit as st
from src.database import init_database
from src.utils import setup_page_config, setup_directories
from tabs.elder_tab import elder_tab
from tabs.seeker_tab import seeker_tab

def main():
    """Main application entry point"""
    
    setup_page_config()
    setup_directories()
    
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()

    st.title("ElderWise")

    tab1, tab2 = st.tabs(["Share a Story", "Discover Stories"])

    with tab1:
        elder_tab()

    with tab2:
        seeker_tab()

if __name__ == "__main__":
    main()
