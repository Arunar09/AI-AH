#!/usr/bin/env python3
"""
Test Lab Setup
Demonstrates the local lab functionality
"""

import os
import sys
import json
from pathlib import Path

def test_lab_setup():
    """Test the lab setup functionality"""
    print("🧪 Testing Lab Setup...")
    
    # Check if lab directory exists
    lab_dir = Path("lab")
    if not lab_dir.exists():
        print("❌ Lab directory not found. Run setup first.")
        return False
    
    # Check lab structure
    required_dirs = [
        "terraform",
        "docker",
        "monitoring",
        "test_results"
    ]
    
    for dir_name in required_dirs:
        dir_path = lab_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name} directory exists")
        else:
            print(f"  ❌ {dir_name} directory missing")
            return False
    
    # Check Terraform modules
    terraform_dir = lab_dir / "terraform"
    modules_dir = terraform_dir / "modules"
    
    if modules_dir.exists():
        modules = list(modules_dir.iterdir())
        print(f"  ✅ Found {len(modules)} Terraform modules")
        for module in modules:
            if module.is_dir():
                print(f"    - {module.name}")
    else:
        print("  ❌ Terraform modules directory missing")
        return False
    
    # Check environments
    environments_dir = terraform_dir / "environments"
    if environments_dir.exists():
        environments = list(environments_dir.iterdir())
        print(f"  ✅ Found {len(environments)} environments")
        for env in environments:
            if env.is_dir():
                print(f"    - {env.name}")
    else:
        print("  ❌ Environments directory missing")
        return False
    
    # Check Docker Compose files
    docker_dir = lab_dir / "docker" / "compose"
    if docker_dir.exists():
        compose_files = list(docker_dir.glob("*.yml"))
        print(f"  ✅ Found {len(compose_files)} Docker Compose files")
        for file in compose_files:
            print(f"    - {file.name}")
    else:
        print("  ❌ Docker Compose files missing")
        return False
    
    # Check test scripts
    test_scripts = [
        "test_agents.py",
        "test_terraform.sh",
        "test_docker.sh",
        "run_lab.py"
    ]
    
    for script in test_scripts:
        script_path = lab_dir / script
        if script_path.exists():
            print(f"  ✅ {script} exists")
        else:
            print(f"  ❌ {script} missing")
            return False
    
    print("✅ Lab setup validation passed!")
    return True

def test_agent_integration():
    """Test agent integration with lab"""
    print("\n🤖 Testing Agent Integration...")
    
    try:
        # Test importing the agent
        sys.path.append('intelligent-agents')
        from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
        
        print("  ✅ Terraform agent imported successfully")
        
        # Test agent initialization
        agent = IntelligentTerraformAgent()
        print("  ✅ Terraform agent initialized successfully")
        
        # Test with simple requirements
        test_requirements = {
            "project_name": "Lab Test",
            "cloud_provider": "AWS",
            "user_load": "100",
            "budget": "50"
        }
        
        # Generate request
        request_parts = []
        for key, value in test_requirements.items():
            request_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        request_text = "\n".join(request_parts)
        
        print(f"  🧪 Testing with requirements: {test_requirements}")
        
        # Process request
        response = agent.process_request(request_text)
        
        print(f"  ✅ Agent response generated")
        print(f"    - Confidence: {response.confidence:.2f}")
        print(f"    - Cost estimate: ${response.cost_estimate:.2f}")
        print(f"    - Files generated: {len(response.terraform_code)}")
        
        # Check if files are valid
        if response.terraform_code:
            print("  📁 Generated files:")
            for filename in response.terraform_code.keys():
                print(f"    - {filename}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Agent integration test failed: {e}")
        return False

def demonstrate_lab_usage():
    """Demonstrate lab usage"""
    print("\n📋 Lab Usage Demonstration:")
    print("=" * 50)
    
    print("\n1. 🏗️ Setup Lab Environment:")
    print("   python lab/setup_local_lab.py")
    
    print("\n2. 🧪 Test Agents (Dry Run):")
    print("   python lab/run_lab.py test --environment basic --dry-run")
    
    print("\n3. 🚀 Deploy to AWS (Real Resources):")
    print("   python lab/run_lab.py deploy --environment basic")
    
    print("\n4. 🧹 Cleanup Resources:")
    print("   python lab/run_lab.py cleanup --environment basic")
    
    print("\n5. 🤖 Run Agent Tests:")
    print("   python lab/test_agents.py")
    
    print("\n6. 🐳 Test Docker Services:")
    print("   python lab/test_docker.sh")
    
    print("\n7. 📊 View Test Results:")
    print("   ls lab/test_results/")

def main():
    """Main test function"""
    print("🚀 AI-AH Lab Setup Test")
    print("=" * 40)
    
    # Test lab setup
    lab_ok = test_lab_setup()
    
    # Test agent integration
    agent_ok = test_agent_integration()
    
    # Show usage
    demonstrate_lab_usage()
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Lab Setup: {'✅ PASS' if lab_ok else '❌ FAIL'}")
    print(f"Agent Integration: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    
    if lab_ok and agent_ok:
        print("\n🎉 All tests passed! Lab is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: python lab/setup_local_lab.py")
        print("2. Test: python lab/run_lab.py test --dry-run")
        print("3. Deploy: python lab/run_lab.py deploy --environment basic")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
    
    return lab_ok and agent_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

