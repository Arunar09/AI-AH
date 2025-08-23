#!/usr/bin/env python3
"""
Debug script to identify exactly which tests are failing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin

def debug_failing_tests():
    """Debug the specific failing tests"""
    print("🔍 Debugging Failing Tests...")
    
    # Initialize agent
    agent = BaseAgent("DebugAgent")
    
    # Add Docker plugin
    docker_config = {
        'name': 'Docker Test Plugin',
        'version': '1.0.0',
        'description': 'Docker plugin for testing',
        'keywords': ['docker', 'container', 'dockerfile'],
        'confidence_threshold': 0.4
    }
    docker_plugin = DockerPlugin(docker_config)
    agent.register_plugin(docker_plugin)
    
    session_id = agent.start_session("debug_user")
    
    # Test Intent Classification failures
    print("\n🔍 Testing Intent Classification Issues:")
    intent_tests = [
        ("What is Docker?", "information_request"),
        ("Explain containerization", "information_request"),
        ("How do I install Docker?", "command_request"),
        ("Create a new container", "command_request"),
        ("I have an error with my setup", "troubleshooting"),
        ("My container is not working", "troubleshooting"),
        ("How does this work and why?", "information_request"),
        ("Install and configure Docker", "command_request"),
        ("What's wrong with my installation?", "troubleshooting"),
        ("Help me understand this error", "troubleshooting")
    ]
    
    for query, expected in intent_tests:
        response = agent.process_query(query, session_id)
        status = "✅" if response.intent == expected else "❌"
        print(f"{status} Query: '{query}'")
        print(f"   Expected: {expected}, Got: {response.intent}")
        print(f"   Confidence: {response.confidence}")
        print()
    
    # Test Plugin Integration failures
    print("\n🔍 Testing Plugin Integration Issues:")
    plugin_tests = [
        ("What is Docker?", True),
        ("How do I run a Docker container?", True),
        ("Explain containerization", True),
        ("Docker installation guide", True),
        ("Create a Dockerfile", True),
        ("Hello world", False),
        ("What can you do?", False),
        ("Explain machine learning", False)
    ]
    
    for query, should_activate in plugin_tests:
        response = agent.process_query(query, session_id)
        plugins_used = response.plugins_used
        status = "✅" if (should_activate and len(plugins_used) > 0) or (not should_activate and len(plugins_used) == 0) else "❌"
        print(f"{status} Query: '{query}'")
        print(f"   Should activate: {should_activate}, Plugins used: {plugins_used}")
        print(f"   Confidence: {response.confidence}")
        print()

if __name__ == "__main__":
    debug_failing_tests()
