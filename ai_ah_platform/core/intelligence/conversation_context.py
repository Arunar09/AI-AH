#!/usr/bin/env python3
"""
Conversation Context Management System

This module provides intelligent conversation context tracking, user preference learning,
and adaptive response generation based on conversation history.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

@dataclass
class ConversationTurn:
    """Represents a single turn in a conversation."""
    timestamp: datetime
    user_query: str
    agent_response: str
    intent: str
    confidence: float
    technology_focus: Optional[str] = None
    user_satisfaction: Optional[float] = None
    follow_up_questions: List[str] = None
    
    def __post_init__(self):
        if self.follow_up_questions is None:
            self.follow_up_questions = []

@dataclass
class UserProfile:
    """User profile with preferences and interaction patterns."""
    user_id: str
    preferred_technologies: List[str]
    expertise_level: str  # beginner, intermediate, advanced
    interaction_style: str  # detailed, concise, technical
    common_topics: List[str]
    last_active: datetime
    total_interactions: int
    satisfaction_scores: List[float]
    
    def __post_init__(self):
        if self.preferred_technologies is None:
            self.preferred_technologies = []
        if self.common_topics is None:
            self.common_topics = []
        if self.satisfaction_scores is None:
            self.satisfaction_scores = []

class ConversationContextManager:
    """Manages conversation context and user learning."""
    
    def __init__(self, max_context_turns: int = 10, max_user_profiles: int = 1000):
        self.max_context_turns = max_context_turns
        self.max_user_profiles = max_user_profiles
        
        # In-memory storage (in production, use Redis or database)
        self.conversation_histories: Dict[str, List[ConversationTurn]] = {}
        self.user_profiles: Dict[str, UserProfile] = {}
        self.context_patterns: Dict[str, List[str]] = {}
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize with some common patterns
        self._initialize_context_patterns()
    
    def _initialize_context_patterns(self):
        """Initialize common conversation patterns for context awareness."""
        self.context_patterns = {
            "infrastructure_setup": [
                "web server", "database", "load balancer", "monitoring", "security"
            ],
            "deployment_pipeline": [
                "ci/cd", "jenkins", "gitlab", "github actions", "deployment", "staging", "production"
            ],
            "cloud_migration": [
                "aws", "azure", "gcp", "migration", "lift and shift", "refactoring", "cost optimization"
            ],
            "security_hardening": [
                "security", "compliance", "vulnerability", "penetration testing", "firewall", "encryption"
            ],
            "performance_optimization": [
                "performance", "scalability", "caching", "load testing", "bottleneck", "optimization"
            ],
            "disaster_recovery": [
                "backup", "disaster recovery", "business continuity", "rto", "rpo", "failover"
            ]
        }
    
    def add_conversation_turn(self, user_id: str, query: str, response: str, 
                            intent: str, confidence: float, technology_focus: str = None) -> None:
        """Add a new conversation turn to the context."""
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_query=query,
            agent_response=response,
            intent=intent,
            confidence=confidence,
            technology_focus=technology_focus
        )
        
        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []
        
        self.conversation_histories[user_id].append(turn)
        
        # Keep only recent turns
        if len(self.conversation_histories[user_id]) > self.max_context_turns:
            self.conversation_histories[user_id] = self.conversation_histories[user_id][-self.max_context_turns:]
        
        # Update user profile
        self._update_user_profile(user_id, turn)
        
        self.logger.info(f"Added conversation turn for user {user_id}: {intent}")
    
    def _update_user_profile(self, user_id: str, turn: ConversationTurn) -> None:
        """Update user profile based on conversation turn."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                preferred_technologies=[],
                expertise_level="intermediate",
                interaction_style="detailed",
                common_topics=[],
                last_active=datetime.now(),
                total_interactions=0,
                satisfaction_scores=[]
            )
        
        profile = self.user_profiles[user_id]
        profile.last_active = datetime.now()
        profile.total_interactions += 1
        
        # Update preferred technologies
        if turn.technology_focus and turn.technology_focus not in profile.preferred_technologies:
            profile.preferred_technologies.append(turn.technology_focus)
        
        # Update common topics
        query_words = turn.user_query.lower().split()
        for word in query_words:
            if len(word) > 3 and word not in profile.common_topics:
                profile.common_topics.append(word)
        
        # Keep only recent topics
        if len(profile.common_topics) > 20:
            profile.common_topics = profile.common_topics[-20:]
    
    def get_conversation_context(self, user_id: str) -> Dict[str, Any]:
        """Get conversation context for a user."""
        if user_id not in self.conversation_histories:
            return {
                "has_context": False,
                "recent_topics": [],
                "conversation_flow": [],
                "user_preferences": {},
                "suggested_follow_ups": []
            }
        
        history = self.conversation_histories[user_id]
        profile = self.user_profiles.get(user_id)
        
        # Analyze recent topics
        recent_topics = []
        for turn in history[-5:]:  # Last 5 turns
            if turn.technology_focus:
                recent_topics.append(turn.technology_focus)
        
        # Analyze conversation flow
        conversation_flow = []
        for turn in history[-3:]:  # Last 3 turns
            conversation_flow.append({
                "intent": turn.intent,
                "technology": turn.technology_focus,
                "confidence": turn.confidence
            })
        
        # Get user preferences
        user_preferences = {}
        if profile:
            user_preferences = {
                "preferred_technologies": profile.preferred_technologies,
                "expertise_level": profile.expertise_level,
                "interaction_style": profile.interaction_style,
                "common_topics": profile.common_topics[-10:]  # Last 10 topics
            }
        
        # Generate suggested follow-ups
        suggested_follow_ups = self._generate_follow_up_suggestions(history, profile)
        
        return {
            "has_context": True,
            "recent_topics": recent_topics,
            "conversation_flow": conversation_flow,
            "user_preferences": user_preferences,
            "suggested_follow_ups": suggested_follow_ups,
            "context_pattern": self._identify_context_pattern(history)
        }
    
    def _generate_follow_up_suggestions(self, history: List[ConversationTurn], 
                                      profile: Optional[UserProfile]) -> List[str]:
        """Generate intelligent follow-up suggestions based on context."""
        suggestions = []
        
        if not history:
            return [
                "What infrastructure challenges are you facing?",
                "Are you looking to set up a new environment?",
                "Do you need help with a specific technology?"
            ]
        
        last_turn = history[-1]
        recent_topics = [turn.technology_focus for turn in history[-3:] if turn.technology_focus]
        
        # Technology-specific follow-ups
        if last_turn.technology_focus:
            tech = last_turn.technology_focus
            if tech == "terraform":
                suggestions.extend([
                    f"Would you like me to help you create a {tech} configuration?",
                    f"Are you looking for {tech} best practices?",
                    f"Do you need help with {tech} state management?"
                ])
            elif tech == "ansible":
                suggestions.extend([
                    f"Would you like me to help you create an {tech} playbook?",
                    f"Are you looking for {tech} inventory management?",
                    f"Do you need help with {tech} roles and tasks?"
                ])
            elif tech in ["aws", "azure", "gcp"]:
                suggestions.extend([
                    f"Would you like me to help you design a {tech} architecture?",
                    f"Are you looking for {tech} cost optimization?",
                    f"Do you need help with {tech} security best practices?"
                ])
        
        # Context-based follow-ups
        if len(recent_topics) > 1:
            suggestions.append(f"I see you're working with {', '.join(recent_topics)}. Would you like help integrating these technologies?")
        
        # User preference-based follow-ups
        if profile and profile.preferred_technologies:
            suggestions.append(f"Based on your interest in {', '.join(profile.preferred_technologies[:2])}, would you like to explore advanced configurations?")
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _identify_context_pattern(self, history: List[ConversationTurn]) -> Optional[str]:
        """Identify the overall context pattern of the conversation."""
        if not history:
            return None
        
        # Analyze recent turns for patterns
        recent_queries = [turn.user_query.lower() for turn in history[-5:]]
        recent_technologies = [turn.technology_focus for turn in history[-5:] if turn.technology_focus]
        
        # Check for pattern matches
        for pattern_name, pattern_keywords in self.context_patterns.items():
            matches = 0
            for keyword in pattern_keywords:
                if any(keyword in query for query in recent_queries):
                    matches += 1
                if keyword in recent_technologies:
                    matches += 1
            
            if matches >= 2:  # At least 2 matches
                return pattern_name
        
        return "general_infrastructure"
    
    def adapt_response_to_context(self, response: str, context: Dict[str, Any], 
                                user_id: str) -> str:
        """Adapt response based on conversation context."""
        if not context.get("has_context"):
            return response
        
        adapted_response = response
        
        # Add context-aware introduction
        if context.get("recent_topics"):
            recent_topics = context["recent_topics"]
            if len(recent_topics) > 1:
                adapted_response = f"Building on our discussion about {', '.join(recent_topics[-2:])}, here's what I recommend:\n\n{adapted_response}"
        
        # Add personalized suggestions
        if context.get("suggested_follow_ups"):
            follow_ups = context["suggested_follow_ups"][:2]  # Top 2
            adapted_response += "\n\n**Next Steps:**\n"
            for i, follow_up in enumerate(follow_ups, 1):
                adapted_response += f"{i}. {follow_up}\n"
        
        # Add context pattern insights
        context_pattern = context.get("context_pattern")
        if context_pattern and context_pattern != "general_infrastructure":
            pattern_insights = self._get_pattern_insights(context_pattern)
            if pattern_insights:
                adapted_response += f"\n\n**Related Considerations:**\n{pattern_insights}"
        
        return adapted_response
    
    def _get_pattern_insights(self, pattern: str) -> str:
        """Get insights for specific context patterns."""
        insights = {
            "infrastructure_setup": "Consider implementing monitoring and backup strategies from the start.",
            "deployment_pipeline": "Ensure proper testing stages and rollback procedures are in place.",
            "cloud_migration": "Plan for data migration, network connectivity, and application compatibility.",
            "security_hardening": "Implement defense in depth with multiple security layers.",
            "performance_optimization": "Profile your application to identify actual bottlenecks before optimizing.",
            "disaster_recovery": "Define clear RTO and RPO objectives based on business requirements."
        }
        return insights.get(pattern, "")
    
    def learn_from_feedback(self, user_id: str, feedback: Dict[str, Any]) -> None:
        """Learn from user feedback to improve future responses."""
        if user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[user_id]
        
        # Update satisfaction scores
        if "satisfaction" in feedback:
            satisfaction = feedback["satisfaction"]
            if 0 <= satisfaction <= 1:
                profile.satisfaction_scores.append(satisfaction)
                if len(profile.satisfaction_scores) > 10:
                    profile.satisfaction_scores = profile.satisfaction_scores[-10:]
        
        # Update expertise level based on feedback
        if "expertise_level" in feedback:
            profile.expertise_level = feedback["expertise_level"]
        
        # Update interaction style
        if "preferred_style" in feedback:
            profile.interaction_style = feedback["preferred_style"]
        
        self.logger.info(f"Updated user profile for {user_id} based on feedback")
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user behavior and preferences."""
        if user_id not in self.user_profiles:
            return {"error": "User not found"}
        
        profile = self.user_profiles[user_id]
        history = self.conversation_histories.get(user_id, [])
        
        # Calculate average satisfaction
        avg_satisfaction = 0
        if profile.satisfaction_scores:
            avg_satisfaction = sum(profile.satisfaction_scores) / len(profile.satisfaction_scores)
        
        # Analyze interaction patterns
        interaction_patterns = {
            "most_common_intent": self._get_most_common_intent(history),
            "technology_preference": profile.preferred_technologies,
            "expertise_trend": self._analyze_expertise_trend(history),
            "session_frequency": self._calculate_session_frequency(history)
        }
        
        return {
            "user_id": user_id,
            "total_interactions": profile.total_interactions,
            "average_satisfaction": avg_satisfaction,
            "expertise_level": profile.expertise_level,
            "interaction_style": profile.interaction_style,
            "preferred_technologies": profile.preferred_technologies,
            "interaction_patterns": interaction_patterns,
            "last_active": profile.last_active.isoformat()
        }
    
    def _get_most_common_intent(self, history: List[ConversationTurn]) -> str:
        """Get the most common intent from conversation history."""
        if not history:
            return "general_infrastructure"
        
        intent_counts = {}
        for turn in history:
            intent_counts[turn.intent] = intent_counts.get(turn.intent, 0) + 1
        
        return max(intent_counts, key=intent_counts.get)
    
    def _analyze_expertise_trend(self, history: List[ConversationTurn]) -> str:
        """Analyze if user expertise is increasing over time."""
        if len(history) < 3:
            return "insufficient_data"
        
        # Simple heuristic: more specific queries over time indicate increasing expertise
        recent_queries = [turn.user_query for turn in history[-3:]]
        older_queries = [turn.user_query for turn in history[-6:-3]] if len(history) >= 6 else []
        
        if not older_queries:
            return "insufficient_data"
        
        # Count technical terms in recent vs older queries
        technical_terms = ["configuration", "deployment", "architecture", "optimization", "security", "monitoring"]
        
        recent_tech_count = sum(1 for query in recent_queries for term in technical_terms if term in query.lower())
        older_tech_count = sum(1 for query in older_queries for term in technical_terms if term in query.lower())
        
        if recent_tech_count > older_tech_count:
            return "increasing"
        elif recent_tech_count < older_tech_count:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_session_frequency(self, history: List[ConversationTurn]) -> str:
        """Calculate how frequently the user interacts."""
        if len(history) < 2:
            return "new_user"
        
        # Calculate average time between interactions
        time_diffs = []
        for i in range(1, len(history)):
            diff = history[i].timestamp - history[i-1].timestamp
            time_diffs.append(diff.total_seconds())
        
        avg_diff = sum(time_diffs) / len(time_diffs)
        
        if avg_diff < 3600:  # Less than 1 hour
            return "high_frequency"
        elif avg_diff < 86400:  # Less than 1 day
            return "medium_frequency"
        else:
            return "low_frequency"
    
    def cleanup_old_data(self, max_age_days: int = 30) -> None:
        """Clean up old conversation data to manage memory."""
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        # Clean up old conversation histories
        for user_id in list(self.conversation_histories.keys()):
            history = self.conversation_histories[user_id]
            self.conversation_histories[user_id] = [
                turn for turn in history if turn.timestamp > cutoff_date
            ]
            
            # Remove empty histories
            if not self.conversation_histories[user_id]:
                del self.conversation_histories[user_id]
        
        # Clean up old user profiles
        for user_id in list(self.user_profiles.keys()):
            profile = self.user_profiles[user_id]
            if profile.last_active < cutoff_date:
                del self.user_profiles[user_id]
        
        self.logger.info(f"Cleaned up data older than {max_age_days} days")
    
    def export_context_data(self, user_id: str) -> Dict[str, Any]:
        """Export conversation context data for analysis."""
        if user_id not in self.conversation_histories:
            return {"error": "No data found for user"}
        
        history = self.conversation_histories[user_id]
        profile = self.user_profiles.get(user_id)
        
        return {
            "user_id": user_id,
            "conversation_history": [asdict(turn) for turn in history],
            "user_profile": asdict(profile) if profile else None,
            "context_analysis": self.get_conversation_context(user_id),
            "export_timestamp": datetime.now().isoformat()
        }
