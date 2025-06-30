# ElderWise - Connecting Generations Through Stories

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Where wisdom meets wonder, and every story has the power to change a life.** 🌟

ElderWise is an AI-powered platform where seniors share their lifetime of knowledge and experiences with younger generations through intelligent storytelling, transcription, and mentorship matching.

## 🚀 Quick Start

### Local Development
```bash
git clone <repository-url>
cd elderwise
conda create -n elderwise python=3.11 -y
conda activate elderwise
pip install -r requirements.txt

# Setup database
python setup_database.py

# Run application
streamlit run app.py
```

### Production Deployment

#### Environment Variables
```bash
# Required
export GEMINI_API_KEY="your_gemini_api_key"
export DATABASE_URL="postgresql://user:pass@host:port/db"

# Optional
export ELDERWISE_DEBUG="false"
export MAX_UPLOAD_SIZE_MB="50"
```

#### Deploy to Heroku
```bash
# Install Heroku CLI, then:
heroku create your-elderwise-app
heroku addons:create heroku-postgresql:mini
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

#### Deploy to Railway
1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Deploy automatically

## 🗄️ Database

### Supported Databases
- **PostgreSQL** (recommended for production)
- **SQLite** (default for development)

### Database Setup
```bash
# Initialize database with sample data
python setup_database.py

# Or just create tables
python -c "from src.database import init_database; init_database()"
```

### Default Users (after setup_database.py)
- **Admin**: `admin` / `admin123`
- **Elder**: `margaret_smith` / `elder123`
- **Seeker**: `alex_johnson` / `seeker123`

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python, SQLAlchemy, PostgreSQL
- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Authentication**: bcrypt, session-based
- **Storage**: Database + file system (audio files)

### Database Schema
- **Users**: Authentication and profiles
- **Stories**: Content and metadata
- **Story Interactions**: Likes, saves, views
- **Connections**: Mentor-seeker relationships

## 📊 Features

- ✅ **User Authentication**: Secure registration and login
- ✅ **Story Recording**: Voice recording with AI transcription
- ✅ **Story Discovery**: Search and browse with AI categorization
- ✅ **User Profiles**: Rich profiles for elders and seekers
- ✅ **Admin Dashboard**: Platform management and analytics
- 🚧 **Mentorship Connections**: Elder-seeker matching (coming soon)
- 🚧 **Community Features**: Discussion and interaction (coming soon)

## 🔧 Development

### Running Tests
```bash
python test_db.py  # Test database connectivity
python -m pytest   # Run full test suite (when available)
```

### Migration Commands
```bash
# If using Alembic for migrations
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🚀 Deployment

### Production Checklist
- [ ] Set up PostgreSQL database
- [ ] Configure environment variables
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test audio upload functionality

### Scaling Considerations
- Database connection pooling
- File storage optimization (consider cloud storage)
- CDN for static assets
- Load balancing for multiple instances

---

**ElderWise**: Connecting generations through the power of shared stories and wisdom. 🌟
    └── connections.json  # Mentorship connections
```

## 💡 How It Works

### For Seniors
1. **Create Profile**: Share your background and areas of expertise
2. **Record Stories**: Use voice recording or text input to share experiences
3. **AI Enhancement**: Your stories are automatically transcribed and categorized
4. **Connect**: Respond to connection requests from interested learners
5. **Mentor**: Guide young people through direct conversations

### For Wisdom Seekers
1. **Create Profile**: Describe your interests and learning goals
2. **Discover**: Search and browse thousands of life stories
3. **Learn**: Listen to recordings or read transcripts
4. **Connect**: Request mentorship from inspiring storytellers
5. **Grow**: Apply wisdom gained to your own life challenges

## 🔧 Technical Details

### AI Integration
- **Google Gemini Pro**: Powers transcription, summarization, and content analysis
- **Smart Categorization**: Automatically sorts stories into relevant topics
- **Emotional Analysis**: Identifies the tone and mood of stories
- **Intelligent Matching**: Connects seekers with relevant mentors

### Data Storage
- **File-based Storage**: Simple JSON and file storage (no database required)
- **Privacy Focused**: User data stored locally with privacy controls
- **Scalable**: Easy to migrate to database when ready to scale

### User Experience
- **Accessibility First**: Large buttons, high contrast, simple navigation
- **Mobile Friendly**: Responsive design works on all devices
- **Progressive Enhancement**: Works without AI features if API unavailable

## 📊 Platform Stats

The platform tracks meaningful metrics:
- Stories shared and their impact
- Connections made between generations
- Questions answered and wisdom exchanged
- Cultural knowledge preserved
- Learning hours facilitated

## 🎯 Use Cases

### Personal Growth
- Young professionals seeking career advice
- New parents learning from experienced mothers/fathers
- Students navigating life transitions
- Anyone facing life challenges

### Cultural Preservation
- Traditional recipes and cooking techniques
- Historical perspectives from different eras
- Family traditions and cultural practices
- Language and dialect preservation

### Skill Transfer
- Professional expertise and industry knowledge
- Practical life skills and problem-solving
- Relationship wisdom and social skills
- Financial literacy and life management

## 🔒 Privacy & Safety

- **User Control**: Users control their privacy level and visibility
- **Content Moderation**: AI and human review ensure appropriate content
- **Safe Connections**: Structured mentorship with community guidelines
- **Data Protection**: Local storage with encryption options

## 🚀 Future Enhancements

### Phase 2 Features
- Advanced search with voice queries
- Group mentorship sessions
- Story challenges and prompts
- Mobile app for iOS/Android

### Phase 3 Features
- Integration with senior centers and libraries
- Corporate partnership programs
- Professional development tracks
- International language support

### Phase 4 Features
- VR/AR storytelling experiences
- AI-generated story illustrations
- Community events and workshops
- Academic research partnerships

## 🤝 Contributing

We welcome contributions! Areas where you can help:
- **Content**: Story prompts and categorization
- **Features**: New functionality and improvements
- **Accessibility**: Making the platform more inclusive
- **Documentation**: Improving guides and tutorials

## 📞 Support

For questions or support:
- Check the in-app help sections
- Review the story prompts for inspiration
- Contact the community moderators
- Submit feedback through the platform

## 🏆 Impact Goals

Our mission is to:
- **Preserve Wisdom**: Capture and share generational knowledge
- **Build Bridges**: Connect people across age gaps
- **Foster Learning**: Enable continuous personal growth
- **Strengthen Communities**: Create supportive intergenerational networks
- **Honor Elders**: Give seniors a platform to share their value

## 📜 License

This project is designed for community benefit and educational purposes. Please use responsibly and respect the privacy of all users.

---

**ElderWise**: Where wisdom meets wonder, and every story has the power to change a life. 🌟
