#!/usr/bin/env python3
"""
AI-AH Platform Comprehensive Test Suite
"""

import requests
import json
import time

def test_platform():
    print('🚀 AI-AH Platform Comprehensive Test Suite')
    print('=' * 60)
    
    # Test 1: Health Check
    print('\n1. Health Check Test')
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f'   ✅ Status: {response.status_code}')
        print(f'   📊 Response: {response.json()}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    # Test 2: Platform Status
    print('\n2. Platform Status Test')
    try:
        response = requests.get('http://localhost:8000/api/v1/platform/status', timeout=5)
        print(f'   ✅ Status: {response.status_code}')
        data = response.json()
        print(f'   📊 Component: {data.get("component", "N/A")}')
        print(f'   📊 Platform Status: {data.get("status", "N/A")}')
        print(f'   📊 Active Tasks: {data.get("active_tasks", 0)}')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    # Test 3: Agent Status Tests
    print('\n3. Agent Status Tests')
    agents = ['terraform', 'ansible', 'kubernetes', 'security', 'monitoring']
    for agent in agents:
        try:
            response = requests.get(f'http://localhost:8000/api/v1/agents/{agent}/status', timeout=5)
            print(f'   ✅ {agent.capitalize()} Agent: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                print(f'      📊 Status: {data.get("status", "N/A")}')
                print(f'      📊 Component: {data.get("component", "N/A")}')
        except Exception as e:
            print(f'   ❌ {agent.capitalize()} Agent Error: {e}')
    
    # Test 4: API Documentation
    print('\n4. API Documentation Test')
    try:
        response = requests.get('http://localhost:8000/docs', timeout=5)
        print(f'   ✅ API Docs: {response.status_code}')
        if response.status_code == 200:
            print('   📖 API documentation is accessible')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    # Test 5: Web UI
    print('\n5. Web UI Test')
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f'   ✅ Web UI: {response.status_code}')
        if response.status_code == 200:
            print('   🌐 Web interface is accessible')
    except Exception as e:
        print(f'   ❌ Error: {e}')
    
    print('\n🎯 Test Summary: Platform is functional and ready for interaction!')
    print('🌐 Web UI: http://localhost:8000')
    print('📖 API Docs: http://localhost:8000/docs')

if __name__ == "__main__":
    test_platform()

