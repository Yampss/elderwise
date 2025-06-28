import streamlit as st
from datetime import datetime, timedelta
import uuid

from src.config import Config
from src.data_manager import DataManager
from src.ai_engine import AIEngine
from src.utils import format_date, format_duration, create_story_card

def community_features(user_type):
    """Community features for both elders and seekers"""
    
    if user_type == "elder":
        show_elder_community()
    else:
        show_seeker_community()

def show_elder_community():
    """Community features specifically for elders"""
    st.markdown("## 🤝 Your Community Impact")
    
    # Check if elder has profile
    if 'elder_profile' not in st.session_state:
        st.warning("Please create your profile first to access community features.")
        return
    
    elder_id = st.session_state.elder_profile.get('id')
    elder_name = st.session_state.elder_profile.get('name', 'Anonymous')
    
    # Tabs for different community features
    tab1, tab2, tab3, tab4 = st.tabs(["📞 Connection Requests", "❓ Questions", "📈 Your Impact", "🌟 Recognition"])
    
    with tab1:
        show_elder_connections(elder_id, elder_name)
    
    with tab2:
        show_elder_questions(elder_id, elder_name)
    
    with tab3:
        show_elder_impact_details(elder_id)
    
    with tab4:
        show_elder_recognition(elder_id)

def show_seeker_community():
    """Community features specifically for wisdom seekers"""
    st.markdown("## 🤝 Your Learning Journey")
    
    # Check if seeker has profile
    if 'seeker_profile' not in st.session_state:
        st.warning("Please create your profile first to access community features.")
        return
    
    seeker_id = st.session_state.seeker_profile.get('id')
    seeker_name = st.session_state.seeker_profile.get('name', 'Anonymous')
    
    # Tabs for different community features
    tab1, tab2, tab3, tab4 = st.tabs(["🤝 My Connections", "❓ Ask Questions", "📚 My Learning", "💡 Recommendations"])
    
    with tab1:
        show_seeker_connections(seeker_id, seeker_name)
    
    with tab2:
        show_ask_questions(seeker_id, seeker_name)
    
    with tab3:
        show_seeker_learning(seeker_id)
    
    with tab4:
        show_recommendations(seeker_id)

def show_elder_connections(elder_id, elder_name):
    """Show connection requests for elders"""
    st.markdown("### 📞 Connection Requests")
    
    data_manager = DataManager()
    connections = data_manager.get_user_connections(elder_id, "elder")
    
    if not connections:
        st.info("No connection requests yet. Keep sharing stories to attract wisdom seekers!")
        return
    
    # Separate pending and accepted connections
    pending_connections = [c for c in connections if c.get('status') == 'pending']
    accepted_connections = [c for c in connections if c.get('status') == 'accepted']
    
    # Pending requests
    if pending_connections:
        st.markdown("#### 🔔 Pending Requests")
        
        for conn in pending_connections:
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 1px solid #ffeaa7;
                    background: #fff9e6;
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">🤝 {conn.get('seeker_name', 'Anonymous')}</h4>
                    <p style="margin: 0.5rem 0;"><strong>About the story:</strong> {conn.get('story_title', 'Unknown story')}</p>
                    <p style="margin: 0.5rem 0;"><strong>Message:</strong> {conn.get('message', 'No message provided')}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                        <strong>Topics to discuss:</strong> {', '.join(conn.get('topics', []))}
                    </p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                        <strong>Preferred contact:</strong> {conn.get('preferred_contact', 'Any method')}
                    </p>
                    <p style="margin: 0; font-size: 0.8rem; color: #888;">
                        Requested on: {format_date(conn.get('created_at', ''))}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("✅ Accept", key=f"accept_{conn['id']}"):
                        data_manager.update_connection_status(conn['id'], 'accepted')
                        st.success(f"Connection accepted! You can now mentor {conn.get('seeker_name')}.")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Decline", key=f"decline_{conn['id']}"):
                        data_manager.update_connection_status(conn['id'], 'declined')
                        st.info("Connection request declined.")
                        st.rerun()
                
                with col3:
                    pass  # Spacer
    
    # Accepted connections
    if accepted_connections:
        st.markdown("#### ✅ Active Mentorships")
        
        for conn in accepted_connections:
            with st.expander(f"🤝 Mentoring {conn.get('seeker_name', 'Anonymous')}"):
                st.write(f"**Connected since:** {format_date(conn.get('updated_at', conn.get('created_at', '')))}")
                st.write(f"**Original story:** {conn.get('story_title', 'Unknown')}")
                st.write(f"**Topics of interest:** {', '.join(conn.get('topics', []))}")
                st.write(f"**Preferred contact:** {conn.get('preferred_contact', 'Any method')}")
                
                # Add communication tools
                st.markdown("**Quick Actions:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💬 Send Message", key=f"message_{conn['id']}"):
                        show_message_interface(conn)
                
                with col2:
                    if st.button("📅 Schedule Call", key=f"schedule_{conn['id']}"):
                        show_scheduling_interface(conn)

