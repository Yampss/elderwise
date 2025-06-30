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
- **Backend**: SQLAlchemy with PostgreSQL/SQLite
- **AI/ML**: Google Gemini API for transcription and analysis
- **Authentication**: bcrypt with session management
- **Storage**: Database + file system for audio files
- **Visualization**: Plotly for charts and analytics

## Development Guidelines

### Database Operations
- Use SQLAlchemy models for all database operations
- Use `get_db_session()` context manager for database transactions
- Implement proper error handling and rollback
- Use database relationships for data integrity

### Authentication
- All pages require authentication except login/register
- Use session state to store user information
- Implement role-based access control (elder/seeker/admin)
- Hash passwords with bcrypt

### Code Organization
- `app.py`: Main application entry point
- `src/database.py`: Database models and operations
- `src/auth.py`: Authentication and user management
- `src/config.py`: Configuration and environment variables
- `pages/`: User interface modules
- `setup_database.py`: Database initialization script

### Deployment Considerations
- Support both SQLite (development) and PostgreSQL (production)
- Use environment variables for configuration
- Implement proper database migrations
- Handle file storage for audio uploads
- Support cloud deployment (Heroku, Railway, etc.)

## Development Best Practices
- Always use database transactions
- Implement proper error handling
- Use environment variables for secrets
- Follow SQLAlchemy best practices
- Test database operations thoroughly
- Handle database connection failures gracefully
- Ensure all dependencies are listed in requirements.txt
- Set up proper environment variable handling
- Consider file storage limitations for production
- Plan for user data backup and recovery
