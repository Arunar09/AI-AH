#!/usr/bin/env python3
import sys
sys.path.append('.')
from core.dictionary import UniversalDictionary
from core.example_docker_plugin import DockerPlugin

d = UniversalDictionary()

failing_queries = [
    "Explain containerization",
    "Create a Dockerfile", 
    "Container troubleshooting",
    "Container networking"
]

print("🔍 DEBUGGING PLUGIN KEYWORD EXTRACTION:")
print("=" * 60)

for query in failing_queries:
    analysis = d.analyze_query(query)
    
    print(f"\nQuery: '{query}'")
    print(f"Keywords: {analysis.keywords}")
    print(f"Intent: {analysis.intent}")
    print(f"Context: {analysis.context}")
    
    # Test if plugin can handle
    docker_config = {
        'name': 'Docker Test Plugin',
        'version': '1.0.0',
        'description': 'Test plugin for Docker operations',
        'keywords': ['docker', 'container', 'image'],
        'confidence_threshold': 0.4  # Lowered threshold
    }
    docker_plugin = DockerPlugin(docker_config)
    
    query_analysis = {
        'keywords': analysis.keywords,
        'context': analysis.context,
        'intent': analysis.intent
    }
    
    can_handle_score = docker_plugin.can_handle(query_analysis)
    print(f"Plugin can_handle score: {can_handle_score}")
    print(f"Above threshold (0.4)? {'YES' if can_handle_score >= 0.4 else 'NO'}")
    print("-" * 40)
