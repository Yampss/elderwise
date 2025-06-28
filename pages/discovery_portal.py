import streamlit as st
from datetime import datetime
import random

from src.config import Config
from src.data_manager import DataManager
from src.ai_engine import AIEngine
from src.utils import (
    create_story_card, create_category_filter, format_duration,
    create_user_profile_form, show_connection_request_form,
    create_featured_story_carousel, truncate_text
)

def wisdom_discovery_portal():
    """Main portal for discovering wisdom and stories"""
    
    # Check if user has profile
    if 'seeker_profile' not in st.session_state:
        st.markdown("## Welcome to ElderWise! 👋")
        st.markdown("Let's create your profile so elders can better connect with you and understand what you're looking for.")
        
        profile_data = create_user_profile_form("seeker")
        if profile_data:
            # Save profile
            data_manager = DataManager()
            user_id = data_manager.save_user_profile(profile_data)
            profile_data['id'] = user_id
            st.session_state.seeker_profile = profile_data
            st.success("Profile created! You can now start discovering wisdom.")
            st.rerun()
        return
    
    # Main discovery interface
    st.markdown("## 🔍 Discover Wisdom")
    st.markdown("Explore stories and experiences from elders who've walked many paths before you.")
    
    # Create tabs for different discovery methods
    tab1, tab2, tab3, tab4 = st.tabs(["🌟 Featured", "🔍 Search", "📂 Browse", "🎲 Random Discovery"])
    
    with tab1:
        show_featured_content()
    
    with tab2:
        show_search_interface()
    
    with tab3:
        show_browse_categories()
    
    with tab4:
        show_random_discovery()

