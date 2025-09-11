#!/usr/bin/env python3
"""
Test script for pattern matching improvements
"""

from ai_ah_platform.core.intelligence.local_knowledge_base import LocalKnowledgeBase

def test_pattern_matching():
    """Test the improved pattern matching."""
    kb = LocalKnowledgeBase()
    
    test_cases = [
        'explain about terraform',
        'what is kubernetes', 
        'tell me about docker',
        'how does monitoring work',
        'explain about aws',
        'what is azure',
        'tell me about gcp'
    ]
    
    print("🧠 Testing Pattern Matching Improvements")
    print("=" * 50)
    
    for query in test_cases:
        analysis = kb.analyze_request(query)
        agent_type = analysis.get('agent_type', 'unknown')
        technology = analysis.get('parameters', {}).get('technology', 'unknown')
        confidence = analysis.get('confidence', 0)
        
        print(f"Query: '{query}'")
        print(f"  -> Agent: {agent_type}")
        print(f"  -> Technology: {technology}")
        print(f"  -> Confidence: {confidence:.2f}")
        print()

if __name__ == "__main__":
    test_pattern_matching()
