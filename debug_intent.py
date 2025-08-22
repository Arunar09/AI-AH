#!/usr/bin/env python3
import sys
sys.path.append('.')
from core.dictionary import UniversalDictionary

d = UniversalDictionary()
test_queries = [
    'What are your features?',
    'What are your capabilities?', 
    'Do you support technical questions?',
    'Show me how this works',
    'Fix this problem',
    'Hello',
    'What can you do?'
]

print("🔍 TESTING FIXED INTENT CLASSIFICATION:")
print("=" * 50)
for query in test_queries:
    intent = d.classify_intent(query)
    print(f'Query: "{query}" -> Intent: {intent}')
