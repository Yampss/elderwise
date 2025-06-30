"""
Simple session management for ElderWise (without authentication)
"""

import streamlit as st
from typing import Dict, Any

def init_session_state():
    """Initialize a mock user session state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
    if 'user' not in st.session_state:
        st.session_state.user = {
            'id': 0,
            'username': 'guest',
            'email': 'guest@example.com',
            'full_name': 'Guest User',
            'user_type': 'seeker',  # Default to 'seeker'
            'profile_complete': True,
            'age': None,
            'location': None,
            'bio': 'A guest user exploring ElderWise.',
            'interests': [],
            'expertise_areas': [],
            'learning_goals': []
        }
