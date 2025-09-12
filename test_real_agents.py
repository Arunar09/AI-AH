#!/usr/bin/env python3
"""
Test real AI-AH agents with actual commands
No fake results - only real agent responses
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_terraform_agent():
    """Test the actual Terraform agent"""
    print("🏗️ Testing Real Terraform Agent...")
    
    try:
        from ai_ah_platform.agents.terraform_agent import TerraformAgent
        from ai_ah_platform.core.base_platform import PlatformConfig
        
        # Create proper configuration
        config = PlatformConfig(
            name="terraform_agent_test",
            version="1.0.0",
            environment="test",
            debug=True
        )
        
        agent = TerraformAgent(config)
        
        # Test simple request
        print("  📋 Testing simple request: 'create a VPC'")
        request = "create a VPC with public and private subnets"
        
        # This will test the actual agent
        response = await agent.process_request(request)
        
        print(f"  📤 Agent Response:")
        print(f"    {response}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing Terraform agent: {str(e)}")
        return False

async def test_ansible_agent():
    """Test the actual Ansible agent"""
    print("\n⚙️ Testing Real Ansible Agent...")
    
    try:
        from ai_ah_platform.agents.ansible_agent import AnsibleAgent
        from ai_ah_platform.core.base_platform import PlatformConfig
        
        # Create proper configuration
        config = PlatformConfig(
            name="ansible_agent_test",
            version="1.0.0",
            environment="test",
            debug=True
        )
        
        agent = AnsibleAgent(config)
        
        # Test simple request
        print("  📋 Testing simple request: 'configure nginx'")
        request = "configure nginx web server with SSL"
        
        # This will test the actual agent
        response = await agent.process_request(request)
        
        print(f"  📤 Agent Response:")
        print(f"    {response}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing Ansible agent: {str(e)}")
        return False

async def test_kubernetes_agent():
    """Test the actual Kubernetes agent"""
    print("\n☸️ Testing Real Kubernetes Agent...")
    
    try:
        from ai_ah_platform.agents.kubernetes_agent import KubernetesAgent
        from ai_ah_platform.core.base_platform import PlatformConfig
        
        # Create proper configuration
        config = PlatformConfig(
            name="kubernetes_agent_test",
            version="1.0.0",
            environment="test",
            debug=True
        )
        
        agent = KubernetesAgent(config)
        
        # Test simple request
        print("  📋 Testing simple request: 'deploy nginx'")
        request = "deploy nginx pod with service"
        
        # This will test the actual agent
        response = await agent.process_request(request)
        
        print(f"  📤 Agent Response:")
        print(f"    {response}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing Kubernetes agent: {str(e)}")
        return False

async def test_reasoning_engine():
    """Test the actual reasoning engine"""
    print("\n🧠 Testing Real Reasoning Engine...")
    
    try:
        from ai_ah_platform.core.intelligence.reasoning_engine import IntelligentReasoningEngine
        
        engine = IntelligentReasoningEngine()
        
        # Test simple request
        print("  📋 Testing reasoning with: 'list capabilities'")
        request = "list me your capabilities"
        
        # This will test the actual reasoning engine
        result = engine.reason_through_request(request)
        
        print(f"  📤 Reasoning Result:")
        print(f"    Confidence: {result.confidence}")
        print(f"    Recommendation: {result.final_recommendation}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing reasoning engine: {str(e)}")
        return False

async def main():
    """Test all real agents"""
    print("🚀 Testing Real AI-AH Agents")
    print("=" * 50)
    print("⚠️  This will test ACTUAL agents - no fake results")
    print("=" * 50)
    
    results = {
        "terraform": False,
        "ansible": False,
        "kubernetes": False,
        "reasoning_engine": False
    }
    
    # Test reasoning engine first
    results["reasoning_engine"] = await test_reasoning_engine()
    
    # Test individual agents
    results["terraform"] = await test_terraform_agent()
    results["ansible"] = await test_ansible_agent()
    results["kubernetes"] = await test_kubernetes_agent()
    
    # Summary
    print("\n📊 Real Test Results:")
    print("=" * 30)
    
    for agent, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {agent.title()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n📈 Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {total_tests - passed_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 All agents are working!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} agents need attention")

if __name__ == "__main__":
    asyncio.run(main())
