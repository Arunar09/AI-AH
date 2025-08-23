#!/usr/bin/env python3
"""
Base Agent - Core AI Agent Foundation
====================================

This is the main base agent that orchestrates all components to provide
intelligent responses with plugin support.

Complete Flow:
User Query → Query Analysis → Keyword Extraction → Dictionary Lookup → 
Pattern Matching → Memory Context → Plugin Selection → Knowledge Integration → 
Response Generation → Intelligence Curation → Final Response
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from .dictionary import UniversalDictionary, QueryAnalysis
from .pattern_matcher import PatternMatcher, PatternMatch
from .memory_system import MemorySystem, ConversationContext
from .plugin_system import PluginManager, PluginResponse


@dataclass
class AgentResponse:
    """Structured response from the base agent"""
    success: bool
    response: str
    confidence: float
    intent: str
    complexity: str
    sources: List[str]
    context_used: bool
    plugins_used: List[str]
    reasoning: List[str]
    suggestions: List[str]
    response_time_ms: float
    timestamp: str


class BaseAgent:
    """
    Base AI Agent with Plugin Architecture
    
    This agent provides a clean foundation for building tool-specific AI assistants.
    It combines universal language understanding with pluggable tool knowledge.
    
    Core Features:
    - Universal language understanding (dictionary system)
    - Conversation pattern matching
    - Memory and context management
    - Plugin-based tool integration
    - Intelligent response generation
    """
    
    def __init__(self, agent_name: str = "BaseAgent", db_path: str = "base_agent.db"):
        """Initialize the base agent with all core systems"""
        self.name = agent_name
        self.version = "1.0.0"
        self.db_path = db_path
        
        # Initialize core systems
        print(f"🚀 Initializing {self.name} v{self.version}")
        
        self.dictionary = UniversalDictionary()
        print("✅ Dictionary system loaded")
        
        self.pattern_matcher = PatternMatcher(db_path)
        print("✅ Pattern matcher loaded")
        
        self.memory = MemorySystem(db_path)
        print("✅ Memory system loaded")
        
        self.plugin_manager = PluginManager()
        print("✅ Plugin manager loaded")
        
        # Agent state
        self.current_session = None
        self.current_user = "default_user"
        
        print(f"🎉 {self.name} is ready!")
    
    def start_session(self, user_id: str = "default_user") -> str:
        """Start a new conversation session"""
        session_id = self.memory.start_session(user_id)
        self.current_session = session_id
        self.current_user = user_id
        return session_id
    
    def process_query(self, query: str, session_id: str = None, 
                     user_id: str = None) -> AgentResponse:
        """
        Main entry point for processing user queries
        
        This method implements the complete flow:
        1. Query Analysis (dictionary)
        2. Pattern Matching
        3. Memory Context
        4. Plugin Knowledge
        5. Response Generation
        6. Intelligence Curation
        """
        start_time = datetime.now()
        
        # Use current session if not provided
        if session_id is None:
            session_id = self.current_session or self.start_session(user_id or self.current_user)
        if user_id is None:
            user_id = self.current_user
        
        reasoning = []
        sources = []
        plugins_used = []
        
        try:
            # Step 1: Query Analysis with Dictionary
            reasoning.append("Analyzing query with universal dictionary")
            query_analysis = self.dictionary.analyze_query(query)
            
            # Step 2: Pattern Matching
            reasoning.append("Searching conversation patterns")
            pattern_match = self.pattern_matcher.find_best_match(
                query_analysis.keywords, 
                query_analysis.intent
            )
            
            # Step 3: Memory Context
            reasoning.append("Retrieving conversation context")
            memory_context = self.memory.get_relevant_context(query, session_id, user_id)
            
            # Step 4: Plugin Knowledge Integration
            reasoning.append("Consulting relevant plugins")
            plugin_responses = self.plugin_manager.get_combined_knowledge(
                query_analysis.keywords,
                query_analysis.context
            )
            plugins_used = [resp.source for resp in plugin_responses if resp.success]
            
            # Step 5: Response Generation
            reasoning.append("Generating intelligent response")
            response_content, confidence = self._generate_response(
                query, query_analysis, pattern_match, memory_context, plugin_responses
            )
            
            # Step 6: Intelligence Curation
            reasoning.append("Curating response with intelligence")
            curated_response, suggestions = self._curate_response(
                response_content, query_analysis, memory_context
            )
            
            # Calculate response time
            end_time = datetime.now()
            response_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Build sources list
            sources = ["base_patterns"]
            if memory_context['has_conversation_history']:
                sources.append("conversation_memory")
            sources.extend(plugins_used)
            
            # Record interaction in memory
            self.memory.add_interaction(
                session_id, query, curated_response,
                query_analysis.intent, confidence, True, user_id
            )
            
            # Update pattern usage if pattern was used
            if pattern_match:
                self.pattern_matcher.update_usage(pattern_match.pattern_id, True)
            
            # Create final response
            agent_response = AgentResponse(
                success=True,
                response=curated_response,
                confidence=confidence,
                intent=query_analysis.intent,
                complexity=query_analysis.complexity,
                sources=sources,
                context_used=memory_context['has_conversation_history'],
                plugins_used=plugins_used,
                reasoning=reasoning,
                suggestions=suggestions,
                response_time_ms=round(response_time_ms, 2),
                timestamp=datetime.now().isoformat()
            )
            
            return agent_response
            
        except Exception as e:
            # Error handling
            error_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AgentResponse(
                success=False,
                response=f"I apologize, but I encountered an error processing your request. Please try rephrasing your question or ask for help with a specific topic.",
                confidence=0.0,
                intent="error",
                complexity="unknown",
                sources=["error_handler"],
                context_used=False,
                plugins_used=[],
                reasoning=[f"Error occurred: {str(e)}"],
                suggestions=["Try rephrasing your question", "Ask for help with a specific topic"],
                response_time_ms=round(error_time, 2),
                timestamp=datetime.now().isoformat()
            )
    
    def _generate_response(self, query: str, query_analysis: QueryAnalysis,
                          pattern_match: Optional[PatternMatch],
                          memory_context: Dict[str, Any],
                          plugin_responses: List[PluginResponse]) -> tuple[str, float]:
        """Generate the core response content"""
        
        # Priority 1: Pattern match with plugin enhancement
        if pattern_match and pattern_match.confidence > 30:  # Lowered threshold for better matching
            base_response = pattern_match.response_template
            
            # Enhance with plugin knowledge if available
            if plugin_responses:
                successful_plugins = [resp for resp in plugin_responses if resp.success]
                if successful_plugins:
                    plugin_content = self._combine_plugin_responses(successful_plugins)
                    base_response = self._enhance_pattern_with_plugins(
                        base_response, plugin_content, query_analysis
                    )
            
            # Pattern confidence is already 0-100, convert to 0-1 scale
            confidence = pattern_match.confidence / 100.0 if pattern_match.confidence > 1 else pattern_match.confidence
            return base_response, min(confidence, 1.0)
        
        # Priority 2: Plugin-driven response
        if plugin_responses:
            successful_plugins = [resp for resp in plugin_responses if resp.success]
            if successful_plugins:
                plugin_content = self._combine_plugin_responses(successful_plugins)
                confidence = max(resp.confidence for resp in successful_plugins)
                return plugin_content, confidence
        
        # Priority 3: Context-aware fallback
        if memory_context['has_conversation_history']:
            topic = memory_context.get('current_topic', 'general')
            return self._generate_contextual_fallback(query, query_analysis, topic), 0.6
        
        # Priority 4: Generic helpful fallback
        return self._generate_generic_fallback(query_analysis), 0.5
    
    def _enhance_pattern_with_plugins(self, base_response: str, 
                                    plugin_content: str, 
                                    query_analysis: QueryAnalysis) -> str:
        """Enhance pattern response with plugin knowledge"""
        # Simple enhancement - in real implementation, this would be more sophisticated
        if plugin_content and len(plugin_content.strip()) > 0:
            enhanced = f"{base_response}\n\n**Additional Information:**\n{plugin_content}"
            return enhanced
        return base_response
    
    def _combine_plugin_responses(self, plugin_responses: List[PluginResponse]) -> str:
        """Combine multiple plugin responses into coherent content"""
        if not plugin_responses:
            return ""
        
        if len(plugin_responses) == 1:
            return plugin_responses[0].content
        
        # Combine multiple responses
        combined_parts = []
        for i, response in enumerate(plugin_responses):
            if response.content.strip():
                combined_parts.append(f"**{response.source}:** {response.content}")
        
        return "\n\n".join(combined_parts)
    
    def _generate_contextual_fallback(self, query: str, query_analysis: QueryAnalysis, 
                                    topic: str) -> str:
        """Generate context-aware fallback response"""
        # Safe keyword handling
        keywords_str = self._safe_join_keywords(query_analysis.keywords[:3], query)
        
        intent_responses = {
            'information_request': f"I'd be happy to provide information about {keywords_str}. Based on our conversation about {topic}, could you be more specific about what aspect you'd like to know?",
            'command_request': f"I can help you with commands related to {keywords_str}. What specific action are you trying to accomplish?",
            'troubleshooting': f"I can help troubleshoot this issue. Based on our discussion about {topic}, could you provide more details about the problem you're experiencing?",
            'capability_inquiry': f"I can assist with various aspects of {topic} and other technical topics. What specific capabilities are you interested in learning about?"
        }
        
        return intent_responses.get(
            query_analysis.intent,
            f"I understand you're asking about {keywords_str}. Could you provide more context about what you're trying to achieve?"
        )
    
    def _generate_generic_fallback(self, query_analysis: QueryAnalysis) -> str:
        """Generate generic helpful fallback"""
        # Safe keyword handling
        keywords_str = self._safe_join_keywords(query_analysis.keywords[:3], "this topic")
        
        intent_fallbacks = {
            'greeting': "Hello! I'm here to help you with technical questions and guidance. What would you like to know about?",
            'capability_inquiry': "I can help you with:\n\n• Technical explanations and guidance\n• Step-by-step instructions\n• Troubleshooting and problem solving\n• Best practices and recommendations\n\nWhat specific area interests you?",
            'information_request': f"I'd be happy to explain {keywords_str}. Could you be more specific about what aspect you'd like to understand?",
            'command_request': f"I can help you with commands and procedures. What are you trying to accomplish with {keywords_str}?",
            'troubleshooting': "I can help you troubleshoot issues. Please provide more details about:\n\n• What you're trying to do\n• What's not working\n• Any error messages you're seeing"
        }
        
        return intent_fallbacks.get(
            query_analysis.intent,
            f"I understand you're asking about {keywords_str}. How can I help you with this topic?"
        )
    
    def _safe_join_keywords(self, keywords: List[str], fallback: str = "this topic") -> str:
        """Safely join keywords with fallback for empty/broken keyword lists"""
        if not keywords:
            return fallback
        
        # Filter out empty or very short keywords
        valid_keywords = [k for k in keywords if k and len(k.strip()) > 1]
        
        if not valid_keywords:
            return fallback
        
        # Join with natural language
        if len(valid_keywords) == 1:
            return valid_keywords[0]
        elif len(valid_keywords) == 2:
            return f"{valid_keywords[0]} and {valid_keywords[1]}"
        else:
            return f"{', '.join(valid_keywords[:-1])}, and {valid_keywords[-1]}"
    
    def _curate_response(self, response: str, query_analysis: QueryAnalysis,
                        memory_context: Dict[str, Any]) -> tuple[str, List[str]]:
        """Curate response and generate helpful suggestions"""
        
        # Clean up response formatting
        curated = response.strip()
        
        # Add contextual enhancements (exclude social queries)
        if (query_analysis.complexity == 'beginner' and 
            query_analysis.intent not in ['social', 'greeting', 'personal']):
            if not any(phrase in curated.lower() for phrase in ['step by step', 'first', 'start']):
                curated += "\n\nWould you like me to provide step-by-step guidance?"
        
        # Generate suggestions based on intent and context
        suggestions = self._generate_suggestions(query_analysis, memory_context)
        
        return curated, suggestions
    
    def _generate_suggestions(self, query_analysis: QueryAnalysis,
                            memory_context: Dict[str, Any]) -> List[str]:
        """Generate helpful follow-up suggestions"""
        suggestions = []
        
        # Intent-based suggestions
        if query_analysis.intent == 'information_request':
            suggestions.extend([
                "Would you like practical examples?",
                "Do you need step-by-step instructions?",
                "Are you interested in best practices?"
            ])
        elif query_analysis.intent == 'command_request':
            suggestions.extend([
                "Would you like to see example commands?",
                "Do you need help with prerequisites?",
                "Should I explain what each step does?"
            ])
        elif query_analysis.intent == 'troubleshooting':
            suggestions.extend([
                "Can you share the exact error message?",
                "What were you trying to accomplish?",
                "Would you like debugging steps?"
            ])
        
        # Context-based suggestions
        if memory_context['current_topic']:
            suggestions.append(f"Would you like to explore more about {memory_context['current_topic']}?")
        
        # Limit suggestions to avoid overwhelming
        return suggestions[:3]
    
    def register_plugin(self, plugin) -> bool:
        """Register a new plugin with the agent"""
        return self.plugin_manager.register_plugin(plugin)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information"""
        pattern_stats = self.pattern_matcher.get_pattern_stats()
        memory_stats = self.memory.get_memory_stats()
        plugin_stats = self.plugin_manager.get_system_stats()
        
        return {
            'name': self.name,
            'version': self.version,
            'current_session': self.current_session,
            'current_user': self.current_user,
            'statistics': {
                'patterns': pattern_stats,
                'memory': memory_stats,
                'plugins': plugin_stats
            },
            'capabilities': {
                'universal_language_understanding': True,
                'conversation_patterns': True,
                'memory_and_context': True,
                'plugin_architecture': True,
                'intelligent_curation': True
            }
        }


# Example usage and testing
if __name__ == "__main__":
    print("🤖 Base Agent - Test Mode\n")
    
    # Initialize agent
    agent = BaseAgent("TestAgent")
    
    # Start session
    session_id = agent.start_session("test_user")
    
    # Test queries
    test_queries = [
        "Hi there!",
        "What can you help me with?",
        "How do I create a Docker container?",
        "I'm having trouble with my setup",
        "Explain Kubernetes to me"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = agent.process_query(query, session_id)
        
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Intent: {response.intent}")
        print(f"Sources: {response.sources}")
        print(f"Response time: {response.response_time_ms}ms")
        print("-" * 60)
    
    # Show agent info
    info = agent.get_agent_info()
    print(f"\nAgent Statistics:")
    print(json.dumps(info['statistics'], indent=2))
