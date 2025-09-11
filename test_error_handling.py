#!/usr/bin/env python3
"""
Test script for error handling improvements
"""

from ai_ah_platform.core.intelligence.local_knowledge_base import LocalKnowledgeBase

def test_error_handling():
    """Test the improved error handling."""
    kb = LocalKnowledgeBase()
    
    error_cases = [
        '',  # Empty query
        'asdfghjkl',  # Nonsensical query
        'explain quantum computing',  # Out of scope
        'how to cook pasta',  # Out of scope
        'hi',  # Short but valid
        'help'  # Short but valid
    ]
    
    print("🛡️ Testing Error Handling Improvements")
    print("=" * 50)
    
    for query in error_cases:
        analysis = kb.analyze_request(query)
        intent = analysis.get('intent', 'unknown')
        confidence = analysis.get('confidence', 0)
        reasoning = analysis.get('reasoning', [])
        
        print(f"Query: '{query}'")
        print(f"  -> Intent: {intent}")
        print(f"  -> Confidence: {confidence:.2f}")
        print(f"  -> Reasoning: {reasoning}")
        print()

if __name__ == "__main__":
    test_error_handling()
