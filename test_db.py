#!/usr/bin/env python3
"""
Test script to verify database setup
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.database import init_database, get_db_session, User, Story
    
    print("✅ Imports successful")
    
    # Initialize database
    init_database()
    print("✅ Database initialized")
    
    # Test database connection
    with get_db_session() as session:
        user_count = session.query(User).count()
        story_count = session.query(Story).count()
        print(f"✅ Database connection successful")
        print(f"   Users in database: {user_count}")
        print(f"   Stories in database: {story_count}")
    
    print("\n🎉 All database tests passed! Your database is ready to use.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install missing packages with: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Database test failed: {e}")
    print("Please check your database configuration.")
