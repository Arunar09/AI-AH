#!/usr/bin/env python3
"""
Universal Dictionary System
==========================

This module provides universal language understanding capabilities for all AI agents.
It handles keyword extraction, semantic lookup, and query analysis.

Flow: User Query → Keyword Extraction → Dictionary Lookup → Semantic Understanding
"""

import re
import json
from typing import Dict, List, Any, Set
from dataclasses import dataclass


@dataclass
class QueryAnalysis:
    """Structured result of query analysis"""
    keywords: List[str]
    intent: str
    complexity: str
    context: Dict[str, Any]
    confidence: float


class UniversalDictionary:
    """
    Universal language understanding system
    
    Responsibilities:
    1. Extract meaningful keywords from user queries
    2. Classify query intent (information, command, troubleshooting, etc.)
    3. Assess complexity level (beginner, intermediate, advanced)
    4. Provide semantic understanding of technical terms
    """
    
    def __init__(self):
        """Initialize the dictionary with core language patterns"""
        self.stop_words = {
            'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but',
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him',
            'her', 'us', 'them', 'can', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'shall', 'do', 'does', 'did', 'have',
            'has', 'had', 'be', 'been', 'being'
        }
        
        self.intent_patterns = {
            'greeting': [
                'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 
                'good evening', 'howdy', 'whats up', 'sup', 'good night',
                'bye', 'goodbye', 'see you', 'talk to you later'
            ],
            'personal': [
                'how are you', 'how you doing', 'who are you', 'what are you',
                'tell me about yourself', 'introduce yourself', 'nice to meet you',
                'pleasure to meet you', 'good to meet you'
            ],
            'capability_inquiry': [
                'can you', 'do you', 'are you able', 'what can you do',
                'capabilities', 'features', 'support', 'what can you',
                'what else can you do', 'more capabilities', 'additional features',
                'what other things', 'are you working', 'do you work'
            ],
            'help_request': [
                'help me', 'need help', 'assistance', 'support', 'guidance',
                'can you help', 'could you assist', 'would you help',
                'i need guidance', 'i need advice', 'i need suggestions'
            ],
            'information_request': [
                'what is', 'how does', 'explain', 'describe', 'tell me about',
                'define', 'definition', 'meaning', 'what does mean',
                'how to', 'instructions', 'steps', 'tutorial', 'guide',
                'show me', 'demonstrate', 'walk through', 'walk me through'
            ],
            'troubleshooting': [
                'error', 'problem', 'issue', 'not working', 'failed', 'broken',
                'stuck', 'debug', 'fix', 'resolve', 'something wrong', 
                'went wrong', 'not working properly', 'behaving strangely'
            ],
            'social': [
                'thank you', 'thanks', 'appreciate', 'grateful',
                'please', 'excuse me', 'sorry', 'apologies', 'pardon me',
                'awesome', 'great', 'excellent', 'fantastic', 'wonderful', 'amazing'
            ],
            'clarification': [
                'dont understand', 'confused', 'unclear', 'not sure',
                'what you mean', 'can you repeat', 'again', 'say that again',
                'didnt catch'
            ],
            'conversation': [
                'interesting', 'cool', 'neat', 'thats nice', 'good to know',
                'what do you think', 'your opinion', 'thoughts', 'recommendations'
            ],
            'command_request': [
                'create', 'build', 'setup', 'configure', 'deploy', 'install',
                'run', 'execute', 'start', 'stop', 'delete', 'remove'
            ]
        }
        
        self.complexity_indicators = {
            'beginner': [
                'basic', 'simple', 'introduction', 'getting started', 'first time',
                'new to', 'beginner', 'what is', 'overview', 'fundamentals'
            ],
            'intermediate': [
                'configure', 'setup', 'implement', 'example', 'tutorial',
                'best practice', 'how to', 'step by step'
            ],
            'advanced': [
                'optimize', 'performance', 'scale', 'enterprise', 'production',
                'architecture', 'design pattern', 'complex', 'advanced'
            ]
        }
        
        # Technical term categories for better understanding
        self.technical_categories = {
            'infrastructure': ['server', 'network', 'vpc', 'subnet', 'firewall', 'load balancer'],
            'cloud_providers': ['aws', 'azure', 'gcp', 'google cloud', 'microsoft azure'],
            'tools': ['terraform', 'kubernetes', 'docker', 'ansible', 'jenkins'],
            'programming': ['python', 'javascript', 'java', 'go', 'bash', 'shell'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch']
        }
    
    def extract_keywords(self, query: str) -> List[str]:
        """
        Extract meaningful keywords from query
        
        Process:
        1. Convert to lowercase and clean
        2. Split into words
        3. Remove stop words
        4. Keep technical terms and meaningful words
        5. Return prioritized keyword list
        """
        # Clean and normalize
        query_clean = re.sub(r'[^\w\s-]', ' ', query.lower())
        words = query_clean.split()
        
        # Remove stop words but keep technical terms and capability-related words
        keywords = []
        capability_words = {'can', 'do', 'does', 'help', 'support', 'assist', 'what', 'how', 'why', 'where', 'when', 'hi', 'hello', 'hey'}
        
        for word in words:
            if len(word) >= 2 and (  # Changed from > 2 to >= 2 to include "hi"
                word not in self.stop_words or 
                self._is_technical_term(word) or
                word in capability_words
            ):
                keywords.append(word)
        
        # Remove duplicates while preserving order
        unique_keywords = []
        seen = set()
        for keyword in keywords:
            if keyword not in seen:
                unique_keywords.append(keyword)
                seen.add(keyword)
        
        return unique_keywords
    
    def classify_intent(self, query: str) -> str:
        """
        Classify the intent of the user query with priority ordering
        
        Returns one of: information_request, command_request, troubleshooting,
                       capability_inquiry, greeting, general
        """
        query_lower = query.lower()
        
        # Priority-ordered intent checking (most specific first)
        intent_priority = [
            'capability_inquiry',    # Most specific - what can you do, capabilities, etc.
            'help_request',          # Specific help requests
            'troubleshooting',       # Error, problem, fix, etc.
            'information_request',   # What is, how does, explain, etc.
            'command_request',       # How to, create, build, etc.
            'social',                # Thank you, sorry, great, etc.
            'clarification',         # Don't understand, confused, etc.
            'conversation',          # Opinion, interesting, etc.
            'greeting',              # Hi, hello, bye, etc. - moved up from personal
            'personal'               # Who are you, how are you, etc. - moved to end
        ]
        
        # Check patterns in priority order
        for intent in intent_priority:
            if intent in self.intent_patterns:
                patterns = self.intent_patterns[intent]
                # Use exact phrase matching for better accuracy
                for pattern in patterns:
                    if pattern in query_lower:
                        return intent
        
        return 'general'
    
    def assess_complexity(self, query: str) -> str:
        """
        Assess the complexity level of the query
        
        Returns: beginner, intermediate, or advanced
        """
        query_lower = query.lower()
        
        # Check complexity indicators
        for level, indicators in self.complexity_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                return level
        
        # Default based on query length and structure
        if len(query.split()) <= 5:
            return 'beginner'
        elif any(word in query_lower for word in ['how to', 'step by step', 'tutorial']):
            return 'intermediate'
        else:
            return 'intermediate'
    
    def get_context(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Extract context information from keywords
        
        Returns dictionary with:
        - technical_domains: List of relevant technical domains
        - tools_mentioned: List of tools mentioned
        - action_type: Type of action requested
        """
        context = {
            'technical_domains': [],
            'tools_mentioned': [],
            'action_type': None
        }
        
        # Identify technical domains
        for keyword in keywords:
            for domain, terms in self.technical_categories.items():
                if keyword in terms:
                    if domain not in context['technical_domains']:
                        context['technical_domains'].append(domain)
                    context['tools_mentioned'].append(keyword)
        
        # Identify action type
        action_keywords = {
            'create': ['create', 'build', 'setup', 'configure'],
            'read': ['show', 'list', 'display', 'get', 'describe'],
            'update': ['update', 'modify', 'change', 'edit'],
            'delete': ['delete', 'remove', 'destroy', 'terminate']
        }
        
        for action, verbs in action_keywords.items():
            if any(verb in keywords for verb in verbs):
                context['action_type'] = action
                break
        
        return context
    
    def analyze_query(self, query: str) -> QueryAnalysis:
        """
        Complete query analysis combining all dictionary capabilities
        
        This is the main entry point for query understanding
        """
        # Extract components
        keywords = self.extract_keywords(query)
        intent = self.classify_intent(query)
        complexity = self.assess_complexity(query)
        context = self.get_context(keywords)
        
        # Calculate confidence based on how well we understood the query
        confidence = self._calculate_confidence(query, keywords, intent, context)
        
        return QueryAnalysis(
            keywords=keywords,
            intent=intent,
            complexity=complexity,
            context=context,
            confidence=confidence
        )
    
    def _is_technical_term(self, word: str) -> bool:
        """Check if a word is a technical term that should be preserved"""
        for category, terms in self.technical_categories.items():
            if word in terms:
                return True
        return False
    
    def _calculate_confidence(self, query: str, keywords: List[str], 
                            intent: str, context: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence for clear intent
        if intent != 'general':
            confidence += 0.2
        
        # Boost confidence for technical terms
        if context['tools_mentioned']:
            confidence += 0.2
        
        # Boost confidence for clear action
        if context['action_type']:
            confidence += 0.1
        
        # Boost confidence for sufficient keywords
        if len(keywords) >= 2:
            confidence += 0.1
        
        return min(confidence, 1.0)


# Example usage and testing
if __name__ == "__main__":
    print("🧠 Universal Dictionary System - Test Mode\n")
    
    dictionary = UniversalDictionary()
    
    # Test queries
    test_queries = [
        "How do I create a VPC in AWS?",
        "What is Terraform?",
        "Help me troubleshoot Docker container errors",
        "Show me Kubernetes deployment examples",
        "Hi, what can you do?"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        analysis = dictionary.analyze_query(query)
        print(f"Keywords: {analysis.keywords}")
        print(f"Intent: {analysis.intent}")
        print(f"Complexity: {analysis.complexity}")
        print(f"Context: {analysis.context}")
        print(f"Confidence: {analysis.confidence:.2f}")
        print("-" * 50)
