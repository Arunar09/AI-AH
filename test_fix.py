#!/usr/bin/env python3
"""
Simple test to verify the base agent fix is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.base_agent import BaseAgent
from core.terraform_engineer_plugin import TerraformEngineerPlugin

def test_command_execution():
    print("🧪 Testing Base Agent Command Execution Fix")
    print("=" * 50)
    
    # Initialize agent
    agent = BaseAgent()
    
    # Register Terraform Engineer plugin
    terraform_config = {
        'terraform_dir': './web_terraform_workspace',
        'name': 'Terraform Engineer',
        'version': '2.0.0',
        'description': 'Real infrastructure engineering capabilities'
    }
    terraform_plugin = TerraformEngineerPlugin(terraform_config)
    agent.plugin_manager.register_plugin(terraform_plugin)
    
    # Test query
    test_query = "Create a serverless architecture with Lambda and DynamoDB"
    print(f"🔍 Testing query: '{test_query}'")
    
    # Test the command execution logic directly
    from core.base_agent import QueryAnalysis
    
    # Create a mock query analysis
    query_analysis = QueryAnalysis(
        keywords=['create', 'serverless', 'architecture', 'lambda', 'dynamodb'],
        intent='command_request',
        complexity='medium',
        context={'domain': 'infrastructure'},
        confidence=0.8
    )
    
    print("\n🔍 Testing _is_command_execution_request...")
    is_command = agent._is_command_execution_request(test_query, query_analysis)
    print(f"   Result: {is_command}")
    
    print("\n🔍 Testing _determine_tool_name...")
    tool_name = agent._determine_tool_name(test_query, query_analysis)
    print(f"   Result: {tool_name}")
    
    print("\n🔍 Testing _execute_plugin_commands...")
    responses = agent._execute_plugin_commands(test_query, query_analysis)
    print(f"   Number of responses: {len(responses)}")
    
    for i, response in enumerate(responses):
        print(f"   Response {i+1}: {response.success} - {response.content[:100]}...")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_command_execution()
