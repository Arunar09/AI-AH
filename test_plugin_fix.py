#!/usr/bin/env python3
import sys
sys.path.append('.')
from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin

# Test the fixed plugin
agent = BaseAgent()

# Register Docker plugin
docker_config = {
    'name': 'Docker Test Plugin',
    'version': '1.0.0',
    'description': 'Test plugin for Docker operations',
    'keywords': ['docker', 'container', 'image'],
    'confidence_threshold': 0.4
}
docker_plugin = DockerPlugin(docker_config)
agent.plugin_manager.register_plugin(docker_plugin)

session_id = agent.start_session()

# Test the failing queries
failing_queries = [
    "Explain containerization",
    "Create a Dockerfile", 
    "Container troubleshooting",
    "Container networking"
]

print("🧪 TESTING FIXED PLUGIN INTEGRATION:")
print("=" * 50)

for query in failing_queries:
    response = agent.process_query(query, session_id)
    print(f"\nQuery: '{query}'")
    print(f"Plugins Used: {response.plugins_used}")
    print(f"Confidence: {response.confidence:.3f}")
    print(f"Response: {response.response[:80]}...")
