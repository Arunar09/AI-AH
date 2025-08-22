#!/usr/bin/env python3
"""
Memory Context System
====================

This module handles conversation memory, context tracking, and learning.
It maintains conversation history and user preferences.

Flow: Query + Context → Memory Lookup → Context Enhancement → Learning Update
"""

import sqlite3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class ConversationContext:
    """Current conversation context"""
    session_id: str
    user_id: str
    conversation_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    current_topic: Optional[str]
    context_confidence: float


class MemorySystem:
    """
    Conversation memory and context management system
    
    Responsibilities:
    1. Track conversation history
    2. Maintain user preferences and patterns
    3. Provide context for current queries
    4. Learn from successful interactions
    """
    
    def __init__(self, db_path: str = "base_agent.db"):
        """Initialize memory system with database"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._init_database()
        self.current_session = None
        self.max_history_length = 10  # Keep last 10 interactions
    
    def _init_database(self):
        """Initialize SQLite database with memory tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Conversation history table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id TEXT DEFAULT 'default_user',
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    intent TEXT,
                    confidence REAL,
                    was_successful BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User preferences table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    preference_key TEXT NOT NULL,
                    preference_value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, preference_key)
                )
            ''')
            
            # Session management table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    topic TEXT,
                    context_data TEXT,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Learned patterns table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL DEFAULT 70.0,
                    usage_count INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            print("✅ Memory system database initialized")
            
        except Exception as e:
            print(f"❌ Error initializing memory database: {e}")
            self.conn = None
            self.cursor = None
    
    def start_session(self, user_id: str = "default_user", 
                     session_id: str = None) -> str:
        """Start a new conversation session"""
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not self.conn:
            return session_id
        
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO sessions 
                (session_id, user_id, started_at, last_activity)
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (session_id, user_id))
            
            self.conn.commit()
            self.current_session = session_id
            print(f"✅ Started session: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"❌ Error starting session: {e}")
            return session_id
    
    def add_interaction(self, session_id: str, query: str, response: str,
                       intent: str = None, confidence: float = 0.8,
                       was_successful: bool = True, user_id: str = "default_user"):
        """Add an interaction to conversation history"""
        if not self.conn:
            return
        
        try:
            self.cursor.execute('''
                INSERT INTO conversation_history 
                (session_id, user_id, query, response, intent, confidence, was_successful)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, user_id, query, response, intent, confidence, was_successful))
            
            # Update session activity
            self.cursor.execute('''
                UPDATE sessions 
                SET last_activity = CURRENT_TIMESTAMP
                WHERE session_id = ?
            ''', (session_id,))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"❌ Error adding interaction: {e}")
    
    def get_conversation_context(self, session_id: str, 
                               user_id: str = "default_user") -> ConversationContext:
        """Get current conversation context"""
        if not self.conn:
            return ConversationContext(
                session_id=session_id,
                user_id=user_id,
                conversation_history=[],
                user_preferences={},
                current_topic=None,
                context_confidence=0.5
            )
        
        try:
            # Get recent conversation history
            self.cursor.execute('''
                SELECT query, response, intent, confidence, was_successful, created_at
                FROM conversation_history 
                WHERE session_id = ? AND user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (session_id, user_id, self.max_history_length))
            
            history_rows = self.cursor.fetchall()
            conversation_history = []
            
            for row in history_rows:
                conversation_history.append({
                    'query': row[0],
                    'response': row[1],
                    'intent': row[2],
                    'confidence': row[3],
                    'was_successful': row[4],
                    'timestamp': row[5]
                })
            
            # Get user preferences
            self.cursor.execute('''
                SELECT preference_key, preference_value
                FROM user_preferences
                WHERE user_id = ?
            ''', (user_id,))
            
            prefs_rows = self.cursor.fetchall()
            user_preferences = {row[0]: row[1] for row in prefs_rows}
            
            # Determine current topic from recent interactions
            current_topic = self._extract_current_topic(conversation_history)
            
            # Calculate context confidence
            context_confidence = self._calculate_context_confidence(conversation_history)
            
            return ConversationContext(
                session_id=session_id,
                user_id=user_id,
                conversation_history=conversation_history,
                user_preferences=user_preferences,
                current_topic=current_topic,
                context_confidence=context_confidence
            )
            
        except Exception as e:
            print(f"❌ Error getting conversation context: {e}")
            return ConversationContext(
                session_id=session_id,
                user_id=user_id,
                conversation_history=[],
                user_preferences={},
                current_topic=None,
                context_confidence=0.5
            )
    
    def update_user_preference(self, user_id: str, key: str, value: str):
        """Update user preference"""
        if not self.conn:
            return
        
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_preferences 
                (user_id, preference_key, preference_value, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, key, value))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"❌ Error updating user preference: {e}")
    
    def learn_pattern(self, user_id: str, pattern_type: str, 
                     pattern_data: Dict[str, Any], confidence: float = 70.0):
        """Learn a new pattern from user behavior"""
        if not self.conn:
            return
        
        try:
            pattern_json = json.dumps(pattern_data)
            
            # Check if similar pattern exists
            self.cursor.execute('''
                SELECT id, usage_count, confidence FROM learned_patterns
                WHERE user_id = ? AND pattern_type = ? AND pattern_data = ?
            ''', (user_id, pattern_type, pattern_json))
            
            existing = self.cursor.fetchone()
            
            if existing:
                # Update existing pattern
                pattern_id, usage_count, old_confidence = existing
                new_confidence = (old_confidence + confidence) / 2  # Average
                new_usage_count = usage_count + 1
                
                self.cursor.execute('''
                    UPDATE learned_patterns 
                    SET confidence = ?, usage_count = ?
                    WHERE id = ?
                ''', (new_confidence, new_usage_count, pattern_id))
            else:
                # Add new pattern
                self.cursor.execute('''
                    INSERT INTO learned_patterns 
                    (user_id, pattern_type, pattern_data, confidence)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, pattern_type, pattern_json, confidence))
            
            self.conn.commit()
            
        except Exception as e:
            print(f"❌ Error learning pattern: {e}")
    
    def get_relevant_context(self, query: str, session_id: str, 
                           user_id: str = "default_user") -> Dict[str, Any]:
        """Get relevant context for current query"""
        context = self.get_conversation_context(session_id, user_id)
        
        # Analyze query for context relevance
        query_lower = query.lower()
        relevant_context = {
            'has_conversation_history': len(context.conversation_history) > 0,
            'current_topic': context.current_topic,
            'user_preferences': context.user_preferences,
            'context_confidence': context.context_confidence,
            'related_interactions': []
        }
        
        # Find related previous interactions
        for interaction in context.conversation_history[:5]:  # Check last 5
            if self._is_related_interaction(query_lower, interaction):
                relevant_context['related_interactions'].append(interaction)
        
        return relevant_context
    
    def _extract_current_topic(self, history: List[Dict[str, Any]]) -> Optional[str]:
        """Extract current conversation topic from history"""
        if not history:
            return None
        
        # Simple topic extraction from recent intents
        recent_intents = [h.get('intent') for h in history[:3] if h.get('intent')]
        
        if recent_intents:
            # Most common recent intent
            topic_counts = {}
            for intent in recent_intents:
                topic_counts[intent] = topic_counts.get(intent, 0) + 1
            
            return max(topic_counts, key=topic_counts.get)
        
        return None
    
    def _calculate_context_confidence(self, history: List[Dict[str, Any]]) -> float:
        """Calculate confidence in current context understanding"""
        if not history:
            return 0.5
        
        # Base confidence on recent successful interactions
        recent_success = [h.get('was_successful', True) for h in history[:3]]
        success_rate = sum(recent_success) / len(recent_success)
        
        # Boost confidence if we have more history
        history_boost = min(len(history) / 10, 0.2)
        
        return min(success_rate + history_boost, 1.0)
    
    def _is_related_interaction(self, query: str, interaction: Dict[str, Any]) -> bool:
        """Check if previous interaction is related to current query"""
        prev_query = interaction.get('query', '').lower()
        
        # Simple keyword overlap check
        query_words = set(query.split())
        prev_words = set(prev_query.split())
        
        overlap = len(query_words.intersection(prev_words))
        return overlap >= 2  # At least 2 words in common
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        if not self.conn:
            return {}
        
        try:
            # Get conversation stats
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total_interactions,
                    COUNT(DISTINCT session_id) as total_sessions,
                    AVG(confidence) as avg_confidence,
                    AVG(CASE WHEN was_successful THEN 1.0 ELSE 0.0 END) as success_rate
                FROM conversation_history
            ''')
            
            stats = self.cursor.fetchone()
            
            # Get learning stats
            self.cursor.execute('''
                SELECT COUNT(*) as learned_patterns
                FROM learned_patterns
            ''')
            
            learned_count = self.cursor.fetchone()[0]
            
            return {
                'total_interactions': stats[0],
                'total_sessions': stats[1],
                'average_confidence': round(stats[2] or 0, 2),
                'success_rate': round((stats[3] or 0) * 100, 2),
                'learned_patterns': learned_count
            }
            
        except Exception as e:
            print(f"❌ Error getting memory stats: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    print("🧠 Memory System - Test Mode\n")
    
    memory = MemorySystem()
    
    # Test session
    session_id = memory.start_session("test_user")
    
    # Add some interactions
    interactions = [
        ("Hi there", "Hello! How can I help you?", "greeting", 0.95, True),
        ("What is Docker?", "Docker is a containerization platform...", "information_request", 0.85, True),
        ("How do I install it?", "Here's how to install Docker...", "command_request", 0.80, True)
    ]
    
    for query, response, intent, confidence, success in interactions:
        memory.add_interaction(session_id, query, response, intent, confidence, success)
    
    # Test context retrieval
    context = memory.get_conversation_context(session_id)
    print(f"Conversation history: {len(context.conversation_history)} items")
    print(f"Current topic: {context.current_topic}")
    print(f"Context confidence: {context.context_confidence:.2f}")
    
    # Test relevant context
    relevant = memory.get_relevant_context("Docker containers", session_id)
    print(f"Related interactions: {len(relevant['related_interactions'])}")
    
    # Show statistics
    stats = memory.get_memory_stats()
    print(f"\nMemory Statistics: {stats}")
