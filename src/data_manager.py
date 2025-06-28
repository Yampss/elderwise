import os
import json
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

from src.config import Config

class DataManager:
    """Manages data storage and retrieval for ElderWise"""
    
    def __init__(self):
        self.config = Config()
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        for dir_path in [
            self.config.DATA_DIR,
            self.config.STORIES_DIR, 
            self.config.AUDIO_DIR,
            self.config.TRANSCRIPTS_DIR,
            self.config.USER_DATA_DIR
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_story(self, story_data: Dict) -> str:
        """Save a story and return the story ID"""
        story_id = str(uuid.uuid4())
        story_data['id'] = story_id
        story_data['created_at'] = datetime.now().isoformat()
        story_data['updated_at'] = datetime.now().isoformat()
        
        # Save story metadata
        story_file = self.config.STORIES_DIR / f"{story_id}.json"
        with open(story_file, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        return story_id
    
    def get_story(self, story_id: str) -> Optional[Dict]:
        """Retrieve a story by ID"""
        story_file = self.config.STORIES_DIR / f"{story_id}.json"
        if story_file.exists():
            with open(story_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_all_stories(self, category: Optional[str] = None, 
                       contributor: Optional[str] = None) -> List[Dict]:
        """Get all stories, optionally filtered by category or contributor"""
        stories = []
        
        for story_file in self.config.STORIES_DIR.glob("*.json"):
            try:
                with open(story_file, 'r', encoding='utf-8') as f:
                    story = json.load(f)
                    
                    # Apply filters
                    if category and story.get('category') != category:
                        continue
                    if contributor and story.get('contributor_name') != contributor:
                        continue
                        
                    stories.append(story)
            except Exception as e:
                print(f"Error loading story {story_file}: {e}")
                continue
        
        # Sort by creation date (newest first)
        stories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return stories
    
    def search_stories(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search stories by text content"""
        all_stories = self.get_all_stories(category=category)
        matching_stories = []
        
        query_lower = query.lower()
        
        for story in all_stories:
            # Search in title, transcript, summary, and tags
            searchable_text = ' '.join([
                story.get('title', ''),
                story.get('transcript', ''),
                story.get('summary', ''),
                ' '.join(story.get('tags', []))
            ]).lower()
            
            if query_lower in searchable_text:
                matching_stories.append(story)
        
        return matching_stories
    
    def save_user_profile(self, user_data: Dict) -> str:
        """Save user profile and return user ID"""
        user_id = user_data.get('id', str(uuid.uuid4()))
        user_data['id'] = user_id
        user_data['updated_at'] = datetime.now().isoformat()
        
        if 'created_at' not in user_data:
            user_data['created_at'] = datetime.now().isoformat()
        
        user_file = self.config.USER_DATA_DIR / f"{user_id}.json"
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        
        return user_id
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Retrieve user profile by ID"""
        user_file = self.config.USER_DATA_DIR / f"{user_id}.json"
        if user_file.exists():
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_connection(self, connection_data: Dict) -> str:
        """Save a mentorship connection"""
        connection_id = str(uuid.uuid4())
        connection_data['id'] = connection_id
        connection_data['created_at'] = datetime.now().isoformat()
        connection_data['status'] = connection_data.get('status', 'pending')
        
        connections_file = self.config.DATA_DIR / "connections.json"
        connections = self._load_json_file(connections_file, [])
        connections.append(connection_data)
        
        with open(connections_file, 'w', encoding='utf-8') as f:
            json.dump(connections, f, indent=2, ensure_ascii=False)
        
        return connection_id
    
    def get_user_connections(self, user_id: str, user_type: str) -> List[Dict]:
        """Get connections for a user"""
        connections_file = self.config.DATA_DIR / "connections.json"
        connections = self._load_json_file(connections_file, [])
        
        user_connections = []
        for conn in connections:
            if user_type == "elder" and conn.get('elder_id') == user_id:
                user_connections.append(conn)
            elif user_type == "seeker" and conn.get('seeker_id') == user_id:
                user_connections.append(conn)
        
        return user_connections
    
    def update_connection_status(self, connection_id: str, status: str):
        """Update connection status"""
        connections_file = self.config.DATA_DIR / "connections.json"
        connections = self._load_json_file(connections_file, [])
        
        for conn in connections:
            if conn.get('id') == connection_id:
                conn['status'] = status
                conn['updated_at'] = datetime.now().isoformat()
                break
        
        with open(connections_file, 'w', encoding='utf-8') as f:
            json.dump(connections, f, indent=2, ensure_ascii=False)
    
    def save_question(self, question_data: Dict) -> str:
        """Save a question from wisdom seeker"""
        question_id = str(uuid.uuid4())
        question_data['id'] = question_id
        question_data['created_at'] = datetime.now().isoformat()
        question_data['status'] = question_data.get('status', 'open')
        
        questions_file = self.config.DATA_DIR / "questions.json"
        questions = self._load_json_file(questions_file, [])
        questions.append(question_data)
        
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        
        return question_id
    
    def get_questions(self, elder_id: Optional[str] = None, 
                     category: Optional[str] = None) -> List[Dict]:
        """Get questions, optionally filtered"""
        questions_file = self.config.DATA_DIR / "questions.json"
        questions = self._load_json_file(questions_file, [])
        
        if elder_id:
            questions = [q for q in questions if q.get('elder_id') == elder_id]
        if category:
            questions = [q for q in questions if q.get('category') == category]
        
        # Sort by creation date (newest first)
        questions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return questions
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get overall platform statistics"""
        stats = {
            'total_stories': len(list(self.config.STORIES_DIR.glob("*.json"))),
            'active_contributors': len(list(self.config.USER_DATA_DIR.glob("*.json"))),
            'connections_made': 0,
            'questions_answered': 0,
            'categories_covered': 0,
            'total_listening_time': 0.0,
            'stories_by_category': {},
            'recent_activity': []
        }
        
        # Count connections
        connections_file = self.config.DATA_DIR / "connections.json"
        connections = self._load_json_file(connections_file, [])
        stats['connections_made'] = len([c for c in connections if c.get('status') == 'accepted'])
        
        # Count answered questions
        questions_file = self.config.DATA_DIR / "questions.json"
        questions = self._load_json_file(questions_file, [])
        stats['questions_answered'] = len([q for q in questions if q.get('status') == 'answered'])
        
        # Stories by category
        stories = self.get_all_stories()
        category_counts = {}
        total_duration = 0.0
        
        for story in stories:
            category = story.get('category', 'other')
            category_counts[category] = category_counts.get(category, 0) + 1
            total_duration += story.get('duration', 0.0)
        
        stats['categories_covered'] = len(category_counts)
        stats['stories_by_category'] = category_counts
        stats['total_listening_time'] = total_duration / 3600  # Convert to hours
        
        # Recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_stories = [
            s for s in stories 
            if datetime.fromisoformat(s.get('created_at', '2020-01-01')) > week_ago
        ]
        stats['recent_activity'] = len(recent_stories)
        
        return stats
    
    def get_featured_stories(self, limit: int = 5) -> List[Dict]:
        """Get featured stories for the homepage"""
        all_stories = self.get_all_stories()
        
        # Simple algorithm: most recent stories with good ratings
        featured = []
        for story in all_stories:
            if len(featured) >= limit:
                break
            # For now, just use most recent
            featured.append(story)
        
        return featured
    
    def get_user_activity(self, user_id: str, user_type: str) -> Dict[str, Any]:
        """Get activity summary for a user"""
        activity = {
            'stories_contributed': 0,
            'stories_listened': 0,
            'connections_made': 0,
            'questions_asked': 0,
            'questions_answered': 0,
            'total_impact_score': 0
        }
        
        if user_type == "elder":
            # Count stories contributed
            stories = self.get_all_stories(contributor=user_id)
            activity['stories_contributed'] = len(stories)
            
            # Count connections
            connections = self.get_user_connections(user_id, "elder")
            activity['connections_made'] = len([c for c in connections if c.get('status') == 'accepted'])
            
            # Count questions answered
            questions = self.get_questions(elder_id=user_id)
            activity['questions_answered'] = len([q for q in questions if q.get('status') == 'answered'])
        
        elif user_type == "seeker":
            # Count connections
            connections = self.get_user_connections(user_id, "seeker")
            activity['connections_made'] = len([c for c in connections if c.get('status') == 'accepted'])
            
            # Count questions asked
            questions_file = self.config.DATA_DIR / "questions.json"
            questions = self._load_json_file(questions_file, [])
            activity['questions_asked'] = len([q for q in questions if q.get('seeker_id') == user_id])
        
        return activity
    
    def _load_json_file(self, file_path: Path, default: Any) -> Any:
        """Safely load a JSON file with fallback to default"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
        return default
    
    def export_data(self) -> Dict[str, Any]:
        """Export all platform data for backup/analysis"""
        return {
            'stories': self.get_all_stories(),
            'connections': self._load_json_file(self.config.DATA_DIR / "connections.json", []),
            'questions': self._load_json_file(self.config.DATA_DIR / "questions.json", []),
            'stats': self.get_platform_stats(),
            'export_date': datetime.now().isoformat()
        }
