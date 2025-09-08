#!/usr/bin/env python3
"""
Test Enhanced Intelligent Infrastructure Analysis
===============================================

Test the new intelligent infrastructure analysis capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.base_agent import BaseAgent
from core.terraform_engineer_plugin import TerraformEngineerPlugin
from core.intelligent_analyzer import IntelligentQueryAnalyzer

def test_intelligent_analysis():
    print("🧪 Testing Enhanced Intelligent Infrastructure Analysis")
    print("=" * 60)
    
    # Test the intelligent analyzer directly
    print("\n🔍 Testing Intelligent Query Analyzer...")
    analyzer = IntelligentQueryAnalyzer()
    
    test_queries = [
        "Create a serverless architecture with Lambda and DynamoDB",
        "Build a microservices infrastructure on Azure",
        "Design a 3-tier web application",
        "Generate container-based infrastructure with Kubernetes"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        plan = analyzer.analyze_infrastructure_request(query)
        
        print(f"   Pattern: {plan.pattern.value}")
        print(f"   Environment: {plan.environment.value}")
        print(f"   Requirements: {len(plan.requirements)}")
        print(f"   Missing Info: {len(plan.missing_info)}")
        print(f"   Estimated Cost: {plan.estimated_cost}")
        
        if plan.missing_info:
            print(f"   Questions to ask:")
            for i, question in enumerate(plan.missing_info[:2], 1):
                print(f"     Q{i}: {question.question}")
    
    print("\n✅ Intelligent Analysis Test Completed!")
    
    # Test the enhanced base agent
    print("\n🔍 Testing Enhanced Base Agent...")
    agent = BaseAgent()
    
    # Register Terraform Engineer plugin
    terraform_config = {
        'terraform_dir': './web_terraform_workspace',
        'name': 'Terraform Engineer',
        'version': '2.0.0',
        'description': 'Real infrastructure engineering capabilities'
    }
    terraform_plugin = TerraformEngineerPlugin(terraform_config)
    agent.plugin_manager.register_plugin(terraform_plugin)
    
    # Test infrastructure creation request
    test_query = "Create a serverless architecture with Lambda and DynamoDB"
    print(f"\n📝 Testing enhanced agent with: '{test_query}'")
    
    # Create a mock query analysis
    from core.base_agent import QueryAnalysis
    query_analysis = QueryAnalysis(
        keywords=['create', 'serverless', 'architecture', 'lambda', 'dynamodb'],
        intent='command_request',
        complexity='medium',
        context={'domain': 'infrastructure'},
        confidence=0.8
    )
    
    # Test the new infrastructure creation detection
    is_infrastructure = agent._is_infrastructure_creation_request(test_query, query_analysis)
    print(f"   Infrastructure creation detected: {is_infrastructure}")
    
    if is_infrastructure:
        print("   ✅ Enhanced analysis will be triggered!")
    else:
        print("   ❌ Enhanced analysis not triggered")
    
    print("\n✅ Enhanced Agent Test Completed!")
    print("\n🚀 Ready to test with interactive script!")

if __name__ == "__main__":
    test_intelligent_analysis()



