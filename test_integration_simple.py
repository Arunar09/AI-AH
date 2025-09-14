#!/usr/bin/env python3
"""
Simple Integration Test
Tests the simplified CodeLlama integration
"""

import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(__file__))

def test_simple_model():
    """Test simple model directly"""
    print("🤖 Testing Simple Model...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.models.simple_local_model import get_simple_model, is_simple_model_available
        
        if is_simple_model_available():
            print("✅ Simple model is available!")
            model = get_simple_model()
            
            # Test generation
            response = model.generate_response("<s>[INST] Write a simple Python function to add two numbers. [/INST]", max_tokens=100)
            print(f"📝 Response: {response[:200]}...")
            return True
        else:
            print("❌ Simple model is not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing simple model: {e}")
        return False

def test_reasoning_engine():
    """Test reasoning engine with simple model"""
    print("\n🧠 Testing Reasoning Engine...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.reasoning.local_reasoning_engine import LocalReasoningEngine
        
        engine = LocalReasoningEngine()
        
        # Test reasoning
        result = engine.reason_through_problem("Create a web application for 1000 users", {})
        print(f"✅ Reasoning completed with confidence: {result.confidence:.2f}")
        print(f"📝 Explanation preview: {result.explanation[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing reasoning engine: {e}")
        return False

def test_terraform_agent():
    """Test Terraform agent with simple model"""
    print("\n🏗️ Testing Terraform Agent...")
    
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Terraform agent: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Simple Integration Tests\n")
    
    tests = [
        ("Simple Model", test_simple_model),
        ("Reasoning Engine", test_reasoning_engine),
        ("Terraform Agent", test_terraform_agent)
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
