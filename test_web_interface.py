#!/usr/bin/env python3
"""
Test Web Interface Functionality
===============================

This script tests the web interface API endpoints
"""

import requests
import json
import time

def test_web_interface():
    """Test the web interface functionality"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Web Interface API\n")
    
    # Test 1: Initialize session
    print("1️⃣ Testing session initialization...")
    try:
        response = requests.post(f"{base_url}/api/initialize", json={}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                session_id = data.get('session_id')
                print(f"✅ Session initialized: {session_id}")
            else:
                print(f"❌ Session initialization failed: {data.get('error')}")
                return
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error initializing session: {e}")
        return
    
    # Test 2: Infrastructure creation request
    print("\n2️⃣ Testing infrastructure creation request...")
    try:
        response = requests.post(f"{base_url}/api/chat", json={
            "message": "Create a serverless architecture with Lambda and DynamoDB",
            "session_id": session_id
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Infrastructure request successful")
                print(f"Response: {data.get('response')[:100]}...")
            else:
                print(f"❌ Infrastructure request failed: {data.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error with infrastructure request: {e}")
    
    time.sleep(1)
    
    # Test 3: Requirements response
    print("\n3️⃣ Testing requirements response...")
    try:
        response = requests.post(f"{base_url}/api/chat", json={
            "message": "low",
            "session_id": session_id
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Requirements response successful")
                print(f"Response: {data.get('response')[:100]}...")
            else:
                print(f"❌ Requirements response failed: {data.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error with requirements response: {e}")
    
    time.sleep(1)
    
    # Test 4: Proceed with defaults
    print("\n4️⃣ Testing proceed with defaults...")
    try:
        response = requests.post(f"{base_url}/api/chat", json={
            "message": "proceed with defaults",
            "session_id": session_id
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Proceed with defaults successful")
                print(f"Response: {data.get('response')[:100]}...")
            else:
                print(f"❌ Proceed with defaults failed: {data.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error with proceed with defaults: {e}")
    
    time.sleep(1)
    
    # Test 5: Code generation
    print("\n5️⃣ Testing code generation...")
    try:
        response = requests.post(f"{base_url}/api/chat", json={
            "message": "generate the code",
            "session_id": session_id
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Code generation successful")
                print(f"Response: {data.get('response')[:100]}...")
            else:
                print(f"❌ Code generation failed: {data.get('error')}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error with code generation: {e}")
    
    print("\n🎉 Web interface test completed!")

if __name__ == "__main__":
    test_web_interface()



