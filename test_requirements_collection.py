#!/usr/bin/env python3
"""
Test Requirements Collection Functionality
=========================================

This script tests the updated requirements collection system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.base_agent import BaseAgent, QueryAnalysis

def test_requirements_collection():
    """Test the requirements collection functionality"""
    print("🧪 Testing Requirements Collection System\n")
    
    # Initialize agent
    agent = BaseAgent("TestRequirements")
    session_id = agent.start_session("test_user")
    
    # Test 1: Infrastructure creation request
    print("1️⃣ Testing infrastructure creation request...")
    query = "Create a serverless architecture with Lambda and DynamoDB"
    response = agent.process_query(query, session_id)
    print(f"✅ Response: {response.response[:200]}...")
    print()
    
    # Test 2: Requirements response
    print("2️⃣ Testing requirements response...")
    query = "answer 1 medium"
    response = agent.process_query(query, session_id)
    print(f"✅ Response: {response.response[:200]}...")
    print()
    
    # Test 3: Requirements summary
    print("3️⃣ Testing requirements summary...")
    query = "requirements summary"
    response = agent.process_query(query, session_id)
    print(f"✅ Response: {response.response[:200]}...")
    print()
    
    # Test 4: Proceed with defaults
    print("4️⃣ Testing proceed with defaults...")
    query = "proceed with defaults"
    response = agent.process_query(query, session_id)
    print(f"✅ Response: {response.response[:200]}...")
    print()
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    test_requirements_collection()



