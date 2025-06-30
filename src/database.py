"""
Database models and operations for ElderWise application
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from contextlib import contextmanager
from datetime import datetime
import os
from pathlib import Path
from src.config import Config

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)  # Allow null for no-login setup
    full_name = Column(String(100), nullable=False)
    user_type = Column(String(20), nullable=False)  # 'elder', 'seeker', 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    profile_complete = Column(Boolean, default=True)  # Set to True by default since we're skipping profile creation
    
    # Profile information
    age = Column(Integer)
    location = Column(String(100))
    bio = Column(Text)
    interests = Column(JSON)  # List of interests
    expertise_areas = Column(JSON)  # List of expertise areas for elders
    learning_goals = Column(JSON)  # List of learning goals for seekers
    
    # Relationships
    stories = relationship("Story", back_populates="author")
    connections_as_elder = relationship("Connection", foreign_keys="Connection.elder_id", back_populates="elder")
    connections_as_seeker = relationship("Connection", foreign_keys="Connection.seeker_id", back_populates="seeker")

class Story(Base):
    __tablename__ = 'stories'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    transcript = Column(Text, nullable=False)
    summary = Column(Text)
    audio_file_path = Column(String(500))
    thumbnail_image_path = Column(String(500))
    
    # AI-generated metadata
    tags = Column(JSON)  # List of tags
    topics = Column(JSON)  # List of topics
    skills = Column(JSON)  # List of skills
    emotional_tone = Column(JSON)  # Emotional analysis data
    
    # Story metrics
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="stories")
    interactions = relationship("StoryInteraction", back_populates="story")

class StoryInteraction(Base):
    __tablename__ = 'story_interactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    story_id = Column(Integer, ForeignKey('stories.id'), nullable=False)
    interaction_type = Column(String(20), nullable=False)  # 'view', 'like', 'save', 'comment'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # For comments and saves
    comment_text = Column(Text)
    
    # Relationships
    user = relationship("User")
    story = relationship("Story", back_populates="interactions")

class Connection(Base):
    __tablename__ = 'connections'
    
    id = Column(Integer, primary_key=True)
    elder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seeker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20), default='pending')  # 'pending', 'accepted', 'declined', 'active'
    
    # Connection details
    initial_message = Column(Text)
    connection_reason = Column(Text)
    topics = Column(JSON)  # Topics of interest
    preferred_contact = Column(String(100))
    
    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    
    # Relationships
    elder = relationship("User", foreign_keys=[elder_id], back_populates="connections_as_elder")
    seeker = relationship("User", foreign_keys=[seeker_id], back_populates="connections_as_seeker")

# Database configuration
class DatabaseManager:
    def __init__(self):
        self.database_url = Config.get_database_url()
        
        # Configure engine based on database type
        if 'postgresql' in self.database_url:
            # PostgreSQL configuration
            self.engine = create_engine(
                self.database_url,
                echo=os.getenv('ELDERWISE_DEBUG') == 'true',
                pool_pre_ping=True,  # For connection health checks
                pool_size=10,
                max_overflow=20
            )
        else:
            # SQLite configuration
            self.engine = create_engine(
                self.database_url,
                echo=os.getenv('ELDERWISE_DEBUG') == 'true',
                connect_args={"check_same_thread": False}  # SQLite specific
            )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a database session"""
        return self.SessionLocal()
    
    def drop_tables(self):
        """Drop all tables (for development/testing)"""
        Base.metadata.drop_all(bind=self.engine)

# Global database instance
db_manager = DatabaseManager()

def init_database():
    """Initialize the database with tables"""
    try:
        # Ensure data directory exists for SQLite
        if 'sqlite' in Config.get_database_url():
            Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
            Config.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create tables
        db_manager.create_tables()
        
        # Create default users if they don't exist
        with get_db_session() as session:
            if session.query(User).count() == 0:
                # Check if we need to create sample users
                sample_users = [
                    {
                        'username': 'admin_user',
                        'email': 'admin@elderwise.com',
                        'full_name': 'Administrator',
                        'user_type': 'admin',
                    },
                    {
                        'username': 'elder_user',
                        'email': 'elder@elderwise.com',
                        'full_name': 'Elder Smith',
                        'user_type': 'elder',
                    },
                    {
                        'username': 'seeker_user',
                        'email': 'seeker@elderwise.com', 
                        'full_name': 'Seeker Johnson',
                        'user_type': 'seeker',
                    }
                ]
                
                for user_data in sample_users:
                    user_exists = session.query(User).filter(User.username == user_data['username']).first()
                    if not user_exists:
                        new_user = User(**user_data)
                        session.add(new_user)
                
                session.commit()
                
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise

@contextmanager
def get_db_session():
    """Get a database session with automatic cleanup"""
    session = db_manager.get_session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
