#!/usr/bin/env python3
"""
Test CodeLlama Integration
Tests the local model integration with the Terraform agent
"""

import os
import sys
import json
from typing import Dict, Any

# Add the project root to the path
sys.path.append(os.path.dirname(__file__))

def test_local_model_availability():
    """Test if local model is available"""
    print("🔍 Testing Local Model Availability...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.models import is_local_model_available, get_local_model
        
        if is_local_model_available():
            print("✅ Local model is available!")
            model = get_local_model()
            model_info = model.get_model_info()
            print(f"📊 Model Info: {json.dumps(model_info, indent=2)}")
            return True
        else:
            print("❌ Local model is not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing local model: {e}")
        return False

def test_reasoning_engine_integration():
    """Test reasoning engine with local model"""
    print("\n🧠 Testing Reasoning Engine Integration...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.reasoning.local_reasoning_engine import LocalReasoningEngine
        
        engine = LocalReasoningEngine()
        model_status = engine.get_model_status()
        print(f"📊 Reasoning Engine Model Status: {json.dumps(model_status, indent=2)}")
        
        # Test reasoning
        result = engine.reason_through_problem("Create a web application for 1000 users", {})
        print(f"✅ Reasoning completed with confidence: {result.confidence:.2f}")
        print(f"📝 Explanation preview: {result.explanation[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing reasoning engine: {e}")
        return False

def test_terraform_agent_integration():
    """Test Terraform agent with local model"""
    print("\n🏗️ Testing Terraform Agent Integration...")
    
    try:
        sys.path.append('intelligent-agents')
        from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
        
        agent = IntelligentTerraformAgent()
        
        # Test with a simple request
        test_request = "Create a web application infrastructure for 1000 users with AWS"
        response = agent.process_request(test_request)
        
        print(f"✅ Terraform agent completed with confidence: {response.confidence:.2f}")
        print(f"💰 Cost estimate: ${response.cost_estimate:.2f}")
        print(f"📁 Generated files: {list(response.terraform_code.keys())}")
        
        # Show a preview of the generated code
        if response.terraform_code:
            first_file = list(response.terraform_code.keys())[0]
            print(f"📝 {first_file} preview:")
            print(response.terraform_code[first_file][:300] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Terraform agent: {e}")
        return False

def test_local_model_direct():
    """Test local model directly"""
    print("\n🤖 Testing Local Model Directly...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.models import get_local_model
        
        model = get_local_model()
        
        # Simple test prompt
        test_prompt = "<s>[INST] Write a simple Python function to add two numbers. [/INST]"
        response = model.generate_response(test_prompt, max_tokens=100, temperature=0.3)
        
        print(f"✅ Direct model test completed")
        print(f"📝 Response: {response.content}")
        print(f"⏱️ Response time: {response.response_time:.2f}s")
        print(f"🎯 Tokens used: {response.tokens_used}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing local model directly: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting CodeLlama Integration Tests\n")
    
    tests = [
        ("Local Model Availability", test_local_model_availability),
        ("Reasoning Engine Integration", test_reasoning_engine_integration),
        ("Terraform Agent Integration", test_terraform_agent_integration),
        ("Direct Model Test", test_local_model_direct)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CodeLlama integration is working!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
