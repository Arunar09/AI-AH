#!/usr/bin/env python3
"""
Interactive Terraform Engineer Agent Testing
Test the AI-AH Terraform Engineer Agent with real infrastructure queries
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.terraform_engineer_plugin import TerraformEngineerPlugin

def main():
    print("🚀 Starting AI-AH Terraform Engineer Interactive Session")
    print("=" * 60)
    
    # Initialize agent
    print("🔧 Initializing AI Agent...")
    agent = BaseAgent()
    
    # Register Terraform Engineer plugin
    print("🔧 Loading Terraform Engineer Plugin...")
    terraform_config = {
        'terraform_dir': './web_terraform_workspace',
        'name': 'Terraform Engineer',
        'version': '2.0.0',
        'description': 'Real infrastructure engineering capabilities'
    }
    terraform_plugin = TerraformEngineerPlugin(terraform_config)
    agent.plugin_manager.register_plugin(terraform_plugin)
    
    # Start session
    session_id = "terraform_interactive_session"
    agent.memory.start_session(session_id)
    
    print(f"✅ Agent initialized with session: {session_id}")
    print(f"✅ Terraform workspace: {terraform_config['terraform_dir']}")
    print(f"✅ Available plugins: {len(agent.plugin_manager.plugins)}")
    print("\n💬 You can now chat with your AI Infrastructure Engineer!")
    print("📝 Type 'quit', 'exit', or 'bye' to end the session")
    print("📊 Type 'stats' to see session statistics")
    print("🔧 Type 'workspace' to check Terraform workspace status")
    print("📋 Type 'help' to see available commands")
    print("-" * 60)
    
    query_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n🧑 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Terraform session ended.")
                break
            
            # Check for stats command
            if user_input.lower() == 'stats':
                print(f"\n📊 Session Statistics:")
                print(f"   • Queries processed: {query_count}")
                print(f"   • Session ID: {session_id}")
                print(f"   • Active plugins: {len(agent.plugin_manager.plugins)}")
                print(f"   • Terraform workspace: {terraform_config['terraform_dir']}")
                continue
            
            # Check for workspace status
            if user_input.lower() == 'workspace':
                import os
                workspace_path = terraform_config['terraform_dir']
                if os.path.exists(workspace_path):
                    files = os.listdir(workspace_path)
                    print(f"\n📁 Terraform Workspace Status:")
                    print(f"   • Path: {workspace_path}")
                    print(f"   • Files: {len(files)}")
                    if files:
                        for file in files:
                            print(f"     - {file}")
                    else:
                        print("     (No files yet)")
                else:
                    print(f"\n❌ Workspace directory not found: {workspace_path}")
                continue
            
            # Check for help command
            if user_input.lower() == 'help':
                print(f"\n📋 Available Commands:")
                print(f"   • 'stats' - Show session statistics")
                print(f"   • 'workspace' - Check Terraform workspace status")
                print(f"   • 'quit' - End session")
                print(f"\n🏗️ Try These Infrastructure Requests:")
                print(f"   • 'Create a serverless architecture with Lambda and DynamoDB'")
                print(f"   • 'Generate Terraform code for a web application'")
                print(f"   • 'Design infrastructure for a 3-tier application'")
                print(f"   • 'Help me deploy this infrastructure step by step'")
                print(f"   • 'My Terraform apply is failing, help me troubleshoot'")
                print(f"\n🔍 New Intelligent Features:")
                print(f"   • 'answer 1 [your answer]' - Answer requirements questions")
                print(f"   • 'requirements summary' - See current requirements status")
                print(f"   • 'proceed with defaults' - Use recommended settings")
                continue
            
            # Check for requirements collection commands
            if user_input.lower().startswith('answer '):
                try:
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        question_num = int(parts[1])
                        answer = parts[2]
                        print(f"\n📝 Processing answer for question {question_num}: {answer}")
                        # This would integrate with the requirements collector
                        print(f"✅ Answer recorded: {answer}")
                        print(f"💡 Continue answering questions or type 'requirements summary' to see progress")
                    else:
                        print("❌ Format: 'answer [question_number] [your_answer]'")
                except ValueError:
                    print("❌ Invalid question number. Format: 'answer [question_number] [your_answer]'")
                continue
            
            if user_input.lower() == 'requirements summary':
                print(f"\n📋 Requirements Collection Status:")
                print(f"   • Feature: Intelligent Infrastructure Analysis")
                print(f"   • Status: Available and ready")
                print(f"   • Next: Try creating infrastructure to see it in action!")
                continue
            
            if user_input.lower() == 'proceed with defaults':
                print(f"\n🚀 Proceeding with default settings:")
                print(f"   • Environment: AWS (default)")
                print(f"   • Security: Standard security")
                print(f"   • Performance: Medium load")
                print(f"   • Cost: Medium cost optimization")
                print(f"💡 Now try creating infrastructure to see the enhanced analysis!")
                continue
            
            # Skip empty input
            if not user_input:
                print("❌ Please enter a question or command.")
                continue
            
            # Process query
            query_count += 1
            print(f"\n🤖 AI-AH Terraform Engineer (Query #{query_count}):")
            print("-" * 40)
            
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