def show_featured_content():
    """Show featured stories and trending content"""
    st.markdown("### ⭐ Featured Stories")
    st.markdown("Handpicked stories that our community loves")
    
    # Featured story carousel
    create_featured_story_carousel()
    
    # Trending topics
    st.markdown("### 📈 Trending Topics")
    data_manager = DataManager()
    stats = data_manager.get_platform_stats()
    
    if stats.get('stories_by_category'):
        # Sort categories by story count
        trending_categories = sorted(
            stats['stories_by_category'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        config = Config()
        cols = st.columns(len(trending_categories))
        
        for idx, (category, count) in enumerate(trending_categories):
            with cols[idx]:
                category_name = config.STORY_CATEGORIES.get(category, category.replace('_', ' ').title())
                
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 1rem;
                    border: 1px solid #e1e5e9;
                    border-radius: 10px;
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <h4 style="margin: 0.5rem 0; color: #2c3e50;">{category_name}</h4>
                    <p style="margin: 0; color: #667eea; font-weight: bold;">{count} stories</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Explore", key=f"trending_{category}"):
                    st.session_state.browse_category = category
                    st.rerun()
    
    # Quick stats
    st.markdown("### 📊 Community Impact")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Stories Shared", stats.get('total_stories', 0))
    with col2:
        st.metric("Active Elders", stats.get('active_contributors', 0))
    with col3:
        st.metric("Hours of Wisdom", f"{stats.get('total_listening_time', 0):.1f}")
    with col4:
        st.metric("Topics Covered", stats.get('categories_covered', 0))

def show_search_interface():
    """Show the search interface for finding specific stories"""
    st.markdown("### 🔍 Search for Wisdom")
    
    # Search form
    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "What would you like to learn about?",
                placeholder="e.g., 'starting a business', 'raising teenagers', 'dealing with loss'",
                help="Search through story transcripts, titles, and tags"
            )
        
        with col2:
            category_filter = create_category_filter()
        
        search_submitted = st.form_submit_button("Search", type="primary")
    
    # Search results
    if search_submitted and search_query:
        show_search_results(search_query, category_filter)
    elif 'last_search_query' in st.session_state:
        # Show last search results
        show_search_results(
            st.session_state.last_search_query, 
            st.session_state.get('last_search_category')
        )
    
    # Search suggestions
    if not search_submitted:
        show_search_suggestions()

def show_search_results(query, category=None):
    """Display search results"""
    st.session_state.last_search_query = query
    st.session_state.last_search_category = category
    
    data_manager = DataManager()
    
    # Get category key if category display name was selected
    category_key = None
    if category:
        config = Config()
        for key, value in config.STORY_CATEGORIES.items():
            if value == category:
                category_key = key
                break
    
    # Perform search
    matching_stories = data_manager.search_stories(query, category_key)
    
    st.markdown(f"### Search Results for '{query}'")
    
    if category:
        st.markdown(f"**Category:** {category}")
    
    if not matching_stories:
        st.info("No stories found matching your search. Try different keywords or browse by category.")
        
        # Suggest similar searches
        suggestions = [
            "Try broader keywords (e.g., 'work' instead of 'software engineering')",
            "Check different categories",
            "Browse featured stories for inspiration",
            "Ask the community a specific question"
        ]
        
        st.markdown("**Suggestions:**")
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")
        
        return
    
    st.markdown(f"Found **{len(matching_stories)}** stories")
    
    # Sort options
    sort_option = st.selectbox(
        "Sort by",
        ["Newest first", "Oldest first", "Most relevant"],
        key="search_sort"
    )
    
    if sort_option == "Oldest first":
        matching_stories.sort(key=lambda x: x.get('created_at', ''))
    elif sort_option == "Most relevant":
        # Simple relevance: count keyword matches
        query_words = set(query.lower().split())
        def relevance_score(story):
            text = ' '.join([
                story.get('title', ''),
                story.get('transcript', ''),
                story.get('summary', '')
            ]).lower()
            return sum(1 for word in query_words if word in text)
        
        matching_stories.sort(key=relevance_score, reverse=True)
    # "Newest first" is already the default order
    
    # Display results
    for story in matching_stories:
        create_story_card(story)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("📖 Read Full Story", key=f"read_{story['id']}"):
                show_full_story(story)
        
        with col2:
            if st.button("🤝 Connect with Elder", key=f"connect_{story['id']}"):
                show_connection_interface(story)
        
        with col3:
            if story.get('follow_up_questions'):
                with st.expander("💭 Ask Follow-up Questions"):
                    for question in story['follow_up_questions'][:3]:
                        st.write(f"• {question}")

def show_browse_categories():
    """Show category-based browsing"""
    st.markdown("### 📂 Browse by Category")
    
    config = Config()
    data_manager = DataManager()
    
    # Get story counts per category
    all_stories = data_manager.get_all_stories()
    category_counts = {}
    for story in all_stories:
        category = story.get('category', 'other')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Create category grid
    categories = list(config.STORY_CATEGORIES.items())
    
    # Split into rows of 3
    for i in range(0, len(categories), 3):
        cols = st.columns(3)
        
        for j, (category_key, category_name) in enumerate(categories[i:i+3]):
            if j < len(cols):
                with cols[j]:
                    count = category_counts.get(category_key, 0)
                    
                    # Category emoji mapping
                    category_emojis = {
                        "life_skills": "🏠", "professional": "💼", "cultural": "🌍",
                        "historical": "📜", "relationships": "❤️", "parenting": "👨‍👩‍👧‍👦",
                        "cooking": "🍳", "crafts": "🎨", "travel": "✈️", "health": "🏥"
                    }
                    
                    emoji = category_emojis.get(category_key, "📚")
                    
                    st.markdown(f"""
                    <div style="
                        text-align: center;
                        padding: 2rem 1rem;
                        border: 2px solid #e1e5e9;
                        border-radius: 15px;
                        background: white;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        margin: 1rem 0;
                        transition: all 0.3s ease;
                    ">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">{emoji}</div>
                        <h4 style="margin: 0.5rem 0; color: #2c3e50;">{category_name}</h4>
                        <p style="margin: 0; color: #667eea; font-weight: bold;">{count} stories</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Explore {category_name}", key=f"browse_{category_key}", use_container_width=True):
                        show_category_stories(category_key, category_name)

def show_category_stories(category_key, category_name):
    """Show all stories in a specific category"""
    st.markdown(f"### 📂 {category_name} Stories")
    
    data_manager = DataManager()
    category_stories = data_manager.get_all_stories(category=category_key)
    
    if not category_stories:
        st.info(f"No stories in {category_name} yet. Be the first to request one!")
        return
    
    st.markdown(f"**{len(category_stories)}** stories in this category")
    
    # Sort options
    sort_option = st.selectbox(
        "Sort by",
        ["Newest first", "Oldest first", "Alphabetical"],
        key=f"category_sort_{category_key}"
    )
    
    if sort_option == "Oldest first":
        category_stories.sort(key=lambda x: x.get('created_at', ''))
    elif sort_option == "Alphabetical":
        category_stories.sort(key=lambda x: x.get('title', '').lower())
    
    # Display stories
    for story in category_stories:
        create_story_card(story)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📖 Read Full Story", key=f"read_cat_{story['id']}"):
                show_full_story(story)
        
        with col2:
            if st.button("🤝 Connect with Elder", key=f"connect_cat_{story['id']}"):
                show_connection_interface(story)

def show_random_discovery():
    """Show random story discovery feature"""
    st.markdown("### 🎲 Random Discovery")
    st.markdown("Sometimes the best wisdom comes from unexpected places. Let serendipity guide your learning!")
    
    data_manager = DataManager()
    all_stories = data_manager.get_all_stories()
    
    if not all_stories:
        st.info("No stories available yet. Check back soon!")
        return
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🎲 Surprise Me!", type="primary", use_container_width=True):
            # Select random story
            random_story = random.choice(all_stories)
            st.session_state.random_story = random_story
    
    with col2:
        st.markdown("Discover wisdom you never knew you were looking for!")
    
    # Show random story if selected
    if 'random_story' in st.session_state:
        story = st.session_state.random_story
        
        st.markdown("---")
        st.markdown("### 🌟 Your Random Discovery")
        
        create_story_card(story, show_full=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🤝 Connect with Elder", key="random_connect"):
                show_connection_interface(story)
        
        with col2:
            if st.button("💖 Save to Favorites", key="random_favorite"):
                save_to_favorites(story)
        
        with col3:
            if st.button("🎲 Another Random Story", key="random_another"):
                random_story = random.choice(all_stories)
                st.session_state.random_story = random_story
                st.rerun()

def show_full_story(story):
    """Display full story in a modal-like interface"""
    st.markdown("---")
    st.markdown(f"## 📖 {story.get('title', 'Untitled Story')}")
    
    # Story metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Storyteller:** {story.get('contributor_name', 'Anonymous')}")
    with col2:
        st.write(f"**Category:** {story.get('category', '').replace('_', ' ').title()}")
    with col3:
        st.write(f"**Duration:** {format_duration(story.get('duration', 0))}")
    
    # Audio player if available
    if story.get('audio_file'):
        st.audio(story['audio_file'])
    
    # Full transcript
    st.markdown("### 📝 Full Story")
    st.write(story.get('transcript', 'No transcript available'))
    
    # Tags
    if story.get('tags'):
        st.markdown("### 🏷️ Tags")
        tags_html = " ".join([
            f"<span style='background: #e3f2fd; padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0.3rem; font-size: 0.9rem; display: inline-block;'>{tag}</span>" 
            for tag in story['tags']
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    # Emotional tone
    if story.get('emotional_tone', {}).get('tone'):
        tone_data = story['emotional_tone']
        st.markdown("### 💭 Story Tone")
        st.write(f"**Mood:** {tone_data['tone'].title()}")
        if tone_data.get('mood_description'):
            st.write(tone_data['mood_description'])
    
    # Follow-up questions
    if story.get('follow_up_questions'):
        st.markdown("### ❓ Questions You Might Ask")
        for question in story['follow_up_questions']:
            st.write(f"• {question}")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤝 Connect with This Elder", key="full_story_connect"):
            show_connection_interface(story)
    
    with col2:
        if st.button("💖 Save to Favorites", key="full_story_favorite"):
            save_to_favorites(story)
    
    with col3:
        if st.button("📤 Share Story", key="full_story_share"):
            show_share_interface(story)

def show_connection_interface(story):
    """Show interface to connect with the story's contributor"""
    st.markdown("---")
    st.markdown("### 🤝 Connect with the Storyteller")
    
    elder_name = story.get('contributor_name', 'Anonymous')
    elder_id = story.get('contributor_id')
    
    if not elder_id:
        st.error("Unable to connect - elder profile not available.")
        return
    
    st.write(f"**Storyteller:** {elder_name}")
    st.write(f"**Story:** {story.get('title', 'Untitled')}")
    
    connection_data = show_connection_request_form(elder_id, elder_name)
    
    if connection_data:
        # Save connection request
        data_manager = DataManager()
        
        # Add seeker information
        connection_data.update({
            "seeker_id": st.session_state.seeker_profile.get('id'),
            "seeker_name": st.session_state.seeker_profile.get('name'),
            "story_id": story.get('id'),
            "story_title": story.get('title')
        })
        
        connection_id = data_manager.save_connection(connection_data)
        
        st.success(f"🎉 Connection request sent to {elder_name}! They'll be notified and can respond through the platform.")
        st.info("💡 Tip: Check your 'My Connections' tab to track the status of your requests.")

def show_search_suggestions():
    """Show search suggestions and popular queries"""
    st.markdown("### 💡 Popular Searches")
    st.markdown("Get inspired by what others are looking for:")
    
    popular_searches = [
        "Starting a business",
        "Raising teenagers", 
        "Dealing with loss",
        "Career change advice",
        "Finding love later in life",
        "Financial planning",
        "Overcoming failure",
        "Family traditions",
        "Travel adventures",
        "Health and wellness"
    ]
    
    # Display as clickable buttons
    cols = st.columns(3)
    for idx, search_term in enumerate(popular_searches):
        with cols[idx % 3]:
            if st.button(search_term, key=f"suggest_{idx}"):
                st.session_state.suggested_search = search_term
                st.rerun()
    
    # If a suggestion was clicked, perform the search
    if 'suggested_search' in st.session_state:
        show_search_results(st.session_state.suggested_search)
        del st.session_state.suggested_search

def save_to_favorites(story):
    """Save story to user's favorites"""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    story_id = story.get('id')
    if story_id not in st.session_state.favorites:
        st.session_state.favorites.append(story_id)
        st.success("💖 Story saved to your favorites!")
    else:
        st.info("This story is already in your favorites.")

def show_share_interface(story):
    """Show story sharing interface"""
    st.markdown("### 📤 Share This Story")
    
    share_text = f"Check out this amazing story on ElderWise: '{story.get('title', 'Untitled')}' by {story.get('contributor_name', 'Anonymous')}"
    
    st.text_area(
        "Share text (copy this)",
        value=share_text,
        height=80,
        help="Copy this text to share on social media or with friends"
    )
    
    st.markdown("**Share on:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("📧 [Email](mailto:?subject=Amazing Story from ElderWise&body=" + share_text.replace(' ', '%20') + ")")
    
    with col2:
        st.markdown("💬 [WhatsApp](https://wa.me/?text=" + share_text.replace(' ', '%20') + ")")
    
    with col3:
        st.markdown("🐦 [Twitter](https://twitter.com/intent/tweet?text=" + share_text.replace(' ', '%20') + ")")
