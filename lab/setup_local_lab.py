#!/usr/bin/env python3
"""
Local Lab Setup for AI-AH Agent Testing
Creates a controlled environment for testing and validating agents
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class LabEnvironment:
    """Lab environment configuration"""
    name: str
    description: str
    services: List[str]
    terraform_enabled: bool
    docker_enabled: bool
    monitoring_enabled: bool

class LocalLabSetup:
    """Setup and manage local lab environment"""
    
    def __init__(self):
        self.lab_dir = Path("lab")
        self.terraform_dir = self.lab_dir / "terraform"
        self.docker_dir = self.lab_dir / "docker"
        self.monitoring_dir = self.lab_dir / "monitoring"
        self.test_results_dir = self.lab_dir / "test_results"
        
        # Lab environments
        self.environments = {
            "basic": LabEnvironment(
                name="Basic Web App",
                description="Simple web application with database",
                services=["web", "database", "load_balancer"],
                terraform_enabled=True,
                docker_enabled=True,
                monitoring_enabled=False
            ),
            "advanced": LabEnvironment(
                name="Advanced Microservices",
                description="Microservices architecture with monitoring",
                services=["api", "auth", "database", "cache", "queue", "monitoring"],
                terraform_enabled=True,
                docker_enabled=True,
                monitoring_enabled=True
            ),
            "production": LabEnvironment(
                name="Production-like",
                description="Production-ready infrastructure",
                services=["web", "api", "database", "cache", "queue", "monitoring", "logging"],
                terraform_enabled=True,
                docker_enabled=True,
                monitoring_enabled=True
            )
        }
    
    def setup_lab_directories(self):
        """Create lab directory structure"""
        print("🏗️ Setting up lab directories...")
        
        directories = [
            self.lab_dir,
            self.terraform_dir,
            self.docker_dir,
            self.monitoring_dir,
            self.test_results_dir,
            self.terraform_dir / "environments",
            self.terraform_dir / "modules",
            self.docker_dir / "compose",
            self.monitoring_dir / "grafana",
            self.monitoring_dir / "prometheus"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory}")
    
    def create_terraform_modules(self):
        """Create reusable Terraform modules"""
        print("📦 Creating Terraform modules...")
        
        # VPC Module
        vpc_dir = self.terraform_dir / "modules" / "vpc"
        vpc_dir.mkdir(parents=True, exist_ok=True)
        
        vpc_main = '''# VPC Module
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.name}-vpc"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.name}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.name}-private-${count.index + 1}"
    Type = "private"
  }
}'''
        
        (vpc_dir / "main.tf").write_text(vpc_main)
        
        vpc_variables = '''variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}'''
        
        (vpc_dir / "variables.tf").write_text(vpc_variables)
        
        vpc_outputs = '''output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}'''
        
        (vpc_dir / "outputs.tf").write_text(vpc_outputs)
        
        # EC2 Module
        ec2_dir = self.terraform_dir / "modules" / "ec2"
        ec2_dir.mkdir(parents=True, exist_ok=True)
        
        ec2_main = '''# EC2 Module
resource "aws_security_group" "main" {
  name_prefix = "${var.name}-"
  vpc_id      = var.vpc_id
  
  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidrs
    }
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.name}-sg"
  }
}

resource "aws_instance" "main" {
  count = var.instance_count
  
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_ids[count.index % length(var.subnet_ids)]
  
  vpc_security_group_ids = [aws_security_group.main.id]
  
  user_data = var.user_data
  
  tags = {
    Name = "${var.name}-${count.index + 1}"
    Environment = var.environment
  }
}'''
        
        (ec2_dir / "main.tf").write_text(ec2_main)
        
        ec2_variables = '''variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}

variable "ami_id" {
  description = "AMI ID for instances"
  type        = string
  default     = "ami-0c02fb55956c7d316"
}

variable "instance_type" {
  description = "Instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
}

variable "allowed_ports" {
  description = "List of allowed ports"
  type        = list(number)
  default     = [22, 80, 443]
}

variable "allowed_cidrs" {
  description = "List of allowed CIDR blocks"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "user_data" {
  description = "User data script"
  type        = string
  default     = ""
}'''
        
        (ec2_dir / "variables.tf").write_text(ec2_variables)
        
        ec2_outputs = '''output "instance_ids" {
  description = "IDs of the instances"
  value       = aws_instance.main[*].id
}

output "instance_public_ips" {
  description = "Public IPs of the instances"
  value       = aws_instance.main[*].public_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.main.id
}'''
        
        (ec2_dir / "outputs.tf").write_text(ec2_outputs)
        
        print("  ✅ Created Terraform modules")
    
    def create_lab_environments(self):
        """Create lab environment configurations"""
        print("🌍 Creating lab environments...")
        
        for env_name, env_config in self.environments.items():
            env_dir = self.terraform_dir / "environments" / env_name
            env_dir.mkdir(parents=True, exist_ok=True)
            
            # Create main.tf for environment
            main_tf = f'''# {env_config.name} Environment
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

# VPC Module
module "vpc" {{
  source = "../../modules/vpc"
  
  name        = "{env_name}"
  environment = var.environment
  cidr_block  = var.vpc_cidr
  
  availability_zones = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}}

# EC2 Module
module "web_servers" {{
  source = "../../modules/ec2"
  
  name        = "{env_name}-web"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.public_subnet_ids
  
  instance_count = var.web_instance_count
  instance_type  = var.web_instance_type
  allowed_ports  = [22, 80, 443]
  
  user_data = file("${{path.module}}/user_data.sh")
}}
'''
            
            (env_dir / "main.tf").write_text(main_tf)
            
            # Create variables.tf
            variables_tf = '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "lab"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

variable "web_instance_count" {
  description = "Number of web instances"
  type        = number
  default     = 2
}

variable "web_instance_type" {
  description = "Instance type for web servers"
  type        = string
  default     = "t3.micro"
}'''
            
            (env_dir / "variables.tf").write_text(variables_tf)
            
            # Create terraform.tfvars
            tfvars = f'''aws_region = "us-east-1"
environment = "lab-{env_name}"
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]
web_instance_count = 2
web_instance_type = "t3.micro"
'''
            
            (env_dir / "terraform.tfvars").write_text(tfvars)
            
            # Create user_data.sh
            user_data = '''#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create a simple test page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AI-AH Lab Test</title>
</head>
<body>
    <h1>AI-AH Agent Test Environment</h1>
    <p>This is a test deployment generated by the AI-AH agent.</p>
    <p>Environment: LAB</p>
    <p>Timestamp: $(date)</p>
</body>
</html>
EOF

systemctl restart httpd
'''
            
            (env_dir / "user_data.sh").write_text(user_data)
            
            print(f"  ✅ Created environment: {env_name}")
    
    def create_docker_compose(self):
        """Create Docker Compose files for local testing"""
        print("🐳 Creating Docker Compose configurations...")
        
        # Basic web app
        basic_compose = '''version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - NGINX_HOST=localhost
      - NGINX_PORT=80

  database:
    image: postgres:13
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
'''
        
        (self.docker_dir / "compose" / "basic.yml").write_text(basic_compose)
        
        print("  ✅ Created Docker Compose files")
    
    def create_test_scripts(self):
        """Create test scripts for validating deployments"""
        print("🧪 Creating test scripts...")
        
        # Terraform validation script
        terraform_test = '''#!/bin/bash
# Terraform Test Script

set -e

echo "🧪 Testing Terraform configuration..."

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan

# Apply if dry-run is not specified
if [ "$1" != "--dry-run" ]; then
    echo "🚀 Applying Terraform configuration..."
    terraform apply tfplan
    
    # Get outputs
    echo "📊 Terraform outputs:"
    terraform output
    
    # Test connectivity
    echo "🔍 Testing connectivity..."
    if command -v curl &> /dev/null; then
        # Get public IP from output
        PUBLIC_IP=$(terraform output -raw web_public_ip 2>/dev/null || echo "")
        if [ ! -z "$PUBLIC_IP" ]; then
            echo "Testing HTTP connectivity to $PUBLIC_IP..."
            curl -f http://$PUBLIC_IP || echo "❌ HTTP test failed"
        fi
    fi
else
    echo "✅ Dry run completed successfully"
fi
'''
        
        (self.lab_dir / "test_terraform.sh").write_text(terraform_test, encoding='utf-8')
        os.chmod(self.lab_dir / "test_terraform.sh", 0o755)
        
        print("  ✅ Created test scripts")
    
    def create_agent_test_framework(self):
        """Create framework for testing agents"""
        print("🤖 Creating agent test framework...")
        
        test_framework = '''#!/usr/bin/env python3
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
        request_text = "\\n".join(request_parts)
        
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
            print(f"\\n🧪 Testing: {test_case['name']}")
            
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
        print("\\n📊 Test Results Summary:")
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
        
        print(f"\\n🎯 Overall: {passed}/{total} tests passed")
        
        return results

if __name__ == "__main__":
    framework = AgentTestFramework()
    framework.run_comprehensive_test()
'''
        
        (self.lab_dir / "test_agents.py").write_text(test_framework, encoding='utf-8')
        os.chmod(self.lab_dir / "test_agents.py", 0o755)
        
        print("  ✅ Created agent test framework")
    
    def create_lab_runner(self):
        """Create main lab runner script"""
        print("🏃 Creating lab runner...")
        
        lab_runner = '''#!/usr/bin/env python3
"""
AI-AH Lab Runner
Main script to run the local lab environment
"""

import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="AI-AH Local Lab Runner")
    parser.add_argument("command", choices=["setup", "test", "deploy", "cleanup"], 
                       help="Command to run")
    parser.add_argument("--environment", choices=["basic", "advanced", "production"],
                       default="basic", help="Environment to use")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Run in dry-run mode (no actual deployment)")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        print("🏗️ Setting up lab environment...")
        from setup_local_lab import LocalLabSetup
        lab = LocalLabSetup()
        lab.setup_lab_directories()
        lab.create_terraform_modules()
        lab.create_lab_environments()
        lab.create_docker_compose()
        lab.create_test_scripts()
        lab.create_agent_test_framework()
        print("✅ Lab setup complete!")
        
    elif args.command == "test":
        print(f"🧪 Testing {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Running in dry-run mode...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan")
        else:
            print("🚀 Running full test...")
            os.system(f"cd lab && python test_agents.py")
            
    elif args.command == "deploy":
        print(f"🚀 Deploying {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Planning deployment...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan")
        else:
            print("⚠️ This will create real AWS resources. Continue? (y/N)")
            if input().lower() == 'y':
                os.system(f"cd lab/terraform/environments/{args.environment} && terraform apply")
            else:
                print("❌ Deployment cancelled")
                
    elif args.command == "cleanup":
        print(f"🧹 Cleaning up {args.environment} environment...")
        
        if args.dry_run:
            print("🔍 Planning cleanup...")
            os.system(f"cd lab/terraform/environments/{args.environment} && terraform plan -destroy")
        else:
            print("⚠️ This will destroy AWS resources. Continue? (y/N)")
            if input().lower() == 'y':
                os.system(f"cd lab/terraform/environments/{args.environment} && terraform destroy")
            else:
                print("❌ Cleanup cancelled")

if __name__ == "__main__":
    main()
'''
        
        (self.lab_dir / "run_lab.py").write_text(lab_runner, encoding='utf-8')
        os.chmod(self.lab_dir / "run_lab.py", 0o755)
        
        print("  ✅ Created lab runner")
    
    def setup_lab(self):
        """Complete lab setup"""
        print("🚀 Setting up AI-AH Local Lab Environment...")
        print("=" * 60)
        
        self.setup_lab_directories()
        self.create_terraform_modules()
        self.create_lab_environments()
        self.create_docker_compose()
        self.create_test_scripts()
        self.create_agent_test_framework()
        self.create_lab_runner()
        
        print("\\n✅ Lab setup complete!")
        print("\\n📋 Next steps:")
        print("1. Run: python lab/run_lab.py setup")
        print("2. Test: python lab/run_lab.py test --dry-run")
        print("3. Deploy: python lab/run_lab.py deploy --environment basic")
        print("4. Cleanup: python lab/run_lab.py cleanup --environment basic")

def main():
    """Main function"""
    print("🚀 AI-AH Local Lab Setup")
    print("=" * 40)
    
    lab = LocalLabSetup()
    lab.setup_lab()

if __name__ == "__main__":
    main()