def show_elder_questions(elder_id, elder_name):
    """Show questions directed to the elder"""
    st.markdown("### ❓ Questions for You")
    
    data_manager = DataManager()
    questions = data_manager.get_questions(elder_id=elder_id)
    
    if not questions:
        st.info("No questions yet. As you share more stories, people will start asking for your advice!")
        return
    
    # Separate open and answered questions
    open_questions = [q for q in questions if q.get('status') == 'open']
    answered_questions = [q for q in questions if q.get('status') == 'answered']
    
    # Open questions
    if open_questions:
        st.markdown("#### 🔔 New Questions")
        
        for question in open_questions:
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 1px solid #74b9ff;
                    background: #f0f8ff;
                    padding: 1.5rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">❓ Question from {question.get('seeker_name', 'Anonymous')}</h4>
                    <p style="margin: 0.5rem 0; font-weight: bold;">{question.get('question', 'No question provided')}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                        <strong>Category:</strong> {question.get('category', 'General').replace('_', ' ').title()}
                    </p>
                    <p style="margin: 0; font-size: 0.8rem; color: #888;">
                        Asked on: {format_date(question.get('created_at', ''))}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Answer form
                with st.form(f"answer_form_{question['id']}"):
                    answer_text = st.text_area(
                        "Your answer",
                        height=120,
                        placeholder="Share your wisdom and experience...",
                        key=f"answer_{question['id']}"
                    )
                    
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if st.form_submit_button("Submit Answer"):
                            if answer_text.strip():
                                # Save answer and update question status
                                question['answer'] = answer_text
                                question['answered_by'] = elder_name
                                question['answered_at'] = datetime.now().isoformat()
                                question['status'] = 'answered'
                                
                                # Update in database (simplified - in real app would have proper answer storage)
                                data_manager.update_connection_status(question['id'], 'answered')
                                
                                st.success("Answer submitted! The person who asked will be notified.")
                                st.rerun()
                            else:
                                st.error("Please provide an answer.")
    
    # Answered questions
    if answered_questions:
        st.markdown("#### ✅ Questions You've Answered")
        
        for question in answered_questions:
            with st.expander(f"❓ {truncate_text(question.get('question', ''), 60)}"):
                st.write(f"**Question:** {question.get('question', '')}")
                st.write(f"**Your answer:** {question.get('answer', 'No answer recorded')}")
                st.write(f"**Answered on:** {format_date(question.get('answered_at', ''))}")

