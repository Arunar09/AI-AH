#!/usr/bin/env python3
"""
Test the specific fix for intent classification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dictionary import UniversalDictionary

def test_specific_fix():
    """Test the specific failing query"""
    print("🔍 Testing Specific Intent Classification Fix...")
    
    dictionary = UniversalDictionary()
    
    # The problematic query
    query = "How does this work and why?"
    
    analysis = dictionary.analyze_query(query)
    
    print(f"Query: '{query}'")
    print(f"Intent: {analysis.intent}")
    print(f"Confidence: {analysis.confidence}")
    print(f"Keywords: {analysis.keywords}")
    
    # Check if it's fixed
    if analysis.intent == "information_request":
        print("✅ FIXED! Intent is now information_request")
    else:
        print(f"❌ Still failing. Got: {analysis.intent}")

if __name__ == "__main__":
    test_specific_fix()
