#!/usr/bin/env python3
import sys
sys.path.append('.')
from core.dictionary import UniversalDictionary

d = UniversalDictionary()

failing_queries = [
    ("Hi there, how are you?", "greeting"),
    ("Hello, nice to meet you", "greeting"), 
    ("Hello, are you working?", "capability_inquiry")
]

print("🔍 TESTING FIXED BASIC CONVERSATION FAILURES:")
print("=" * 60)

for query, expected_intent in failing_queries:
    actual_intent = d.classify_intent(query)
    
    print(f"\nQuery: '{query}'")
    print(f"Expected Intent: {expected_intent}")
    print(f"Actual Intent: {actual_intent}")
    print(f"Match: {'✅ YES' if actual_intent == expected_intent else '❌ NO'}")
    print("-" * 40)