def show_elder_impact_details(elder_id):
    """Show detailed impact metrics for elder"""
    st.markdown("### 📈 Your Impact Details")
    
    data_manager = DataManager()
    activity = data_manager.get_user_activity(elder_id, "elder")
    
    # Impact metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Stories Shared", activity['stories_contributed'], help="Total number of stories you've recorded")
    
    with col2:
        estimated_listeners = activity['stories_contributed'] * 5  # Rough estimate
        st.metric("Estimated Listeners", estimated_listeners, help="Approximate number of people who've heard your stories")
    
    with col3:
        st.metric("Active Mentorships", activity['connections_made'], help="Number of people you're currently mentoring")
    
    with col4:
        st.metric("Questions Answered", activity['questions_answered'], help="Questions you've responded to")
    
    # Recent activity timeline
    st.markdown("#### 📅 Recent Activity")
    
    # Get recent stories
    user_stories = data_manager.get_all_stories(contributor=st.session_state.elder_profile.get('name'))
    recent_stories = user_stories[:5]  # Last 5 stories
    
    if recent_stories:
        for story in recent_stories:
            days_ago = (datetime.now() - datetime.fromisoformat(story.get('created_at', datetime.now().isoformat()))).days
            
            st.markdown(f"""
            <div style="
                border-left: 4px solid #00b894;
                padding: 1rem;
                margin: 0.5rem 0;
                background: #f8f9fa;
            ">
                <strong>📚 Shared story:</strong> {story.get('title', 'Untitled')} 
                <br><small>{days_ago} days ago</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Wisdom impact score
    st.markdown("#### 🌟 Wisdom Impact Score")
    
    # Calculate a simple impact score
    impact_score = (
        activity['stories_contributed'] * 10 +
        activity['connections_made'] * 25 +
        activity['questions_answered'] * 15
    )
    
    st.progress(min(impact_score / 500, 1.0))  # Max score of 500 for full bar
    st.write(f"**Score: {impact_score}/500**")
    
    if impact_score < 50:
        st.info("🌱 Just getting started! Keep sharing your stories to increase your impact.")
    elif impact_score < 150:
        st.success("🌿 Growing influence! Your wisdom is starting to reach people.")
    elif impact_score < 300:
        st.success("🌳 Strong impact! You're making a real difference in people's lives.")
    else:
        st.success("🏆 Wisdom leader! You're inspiring and guiding many people.")

def show_elder_recognition(elder_id):
    """Show recognition and achievements for elder"""
    st.markdown("### 🌟 Recognition & Achievements")
    
    data_manager = DataManager()
    activity = data_manager.get_user_activity(elder_id, "elder")
    
    # Calculate achievements
    achievements = []
    
    if activity['stories_contributed'] >= 1:
        achievements.append(("📚", "First Story", "Shared your first piece of wisdom"))
    
    if activity['stories_contributed'] >= 5:
        achievements.append(("🎯", "Story Teller", "Shared 5 stories"))
    
    if activity['stories_contributed'] >= 10:
        achievements.append(("📖", "Wisdom Keeper", "Shared 10 stories"))
    
    if activity['connections_made'] >= 1:
        achievements.append(("🤝", "First Connection", "Made your first mentorship connection"))
    
    if activity['connections_made'] >= 5:
        achievements.append(("👥", "Community Builder", "Mentoring 5 people"))
    
    if activity['questions_answered'] >= 10:
        achievements.append(("💡", "Advice Giver", "Answered 10 questions"))
    
    # Display achievements
    if achievements:
        st.markdown("#### 🏆 Your Achievements")
        
        cols = st.columns(min(3, len(achievements)))
        
        for idx, (emoji, title, description) in enumerate(achievements):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 1.5rem;
                    border: 2px solid #ffd700;
                    border-radius: 15px;
                    background: linear-gradient(135deg, #fff9c4, #ffd700);
                    margin: 0.5rem 0;
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                    <h4 style="margin: 0.5rem 0; color: #2c3e50;">{title}</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #555;">{description}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Community feedback
    st.markdown("#### 💬 Community Feedback")
    
    # Simulated feedback (in a real app, this would come from actual user feedback)
    sample_feedback = [
        {
            "text": "Your story about starting a business really inspired me to take the leap!",
            "author": "Sarah, 28",
            "story": "Starting with $50"
        },
        {
            "text": "Thank you for sharing your parenting wisdom. It helped me handle my teenager's attitude.",
            "author": "Mike, 45", 
            "story": "Raising Confident Kids"
        }
    ]
    
    for feedback in sample_feedback:
        st.markdown(f"""
        <div style="
            border-left: 4px solid #74b9ff;
            padding: 1rem;
            margin: 1rem 0;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
        ">
            <p style="margin: 0 0 0.5rem 0; font-style: italic;">"{feedback['text']}"</p>
            <small><strong>{feedback['author']}</strong> about your story <em>"{feedback['story']}"</em></small>
        </div>
        """, unsafe_allow_html=True)

def show_seeker_connections(seeker_id, seeker_name):
    """Show connections for wisdom seekers"""
    st.markdown("### 🤝 My Connections")
    
    data_manager = DataManager()
    connections = data_manager.get_user_connections(seeker_id, "seeker")
    
    if not connections:
        st.info("No connections yet. Start by discovering stories and connecting with elders who inspire you!")
        
        if st.button("🔍 Discover Stories"):
            st.session_state.switch_to_discovery = True
        
        return
    
    # Separate by status
    pending_connections = [c for c in connections if c.get('status') == 'pending']
    accepted_connections = [c for c in connections if c.get('status') == 'accepted']
    declined_connections = [c for c in connections if c.get('status') == 'declined']
    
    # Pending requests
    if pending_connections:
        st.markdown("#### ⏳ Pending Requests")
        
        for conn in pending_connections:
            st.markdown(f"""
            <div style="
                border: 1px solid #fdcb6e;
                background: #fff8e1;
                padding: 1rem;
                border-radius: 8px;
                margin: 0.5rem 0;
            ">
                <strong>🤝 Request to {conn.get('elder_name', 'Anonymous')}</strong><br>
                <small>About story: {conn.get('story_title', 'Unknown')}</small><br>
                <small>Sent: {format_date(conn.get('created_at', ''))}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Active connections
    if accepted_connections:
        st.markdown("#### ✅ Active Mentorships")
        
        for conn in accepted_connections:
            with st.expander(f"🤝 Mentorship with {conn.get('elder_name', 'Anonymous')}"):
                st.write(f"**Connected since:** {format_date(conn.get('updated_at', ''))}")
                st.write(f"**Original story:** {conn.get('story_title', 'Unknown')}")
                st.write(f"**Your message:** {conn.get('message', 'No message')}")
                
                # Communication tools
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💬 Send Message", key=f"msg_{conn['id']}"):
                        show_message_interface(conn)
                
                with col2:
                    if st.button("❓ Ask Question", key=f"ask_{conn['id']}"):
                        show_question_interface(conn)
    
    # Declined requests
    if declined_connections:
        with st.expander("❌ Declined Requests"):
            for conn in declined_connections:
                st.write(f"• Request to {conn.get('elder_name', 'Anonymous')} - Declined on {format_date(conn.get('updated_at', ''))}")

def show_ask_questions(seeker_id, seeker_name):
    """Interface for seekers to ask questions"""
    st.markdown("### ❓ Ask the Community")
    st.markdown("Have a specific question? Ask the community of wise elders!")
    
    # Question form
    with st.form("ask_question_form"):
        question_text = st.text_area(
            "What would you like to ask?",
            height=120,
            placeholder="e.g., How do I handle work stress? What's the secret to a happy marriage?",
            help="Be specific about your situation and what kind of advice you're looking for"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            config = Config()
            category = st.selectbox(
                "Category",
                options=list(config.STORY_CATEGORIES.keys()),
                format_func=lambda x: config.STORY_CATEGORIES[x],
                help="Choose the most relevant category"
            )
        
        with col2:
            urgency = st.selectbox(
                "Urgency",
                ["Low - General advice", "Medium - Would like answer soon", "High - Need guidance urgently"],
                help="How urgent is your need for this advice?"
            )
        
        submit_question = st.form_submit_button("Ask Question", type="primary")
        
        if submit_question and question_text.strip():
            # Save question
            data_manager = DataManager()
            
            question_data = {
                "question": question_text,
                "category": category,
                "urgency": urgency,
                "seeker_id": seeker_id,
                "seeker_name": seeker_name
            }
            
            question_id = data_manager.save_question(question_data)
            
            st.success("🎉 Your question has been posted! Elders in the community will see it and can respond.")
            st.info("💡 You'll be notified when someone answers your question.")
            
        elif submit_question and not question_text.strip():
            st.error("Please enter your question.")
    
    # Show user's previous questions
    st.markdown("---")
    st.markdown("### Your Previous Questions")
    
    data_manager = DataManager()
    questions_file = data_manager.config.DATA_DIR / "questions.json"
    all_questions = data_manager._load_json_file(questions_file, [])
    
    user_questions = [q for q in all_questions if q.get('seeker_id') == seeker_id]
    
    if not user_questions:
        st.info("You haven't asked any questions yet.")
        return
    
    for question in user_questions:
        status_color = {
            'open': '#fdcb6e',
            'answered': '#00b894'
        }.get(question.get('status', 'open'), '#ddd')
        
        status_text = {
            'open': 'Waiting for answer',
            'answered': 'Answered'
        }.get(question.get('status', 'open'), 'Unknown')
        
        with st.container():
            st.markdown(f"""
            <div style="
                border-left: 4px solid {status_color};
                padding: 1rem;
                margin: 1rem 0;
                background: #f8f9fa;
                border-radius: 0 8px 8px 0;
            ">
                <p style="margin: 0 0 0.5rem 0; font-weight: bold;">{question.get('question', '')}</p>
                <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                    <strong>Category:</strong> {question.get('category', '').replace('_', ' ').title()} | 
                    <strong>Status:</strong> {status_text} |
                    <strong>Asked:</strong> {format_date(question.get('created_at', ''))}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if question.get('status') == 'answered' and question.get('answer'):
                with st.expander("View Answer"):
                    st.write(f"**Answer by {question.get('answered_by', 'Anonymous')}:**")
                    st.write(question.get('answer', ''))
                    st.write(f"*Answered on {format_date(question.get('answered_at', ''))}*")

def show_seeker_learning(seeker_id):
    """Show learning progress and history for seeker"""
    st.markdown("### 📚 My Learning Journey")
    
    # Learning statistics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get favorites from session state
    favorites = st.session_state.get('favorites', [])
    
    with col1:
        st.metric("Stories Discovered", len(favorites), help="Stories you've read or listened to")
    
    with col2:
        st.metric("Categories Explored", "5", help="Different categories you've learned about")
    
    with col3:
        st.metric("Learning Hours", "12.5", help="Estimated time spent learning")
    
    with col4:
        st.metric("Connections Made", "3", help="Elders you're connected with")
    
    # Favorite stories
    if favorites:
        st.markdown("#### 💖 Your Favorite Stories")
        
        data_manager = DataManager()
        
        for story_id in favorites[:5]:  # Show first 5 favorites
            story = data_manager.get_story(story_id)
            if story:
                create_story_card(story)
    
    # Learning goals
    st.markdown("#### 🎯 Learning Goals")
    
    with st.form("learning_goals"):
        current_goals = st.text_area(
            "What are your current learning goals?",
            value=st.session_state.get('learning_goals', ''),
            height=100,
            placeholder="e.g., Learn to manage stress better, improve parenting skills, start a business..."
        )
        
        if st.form_submit_button("Update Goals"):
            st.session_state.learning_goals = current_goals
            st.success("Learning goals updated!")
    
    # Progress tracking
    st.markdown("#### 📈 Learning Progress")
    
    progress_areas = [
        ("Career Development", 0.7),
        ("Life Skills", 0.5),
        ("Relationships", 0.3),
        ("Personal Growth", 0.8)
    ]
    
    for area, progress in progress_areas:
        st.write(f"**{area}**")
        st.progress(progress)
        st.write(f"Progress: {int(progress * 100)}%")

def show_recommendations(seeker_id):
    """Show personalized recommendations for seeker"""
    st.markdown("### 💡 Personalized Recommendations")
    
    # Get user profile for personalization
    seeker_profile = st.session_state.get('seeker_profile', {})
    interests = seeker_profile.get('interests', [])
    
    if not interests:
        st.info("Complete your profile with interests to get personalized recommendations!")
        return
    
    # AI-powered recommendations would go here
    # For now, showing category-based recommendations
    
    st.markdown("#### 📚 Stories You Might Like")
    st.markdown(f"Based on your interests: {', '.join(interests)}")
    
    data_manager = DataManager()
    
    # Simple recommendation: get stories from user's interest categories
    recommended_stories = []
    
    for interest in interests:
        # Map interest to category key
        interest_lower = interest.lower().replace(' ', '_')
        stories = data_manager.get_all_stories(category=interest_lower)
        recommended_stories.extend(stories[:2])  # Top 2 from each category
    
    if recommended_stories:
        for story in recommended_stories[:6]:  # Show max 6 recommendations
            create_story_card(story)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📖 Read Story", key=f"rec_read_{story['id']}"):
                    st.session_state.recommended_story = story
            
            with col2:
                if st.button("🤝 Connect", key=f"rec_connect_{story['id']}"):
                    st.session_state.recommended_connection = story
    
    # Recommended elders to connect with
    st.markdown("#### 👥 Elders You Might Want to Connect With")
    
    # This would use AI matching in a real implementation
    st.info("🔄 AI-powered elder matching coming soon! For now, browse stories to find elders who share your interests.")
    
    # Learning path recommendations
    st.markdown("#### 🛤️ Suggested Learning Paths")
    
    learning_paths = [
        {
            "title": "🏢 Career Success Journey",
            "description": "From entry level to leadership",
            "stories": 12,
            "estimated_time": "4 hours"
        },
        {
            "title": "💰 Financial Wisdom Path", 
            "description": "Money management across life stages",
            "stories": 8,
            "estimated_time": "3 hours"
        },
        {
            "title": "❤️ Relationship Mastery",
            "description": "Building and maintaining strong relationships",
            "stories": 10,
            "estimated_time": "3.5 hours"
        }
    ]
    
    for path in learning_paths:
        with st.container():
            st.markdown(f"""
            <div style="
                border: 1px solid #e1e5e9;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{path['title']}</h4>
                <p style="margin: 0.5rem 0; color: #555;">{path['description']}</p>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #777;">
                    <span>📚 {path['stories']} stories</span>
                    <span>⏱️ {path['estimated_time']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Start Learning Path", key=f"path_{path['title']}"):
                st.success(f"Starting {path['title']}! Stories will be curated for your learning journey.")

def show_message_interface(connection):
    """Show messaging interface for connections"""
    st.markdown("### 💬 Send Message")
    
    with st.form("send_message"):
        message_text = st.text_area(
            f"Message to {connection.get('elder_name' if 'elder_name' in connection else 'seeker_name', 'Unknown')}",
            height=120,
            placeholder="Type your message here..."
        )
        
        if st.form_submit_button("Send Message"):
            if message_text.strip():
                st.success("Message sent! They'll be notified.")
                # In a real app, this would save to a messages database
            else:
                st.error("Please enter a message.")

def show_question_interface(connection):
    """Show interface to ask specific question to connected elder"""
    st.markdown("### ❓ Ask a Question")
    
    with st.form("ask_specific_question"):
        question_text = st.text_area(
            f"Question for {connection.get('elder_name', 'Unknown')}",
            height=120,
            placeholder="What specific advice would you like from this elder?"
        )
        
        if st.form_submit_button("Ask Question"):
            if question_text.strip():
                # Save as a directed question
                data_manager = DataManager()
                
                question_data = {
                    "question": question_text,
                    "elder_id": connection.get('elder_id'),
                    "seeker_id": connection.get('seeker_id'),
                    "seeker_name": connection.get('seeker_name'),
                    "connection_id": connection.get('id')
                }
                
                data_manager.save_question(question_data)
                st.success("Question sent! Your mentor will be notified.")
            else:
                st.error("Please enter your question.")

def show_scheduling_interface(connection):
    """Show interface to schedule calls with connections"""
    st.markdown("### 📅 Schedule a Call")
    
    with st.form("schedule_call"):
        col1, col2 = st.columns(2)
        
        with col1:
            preferred_date = st.date_input("Preferred Date")
        
        with col2:
            preferred_time = st.time_input("Preferred Time")
        
        call_type = st.selectbox(
            "Call Type",
            ["Video call", "Voice call", "In-person meeting (if local)"]
        )
        
        agenda = st.text_area(
            "What would you like to discuss?",
            height=80,
            placeholder="Brief agenda for the call..."
        )
        
        if st.form_submit_button("Send Scheduling Request"):
            if agenda.strip():
                st.success("Scheduling request sent! They'll respond with their availability.")
                # In a real app, this would integrate with calendar systems
            else:
                st.error("Please provide a brief agenda for the call.")

def truncate_text(text, max_length=100):
    """Helper function to truncate text"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
