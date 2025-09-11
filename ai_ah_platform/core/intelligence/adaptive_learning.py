#!/usr/bin/env python3
"""
Adaptive Learning System

This module provides intelligent learning capabilities that adapt the AI-AH platform
based on user interactions, feedback, and usage patterns.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import statistics

@dataclass
class LearningPattern:
    """Represents a learned pattern from user interactions."""
    pattern_id: str
    pattern_type: str  # query_pattern, response_preference, technology_combination
    confidence: float
    frequency: int
    last_seen: datetime
    examples: List[Dict[str, Any]]
    success_rate: float
    user_satisfaction: float

@dataclass
class UserLearningProfile:
    """User-specific learning profile."""
    user_id: str
    interaction_count: int
    preferred_response_style: str
    technology_expertise: Dict[str, float]  # technology -> expertise level
    common_query_patterns: List[str]
    successful_interactions: int
    failed_interactions: int
    learning_velocity: float  # How quickly user learns new concepts
    last_updated: datetime

class AdaptiveLearningEngine:
    """Engine for adaptive learning from user interactions."""
    
    def __init__(self, learning_threshold: float = 0.7, max_patterns: int = 1000):
        self.learning_threshold = learning_threshold
        self.max_patterns = max_patterns
        
        # Learning storage
        self.learned_patterns: Dict[str, LearningPattern] = {}
        self.user_profiles: Dict[str, UserLearningProfile] = {}
        self.interaction_history: List[Dict[str, Any]] = []
        
        self.logger = logging.getLogger(__name__)
        
        # Learning metrics
        self.total_interactions = 0
        self.successful_learnings = 0
        self.learning_accuracy = 0.0
        self.confidence_threshold = 0.7  # Threshold for considering a response successful
        
        # Initialize with some basic patterns
        self._initialize_basic_patterns()
    
    def _initialize_basic_patterns(self):
        """Initialize with some basic learning patterns."""
        basic_patterns = [
            {
                "pattern_id": "terraform_beginners",
                "pattern_type": "query_pattern",
                "confidence": 0.8,
                "frequency": 10,
                "last_seen": datetime.now(),
                "examples": [
                    {"query": "how to start with terraform", "intent": "explain_technology"},
                    {"query": "terraform basics", "intent": "explain_technology"}
                ],
                "success_rate": 0.9,
                "user_satisfaction": 0.85
            },
            {
                "pattern_id": "aws_cost_optimization",
                "pattern_type": "technology_combination",
                "confidence": 0.75,
                "frequency": 8,
                "last_seen": datetime.now(),
                "examples": [
                    {"query": "aws cost optimization", "technologies": ["aws", "cost"]},
                    {"query": "reduce aws bills", "technologies": ["aws", "cost"]}
                ],
                "success_rate": 0.8,
                "user_satisfaction": 0.8
            }
        ]
        
        for pattern_data in basic_patterns:
            pattern = LearningPattern(**pattern_data)
            self.learned_patterns[pattern.pattern_id] = pattern
    
    def learn_from_interaction(self, user_id: str, query: str, response: str, 
                             intent: str, confidence: float, user_feedback: Optional[Dict[str, Any]] = None) -> None:
        """Learn from a user interaction."""
        self.total_interactions += 1
        
        # Create interaction record
        interaction = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "query": query,
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "user_feedback": user_feedback
        }
        
        self.interaction_history.append(interaction)
        
        # Update user profile
        self._update_user_profile(user_id, interaction)
        
        # Extract learning patterns
        patterns = self._extract_patterns(interaction)
        
        # Update learned patterns
        for pattern in patterns:
            self._update_learned_pattern(pattern)
        
        # Learn from feedback if available
        if user_feedback:
            self._learn_from_feedback(user_id, interaction, user_feedback)
        
        self.logger.info(f"Learned from interaction for user {user_id}: {intent}")
    
    def _update_user_profile(self, user_id: str, interaction: Dict[str, Any]) -> None:
        """Update user learning profile based on interaction."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserLearningProfile(
                user_id=user_id,
                interaction_count=0,
                preferred_response_style="detailed",
                technology_expertise={},
                common_query_patterns=[],
                successful_interactions=0,
                failed_interactions=0,
                learning_velocity=0.5,
                last_updated=datetime.now()
            )
        
        profile = self.user_profiles[user_id]
        profile.interaction_count += 1
        profile.last_updated = datetime.now()
        
        # Update technology expertise based on query
        query_lower = interaction["query"].lower()
        technologies = ["terraform", "ansible", "kubernetes", "aws", "azure", "gcp", "docker", "monitoring", "security"]
        
        for tech in technologies:
            if tech in query_lower:
                if tech not in profile.technology_expertise:
                    profile.technology_expertise[tech] = 0.5
                else:
                    # Gradually increase expertise based on interaction complexity
                    complexity = self._assess_query_complexity(interaction["query"])
                    profile.technology_expertise[tech] = min(1.0, profile.technology_expertise[tech] + complexity * 0.1)
        
        # Update success/failure counts based on confidence threshold
        if interaction["confidence"] > self.confidence_threshold:
            profile.successful_interactions += 1
            self.successful_learnings += 1
        else:
            profile.failed_interactions += 1
        
        # Update learning velocity
        if profile.interaction_count > 1:
            recent_success_rate = profile.successful_interactions / profile.interaction_count
            profile.learning_velocity = recent_success_rate
    
    def _assess_query_complexity(self, query: str) -> float:
        """Assess the complexity of a user query."""
        complexity_indicators = {
            "high": ["architecture", "design", "optimization", "scalability", "security", "compliance"],
            "medium": ["setup", "configuration", "deployment", "monitoring", "backup"],
            "low": ["what is", "explain", "basics", "introduction", "getting started"]
        }
        
        query_lower = query.lower()
        
        high_count = sum(1 for indicator in complexity_indicators["high"] if indicator in query_lower)
        medium_count = sum(1 for indicator in complexity_indicators["medium"] if indicator in query_lower)
        low_count = sum(1 for indicator in complexity_indicators["low"] if indicator in query_lower)
        
        if high_count > 0:
            return 0.8
        elif medium_count > 0:
            return 0.5
        elif low_count > 0:
            return 0.2
        else:
            return 0.3  # Default complexity
    
    def _extract_patterns(self, interaction: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learning patterns from interaction."""
        patterns = []
        
        # Query pattern extraction
        query_pattern = self._extract_query_pattern(interaction)
        if query_pattern:
            patterns.append(query_pattern)
        
        # Technology combination pattern
        tech_pattern = self._extract_technology_pattern(interaction)
        if tech_pattern:
            patterns.append(tech_pattern)
        
        # Response preference pattern
        response_pattern = self._extract_response_pattern(interaction)
        if response_pattern:
            patterns.append(response_pattern)
        
        return patterns
    
    def _extract_query_pattern(self, interaction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract query pattern from interaction."""
        query = interaction["query"].lower()
        intent = interaction["intent"]
        
        # Look for common query structures
        query_structures = {
            "how_to": ["how to", "how do i", "how can i"],
            "what_is": ["what is", "what are", "explain"],
            "why_should": ["why should", "why use", "benefits of"],
            "compare": ["vs", "versus", "compare", "difference between"],
            "troubleshoot": ["error", "problem", "issue", "not working", "failed"]
        }
        
        for structure, indicators in query_structures.items():
            if any(indicator in query for indicator in indicators):
                return {
                    "pattern_id": f"{structure}_{intent}",
                    "pattern_type": "query_pattern",
                    "confidence": 0.7,
                    "frequency": 1,
                    "last_seen": datetime.now(),
                    "examples": [{"query": interaction["query"], "intent": intent}],
                    "success_rate": 1.0 if interaction["confidence"] > 0.8 else 0.5,
                    "user_satisfaction": 0.8
                }
        
        return None
    
    def _extract_technology_pattern(self, interaction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract technology combination pattern."""
        query = interaction["query"].lower()
        technologies = ["terraform", "ansible", "kubernetes", "aws", "azure", "gcp", "docker", "monitoring", "security", "cicd"]
        
        found_technologies = [tech for tech in technologies if tech in query]
        
        if len(found_technologies) >= 2:
            pattern_id = f"tech_combo_{'_'.join(sorted(found_technologies))}"
            return {
                "pattern_id": pattern_id,
                "pattern_type": "technology_combination",
                "confidence": 0.8,
                "frequency": 1,
                "last_seen": datetime.now(),
                "examples": [{"query": interaction["query"], "technologies": found_technologies}],
                "success_rate": 1.0 if interaction["confidence"] > 0.8 else 0.5,
                "user_satisfaction": 0.8
            }
        
        return None
    
    def _extract_response_pattern(self, interaction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract response preference pattern."""
        response = interaction["response"]
        
        # Analyze response characteristics
        response_length = len(response)
        has_code = "```" in response or "code" in response.lower()
        has_examples = "example" in response.lower() or "for instance" in response.lower()
        has_best_practices = "best practice" in response.lower() or "recommend" in response.lower()
        
        # Determine response style
        if response_length > 1000 and has_code and has_examples:
            style = "detailed_technical"
        elif response_length > 500 and has_examples:
            style = "detailed_examples"
        elif response_length < 300:
            style = "concise"
        else:
            style = "balanced"
        
        return {
            "pattern_id": f"response_style_{style}",
            "pattern_type": "response_preference",
            "confidence": 0.6,
            "frequency": 1,
            "last_seen": datetime.now(),
            "examples": [{"query": interaction["query"], "style": style, "length": response_length}],
            "success_rate": 1.0 if interaction["confidence"] > 0.8 else 0.5,
            "user_satisfaction": 0.8
        }
    
    def _update_learned_pattern(self, pattern_data: Dict[str, Any]) -> None:
        """Update or create a learned pattern."""
        pattern_id = pattern_data["pattern_id"]
        
        if pattern_id in self.learned_patterns:
            # Update existing pattern
            pattern = self.learned_patterns[pattern_id]
            pattern.frequency += 1
            pattern.last_seen = datetime.now()
            pattern.examples.append(pattern_data["examples"][0])
            
            # Keep only recent examples
            if len(pattern.examples) > 10:
                pattern.examples = pattern.examples[-10:]
            
            # Update confidence based on success rate
            recent_success_rate = pattern_data["success_rate"]
            pattern.confidence = (pattern.confidence + recent_success_rate) / 2
            
        else:
            # Create new pattern
            pattern = LearningPattern(**pattern_data)
            self.learned_patterns[pattern_id] = pattern
        
        # Clean up old patterns if we have too many
        if len(self.learned_patterns) > self.max_patterns:
            self._cleanup_old_patterns()
    
    def _cleanup_old_patterns(self) -> None:
        """Remove old or low-confidence patterns."""
        # Sort patterns by confidence and frequency
        sorted_patterns = sorted(
            self.learned_patterns.items(),
            key=lambda x: (x[1].confidence, x[1].frequency),
            reverse=True
        )
        
        # Keep only the top patterns
        keep_count = int(self.max_patterns * 0.8)  # Keep 80% of max
        patterns_to_keep = dict(sorted_patterns[:keep_count])
        
        self.learned_patterns = patterns_to_keep
        self.logger.info(f"Cleaned up patterns, kept {len(patterns_to_keep)} patterns")
    
    def _learn_from_feedback(self, user_id: str, interaction: Dict[str, Any], feedback: Dict[str, Any]) -> None:
        """Learn from user feedback."""
        if "satisfaction" in feedback:
            satisfaction = feedback["satisfaction"]
            
            # Update pattern success rates based on feedback
            for pattern in self.learned_patterns.values():
                if any(interaction["query"] in example.get("query", "") for example in pattern.examples):
                    pattern.user_satisfaction = (pattern.user_satisfaction + satisfaction) / 2
        
        if "preferred_style" in feedback:
            # Update user's preferred response style
            if user_id in self.user_profiles:
                self.user_profiles[user_id].preferred_response_style = feedback["preferred_style"]
        
        if "expertise_level" in feedback:
            # Update user's expertise level
            if user_id in self.user_profiles:
                # Update technology expertise based on feedback
                query_lower = interaction["query"].lower()
                technologies = ["terraform", "ansible", "kubernetes", "aws", "azure", "gcp", "docker", "monitoring", "security"]
                
                for tech in technologies:
                    if tech in query_lower:
                        self.user_profiles[user_id].technology_expertise[tech] = feedback["expertise_level"]
    
    def get_adaptive_response(self, user_id: str, query: str, base_response: str) -> str:
        """Adapt response based on learned patterns and user profile."""
        if user_id not in self.user_profiles:
            return base_response
        
        profile = self.user_profiles[user_id]
        
        # Adapt based on user's preferred response style
        if profile.preferred_response_style == "concise":
            return self._make_response_concise(base_response)
        elif profile.preferred_response_style == "detailed_technical":
            return self._make_response_technical(base_response)
        elif profile.preferred_response_style == "detailed_examples":
            return self._make_response_with_examples(base_response)
        
        # Adapt based on user's expertise level
        query_lower = query.lower()
        technologies = ["terraform", "ansible", "kubernetes", "aws", "azure", "gcp", "docker", "monitoring", "security"]
        
        for tech in technologies:
            if tech in query_lower and tech in profile.technology_expertise:
                expertise = profile.technology_expertise[tech]
                if expertise < 0.3:
                    return self._add_beginner_explanations(base_response)
                elif expertise > 0.7:
                    return self._add_advanced_insights(base_response)
        
        return base_response
    
    def _make_response_concise(self, response: str) -> str:
        """Make response more concise."""
        # Simple implementation - in production, use more sophisticated text processing
        lines = response.split('\n')
        important_lines = [line for line in lines if any(keyword in line.lower() for keyword in ['##', '•', '1)', '2)', '3)'])]
        return '\n'.join(important_lines[:5])  # Keep only top 5 important lines
    
    def _make_response_technical(self, response: str) -> str:
        """Make response more technical."""
        if "```" not in response:
            response += "\n\n**Technical Implementation:**\n```yaml\n# Add technical details here\n```"
        return response
    
    def _make_response_with_examples(self, response: str) -> str:
        """Add more examples to response."""
        if "example" not in response.lower():
            response += "\n\n**Example:**\nHere's a practical example of how to implement this solution."
        return response
    
    def _add_beginner_explanations(self, response: str) -> str:
        """Add beginner-friendly explanations."""
        response += "\n\n**For Beginners:**\nThis is a fundamental concept that forms the foundation for more advanced topics."
        return response
    
    def _add_advanced_insights(self, response: str) -> str:
        """Add advanced insights for expert users."""
        response += "\n\n**Advanced Insights:**\nConsider these advanced optimization techniques and edge cases."
        return response
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about the learning system."""
        total_patterns = len(self.learned_patterns)
        high_confidence_patterns = sum(1 for p in self.learned_patterns.values() if p.confidence > 0.8)
        
        # Calculate learning accuracy
        if self.total_interactions > 0:
            self.learning_accuracy = self.successful_learnings / self.total_interactions
        else:
            self.learning_accuracy = 0.0
        
        # Get most common patterns
        common_patterns = sorted(
            self.learned_patterns.values(),
            key=lambda x: x.frequency,
            reverse=True
        )[:5]
        
        return {
            "total_interactions": self.total_interactions,
            "total_patterns": total_patterns,
            "high_confidence_patterns": high_confidence_patterns,
            "learning_accuracy": self.learning_accuracy,
            "most_common_patterns": [{"id": p.pattern_id, "frequency": p.frequency, "confidence": p.confidence} for p in common_patterns],
            "user_profiles_count": len(self.user_profiles),
            "system_learning_rate": self.learning_accuracy
        }
    
    def export_learning_data(self) -> Dict[str, Any]:
        """Export learning data for analysis."""
        return {
            "learned_patterns": {pid: asdict(pattern) for pid, pattern in self.learned_patterns.items()},
            "user_profiles": {uid: asdict(profile) for uid, profile in self.user_profiles.items()},
            "learning_insights": self.get_learning_insights(),
            "export_timestamp": datetime.now().isoformat()
        }
