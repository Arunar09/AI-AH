#!/usr/bin/env python3
"""
AI-AH Platform Agent Interaction Test Suite
"""

import requests
import json

def test_agent_interaction():
    print('🤖 Testing Agent Interaction Capabilities')
    print('=' * 50)
    
    # Test Terraform Agent Request
    print('\n1. Testing Terraform Agent Request:')
    terraform_request = {
        'requirements': 'Create a web server in AWS with load balancer',
        'context': {'environment': 'development', 'region': 'us-east-1'},
        'request_id': 'test_001'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/agents/terraform/request',
            json=terraform_request,
            timeout=10
        )
        print(f'   ✅ Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   📊 Agent ID: {data.get("agent_id")}')
            print(f'   📊 Response Type: {data.get("response_type")}')
            print(f'   📊 Confidence: {data.get("confidence")}')
            content = str(data.get("content", ""))
            print(f'   📊 Content Preview: {content[:100]}...')
        else:
            print(f'   ❌ Error: {response.text}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    # Test Conversation Endpoint
    print('\n2. Testing Conversation Endpoint:')
    conversation_request = {
        'message': 'Help me set up a Kubernetes cluster',
        'agent_type': 'kubernetes',
        'user_id': 'test_user',
        'session_id': 'test_session_001',
        'context': {'environment': 'production'}
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/agents/conversation',
            json=conversation_request,
            timeout=10
        )
        print(f'   ✅ Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   📊 Session ID: {data.get("session_id")}')
            print(f'   📊 Agent Type: {data.get("agent_type")}')
            print(f'   📊 Confidence: {data.get("confidence")}')
            response_content = str(data.get("response", ""))
            print(f'   📊 Response Preview: {response_content[:100]}...')
        else:
            print(f'   ❌ Error: {response.text}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    # Test Platform Info
    print('\n3. Testing Platform Info:')
    try:
        response = requests.get('http://localhost:8000/api/v1/platform/info', timeout=5)
        print(f'   ✅ Status: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   📊 Platform Name: {data.get("data", {}).get("name", "N/A")}')
            print(f'   📊 Version: {data.get("data", {}).get("version", "N/A")}')
            print(f'   📊 Environment: {data.get("data", {}).get("environment", "N/A")}')
        else:
            print(f'   ❌ Error: {response.text}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    print('\n✅ Agent interaction tests completed!')
    print('🌐 You can now interact with the platform at: http://localhost:8000')

if __name__ == "__main__":
    test_agent_interaction()

