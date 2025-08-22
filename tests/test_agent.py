#!/usr/bin/env python3
"""
Base Agent Test Suite
====================

Simple test script to validate the base agent functionality
"""

import json
from base_agent import BaseAgent


def test_basic_functionality():
    """Test basic agent functionality"""
    print("🧪 Testing Basic Agent Functionality\n")
    
    # Initialize agent
    print("1. Initializing agent...")
    agent = BaseAgent("TestAgent")
    
    # Start session
    print("2. Starting session...")
    session_id = agent.start_session("test_user")
    print(f"   Session ID: {session_id}")
    
    # Test basic queries
    print("3. Testing basic queries...")
    
    test_queries = [
        {
            'query': "Hello!",
            'expected_intent': 'greeting',
            'min_confidence': 0.8
        },
        {
            'query': "What can you do?",
            'expected_intent': 'capability_inquiry',
            'min_confidence': 0.7
        },
        {
            'query': "Help me with Docker",
            'expected_intent': 'information_request',
            'min_confidence': 0.5
        },
        {
            'query': "I have an error",
            'expected_intent': 'troubleshooting',
            'min_confidence': 0.6
        }
    ]
    
    passed = 0
    total = len(test_queries)
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case['query']
        expected_intent = test_case['expected_intent']
        min_confidence = test_case['min_confidence']
        
        print(f"\n   Test {i}: '{query}'")
        
        try:
            response = agent.process_query(query, session_id)
            
            # Check if successful
            if response.success:
                print(f"   ✅ Success: {response.response[:50]}...")
                print(f"   📊 Intent: {response.intent} (expected: {expected_intent})")
                print(f"   📊 Confidence: {response.confidence:.2f} (min: {min_confidence})")
                print(f"   📊 Response time: {response.response_time_ms}ms")
                
                # Validate intent and confidence
                intent_match = response.intent == expected_intent
                confidence_ok = response.confidence >= min_confidence
                
                if intent_match and confidence_ok:
                    print(f"   ✅ Test passed!")
                    passed += 1
                else:
                    print(f"   ❌ Test failed - Intent: {intent_match}, Confidence: {confidence_ok}")
            else:
                print(f"   ❌ Failed: {response.response}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    return passed == total


def test_conversation_flow():
    """Test conversation flow and memory"""
    print("\n🗣️ Testing Conversation Flow\n")
    
    agent = BaseAgent("ConversationAgent")
    session_id = agent.start_session("conversation_user")
    
    conversation = [
        "Hi there!",
        "I want to learn about Docker",
        "How do I install it?",
        "What about containers?",
        "Thanks for your help!"
    ]
    
    print("Simulating conversation:")
    for i, query in enumerate(conversation, 1):
        print(f"\n{i}. User: {query}")
        
        try:
            response = agent.process_query(query, session_id)
            print(f"   Agent: {response.response[:100]}...")
            print(f"   Context used: {response.context_used}")
            print(f"   Sources: {response.sources}")
            
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    return True


def test_agent_statistics():
    """Test agent statistics and info"""
    print("\n📈 Testing Agent Statistics\n")
    
    agent = BaseAgent("StatsAgent")
    session_id = agent.start_session("stats_user")
    
    # Generate some interactions
    queries = ["Hello", "What can you do?", "Help me", "Explain Docker", "Thanks"]
    
    for query in queries:
        try:
            agent.process_query(query, session_id)
        except Exception as e:
            print(f"Error processing '{query}': {e}")
    
    # Get agent info
    try:
        info = agent.get_agent_info()
        print("Agent Information:")
        print(f"  Name: {info['name']}")
        print(f"  Version: {info['version']}")
        print(f"  Current session: {info['current_session']}")
        
        print("\nStatistics:")
        stats = info['statistics']
        print(f"  Patterns: {stats.get('patterns', {})}")
        print(f"  Memory: {stats.get('memory', {})}")
        print(f"  Plugins: {stats.get('plugins', {})}")
        
        print("\nCapabilities:")
        for capability, status in info['capabilities'].items():
            print(f"  {capability}: {'✅' if status else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"Error getting agent info: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Base Agent Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Conversation Flow", test_conversation_flow),
        ("Agent Statistics", test_agent_statistics)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if test_func():
                print(f"✅ {test_name} - PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n{'='*60}")
    print(f"🏁 Test Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Base agent is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
