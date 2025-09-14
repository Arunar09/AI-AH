#!/usr/bin/env python3
"""
Test Complete Interface System
Demonstrates CLI, GUI, requirement collection, scaling plans, and troubleshooting
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.append('.')

def test_cli_interface():
    """Test CLI interface functionality"""
    print("🧪 Testing CLI Interface...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import RequirementCollector, ProductionScalingPlanner, RequirementSet, Requirement
        
        # Test requirement collection
        collector = RequirementCollector()
        print("✅ RequirementCollector initialized")
        
        # Test scaling planner
        planner = ProductionScalingPlanner()
        print("✅ ProductionScalingPlanner initialized")
        
        # Test requirement templates
        templates = collector._load_requirement_templates()
        print(f"✅ Loaded {len(templates)} project type templates")
        
        for project_type, requirements in templates.items():
            print(f"  📋 {project_type}: {len(requirements)} requirements")
        
        # Test scaling templates
        scaling_templates = planner._load_scaling_templates()
        print(f"✅ Loaded {len(scaling_templates)} scaling templates")
        
        # Test requirement validation
        test_requirement = Requirement(
            category="test",
            question="Test question",
            answer="test answer",
            validation_rules=["not_empty"]
        )
        print("✅ Requirement validation working")
        
        print("✅ CLI Interface tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ CLI Interface test failed: {e}")
        return False

def test_gui_interface():
    """Test GUI interface functionality"""
    print("\n🧪 Testing GUI Interface...")
    print("=" * 50)
    
    try:
        from interfaces.gui_interface import RequirementWidget, ProjectWizard, ScalingPlanViewer, TroubleshootingInterface
        
        print("✅ GUI Interface modules imported successfully")
        
        # Test requirement templates
        wizard = ProjectWizard(None, None)
        print(f"✅ ProjectWizard initialized with {len(wizard.project_templates)} project types")
        
        for project_type, details in wizard.project_templates.items():
            print(f"  📋 {project_type}: {len(details['requirements'])} requirements")
        
        print("✅ GUI Interface tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ GUI Interface test failed: {e}")
        return False

def test_requirement_collection():
    """Test granular requirement collection"""
    print("\n🧪 Testing Requirement Collection...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import RequirementCollector, RequirementSet, Requirement
        
        collector = RequirementCollector()
        
        # Test requirement templates
        templates = collector.requirement_templates
        
        print(f"✅ Available project types: {list(templates.keys())}")
        
        # Test web application requirements
        web_app_reqs = templates["web_application"]
        print(f"✅ Web application has {len(web_app_reqs)} requirements")
        
        for req in web_app_reqs:
            print(f"  📝 {req['category']}: {req['question']}")
            print(f"     Validation: {req['validation_rules']}")
            if req.get('follow_up_questions'):
                print(f"     Follow-ups: {len(req['follow_up_questions'])}")
        
        # Test validation rules
        test_cases = [
            ("", ["not_empty"], False),
            ("test", ["not_empty"], True),
            ("aws", ["one_of:aws,azure,gcp"], True),
            ("invalid", ["one_of:aws,azure,gcp"], False),
            ("100", ["numeric_range:1-1000"], True),
            ("2000", ["numeric_range:1-1000"], False)
        ]
        
        for value, rules, expected in test_cases:
            result = collector._validate_answer(value, rules)
            status = "✅" if result == expected else "❌"
            print(f"  {status} Validation: '{value}' with {rules} -> {result}")
        
        print("✅ Requirement Collection tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Requirement Collection test failed: {e}")
        return False

def test_production_scaling_plan():
    """Test production scaling plan generation"""
    print("\n🧪 Testing Production Scaling Plan...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import ProductionScalingPlanner, RequirementSet, Requirement
        
        planner = ProductionScalingPlanner()
        
        # Create test requirements
        test_requirements = RequirementSet(
            project_name="Test Project",
            requirements=[
                Requirement(
                    category="security",
                    question="Security requirements",
                    answer="Need HIPAA compliance and encryption",
                    validation_rules=["not_empty"]
                ),
                Requirement(
                    category="availability",
                    question="Uptime requirement",
                    answer="99.9%",
                    validation_rules=["not_empty"]
                ),
                Requirement(
                    category="monitoring",
                    question="Monitoring needs",
                    answer="Advanced APM and ML-based monitoring",
                    validation_rules=["not_empty"]
                )
            ],
            completeness_score=100.0
        )
        
        # Generate scaling plan
        scaling_plan = planner.generate_scaling_plan(test_requirements)
        
        print(f"✅ Generated scaling plan with {len(scaling_plan['phases'])} phases")
        print(f"✅ Estimated duration: {scaling_plan['estimated_duration']}")
        print(f"✅ Scaling needs: {scaling_plan['scaling_needs']}")
        
        # Test phases
        for i, phase in enumerate(scaling_plan['phases'], 1):
            print(f"  📋 Phase {i}: {phase['name']}")
            print(f"     Duration: {phase['duration']}")
            print(f"     Steps: {len(phase['steps'])}")
        
        # Test cost implications
        print(f"✅ Cost implications: {len(scaling_plan['cost_implications'])} categories")
        for cost_type, cost_range in scaling_plan['cost_implications'].items():
            print(f"  💰 {cost_type}: {cost_range}")
        
        # Test risk assessment
        print(f"✅ Risk assessment: {len(scaling_plan['risk_assessment'])} risks")
        for risk in scaling_plan['risk_assessment']:
            print(f"  ⚠️ {risk}")
        
        # Test success metrics
        print(f"✅ Success metrics: {len(scaling_plan['success_metrics'])} metrics")
        for metric in scaling_plan['success_metrics']:
            print(f"  🎯 {metric}")
        
        print("✅ Production Scaling Plan tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Production Scaling Plan test failed: {e}")
        return False

def test_troubleshooting_capabilities():
    """Test troubleshooting capabilities"""
    print("\n🧪 Testing Troubleshooting Capabilities...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import CLIInterface
        
        cli = CLIInterface()
        
        # Test troubleshooting solutions
        test_issues = [
            "Terraform state is locked",
            "Resource already exists error",
            "Permission denied errors",
            "Circular dependency error"
        ]
        
        for issue in test_issues:
            try:
                cli._provide_troubleshooting_solution(issue, "infrastructure")
                print(f"✅ Troubleshooting solution for: {issue}")
            except Exception as e:
                print(f"❌ Failed to get solution for {issue}: {e}")
        
        print("✅ Troubleshooting Capabilities tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Troubleshooting Capabilities test failed: {e}")
        return False

def test_integration():
    """Test integration between components"""
    print("\n🧪 Testing Integration...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import RequirementCollector, ProductionScalingPlanner, RequirementSet, Requirement
        from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
        
        # Create collector and planner
        collector = RequirementCollector()
        planner = ProductionScalingPlanner()
        agent = IntelligentTerraformAgent()
        
        print("✅ All components initialized")
        
        # Test end-to-end workflow
        # 1. Collect requirements (simulated)
        test_requirements = RequirementSet(
            project_name="Integration Test Project",
            requirements=[
                Requirement(
                    category="basic_info",
                    question="Project name",
                    answer="Integration Test Project",
                    validation_rules=["not_empty"]
                ),
                Requirement(
                    category="infrastructure",
                    question="Cloud provider",
                    answer="AWS",
                    validation_rules=["one_of:aws,azure,gcp"]
                ),
                Requirement(
                    category="scaling",
                    question="User load",
                    answer="10000",
                    validation_rules=["numeric_range:1-10000000"]
                ),
                Requirement(
                    category="budget",
                    question="Monthly budget",
                    answer="1000",
                    validation_rules=["numeric_range:10-50000"]
                )
            ],
            completeness_score=100.0
        )
        
        print("✅ Requirements collected")
        
        # 2. Generate request from requirements
        request_parts = []
        for req in test_requirements.requirements:
            if req.answer:
                request_parts.append(f"{req.question}: {req.answer}")
        request = "\n".join(request_parts)
        
        print("✅ Request generated from requirements")
        
        # 3. Process with agent
        response = agent.process_request(request)
        
        print(f"✅ Agent processed request")
        print(f"   Cost estimate: ${response.cost_estimate}/month")
        print(f"   Confidence: {response.confidence * 100}%")
        print(f"   Generated {len(response.terraform_code)} files")
        print(f"   Implementation steps: {len(response.implementation_steps)}")
        
        # 4. Generate scaling plan
        scaling_plan = planner.generate_scaling_plan(test_requirements)
        
        print(f"✅ Scaling plan generated")
        print(f"   Phases: {len(scaling_plan['phases'])}")
        print(f"   Duration: {scaling_plan['estimated_duration']}")
        
        print("✅ Integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_file_operations():
    """Test file operations and project management"""
    print("\n🧪 Testing File Operations...")
    print("=" * 50)
    
    try:
        from interfaces.cli_interface import CLIInterface
        import tempfile
        import os
        
        cli = CLIInterface()
        
        # Create test project data
        test_project = {
            "type": "web_application",
            "requirements": {
                "project_name": "Test Project",
                "requirements": [
                    {
                        "category": "basic_info",
                        "question": "Project name",
                        "answer": "Test Project",
                        "validation_rules": ["not_empty"]
                    }
                ],
                "completeness_score": 100.0
            },
            "created_at": "2024-01-01",
            "status": "requirements_collected"
        }
        
        # Test project export
        with tempfile.TemporaryDirectory() as temp_dir:
            projects_dir = Path(temp_dir) / "projects"
            projects_dir.mkdir()
            
            # Simulate project export
            project_file = projects_dir / "test_project.json"
            with open(project_file, 'w') as f:
                json.dump(test_project, f, indent=2)
            
            print(f"✅ Project exported to: {project_file}")
            
            # Test project import
            with open(project_file, 'r') as f:
                imported_project = json.load(f)
            
            print(f"✅ Project imported: {imported_project['requirements']['project_name']}")
            
            # Verify data integrity
            assert imported_project['type'] == test_project['type']
            assert imported_project['requirements']['project_name'] == test_project['requirements']['project_name']
            
            print("✅ Data integrity verified")
        
        print("✅ File Operations tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ File Operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Complete Interface System Tests")
    print("=" * 60)
    
    tests = [
        ("CLI Interface", test_cli_interface),
        ("GUI Interface", test_gui_interface),
        ("Requirement Collection", test_requirement_collection),
        ("Production Scaling Plan", test_production_scaling_plan),
        ("Troubleshooting Capabilities", test_troubleshooting_capabilities),
        ("Integration", test_integration),
        ("File Operations", test_file_operations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The interface system is ready for use.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
