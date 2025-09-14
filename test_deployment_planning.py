#!/usr/bin/env python3
"""
Test Deployment Planning Capabilities
"""

import sys
sys.path.append('.')
from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent

def test_deployment_planning():
    """Test comprehensive deployment planning capabilities"""
    
    print("🏗️ Testing Comprehensive Deployment Planning...")
    print("=" * 70)
    
    agent = IntelligentTerraformAgent()
    
    # Test 1: Simple web application deployment
    print("\n📝 Test 1: Simple Web Application Deployment")
    print("-" * 50)
    
    request1 = """
    I need a simple web application on AWS with:
    - EC2 instance for web server
    - RDS MySQL database
    - Application Load Balancer
    - Auto-scaling capability
    - Budget: $300/month
    - Expected users: 5,000
    """
    
    response1 = agent.process_request(request1)
    
    print(f"✅ Generated {len(response1.terraform_code)} Terraform files")
    print(f"✅ Cost estimate: ${response1.cost_estimate}/month")
    print(f"✅ Confidence: {response1.confidence * 100}%")
    
    print("\n📋 Implementation Steps:")
    for i, step in enumerate(response1.implementation_steps, 1):
        print(f"  {i}. {step}")
    
    # Test 2: Complex microservices deployment
    print("\n📝 Test 2: Complex Microservices Deployment")
    print("-" * 50)
    
    request2 = """
    I need a production-ready microservices architecture on AWS with:
    - EKS cluster with 3 worker nodes
    - RDS PostgreSQL with read replicas
    - ElastiCache Redis cluster
    - API Gateway with rate limiting
    - Application Load Balancer
    - Auto-scaling groups
    - CloudWatch monitoring and alerting
    - VPC with public/private subnets
    - Security groups and IAM roles
    - Budget: $2000/month
    - Expected users: 100,000
    - High availability across 3 AZs
    - Security hardening required
    - CI/CD pipeline ready
    """
    
    response2 = agent.process_request(request2)
    
    print(f"✅ Generated {len(response2.terraform_code)} Terraform files")
    print(f"✅ Cost estimate: ${response2.cost_estimate}/month")
    print(f"✅ Confidence: {response2.confidence * 100}%")
    
    print("\n📋 Implementation Steps:")
    for i, step in enumerate(response2.implementation_steps, 1):
        print(f"  {i}. {step}")
    
    # Test 3: Multi-cloud deployment
    print("\n📝 Test 3: Multi-Cloud Deployment Planning")
    print("-" * 50)
    
    request3 = """
    I need a hybrid cloud setup with:
    - Primary: AWS (EKS, RDS, S3)
    - Secondary: Azure (AKS, CosmosDB, Blob Storage)
    - Disaster recovery: GCP (GKE, Cloud SQL, Cloud Storage)
    - Cross-cloud networking
    - Budget: $5000/month
    - Expected users: 500,000
    - 99.9% uptime requirement
    """
    
    response3 = agent.process_request(request3)
    
    print(f"✅ Generated {len(response3.terraform_code)} Terraform files")
    print(f"✅ Cost estimate: ${response3.cost_estimate}/month")
    print(f"✅ Confidence: {response3.confidence * 100}%")
    
    print("\n📋 Implementation Steps:")
    for i, step in enumerate(response3.implementation_steps, 1):
        print(f"  {i}. {step}")
    
    # Test 4: Serverless deployment
    print("\n📝 Test 4: Serverless Deployment Planning")
    print("-" * 50)
    
    request4 = """
    I need a serverless architecture on AWS with:
    - Lambda functions for API
    - API Gateway for routing
    - DynamoDB for data storage
    - S3 for static assets
    - CloudFront for CDN
    - Cognito for authentication
    - Budget: $200/month
    - Expected users: 50,000
    - Auto-scaling required
    """
    
    response4 = agent.process_request(request4)
    
    print(f"✅ Generated {len(response4.terraform_code)} Terraform files")
    print(f"✅ Cost estimate: ${response4.cost_estimate}/month")
    print(f"✅ Confidence: {response4.confidence * 100}%")
    
    print("\n📋 Implementation Steps:")
    for i, step in enumerate(response4.implementation_steps, 1):
        print(f"  {i}. {step}")
    
    print("\n🎉 All Deployment Planning Tests Completed!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_deployment_planning()
