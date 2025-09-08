#!/usr/bin/env python3
"""
Pattern Matching System
=======================

This module handles conversation pattern matching and knowledge base operations.
It stores and retrieves conversational patterns based on query analysis.

Flow: Query Analysis → Pattern Search → Best Match Selection → Response Template
"""

import sqlite3
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class PatternMatch:
    """Result of pattern matching"""
    pattern_id: int
    category: str
    keywords: str
    response_template: str
    confidence: float
    usage_count: int
    success_rate: float

class PatternMatcher:
    """
    Conversation pattern matching and knowledge base system
    
    Responsibilities:
    1. Store conversation patterns and responses
    2. Match user queries to existing patterns
    3. Provide response templates based on best matches
    4. Learn from usage patterns and success rates
    """
    
    def __init__(self, db_path: str = "base_agent.db"):
        """Initialize pattern matcher with database"""
        self.db_path = db_path
        self._local = threading.local()
        self._init_database()
        self._load_base_patterns()
    
    def _get_connection(self):
        """Get a thread-safe database connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,
                timeout=30.0
            )
            # Enable WAL mode for better concurrency
            self._local.connection.execute("PRAGMA journal_mode = WAL")
            self._local.connection.execute("PRAGMA synchronous = NORMAL")
        return self._local.connection
    
    def _close_connection(self):
        """Close the current thread's database connection"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
    
    def _init_database(self):
        """Initialize SQLite database with pattern tables"""
        try:
            conn = self._get_connection()
            
            # Main patterns table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversation_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    keywords TEXT NOT NULL,
                    response_template TEXT NOT NULL,
                    confidence REAL DEFAULT 90.0,
                    usage_count INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Pattern feedback table for learning
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pattern_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_id INTEGER,
                    query TEXT,
                    was_helpful BOOLEAN,
                    user_feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pattern_id) REFERENCES conversation_patterns (id)
                )
            ''')
            
            conn.commit()
            print("✅ Pattern matcher database initialized")
            
        except Exception as e:
            print(f"❌ Error initializing pattern database: {e}")
    
    def _load_base_patterns(self):
        """Load essential conversation patterns"""
        try:
            conn = self._get_connection()
            
            base_patterns = [
                # === BASIC GREETINGS ===
                {
                    'category': 'GREETING',
                    'keywords': 'hi hello hey greetings good morning good afternoon good evening',
                    'response_template': 'Hello! I\'m your AI assistant. I can help you with technical questions, provide guidance, and assist with various tools and technologies. What would you like to know about?',
                    'confidence': 95.0
                },
                {
                    'category': 'GREETING',
                    'keywords': 'howdy whats up sup how are you doing',
                    'response_template': 'Hey there! I\'m doing great and ready to help you out. What can I assist you with today?',
                    'confidence': 92.0
                },
                {
                    'category': 'GREETING',
                    'keywords': 'good night bye goodbye see you later talk to you later',
                    'response_template': 'Goodbye! It was great helping you today. Feel free to come back anytime you need assistance. Have a wonderful day!',
                    'confidence': 94.0
                },
                
                # === PERSONAL INTERACTION ===
                {
                    'category': 'PERSONAL',
                    'keywords': 'how are you how you doing how is your day',
                    'response_template': 'I\'m doing well, thank you for asking! I\'m here and ready to help you with whatever you need. How are you doing today?',
                    'confidence': 90.0
                },
                {
                    'category': 'PERSONAL',
                    'keywords': 'who are you what are you tell me about yourself introduce yourself',
                    'response_template': 'I\'m an AI assistant designed to help you with technical questions and various tasks. I have access to a wide range of knowledge and can provide step-by-step guidance, explanations, and troubleshooting support. I\'m here to make your work easier and more efficient. What would you like to know more about?',
                    'confidence': 93.0
                },
                {
                    'category': 'PERSONAL',
                    'keywords': 'nice to meet you pleasure to meet you good to meet you',
                    'response_template': 'Nice to meet you too! I\'m excited to help you with whatever you\'re working on. What brings you here today?',
                    'confidence': 88.0
                },
                
                # === CAPABILITIES & FEATURES ===
                {
                    'category': 'CAPABILITIES',
                    'keywords': 'what can you do capabilities features help assist support',
                    'response_template': 'I can help you with:\n\n• Technical guidance and explanations\n• Step-by-step instructions\n• Troubleshooting and problem solving\n• Best practices and recommendations\n• Tool-specific knowledge through plugins\n\nWhat specific area would you like assistance with?',
                    'confidence': 95.0
                },
                {
                    'category': 'CAPABILITIES',
                    'keywords': 'what else can you do more capabilities additional features what other things',
                    'response_template': 'I have quite a few capabilities! Beyond basic help, I can:\n\n• Provide detailed technical explanations\n• Walk through complex procedures step-by-step\n• Help debug and solve problems\n• Suggest best practices and alternatives\n• Integrate with various tools through plugins\n• Learn and adapt to your preferences\n\nWhat specific type of assistance are you looking for?',
                    'confidence': 92.0
                },
                {
                    'category': 'CAPABILITIES',
                    'keywords': 'are you working functioning operational available',
                    'response_template': 'Yes, I\'m fully operational and ready to help! I can assist with:\n\n• Technical guidance and explanations\n• Step-by-step instructions\n• Troubleshooting and problem solving\n• Best practices and recommendations\n• Tool-specific knowledge through plugins\n\nWhat would you like to work on?',
                    'confidence': 92.0
                },
                
                # === HELP & ASSISTANCE ===
                {
                    'category': 'HELP',
                    'keywords': 'help me need help assistance support guidance',
                    'response_template': 'I\'m here to help! Please tell me more about what you need assistance with. You can ask me about:\n\n• Specific technical topics\n• Step-by-step procedures\n• Troubleshooting issues\n• Best practices\n\nWhat would you like help with?',
                    'confidence': 90.0
                },
                {
                    'category': 'HELP',
                    'keywords': 'can you help me could you assist me would you help me',
                    'response_template': 'Absolutely! I\'d be happy to help you. Just let me know what you\'re working on or what questions you have, and I\'ll do my best to provide clear, helpful guidance.',
                    'confidence': 91.0
                },
                {
                    'category': 'HELP',
                    'keywords': 'i need guidance i need advice i need suggestions i need recommendations',
                    'response_template': 'I\'m great at providing guidance and recommendations! To give you the most helpful advice, could you tell me a bit more about:\n\n• What you\'re trying to accomplish\n• Any specific challenges you\'re facing\n• Your experience level with the topic\n\nThis will help me tailor my suggestions to your needs.',
                    'confidence': 87.0
                },
                
                # === INFORMATION REQUESTS ===
                {
                    'category': 'INFORMATION',
                    'keywords': 'what is how does explain describe tell me about',
                    'response_template': 'I\'d be happy to explain that for you. Could you be more specific about what aspect you\'d like me to cover? This will help me provide the most relevant and useful information.',
                    'confidence': 85.0
                },
                {
                    'category': 'INFORMATION',
                    'keywords': 'define definition meaning what does mean',
                    'response_template': 'Let me provide you with a clear definition and explanation. What specific term or concept would you like me to define?',
                    'confidence': 88.0
                },
                {
                    'category': 'INFORMATION',
                    'keywords': 'how to instructions steps tutorial guide walkthrough',
                    'response_template': 'I\'ll be happy to provide step-by-step instructions! To give you the most accurate guidance, please let me know:\n\n• What you\'re trying to accomplish\n• Your current setup or environment\n• Your experience level\n\nThis will help me tailor the instructions to your specific situation.',
                    'confidence': 90.0
                },
                
                # === TROUBLESHOOTING ===
                {
                    'category': 'TROUBLESHOOTING',
                    'keywords': 'error problem issue not working failed broken stuck debug fix resolve',
                    'response_template': 'I can help you troubleshoot this issue. To provide the best assistance, could you share:\n\n• The specific error message (if any)\n• What you were trying to do\n• What happened instead\n• Your environment details\n\nThis will help me give you targeted solutions.',
                    'confidence': 88.0
                },
                {
                    'category': 'TROUBLESHOOTING',
                    'keywords': 'something wrong went wrong not working properly behaving strangely',
                    'response_template': 'Let\'s figure out what\'s going wrong. I\'ll help you diagnose and fix the issue. Can you describe:\n\n• What should be happening\n• What\'s actually happening\n• When this started occurring\n• Any recent changes you made\n\nWith these details, I can help you get to the bottom of it.',
                    'confidence': 86.0
                },
                {
                    'category': 'TROUBLESHOOTING',
                    'keywords': 'whats wrong installation problem help me understand',
                    'response_template': 'I can help you troubleshoot this issue. To provide the best assistance, could you share:\n\n• The specific error message (if any)\n• What you were trying to do\n• What happened instead\n• Your environment details\n\nThis will help me give you targeted solutions.',
                    'confidence': 90.0
                },
                
                # === SOCIAL & CONVERSATIONAL ===
                {
                    'category': 'SOCIAL',
                    'keywords': 'thank you thanks appreciate it grateful thank you so much',
                    'response_template': 'You\'re very welcome! I\'m glad I could help. Feel free to ask if you need anything else.',
                    'confidence': 94.0
                },
                {
                    'category': 'SOCIAL',
                    'keywords': 'please excuse me sorry my apologies pardon me',
                    'response_template': 'No problem at all! No need to apologize. I\'m here to help and I\'m happy to assist you with whatever you need. What can I do for you?',
                    'confidence': 89.0
                },
                {
                    'category': 'SOCIAL',
                    'keywords': 'awesome great excellent fantastic wonderful amazing',
                    'response_template': 'I\'m so glad to hear that! It makes me happy when I can be helpful. Is there anything else you\'d like to work on or any other questions I can answer for you?',
                    'confidence': 85.0
                },
                
                # === CLARIFICATION & UNDERSTANDING ===
                {
                    'category': 'CLARIFICATION',
                    'keywords': 'i dont understand confused unclear not sure what you mean',
                    'response_template': 'No worries! Let me clarify that for you. I want to make sure I explain things clearly. Which part would you like me to go over again or explain differently?',
                    'confidence': 87.0
                },
                {
                    'category': 'CLARIFICATION',
                    'keywords': 'can you repeat that again say that again didnt catch that',
                    'response_template': 'Of course! Let me go through that again, and I\'ll try to be even clearer this time. Which specific part would you like me to repeat or explain further?',
                    'confidence': 86.0
                },
                
                # === GENERAL CONVERSATION ===
                {
                    'category': 'CONVERSATION',
                    'keywords': 'interesting cool neat thats nice good to know',
                    'response_template': 'I\'m glad you found that interesting! There\'s always more to explore on most topics. Is there anything specific you\'d like to dive deeper into or learn more about?',
                    'confidence': 82.0
                },
                {
                    'category': 'CONVERSATION',
                    'keywords': 'what do you think your opinion thoughts recommendations suggestions',
                    'response_template': 'Based on my knowledge and experience helping others, I think the best approach would depend on your specific situation. Could you share more details about what you\'re considering? That way I can give you more targeted recommendations.',
                    'confidence': 84.0
                }
            ]
            
            # Insert base patterns if they don't exist
            for pattern in base_patterns:
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM conversation_patterns 
                    WHERE category = ? AND keywords = ?
                ''', (pattern['category'], pattern['keywords']))
                
                if cursor.fetchone()[0] == 0:
                    self.add_pattern(
                        pattern['category'],
                        pattern['keywords'],
                        pattern['response_template'],
                        pattern['confidence']
                    )
            
            print(f"✅ Loaded {len(base_patterns)} base conversation patterns")
            
        except Exception as e:
            print(f"❌ Error loading base patterns: {e}")
    
    def add_pattern(self, category: str, keywords: str, 
                   response_template: str, confidence: float = 90.0) -> int:
        """Add a new conversation pattern"""
        try:
            conn = self._get_connection()
            conn.execute('''
                INSERT INTO conversation_patterns 
                (category, keywords, response_template, confidence)
                VALUES (?, ?, ?, ?)
            ''', (category, keywords, response_template, confidence))
            
            conn.commit()
            pattern_id = conn.lastrowid
            print(f"✅ Added pattern: {category} (ID: {pattern_id})")
            return pattern_id
            
        except Exception as e:
            print(f"❌ Error adding pattern: {e}")
            return -1
    
    def find_best_match(self, keywords: List[str], intent: str = None) -> Optional[PatternMatch]:
        """
        Find the best matching pattern for given keywords and intent
        
        Scoring system:
        - Keyword match score (0-100)
        - Category relevance bonus
        - Usage success rate bonus
        """
        try:
            conn = self._get_connection()
            
            # Get all patterns
            cursor = conn.execute('''
                SELECT id, category, keywords, response_template, confidence,
                       usage_count, success_count
                FROM conversation_patterns
                ORDER BY confidence DESC
            ''')
            
            patterns = cursor.fetchall()
            
            # Find best match
            best_match = None
            highest_score = 0
            
            for pattern in patterns:
                score = self._calculate_match_score(
                    keywords, intent, pattern
                )
                
                if score > highest_score and score > 30:  # Minimum threshold
                    highest_score = score
                    pattern_id, category, pattern_keywords, response_template, \
                    confidence, usage_count, success_count = pattern
                    
                    success_rate = (success_count / max(usage_count, 1)) * 100
                    
                    best_match = PatternMatch(
                        pattern_id=pattern_id,
                        category=category,
                        keywords=pattern_keywords,
                        response_template=response_template,
                        confidence=confidence,  # Use stored confidence, not calculated score
                        usage_count=usage_count,
                        success_rate=success_rate
                    )
            
            return best_match
            
        except Exception as e:
            print(f"❌ Error finding pattern match: {e}")
            return None
    
    def _calculate_match_score(self, query_keywords: List[str], 
                              intent: str, pattern_data: Tuple) -> float:
        """Calculate match score between query and pattern"""
        pattern_id, category, pattern_keywords, response_template, \
        confidence, usage_count, success_count = pattern_data
        
        pattern_keyword_list = pattern_keywords.lower().split()
        query_keyword_set = set(word.lower() for word in query_keywords)
        pattern_keyword_set = set(pattern_keyword_list)
        
        # Keyword overlap score (0-80 points)
        if pattern_keyword_set:
            overlap = len(query_keyword_set.intersection(pattern_keyword_set))
            # Score based on overlap ratio with a minimum boost for any match
            keyword_score = min((overlap / len(pattern_keyword_set)) * 80 + (overlap * 20), 80)
        else:
            keyword_score = 0
        
        # Intent/Category relevance bonus (0-15 points)
        category_bonus = 0
        if intent:
            intent_category_map = {
                'greeting': 'GREETING',
                'capability_inquiry': 'CAPABILITIES',
                'information_request': 'INFORMATION',
                'troubleshooting': 'TROUBLESHOOTING',
                'general': 'HELP'
            }
            
            if intent in intent_category_map and category == intent_category_map[intent]:
                category_bonus = 15
        
        # Success rate bonus (0-5 points)
        if usage_count > 0:
            success_rate = success_count / usage_count
            success_bonus = success_rate * 5
        else:
            success_bonus = 2.5  # Neutral for unused patterns
        
        total_score = keyword_score + category_bonus + success_bonus
        return min(total_score, 100)  # Cap at 100
    
    def update_usage(self, pattern_id: int, was_successful: bool = True):
        """Update pattern usage statistics"""
        try:
            conn = self._get_connection()
            
            # Increment usage count
            conn.execute('''
                UPDATE conversation_patterns 
                SET usage_count = usage_count + 1,
                    success_count = success_count + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (1 if was_successful else 0, pattern_id))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error updating pattern usage: {e}")
    
    def add_feedback(self, pattern_id: int, query: str, 
                    was_helpful: bool, feedback: str = ""):
        """Add user feedback for pattern improvement"""
        try:
            conn = self._get_connection()
            conn.execute('''
                INSERT INTO pattern_feedback 
                (pattern_id, query, was_helpful, user_feedback)
                VALUES (?, ?, ?, ?)
            ''', (pattern_id, query, was_helpful, feedback))
            
            conn.commit()
            
            # Update pattern success rate based on feedback
            self.update_usage(pattern_id, was_helpful)
            
        except Exception as e:
            print(f"❌ Error adding feedback: {e}")
    
    def get_pattern_stats(self) -> Dict[str, Any]:
        """Get statistics about pattern usage"""
        try:
            conn = self._get_connection()
            
            # Get conversation stats
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as total_patterns,
                    AVG(usage_count) as avg_usage,
                    AVG(CASE WHEN usage_count > 0 
                        THEN CAST(success_count AS FLOAT) / usage_count 
                        ELSE 0 END) as avg_success_rate
                FROM conversation_patterns
            ''')
            
            stats = cursor.fetchone()
            
            return {
                'total_patterns': stats[0],
                'average_usage': round(stats[1], 2),
                'average_success_rate': round(stats[2] * 100, 2)
            }
            
        except Exception as e:
            print(f"❌ Error getting pattern stats: {e}")
            return {}
    
    def __del__(self):
        """Cleanup when the object is destroyed"""
        self._close_connection()

# Test the pattern matcher
if __name__ == "__main__":
    matcher = PatternMatcher()
    
    # Test cases
    test_cases = [
        (["hi", "there"], "greeting"),
        (["what", "can", "you", "do"], "capability_inquiry"),
        (["help", "me"], "help"),
        (["error", "problem"], "troubleshooting")
    ]
    
    for keywords, intent in test_cases:
        print(f"Keywords: {keywords}, Intent: {intent}")
        match = matcher.find_best_match(keywords, intent)
        
        if match:
            print(f"Best match: {match.category} (Score: {match.confidence:.1f})")
            print(f"Template: {match.response_template[:100]}...")
        else:
            print("No match found")
        print()
