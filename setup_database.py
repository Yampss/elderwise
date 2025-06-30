#!/usr/bin/env python3
"""
Database setup and migration script for ElderWise
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from src.database import init_database, get_db_session, User, Story, db_manager

def setup_database():
    """Set up the database with initial data"""
    print("🔧 Setting up ElderWise database...")
    print(f"🗄️  Database type: {'PostgreSQL' if 'postgresql' in os.getenv('DATABASE_URL', '') else 'SQLite'}")
    
    try:
        # Drop all tables first
        print("⚠️  Dropping all existing tables...")
        db_manager.drop_tables()
        print("✅ Tables dropped successfully.")

        # Initialize database
        init_database()
        print("✅ Database tables created successfully")
        
        # Check if we need to create sample data
        with get_db_session() as session:
            user_count = session.query(User).count()
            story_count = session.query(Story).count()
            
            print(f"📊 Current database state:")
            print(f"   - Users: {user_count}")
            print(f"   - Stories: {story_count}")
            
            if user_count == 0:
                print("🎯 Creating sample users...")
                create_sample_users(session)
            else:
                print("ℹ️  Users already exist, skipping sample data creation")
                
        print("🎉 Database setup completed successfully!")
        print("\n📝 Default login credentials:")
        print("   - Admin: admin / admin123")
        print("   - Elder: margaret_smith / elder123") 
        print("   - Seeker: alex_johnson / seeker123")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print(f"💡 Make sure your database is running and environment variables are set correctly")
        sys.exit(1)

def create_sample_users(session):
    """Create sample users for testing"""
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@elderwise.com',
        full_name='System Administrator',
        user_type='admin',
        profile_complete=True
    )
    session.add(admin)
    
    # Create sample elder
    elder = User(
        username='margaret_smith',
        email='margaret@example.com',
        full_name='Margaret Smith',
        user_type='elder',
        age=67,
        location='Portland, OR',
        bio='Retired teacher with 35 years of experience. Love sharing stories about education and family life.',
        expertise_areas=['Education', 'Parenting', 'Life Skills'],
        profile_complete=True
    )
    session.add(elder)
    
    # Create sample seeker
    seeker = User(
        username='alex_johnson',
        email='alex@example.com',
        full_name='Alex Johnson',
        user_type='seeker',
        age=24,
        location='San Francisco, CA',
        bio='Recent college graduate looking for career guidance and life advice.',
        interests=['Career Development', 'Life Skills', 'Finance'],
        learning_goals=['Find career direction', 'Learn financial planning', 'Develop life skills'],
        profile_complete=True
    )
    session.add(seeker)
    
    session.commit()
    print("✅ Sample users created")

if __name__ == "__main__":
    setup_database()
