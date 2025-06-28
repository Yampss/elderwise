# ElderWise - Connecting Generations Through Stories

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/elderwise/workflows/ElderWise%20CI/CD/badge.svg)](https://github.com/yourusername/elderwise/actions)

> **Where wisdom meets wonder, and every story has the power to change a life.** 🌟

ElderWise is an AI-powered platform where seniors share their lifetime of knowledge and experiences with younger generations through intelligent storytelling, transcription, and mentorship matching.

## 🌟 Features

### For Seniors (Elders)
- **Voice Recording Interface**: Simple, large-button design for easy story recording
- **AI-Powered Transcription**: Automatic conversion of speech to text using Google Gemini
- **Story Organization**: AI categorizes and tags stories for easy discovery
- **Impact Tracking**: See how your wisdom is helping others
- **Mentorship Opportunities**: Connect with young people seeking guidance

### For Young People (Wisdom Seekers)
- **Smart Discovery**: Search and browse stories by topic, category, or keyword
- **Personalized Recommendations**: AI suggests relevant stories based on interests
- **Direct Connections**: Request mentorship from inspiring elders
- **Learning Paths**: Curated series of related stories for structured learning
- **Question & Answer**: Ask specific questions to the community

### AI-Powered Features
- **Automatic Transcription**: Convert voice recordings to searchable text
- **Smart Categorization**: AI identifies story topics and themes
- **Content Analysis**: Extract key insights, emotional tone, and wisdom nuggets
- **Intelligent Matching**: Connect seekers with relevant mentors
- **Story Summarization**: Generate compelling summaries for discovery

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Anaconda or Miniconda (recommended)
- Google Gemini API key (free tier available)

### Quick Setup with Conda (Recommended)

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd elderwise
   ```

2. **Create and activate conda environment**
   ```bash
   # Windows
   conda create -n elderwise python=3.11 -y
   conda activate elderwise
   
   # Or use the setup script
   setup_env.bat
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key for use in the application

5. **Run the application**
   ```bash
   streamlit run app.py
   # Or use the run script
   run.bat
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Enter your Gemini API key when prompted
   - Choose your user type (Senior or Wisdom Seeker)

### Alternative Setup (without conda)

If you prefer not to use conda:

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd elderwise
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key for use in the application

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Enter your Gemini API key when prompted
   - Choose your user type (Senior or Wisdom Seeker)

## 🏗️ Project Structure

```
elderwise/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/                  # Core application modules
│   ├── config.py         # Configuration and settings
│   ├── data_manager.py   # Data storage and retrieval
│   ├── ai_engine.py      # AI-powered features
│   └── utils.py          # Utility functions
├── pages/                # Application pages
│   ├── elder_interface.py     # Senior recording interface
│   ├── discovery_portal.py    # Story discovery for seekers
│   ├── community.py           # Community features
│   └── admin_dashboard.py     # Admin management interface
└── data/                 # Data storage (created automatically)
    ├── stories/          # Story metadata and transcripts
    ├── audio/            # Audio recordings
    ├── users/            # User profiles
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
