#!/usr/bin/env python3
"""
Test the networking false positive fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin

def test_networking_fix():
    """Test if networking no longer falsely activates Docker plugin"""
    print("🔍 Testing Networking False Positive Fix...")
    
    # Initialize agent
    agent = BaseAgent("TestAgent")
    
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
    
    session_id = agent.start_session("test_user")
    
    # Test the problematic query
    query = "How does networking work?"
    
    response = agent.process_query(query, session_id)
    plugins_used = response.plugins_used
    
    print(f"Query: '{query}'")
    print(f"Plugins used: {plugins_used}")
    print(f"Should activate: False")
    
    if len(plugins_used) == 0:
        print("✅ FIXED! Docker plugin no longer falsely activates")
    else:
        print(f"❌ Still failing. Plugins used: {plugins_used}")

if __name__ == "__main__":
    test_networking_fix()
