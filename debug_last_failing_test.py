#!/usr/bin/env python3
"""
Debug the last failing test in Plugin Integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin

def debug_last_failing_test():
    """Debug the last failing test"""
    print("🔍 Debugging Last Failing Test in Plugin Integration...")
    
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
    
    # Test all plugin integration cases
    print("\n🔍 Testing All Plugin Integration Cases:")
    plugin_tests = [
        ("What is Docker?", True),
        ("How do I run a Docker container?", True),
        ("Explain containerization", True),
        ("Docker installation guide", True),
        ("Create a Dockerfile", True),
        ("Docker build command", True),
        ("Container troubleshooting", True),
        ("Docker image management", True),
        ("Container networking", True),
        ("Docker volumes explained", True),
        ("Hello world", False),
        ("What can you do?", False),
        ("Explain machine learning", False),
        ("How does networking work?", False),
        ("Python programming help", False),
        ("Database design principles", False),
        ("Cloud computing overview", False),
        ("Software architecture", False),
        ("Good morning", False),
        ("Help me understand APIs", False)
    ]
    
    for i, (query, should_activate) in enumerate(plugin_tests):
        response = agent.process_query(query, session_id)
        plugins_used = response.plugins_used
        success = (should_activate and len(plugins_used) > 0) or (not should_activate and len(plugins_used) == 0)
        status = "✅" if success else "❌"
        print(f"{status} Test {i+1}: '{query}'")
        print(f"   Should activate: {should_activate}, Plugins used: {plugins_used}")
        print(f"   Success: {success}")
        print()

if __name__ == "__main__":
    debug_last_failing_test()
