import google.generativeai as genai
import json
import re
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from src.config import Config

class AIEngine:
    """AI-powered features using Gemini API"""
    
    def __init__(self):
        self.config = Config()
        self._configure_genai()
        
    def _configure_genai(self):
        """Configure the Gemini AI client"""
        api_key = self.config.get_gemini_api_key()
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            self.is_configured = True
        else:
            self.model = None
            self.is_configured = False
    
    def is_ready(self) -> bool:
        """Check if AI engine is ready to use"""
        return self.is_configured and self.model is not None
    
    def transcribe_audio_text(self, audio_text: str) -> str:
        """Process transcribed text to improve readability"""
        if not self.is_ready():
            return audio_text
        
        try:
            prompt = f"""
            Please clean up and improve the following transcribed text from an elderly person's story. 
            Fix any obvious transcription errors, add appropriate punctuation, and make it more readable 
            while preserving the original meaning and tone. Keep the personal, conversational style.
            
            Original text: {audio_text}
            
            Improved text:
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Error in transcription cleanup: {e}")
            return audio_text
    
    def generate_story_summary(self, transcript: str, max_length: int = 150) -> str:
        """Generate a concise summary of a story"""
        if not self.is_ready():
            return transcript[:max_length] + "..." if len(transcript) > max_length else transcript
        
        try:
            prompt = f"""
            Create a brief, engaging summary of this elderly person's story in {max_length} characters or less. 
            Capture the key wisdom or lesson shared. Make it compelling for younger readers.
            
            Story: {transcript}
            
            Summary:
            """
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            # Ensure it's within length limit
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            
            return summary
            
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            fallback = transcript[:max_length-3] + "..." if len(transcript) > max_length else transcript
            return fallback
    
    def extract_tags_and_topics(self, transcript: str, title: str = "") -> Dict[str, List[str]]:
        """Extract relevant tags and topics from story content"""
        if not self.is_ready():
            return {"tags": [], "topics": [], "skills": []}
        
        try:
            prompt = f"""
            Analyze this elderly person's story and extract relevant information:
            
            Title: {title}
            Story: {transcript}
            
            Please provide:
            1. Tags: 5-8 specific keywords that describe the story (e.g., "resilience", "family-business", "great-depression")
            2. Topics: 3-5 broader topic categories (e.g., "entrepreneurship", "family-relationships", "historical-events")
            3. Skills: 3-5 specific skills or knowledge areas mentioned (e.g., "budget-management", "customer-service", "problem-solving")
            
            Format your response as JSON:
            {
                "tags": ["tag1", "tag2", ...],
                "topics": ["topic1", "topic2", ...],
                "skills": ["skill1", "skill2", ...]
            }
            """
            
            response = self.model.generate_content(prompt)
            
            # Try to parse JSON response
            try:
                result = json.loads(response.text.strip())
                return {
                    "tags": result.get("tags", [])[:8],
                    "topics": result.get("topics", [])[:5],
                    "skills": result.get("skills", [])[:5]
                }
            except json.JSONDecodeError:
                # Fallback to regex extraction if JSON parsing fails
                return self._extract_tags_fallback(transcript, title)
                
        except Exception as e:
            logging.error(f"Error extracting tags: {e}")
            return self._extract_tags_fallback(transcript, title)
    
    def _extract_tags_fallback(self, transcript: str, title: str) -> Dict[str, List[str]]:
        """Fallback method for tag extraction without AI"""
        words = (title + " " + transcript).lower()
        
        # Common themes and keywords
        theme_keywords = {
            "family": ["family", "parent", "child", "marriage", "spouse"],
            "work": ["job", "career", "business", "work", "money"],
            "cooking": ["cook", "recipe", "food", "kitchen", "meal"],
            "wisdom": ["learn", "advice", "lesson", "experience"],
            "historical": ["war", "depression", "past", "history"],
            "challenges": ["difficult", "hard", "struggle", "overcome"],
            "relationships": ["friend", "love", "relationship", "people"],
            "skills": ["skill", "learn", "teach", "know", "craft"]
        }
        
        tags = []
        topics = []
        
        for topic, keywords in theme_keywords.items():
            if any(keyword in words for keyword in keywords):
                topics.append(topic)
                tags.extend([kw for kw in keywords if kw in words])
        
        return {
            "tags": list(set(tags))[:8],
            "topics": list(set(topics))[:5],
            "skills": ["life-experience", "wisdom-sharing"]
        }
    
    def categorize_story(self, transcript: str, title: str = "") -> str:
        """Automatically categorize a story into predefined categories"""
        if not self.is_ready():
            return self._categorize_fallback(transcript, title)
        
        categories = list(self.config.STORY_CATEGORIES.keys())
        category_descriptions = {k: v for k, v in self.config.STORY_CATEGORIES.items()}
        
        try:
            prompt = f"""
            Categorize this elderly person's story into one of the following categories:
            
            {json.dumps(category_descriptions, indent=2)}
            
            Title: {title}
            Story: {transcript}
            
            Choose the single most appropriate category key (not the display name) from the list above.
            Only respond with the category key (e.g., "life_skills" or "professional").
            """
            
            response = self.model.generate_content(prompt)
            predicted_category = response.text.strip().lower()
            
            # Validate the response
            if predicted_category in categories:
                return predicted_category
            else:
                return self._categorize_fallback(transcript, title)
                
        except Exception as e:
            logging.error(f"Error in categorization: {e}")
            return self._categorize_fallback(transcript, title)
    
    def _categorize_fallback(self, transcript: str, title: str) -> str:
        """Fallback categorization without AI"""
        text = (title + " " + transcript).lower()
        
        category_keywords = {
            "cooking": ["recipe", "cook", "food", "kitchen", "meal", "ingredient"],
            "professional": ["work", "job", "career", "business", "office", "boss"],
            "parenting": ["child", "parent", "kid", "family", "raise", "discipline"],
            "relationships": ["marriage", "love", "friend", "relationship", "spouse"],
            "health": ["health", "doctor", "medicine", "illness", "hospital"],
            "travel": ["travel", "trip", "journey", "place", "country", "visit"],
            "historical": ["war", "depression", "past", "history", "old days"],
            "cultural": ["tradition", "culture", "heritage", "custom", "celebration"],
            "crafts": ["craft", "hobby", "make", "create", "build", "art"],
            "life_skills": ["money", "budget", "home", "house", "practical"]
        }
        
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores.keys(), key=lambda k: scores[k])
        else:
            return "life_skills"  # Default category
    
    def analyze_emotional_tone(self, transcript: str) -> Dict[str, Any]:
        """Analyze the emotional tone of a story"""
        if not self.is_ready():
            return {"tone": "neutral", "confidence": 0.5, "emotions": []}
        
        try:
            prompt = f"""
            Analyze the emotional tone of this elderly person's story. 
            
            Story: {transcript}
            
            Provide your analysis in JSON format:
            {
                "tone": "inspiring/cautionary/humorous/nostalgic/educational/bittersweet",
                "confidence": 0.8,
                "emotions": ["hopeful", "wise", "reflective"],
                "mood_description": "Brief description of the overall mood"
            }
            
            The confidence should be between 0 and 1.
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                result = json.loads(response.text.strip())
                return {
                    "tone": result.get("tone", "neutral"),
                    "confidence": float(result.get("confidence", 0.5)),
                    "emotions": result.get("emotions", []),
                    "mood_description": result.get("mood_description", "")
                }
            except (json.JSONDecodeError, ValueError):
                return {"tone": "neutral", "confidence": 0.5, "emotions": []}
                
        except Exception as e:
            logging.error(f"Error in emotional analysis: {e}")
            return {"tone": "neutral", "confidence": 0.5, "emotions": []}
    
    def suggest_follow_up_questions(self, transcript: str, category: str) -> List[str]:
        """Suggest follow-up questions based on the story"""
        if not self.is_ready():
            return self._default_follow_up_questions(category)
        
        try:
            prompt = f"""
            Based on this elderly person's story, suggest 3-5 thoughtful follow-up questions that 
            young people might want to ask to learn more. Make them specific to the story content
            and designed to extract more wisdom or details.
            
            Story: {transcript}
            Category: {category}
            
            Format as a JSON list of strings:
            ["Question 1?", "Question 2?", "Question 3?"]
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                questions = json.loads(response.text.strip())
                return questions[:5] if isinstance(questions, list) else []
            except json.JSONDecodeError:
                return self._default_follow_up_questions(category)
                
        except Exception as e:
            logging.error(f"Error generating follow-up questions: {e}")
            return self._default_follow_up_questions(category)
    
    def _default_follow_up_questions(self, category: str) -> List[str]:
        """Default follow-up questions by category"""
        defaults = {
            "life_skills": [
                "What would you do differently if you could go back?",
                "How did you learn this skill?",
                "What advice would you give to someone starting out?"
            ],
            "professional": [
                "What was the workplace culture like back then?",
                "How did you handle difficult colleagues?",
                "What skills were most valuable in your career?"
            ],
            "relationships": [
                "How did people meet partners in your day?",
                "What kept your relationships strong?",
                "How did you resolve conflicts?"
            ]
        }
        
        return defaults.get(category, [
            "Can you tell me more about that experience?",
            "What did you learn from this situation?",
            "How did this change your perspective?"
        ])
    
    def match_mentor_seeker(self, seeker_interests: List[str], 
                           elder_expertise: List[str], 
                           seeker_goals: str = "") -> float:
        """Calculate compatibility score between seeker and elder"""
        if not self.is_ready():
            return self._simple_matching_score(seeker_interests, elder_expertise)
        
        try:
            prompt = f"""
            Calculate how well this elder and young person would match as mentor/mentee.
            
            Seeker interests: {seeker_interests}
            Elder expertise: {elder_expertise}
            Seeker goals: {seeker_goals}
            
            Provide a compatibility score between 0 and 1, where:
            - 0.0-0.3: Poor match
            - 0.4-0.6: Moderate match  
            - 0.7-0.8: Good match
            - 0.9-1.0: Excellent match
            
            Only respond with the numerical score (e.g., 0.75).
            """
            
            response = self.model.generate_content(prompt)
            
            try:
                score = float(response.text.strip())
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            except ValueError:
                return self._simple_matching_score(seeker_interests, elder_expertise)
                
        except Exception as e:
            logging.error(f"Error in mentor matching: {e}")
            return self._simple_matching_score(seeker_interests, elder_expertise)
    
    def _simple_matching_score(self, seeker_interests: List[str], 
                              elder_expertise: List[str]) -> float:
        """Simple keyword-based matching score"""
        if not seeker_interests or not elder_expertise:
            return 0.0
        
        seeker_set = set(word.lower() for word in seeker_interests)
        elder_set = set(word.lower() for word in elder_expertise)
        
        intersection = len(seeker_set.intersection(elder_set))
        union = len(seeker_set.union(elder_set))
        
        return intersection / union if union > 0 else 0.0
