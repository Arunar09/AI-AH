#!/usr/bin/env python3
"""
Agent Test Framework
Tests AI-AH agents against real infrastructure deployments
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class AgentTestFramework:
    """Framework for testing agents"""
    
    def __init__(self):
        self.lab_dir = Path("lab")
        self.test_results = []
    
    def test_terraform_agent(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Test Terraform agent with given requirements"""
        print(f"🧪 Testing Terraform agent with requirements: {requirements}")
        
        # Import and test the agent
        sys.path.append('intelligent-agents')
        from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
        
        agent = IntelligentTerraformAgent()
        
        # Generate request
        request_parts = []
        for key, value in requirements.items():
            request_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        request_text = "\n".join(request_parts)
        
        # Process with agent
        start_time = time.time()
        response = agent.process_request(request_text)
        end_time = time.time()
        
        result = {
            "test_name": "terraform_agent",
            "requirements": requirements,
            "response_time": end_time - start_time,
            "confidence": response.confidence,
            "cost_estimate": response.cost_estimate,
            "files_generated": list(response.terraform_code.keys()),
            "success": response.confidence > 0.7
        }
        
        # Save generated code for validation
        if response.terraform_code:
            test_dir = self.lab_dir / "test_results" / f"test_{int(time.time())}"
            test_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in response.terraform_code.items():
                (test_dir / filename).write_text(content)
            
            result["test_directory"] = str(test_dir)
        
        return result
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print("🚀 Running comprehensive agent test suite...")
        
        test_cases = [
            {
                "name": "Basic Web App",
                "requirements": {
                    "project_name": "Basic Web App",
                    "cloud_provider": "AWS",
                    "user_load": "100",
                    "budget": "50",
                    "security": "basic"
                }
            },
            {
                "name": "High Traffic App",
                "requirements": {
                    "project_name": "High Traffic App",
                    "cloud_provider": "AWS",
                    "user_load": "10000",
                    "budget": "500",
                    "security": "high",
                    "uptime": "99.9%"
                }
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            print(f"\n🧪 Testing: {test_case['name']}")
            
            # Test agent
            agent_result = self.test_terraform_agent(test_case["requirements"])
            
            results.append({
                "test_case": test_case,
                "result": agent_result
            })
        
        # Save results
        results_file = self.lab_dir / "test_results" / "comprehensive_test_results.json"
        results_file.parent.mkdir(parents=True, exist_ok=True)
        results_file.write_text(json.dumps(results, indent=2))
        
        # Print summary
        print("\n📊 Test Results Summary:")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for result in results:
            test_name = result["test_case"]["name"]
            success = result["result"]["success"]
            confidence = result["result"]["confidence"]
            response_time = result["result"]["response_time"]
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{test_name}: {status} (Confidence: {confidence:.2f}, Time: {response_time:.2f}s)")
            
            if success:
                passed += 1
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        return results

if __name__ == "__main__":
    framework = AgentTestFramework()
    framework.run_comprehensive_test()
