# ElderWise Project Instructions

This is the ElderWise project - a platform connecting generations through storytelling and wisdom sharing.

## Project Overview
ElderWise is a Streamlit-based application that allows seniors to record and share their life stories and wisdom with younger generations. The platform uses AI (Google Gemini) for transcription, categorization, and intelligent matching between mentors and seekers.

## Key Features
- Voice recording interface for seniors
- AI-powered story transcription and analysis
- Story discovery portal for wisdom seekers
- Mentorship matching system
- Community features for intergenerational connections
- Admin dashboard for platform management

## Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **AI/ML**: Google Gemini API for transcription and analysis
- **Storage**: File-based JSON storage (no database required)
- **Audio**: Speech recognition and audio processing
- **Visualization**: Plotly for charts and analytics

## Development Guidelines

### Code Organization
- `app.py`: Main application entry point
- `src/`: Core modules (config, data management, AI engine, utilities)
- `pages/`: Different user interfaces (elder, seeker, community, admin)
- `data/`: Automatically created data storage directory

### AI Integration
- Always check API key availability before using AI features
- Provide fallbacks when AI services are unavailable
- Use the AIEngine class for all AI-related functionality

### User Experience
- Prioritize accessibility (large buttons, clear navigation)
- Support both seniors and young people with appropriate interfaces
- Maintain simple, intuitive design patterns

### Data Management
- Use DataManager class for all data operations
- Store user data with appropriate privacy controls
- Implement proper error handling for file operations

## Development Best Practices
- Follow Streamlit best practices for session state management
- Implement proper form validation and user feedback
- Use meaningful progress indicators for long operations
- Provide clear error messages and recovery options
- Test with different user types and scenarios

## API Usage
- Google Gemini API for transcription and text analysis
- Implement rate limiting and error handling
- Cache results when appropriate to reduce API calls
- Provide graceful degradation when API is unavailable

## Deployment Considerations
- Ensure all dependencies are listed in requirements.txt
- Set up proper environment variable handling
- Consider file storage limitations for production
- Plan for user data backup and recovery
