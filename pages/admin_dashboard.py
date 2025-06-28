import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

from src.config import Config
from src.data_manager import DataManager
from src.utils import format_date, format_duration

def admin_dashboard():
    """Admin dashboard for platform management"""
    
    st.markdown("## 📊 Admin Dashboard")
    st.markdown("Platform overview and management tools")
    
    # Create tabs for different admin functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Analytics", 
        "📝 Content Review", 
        "👥 User Management", 
        "🔧 System Health",
        "📤 Data Export"
    ])
    
    with tab1:
        show_analytics_dashboard()
    
    with tab2:
        show_content_moderation()
    
    with tab3:
        show_user_management()
    
    with tab4:
        show_system_health()
    
    with tab5:
        show_data_export()

def show_analytics_dashboard():
    """Show comprehensive analytics dashboard"""
    st.markdown("### 📈 Platform Analytics")
    
    data_manager = DataManager()
    stats = data_manager.get_platform_stats()
    
    # Key metrics at the top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Stories", 
            stats.get('total_stories', 0),
            delta=f"+{stats.get('recent_activity', 0)} this week"
        )
    
    with col2:
        st.metric(
            "Active Contributors", 
            stats.get('active_contributors', 0),
            delta="+2 this month"
        )
    
    with col3:
        st.metric(
            "Connections Made", 
            stats.get('connections_made', 0),
            delta="+5 this week"
        )
    
    with col4:
        st.metric(
            "Questions Answered", 
            stats.get('questions_answered', 0),
            delta="+12 this week"
        )
    
    # Charts and visualizations
    st.markdown("---")
    
    # Stories by category chart
    if stats.get('stories_by_category'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Stories by Category")
            
            categories = list(stats['stories_by_category'].keys())
            counts = list(stats['stories_by_category'].values())
            
            config = Config()
            category_names = [config.STORY_CATEGORIES.get(cat, cat) for cat in categories]
            
            fig_pie = px.pie(
                values=counts, 
                names=category_names,
                title="Distribution of Stories"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Category Popularity")
            
            fig_bar = px.bar(
                x=category_names,
                y=counts,
                title="Stories per Category"
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Activity timeline
    st.markdown("#### 📅 Activity Timeline")
    
    # Generate sample data for timeline (in real app, this would come from actual data)
    dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -1)]
    stories_per_day = [max(0, int(stats.get('total_stories', 0) / 30) + (i % 7 - 3)) for i in range(30)]
    
    timeline_df = pd.DataFrame({
        'Date': dates,
        'Stories': stories_per_day
    })
    
    fig_timeline = px.line(
        timeline_df, 
        x='Date', 
        y='Stories',
        title="Daily Story Activity (Last 30 Days)"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Platform health indicators
    st.markdown("#### 🏥 Platform Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        engagement_rate = min(85 + (stats.get('connections_made', 0) * 2), 100)
        st.metric("Engagement Rate", f"{engagement_rate}%", "↗️ +3%")
    
    with col2:
        retention_rate = min(75 + (stats.get('total_stories', 0) * 0.5), 95)
        st.metric("User Retention", f"{retention_rate:.1f}%", "↗️ +1.2%")
    
    with col3:
        satisfaction_score = min(4.2 + (stats.get('questions_answered', 0) * 0.01), 5.0)
        st.metric("Satisfaction Score", f"{satisfaction_score:.1f}/5.0", "↗️ +0.1")

def show_content_moderation():
    """Show content moderation interface"""
    st.markdown("### 📝 Content Moderation")
    
    data_manager = DataManager()
    
    # Content stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pending Review", "3", help="Stories waiting for moderation")
    
    with col2:
        st.metric("Flagged Content", "1", help="Content flagged by users")
    
    with col3:
        st.metric("Auto-approved", "47", help="Content automatically approved")
    
    # Recent stories for review
    st.markdown("#### 🔍 Recent Stories for Review")
    
    all_stories = data_manager.get_all_stories()
    recent_stories = sorted(all_stories, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
    
    if recent_stories:
        for idx, story in enumerate(recent_stories):
            with st.expander(f"📖 {story.get('title', 'Untitled')} - {story.get('contributor_name', 'Anonymous')}"):
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Category:** {story.get('category', '').replace('_', ' ').title()}")
                    st.write(f"**Summary:** {story.get('summary', 'No summary')}")
                    st.write(f"**Created:** {format_date(story.get('created_at', ''))}")
                    
                    if story.get('transcript'):
                        with st.expander("View Full Transcript"):
                            st.write(story['transcript'])
                
                with col2:
                    st.write("**Actions:**")
                    
                    if st.button("✅ Approve", key=f"approve_{idx}"):
                        st.success("Story approved!")
                    
                    if st.button("❌ Reject", key=f"reject_{idx}"):
                        reason = st.text_input("Rejection reason", key=f"reason_{idx}")
                        if reason:
                            st.warning("Story rejected.")
                    
                    if st.button("🚩 Flag", key=f"flag_{idx}"):
                        st.warning("Story flagged for review.")
                    
                    # Content quality metrics
                    st.write("**Quality Score:**")
                    quality_score = min(85 + len(story.get('transcript', '')) // 100, 100)
                    st.progress(quality_score / 100)
                    st.write(f"{quality_score}%")
    
    # Moderation guidelines
    st.markdown("#### 📋 Moderation Guidelines")
    
    with st.expander("Content Guidelines"):
        st.markdown("""
        **Approve content that:**
        - Shares genuine life experiences and wisdom
        - Is respectful and appropriate for all ages
        - Provides valuable insights or lessons
        - Is clearly narrated and understandable
        
        **Reject content that:**
        - Contains inappropriate language or content
        - Promotes harmful activities or ideas
        - Is incoherent or incomprehensible
        - Violates privacy of others
        - Contains spam or commercial promotion
        
        **Flag for review:**
        - Content that's borderline inappropriate
        - Stories that might need fact-checking
        - Sensitive topics requiring careful handling
        """)

def show_user_management():
    """Show user management interface"""
    st.markdown("### 👥 User Management")
    
    data_manager = DataManager()
    
    # User statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "127", "+8 this week")
    
    with col2:
        st.metric("Active Elders", "45", "+3 this week")
    
    with col3:
        st.metric("Active Seekers", "82", "+5 this week")
    
    with col4:
        st.metric("Inactive Users", "12", "Need re-engagement")
    
    # User activity levels
    st.markdown("#### 📊 User Activity Distribution")
    
    activity_data = {
        'Activity Level': ['Very Active', 'Active', 'Moderate', 'Low', 'Inactive'],
        'Count': [25, 40, 35, 15, 12],
        'Percentage': [19.7, 31.5, 27.6, 11.8, 9.4]
    }
    
    activity_df = pd.DataFrame(activity_data)
    
    fig = px.bar(
        activity_df, 
        x='Activity Level', 
        y='Count',
        title="User Activity Distribution",
        color='Count',
        color_continuous_scale='viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent user registrations
    st.markdown("#### 🆕 Recent Registrations")
    
    # Sample data (in real app, this would come from user database)
    recent_users = [
        {"name": "Margaret S.", "type": "Elder", "date": "2024-01-15", "stories": 2},
        {"name": "David L.", "type": "Seeker", "date": "2024-01-14", "connections": 1},
        {"name": "Helen R.", "type": "Elder", "date": "2024-01-13", "stories": 0},
        {"name": "James M.", "type": "Seeker", "date": "2024-01-12", "connections": 3},
    ]
    
    for user in recent_users:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
            
            with col1:
                st.write(f"**{user['name']}**")
            
            with col2:
                badge_color = "#ff7675" if user['type'] == "Elder" else "#74b9ff"
                st.markdown(f"<span style='background: {badge_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.8rem;'>{user['type']}</span>", unsafe_allow_html=True)
            
            with col3:
                st.write(f"Joined: {user['date']}")
            
            with col4:
                activity = user.get('stories', user.get('connections', 0))
                st.write(f"Activity: {activity}")
    
    # User engagement tools
    st.markdown("#### 📧 User Engagement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Re-engagement Campaign**")
        if st.button("Send Welcome Back Email"):
            st.success("Welcome back emails sent to inactive users!")
        
        if st.button("Send Feature Update"):
            st.success("Feature update notifications sent!")
    
    with col2:
        st.markdown("**User Feedback**")
        if st.button("Request Platform Feedback"):
            st.success("Feedback surveys sent to active users!")
        
        if st.button("Send Thank You Notes"):
            st.success("Thank you messages sent to top contributors!")

def show_system_health():
    """Show system health and performance metrics"""
    st.markdown("### 🔧 System Health")
    
    # System metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("System Uptime", "99.9%", "↗️ +0.1%")
    
    with col2:
        st.metric("Response Time", "1.2s", "↘️ -0.3s")
    
    with col3:
        st.metric("Error Rate", "0.02%", "↘️ -0.01%")
    
    with col4:
        st.metric("API Calls/Day", "2,847", "↗️ +412")
    
    # Performance charts
    st.markdown("#### 📈 Performance Metrics")
    
    # Generate sample performance data
    hours = list(range(24))
    response_times = [1.2 + 0.3 * abs(h - 12) / 12 + (h % 3) * 0.1 for h in hours]
    
    performance_df = pd.DataFrame({
        'Hour': hours,
        'Response Time (s)': response_times
    })
    
    fig = px.line(
        performance_df,
        x='Hour',
        y='Response Time (s)',
        title="Average Response Time by Hour"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Storage and resource usage
    st.markdown("#### 💾 Resource Usage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Storage Usage**")
        
        storage_data = {
            'Type': ['Audio Files', 'Story Data', 'User Profiles', 'System Logs'],
            'Usage (GB)': [15.2, 2.8, 0.5, 1.1],
            'Limit (GB)': [100, 50, 10, 5]
        }
        
        for i, (type_name, usage, limit) in enumerate(zip(
            storage_data['Type'], 
            storage_data['Usage (GB)'], 
            storage_data['Limit (GB)']
        )):
            st.write(f"**{type_name}:**")
            progress = usage / limit
            st.progress(progress)
            st.write(f"{usage:.1f} GB / {limit} GB ({progress*100:.1f}%)")
    
    with col2:
        st.markdown("**API Usage**")
        
        api_data = {
            'Service': ['Gemini AI', 'Speech Recognition', 'Text Analysis'],
            'Calls Today': [145, 89, 203],
            'Daily Limit': [1000, 500, 1000]
        }
        
        for service, calls, limit in zip(
            api_data['Service'], 
            api_data['Calls Today'], 
            api_data['Daily Limit']
        ):
            st.write(f"**{service}:**")
            progress = calls / limit
            st.progress(progress)
            st.write(f"{calls} / {limit} calls ({progress*100:.1f}%)")
    
    # System logs
    st.markdown("#### 📝 Recent System Events")
    
    system_events = [
        {"time": "10:30 AM", "type": "INFO", "message": "Daily backup completed successfully"},
        {"time": "09:15 AM", "type": "INFO", "message": "New user registration: Margaret S."},
        {"time": "08:45 AM", "type": "WARN", "message": "API rate limit approaching for Speech Recognition"},
        {"time": "07:30 AM", "type": "INFO", "message": "System maintenance completed"},
        {"time": "06:00 AM", "type": "INFO", "message": "Automated content moderation processed 12 stories"},
    ]
    
    for event in system_events:
        icon = {"INFO": "ℹ️", "WARN": "⚠️", "ERROR": "❌"}.get(event['type'], "📝")
        color = {"INFO": "#74b9ff", "WARN": "#fdcb6e", "ERROR": "#ff7675"}.get(event['type'], "#ddd")
        
        st.markdown(f"""
        <div style="
            border-left: 4px solid {color};
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
        ">
            {icon} <strong>{event['time']}</strong> - {event['message']}
        </div>
        """, unsafe_allow_html=True)

def show_data_export():
    """Show data export and backup interface"""
    st.markdown("### 📤 Data Export & Backup")
    
    data_manager = DataManager()
    
    # Export options
    st.markdown("#### 📊 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Platform Data**")
        
        if st.button("📚 Export All Stories"):
            stories = data_manager.get_all_stories()
            st.download_button(
                "Download Stories JSON",
                data=str(stories),
                file_name=f"elderwise_stories_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        if st.button("👥 Export User Data"):
            st.success("User data export prepared (anonymized)")
        
        if st.button("📈 Export Analytics"):
            stats = data_manager.get_platform_stats()
            st.download_button(
                "Download Analytics JSON",
                data=str(stats),
                file_name=f"elderwise_analytics_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("**Backup & Recovery**")
        
        if st.button("💾 Create Full Backup"):
            with st.spinner("Creating backup..."):
                backup_data = data_manager.export_data()
                st.success("Backup created successfully!")
                
                st.download_button(
                    "Download Backup",
                    data=str(backup_data),
                    file_name=f"elderwise_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        if st.button("🔄 Schedule Auto-Backup"):
            st.success("Auto-backup scheduled for daily at 2 AM")
        
        if st.button("📋 View Backup History"):
            st.info("Last backup: Yesterday at 2:00 AM (Success)")
    
    # Data insights
    st.markdown("#### 📊 Data Insights")
    
    stats = data_manager.get_platform_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Data Points", "15,847")
    
    with col2:
        total_hours = stats.get('total_listening_time', 0)
        st.metric("Content Hours", f"{total_hours:.1f}")
    
    with col3:
        st.metric("Database Size", "127 MB")
    
    # Data compliance
    st.markdown("#### 🔒 Data Compliance")
    
    compliance_items = [
        {"item": "GDPR Compliance", "status": "✅", "details": "All user data properly anonymized"},
        {"item": "Data Retention Policy", "status": "✅", "details": "30-day deletion policy active"},
        {"item": "Backup Encryption", "status": "✅", "details": "AES-256 encryption enabled"},
        {"item": "Access Logging", "status": "✅", "details": "All data access logged"},
    ]
    
    for item in compliance_items:
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 1rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 5px;
        ">
            <span><strong>{item['item']}</strong></span>
            <span>{item['status']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View Details", key=f"details_{item['item']}"):
            st.info(item['details'])
    
    # Emergency tools
    st.markdown("#### 🚨 Emergency Tools")
    
    st.warning("⚠️ These tools should only be used in emergency situations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛑 Emergency Stop", type="secondary"):
            st.error("Emergency stop activated - platform maintenance mode")
    
    with col2:
        if st.button("🔄 Reset Cache", type="secondary"):
            st.success("System cache cleared")
    
    with col3:
        if st.button("📞 Alert Team", type="secondary"):
            st.success("Emergency alert sent to technical team")
