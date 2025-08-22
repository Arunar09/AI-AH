#!/usr/bin/env python3
"""
Interactive Agent Testing
Allow manual testing of the base agent with real user queries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin

def main():
    print("🚀 Starting Interactive Agent Session")
    print("=" * 50)
    
    # Initialize agent
    agent = BaseAgent()
    
    # Register plugins
    docker_config = {
        'name': 'Docker Test Plugin',
        'version': '1.0.0',
        'description': 'Test plugin for Docker operations',
        'keywords': ['docker', 'container', 'image'],
        'confidence_threshold': 0.7
    }
    docker_plugin = DockerPlugin(docker_config)
    agent.plugin_manager.register_plugin(docker_plugin)
    
    # Start session
    session_id = "interactive_session"
    agent.memory.start_session(session_id)
    
    print(f"✅ Agent initialized with session: {session_id}")
    print(f"✅ Registered plugins: {len(agent.plugin_manager.plugins)}")
    print("\n💬 You can now chat with the agent!")
    print("📝 Type 'quit', 'exit', or 'bye' to end the session")
    print("📊 Type 'stats' to see session statistics")
    print("-" * 50)
    
    query_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n🧑 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Session ended.")
                break
            
            # Check for stats command
            if user_input.lower() == 'stats':
                print(f"\n📊 Session Statistics:")
                print(f"   • Queries processed: {query_count}")
                print(f"   • Session ID: {session_id}")
                print(f"   • Active plugins: {len(agent.plugin_manager.plugins)}")
                continue
            
            # Skip empty input
            if not user_input:
                print("❌ Please enter a question or command.")
                continue
            
            # Process query
            query_count += 1
            print(f"\n🤖 Agent (Query #{query_count}):")
            
            try:
                response = agent.process_query(user_input, session_id)
                
                print(f"📝 Response: {response.response}")
                print(f"🎯 Confidence: {response.confidence:.2f}")
                print(f"🧠 Intent: {response.intent}")
                print(f"📚 Context Used: {'Yes' if response.context_used else 'No'}")
                print(f"⏱️ Response Time: {response.response_time_ms:.1f}ms")
                
                if response.plugins_used:
                    print(f"🔌 Plugins Used: {', '.join(response.plugins_used)}")
                
                if response.reasoning:
                    print(f"🤔 Reasoning: {', '.join(response.reasoning)}")
                
                if response.suggestions:
                    print(f"💡 Suggestions: {', '.join(response.suggestions)}")
                
                if not response.success:
                    print(f"⚠️ Warning: Response may have issues")
                
            except Exception as e:
                print(f"❌ Error processing query: {str(e)}")
                print("🔧 Please try a different question.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("🔧 Continuing session...")

if __name__ == "__main__":
    main()
