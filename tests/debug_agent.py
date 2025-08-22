#!/usr/bin/env python3
"""
Debug Agent Components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.dictionary import UniversalDictionary
from core.pattern_matcher import PatternMatcher

def debug_query(query: str):
    print(f"\n🔍 DEBUGGING QUERY: '{query}'")
    print("=" * 60)
    
    # Test dictionary
    dictionary = UniversalDictionary()
    analysis = dictionary.analyze_query(query)
    
    print(f"📊 DICTIONARY ANALYSIS:")
    print(f"   Keywords: {analysis.keywords}")
    print(f"   Intent: {analysis.intent}")
    print(f"   Complexity: {analysis.complexity}")
    print(f"   Confidence: {analysis.confidence}")
    print(f"   Context: {analysis.context}")
    
    # Test pattern matcher
    pattern_matcher = PatternMatcher()
    pattern_match = pattern_matcher.find_best_match(analysis.keywords, analysis.intent)
    
    print(f"\n🎯 PATTERN MATCHING:")
    if pattern_match:
        print(f"   ✅ FOUND MATCH!")
        print(f"   Pattern ID: {pattern_match.pattern_id}")
        print(f"   Category: {pattern_match.category}")
        print(f"   Keywords: {pattern_match.keywords}")
        print(f"   Confidence: {pattern_match.confidence}")
        print(f"   Template: {pattern_match.response_template[:100]}...")
    else:
        print(f"   ❌ NO PATTERN MATCH FOUND")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_queries = [
        "hi",
        "hello",
        "what can you do",
        "what can you do and list all the things you are capable of",
        "what else you can do"
    ]
    
    for query in test_queries:
        debug_query(query)
