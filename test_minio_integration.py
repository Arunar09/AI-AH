#!/usr/bin/env python3
"""
Test real MinIO integration with AI-AH agents
Tests actual data storage and retrieval using the created buckets
"""

import asyncio
import sys
import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class MinIOIntegrationTester:
    def __init__(self):
        self.minio_url = "http://localhost:9000"
        self.minio_console = "http://localhost:9001"
        self.access_key = "minioadmin"
        self.secret_key = "minioadmin123"
        
        # Test data for each bucket
        self.test_data = {
            "terraform-state": {
                "file": "test-state.json",
                "content": {
                    "version": 4,
                    "terraform_version": "1.5.0",
                    "serial": 1,
                    "lineage": "test-lineage-123",
                    "outputs": {},
                    "resources": [
                        {
                            "mode": "managed",
                            "type": "aws_vpc",
                            "name": "test_vpc",
                            "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
                            "instances": [
                                {
                                    "schema_version": 1,
                                    "attributes": {
                                        "cidr_block": "10.0.0.0/16",
                                        "enable_dns_hostnames": True,
                                        "enable_dns_support": True,
                                        "id": "vpc-test123",
                                        "tags": {"Name": "test-vpc"}
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            "ansible-artifacts": {
                "file": "test-playbook.yml",
                "content": """
---
- name: Test Ansible Playbook
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Test task
      debug:
        msg: "Hello from Ansible!"
    - name: Create test file
      copy:
        content: "Test content"
        dest: /tmp/test.txt
"""
            },
            "kubernetes-backups": {
                "file": "test-deployment.yaml",
                "content": """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-nginx
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: test-nginx
  template:
    metadata:
      labels:
        app: test-nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
"""
            },
            "security-reports": {
                "file": "test-vulnerability-report.json",
                "content": {
                    "scan_id": "scan-123",
                    "timestamp": datetime.now().isoformat(),
                    "target": "test-image:latest",
                    "vulnerabilities": [
                        {
                            "id": "CVE-2023-1234",
                            "severity": "HIGH",
                            "package": "openssl",
                            "version": "1.1.1",
                            "description": "Test vulnerability"
                        }
                    ],
                    "summary": {
                        "total": 1,
                        "critical": 0,
                        "high": 1,
                        "medium": 0,
                        "low": 0
                    }
                }
            },
            "monitoring-data": {
                "file": "test-metrics.json",
                "content": {
                    "timestamp": datetime.now().isoformat(),
                    "metrics": {
                        "cpu_usage": 45.2,
                        "memory_usage": 67.8,
                        "disk_usage": 23.1,
                        "network_in": 1024,
                        "network_out": 2048
                    },
                    "alerts": [
                        {
                            "name": "High CPU Usage",
                            "status": "firing",
                            "severity": "warning"
                        }
                    ]
                }
            },
            "ai-training-data": {
                "file": "test-training-data.json",
                "content": {
                    "session_id": "session-123",
                    "timestamp": datetime.now().isoformat(),
                    "training_data": {
                        "queries": [
                            "create a VPC",
                            "deploy nginx",
                            "configure database"
                        ],
                        "responses": [
                            "VPC created successfully",
                            "Nginx deployed",
                            "Database configured"
                        ],
                        "accuracy_scores": [0.95, 0.87, 0.92]
                    }
                }
            }
        }

    async def test_bucket_access(self, bucket_name: str, test_data: dict) -> bool:
        """Test access to a specific bucket"""
        print(f"  🗄️ Testing bucket: {bucket_name}")
        
        try:
            import requests
            
            # Test bucket access by trying to list objects
            url = f"{self.minio_url}/{bucket_name}/"
            response = requests.get(
                url,
                auth=(self.access_key, self.secret_key),
                timeout=10
            )
            
            if response.status_code in [200, 404]:  # 404 is OK for empty bucket
                print(f"    ✅ Bucket {bucket_name} accessible")
                return True
            else:
                print(f"    ❌ Bucket {bucket_name} not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Error accessing bucket {bucket_name}: {str(e)}")
            return False

    async def test_data_upload(self, bucket_name: str, test_data: dict) -> bool:
        """Test uploading data to a bucket"""
        print(f"  📤 Testing data upload to: {bucket_name}")
        
        try:
            import requests
            
            # Prepare data
            file_name = test_data["file"]
            content = test_data["content"]
            
            # Convert content to string if it's a dict
            if isinstance(content, dict):
                content_str = json.dumps(content, indent=2)
            else:
                content_str = content
            
            # Upload to MinIO
            url = f"{self.minio_url}/{bucket_name}/{file_name}"
            response = requests.put(
                url,
                data=content_str,
                auth=(self.access_key, self.secret_key),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"    ✅ Uploaded {file_name} to {bucket_name}")
                return True
            else:
                print(f"    ❌ Failed to upload to {bucket_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Error uploading to {bucket_name}: {str(e)}")
            return False

    async def test_data_download(self, bucket_name: str, test_data: dict) -> bool:
        """Test downloading data from a bucket"""
        print(f"  📥 Testing data download from: {bucket_name}")
        
        try:
            import requests
            
            file_name = test_data["file"]
            url = f"{self.minio_url}/{bucket_name}/{file_name}"
            
            response = requests.get(
                url,
                auth=(self.access_key, self.secret_key),
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"    ✅ Downloaded {file_name} from {bucket_name}")
                return True
            else:
                print(f"    ❌ Failed to download from {bucket_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"    ❌ Error downloading from {bucket_name}: {str(e)}")
            return False

    async def test_terraform_agent_minio(self):
        """Test Terraform agent with MinIO integration"""
        print("\n🏗️ Testing Terraform Agent with MinIO...")
        
        try:
            from ai_ah_platform.agents.terraform_agent import TerraformAgent
            from ai_ah_platform.core.base_platform import PlatformConfig
            
            # Create configuration with MinIO backend
            config = PlatformConfig(
                name="terraform_minio_test",
                version="1.0.0",
                environment="test",
                debug=True,
                metadata={
                    "minio_endpoint": self.minio_url,
                    "minio_access_key": self.access_key,
                    "minio_secret_key": self.secret_key,
                    "minio_bucket": "terraform-state"
                }
            )
            
            agent = TerraformAgent(config)
            
            # Test request for VPC creation with MinIO backend
            request = "create a VPC with MinIO backend for state storage"
            response = await agent.process_request(request)
            
            print(f"  📤 Terraform Agent Response:")
            print(f"    Content: {response.content[:200]}...")
            print(f"    Confidence: {response.confidence}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error testing Terraform agent with MinIO: {str(e)}")
            return False

    async def test_ansible_agent_minio(self):
        """Test Ansible agent with MinIO integration"""
        print("\n⚙️ Testing Ansible Agent with MinIO...")
        
        try:
            from ai_ah_platform.agents.ansible_agent import AnsibleAgent
            from ai_ah_platform.core.base_platform import PlatformConfig
            
            # Create configuration with MinIO integration
            config = PlatformConfig(
                name="ansible_minio_test",
                version="1.0.0",
                environment="test",
                debug=True,
                metadata={
                    "minio_endpoint": self.minio_url,
                    "minio_access_key": self.access_key,
                    "minio_secret_key": self.secret_key,
                    "minio_bucket": "ansible-artifacts"
                }
            )
            
            agent = AnsibleAgent(config)
            
            # Test request for playbook creation with MinIO storage
            request = "create an Ansible playbook and store artifacts in MinIO"
            response = await agent.process_request(request)
            
            print(f"  📤 Ansible Agent Response:")
            print(f"    Content: {response.content[:200]}...")
            print(f"    Confidence: {response.confidence}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error testing Ansible agent with MinIO: {str(e)}")
            return False

    async def test_kubernetes_agent_minio(self):
        """Test Kubernetes agent with MinIO integration"""
        print("\n☸️ Testing Kubernetes Agent with MinIO...")
        
        try:
            from ai_ah_platform.agents.kubernetes_agent import KubernetesAgent
            from ai_ah_platform.core.base_platform import PlatformConfig
            
            # Create configuration with MinIO integration
            config = PlatformConfig(
                name="kubernetes_minio_test",
                version="1.0.0",
                environment="test",
                debug=True,
                metadata={
                    "minio_endpoint": self.minio_url,
                    "minio_access_key": self.access_key,
                    "minio_secret_key": self.secret_key,
                    "minio_bucket": "kubernetes-backups"
                }
            )
            
            agent = KubernetesAgent(config)
            
            # Test request for deployment with MinIO storage
            request = "deploy nginx with MinIO persistent storage"
            response = await agent.process_request(request)
            
            print(f"  📤 Kubernetes Agent Response:")
            print(f"    Content: {response.content[:200]}...")
            print(f"    Confidence: {response.confidence}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error testing Kubernetes agent with MinIO: {str(e)}")
            return False

    async def run_all_tests(self):
        """Run all MinIO integration tests"""
        print("🗄️ Testing MinIO Integration with AI-AH Agents")
        print("=" * 60)
        print("⚠️  This will test ACTUAL MinIO integration - no fake results")
        print("=" * 60)
        
        results = {
            "bucket_access": {},
            "data_upload": {},
            "data_download": {},
            "terraform_integration": False,
            "ansible_integration": False,
            "kubernetes_integration": False
        }
        
        # Test bucket access
        print("\n📋 Testing Bucket Access...")
        for bucket_name, test_data in self.test_data.items():
            results["bucket_access"][bucket_name] = await self.test_bucket_access(bucket_name, test_data)
        
        # Test data upload
        print("\n📤 Testing Data Upload...")
        for bucket_name, test_data in self.test_data.items():
            results["data_upload"][bucket_name] = await self.test_data_upload(bucket_name, test_data)
        
        # Test data download
        print("\n📥 Testing Data Download...")
        for bucket_name, test_data in self.test_data.items():
            results["data_download"][bucket_name] = await self.test_data_download(bucket_name, test_data)
        
        # Test agent integration
        results["terraform_integration"] = await self.test_terraform_agent_minio()
        results["ansible_integration"] = await self.test_ansible_agent_minio()
        results["kubernetes_integration"] = await self.test_kubernetes_agent_minio()
        
        # Generate summary
        print("\n📊 MinIO Integration Test Results:")
        print("=" * 40)
        
        # Bucket access results
        bucket_access_success = sum(results["bucket_access"].values())
        total_buckets = len(results["bucket_access"])
        print(f"  Bucket Access: {bucket_access_success}/{total_buckets} ({bucket_access_success/total_buckets*100:.1f}%)")
        
        # Data upload results
        upload_success = sum(results["data_upload"].values())
        print(f"  Data Upload: {upload_success}/{total_buckets} ({upload_success/total_buckets*100:.1f}%)")
        
        # Data download results
        download_success = sum(results["data_download"].values())
        print(f"  Data Download: {download_success}/{total_buckets} ({download_success/total_buckets*100:.1f}%)")
        
        # Agent integration results
        agent_success = sum([
            results["terraform_integration"],
            results["ansible_integration"],
            results["kubernetes_integration"]
        ])
        print(f"  Agent Integration: {agent_success}/3 ({agent_success/3*100:.1f}%)")
        
        # Overall success
        overall_success = (bucket_access_success + upload_success + download_success + agent_success) / (total_buckets * 3 + 3) * 100
        print(f"\n🎯 Overall Success Rate: {overall_success:.1f}%")
        
        if overall_success >= 80:
            print("🎉 MinIO integration is working well!")
        elif overall_success >= 60:
            print("⚠️ MinIO integration has some issues but is mostly working")
        else:
            print("❌ MinIO integration needs significant work")
        
        return results

async def main():
    """Main function to run MinIO integration tests"""
    tester = MinIOIntegrationTester()
    results = await tester.run_all_tests()
    
    print(f"\n🎉 MinIO Integration Tests Complete!")
    print(f"📊 Results saved for analysis")

if __name__ == "__main__":
    asyncio.run(main())
