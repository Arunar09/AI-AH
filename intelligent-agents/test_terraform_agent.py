#!/usr/bin/env python3
"""
Test the Intelligent Terraform Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent

def test_terraform_agent():
    """Test the intelligent Terraform agent with a real scenario"""
    print("🏗️ Testing Intelligent Terraform Agent...")
    
    try:
        # Initialize the Terraform agent
        agent = IntelligentTerraformAgent()
        print("✅ Terraform agent initialized successfully")
        
        # Test with a real infrastructure request
        request = "I need a web application that can handle 5000 users with high availability and costs under $300/month. I prefer AWS."
        session_id = "test_session_001"
        
        print(f"\n📝 Testing with request: {request}")
        
        # Process the request
        response = agent.process_request(request, session_id)
        
        print(f"\n🎯 Agent Response:")
        print(f"Confidence: {response.confidence:.1%}")
        print(f"Cost Estimate: ${response.cost_estimate}/month")
        print(f"Reasoning Steps: {len(response.reasoning_steps)}")
        
        print(f"\n📋 Reasoning Steps:")
        for i, step in enumerate(response.reasoning_steps, 1):
            print(f"{i}. {step}")
        
        print(f"\n💡 Generated Terraform Files:")
        for filename, content in response.terraform_code.items():
            print(f"- {filename}: {len(content)} characters")
        
        print(f"\n📖 Explanation:")
        print(response.content)
        
        print(f"\n🛠️ Implementation Steps:")
        for step in response.implementation_steps:
            print(f"  {step}")
        
        print(f"\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_terraform_code_generation():
    """Test Terraform code generation specifically"""
    print("\n🔧 Testing Terraform Code Generation...")
    
    try:
        agent = IntelligentTerraformAgent()
        
        # Test different scenarios
        test_cases = [
            "Create a basic web app on AWS",
            "Build a scalable web application on Azure",
            "Deploy a serverless API on GCP"
        ]
        
        for i, request in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: {request}")
            response = agent.process_request(request)
            
            # Check if Terraform code was generated
            if response.terraform_code:
                print(f"✅ Generated {len(response.terraform_code)} Terraform files")
                for filename in response.terraform_code.keys():
                    print(f"   - {filename}")
            else:
                print("❌ No Terraform code generated")
                return False
        
        print(f"\n✅ All Terraform code generation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Terraform code generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Terraform Agent Tests...")
    
    # Test 1: Basic agent functionality
    success1 = test_terraform_agent()
    
    # Test 2: Code generation
    success2 = test_terraform_code_generation()
    
    if success1 and success2:
        print("\n🎉 All Terraform Agent tests passed!")
        print("🏗️ Intelligent Terraform Agent is working correctly!")
    else:
        print("\n💥 Some Terraform Agent tests failed!")
        sys.exit(1)

