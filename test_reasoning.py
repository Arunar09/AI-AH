#!/usr/bin/env python3
"""
Test script for reasoning capabilities
"""

from ai_ah_platform.core.intelligence.local_knowledge_base import LocalKnowledgeBase

def test_reasoning():
    """Test the improved reasoning capabilities."""
    kb = LocalKnowledgeBase()
    
    reasoning_tests = [
        'why should I use terraform over manual setup',
        'what happens if I don\'t implement monitoring',
        'how do I choose between aws and azure',
        'explain about ansible',
        'what is kubernetes'
    ]
    
    print("🧠 Testing Reasoning Capabilities")
    print("=" * 50)
    
    for query in reasoning_tests:
        analysis = kb.analyze_request(query)
        reasoning = analysis.get('reasoning', [])
        intent = analysis.get('intent', 'unknown')
        confidence = analysis.get('confidence', 0)
        
        print(f"Query: '{query}'")
        print(f"  -> Intent: {intent}")
        print(f"  -> Confidence: {confidence:.2f}")
        print(f"  -> Reasoning: {reasoning}")
        print()

if __name__ == "__main__":
    test_reasoning()
