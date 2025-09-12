#!/usr/bin/env python3
"""
AI-AH Platform CLI Chat Interface
Real-time interaction with the AI infrastructure assistant
"""

import requests
import json
import sys
import time
from datetime import datetime

class AIChatCLI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.user_id = f"cli_user_{int(time.time())}"
        self.session_id = f"cli_session_{int(time.time())}"
        self.conversation_history = []
        
    def test_connection(self):
        """Test if the API server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/platform/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Connected to AI-AH Platform")
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Agents: {data.get('metrics', {}).get('agents_count', 0)}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to {self.base_url}")
            print("   Make sure the server is running: python main.py")
            return False
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def send_message(self, message):
        """Send message to the agent and get response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/agents/conversation",
                json={
                    'message': message,
                    'user_id': self.user_id,
                    'session_id': self.session_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', 'No response received')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error sending message: {str(e)}"
    
    def format_response(self, response):
        """Format the response for CLI display"""
        # Convert markdown-like formatting to console-friendly text
        formatted = response
        formatted = formatted.replace('## ', '\n📋 ')
        formatted = formatted.replace('### ', '\n  📌 ')
        formatted = formatted.replace('**', '')
        formatted = formatted.replace('•', '  •')
        formatted = formatted.replace('```hcl', '\n💻 Code:\n')
        formatted = formatted.replace('```', '\n')
        return formatted
    
    def run(self):
        """Main CLI loop"""
        print("🤖 AI-AH Multi-Agent Infrastructure Intelligence Platform")
        print("=" * 60)
        
        # Test connection
        if not self.test_connection():
            return
        
        print(f"\n💬 Starting chat session: {self.session_id}")
        print("Type 'exit', 'quit', or 'bye' to end the conversation")
        print("Type 'help' for available commands")
        print("-" * 60)
        
        # Get initial greeting
        greeting = self.send_message("hi")
        print(f"\n🤖 AI Assistant: {self.format_response(greeting)}")
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n👋 Goodbye! Thanks for using AI-AH Platform.")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️ Conversation history cleared.")
                    continue
                
                # Store user message
                self.conversation_history.append({
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'user': user_input,
                    'ai': None
                })
                
                # Send message and get response
                print("🤖 AI Assistant: ", end="", flush=True)
                ai_response = self.send_message(user_input)
                
                # Store AI response
                if len(self.conversation_history) > 0:
                    self.conversation_history[-1]['ai'] = ai_response
                
                # Display formatted response
                formatted_response = self.format_response(ai_response)
                print(formatted_response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using AI-AH Platform.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 Available Commands:")
        print("  help     - Show this help message")
        print("  history  - Show conversation history")
        print("  clear    - Clear conversation history")
        print("  exit     - Exit the chat")
        print("\n💡 Example Queries:")
        print("  • 'list me terraform'")
        print("  • 'create a web server with database'")
        print("  • 'help me optimize costs'")
        print("  • 'set up monitoring for my infrastructure'")
        print("  • 'compare AWS vs Azure'")
    
    def show_history(self):
        """Show conversation history"""
        if not self.conversation_history:
            print("\n📝 No conversation history yet.")
            return
        
        print(f"\n📝 Conversation History ({len(self.conversation_history)} messages):")
        print("-" * 50)
        
        for i, msg in enumerate(self.conversation_history, 1):
            print(f"\n{i}. [{msg['timestamp']}]")
            print(f"   👤 You: {msg['user']}")
            if msg['ai']:
                print(f"   🤖 AI: {msg['ai'][:100]}{'...' if len(msg['ai']) > 100 else ''}")

def main():
    """Main entry point"""
    cli = AIChatCLI()
    cli.run()

if __name__ == "__main__":
    main()
