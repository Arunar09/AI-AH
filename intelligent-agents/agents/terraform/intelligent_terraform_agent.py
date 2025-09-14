"""
Intelligent Terraform Agent
Builds truly intelligent infrastructure as code solutions
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from core.reasoning.local_reasoning_engine import LocalReasoningEngine

try:
    from core.models.simple_local_model import get_simple_model, is_simple_model_available
    LOCAL_MODEL_AVAILABLE = True
except ImportError:
    LOCAL_MODEL_AVAILABLE = False
    print("⚠️ Local model integration not available in Terraform agent")

@dataclass
class TerraformResource:
    """Terraform resource definition"""
    type: str
    name: str
    properties: Dict[str, Any]
    dependencies: List[str] = None

@dataclass
class TerraformFile:
    """Terraform file content"""
    filename: str
    content: str
    description: str

@dataclass
class TerraformProject:
    """Complete Terraform project"""
    name: str
    files: List[TerraformFile]
    variables: Dict[str, Any]
    outputs: Dict[str, Any]
    provider: str

@dataclass
class AgentResponse:
    """Agent response with reasoning and code"""
    content: str
    terraform_code: Dict[str, str]
    confidence: float
    reasoning_steps: List[str]
    cost_estimate: float
    implementation_steps: List[str]

class IntelligentTerraformAgent:
    """
    Intelligent Terraform Agent that can:
    - Analyze infrastructure requirements
    - Design optimal cloud architectures
    - Generate production-ready Terraform code
    - Explain decisions with clear reasoning
    - Troubleshoot and optimize solutions
    """
    
    def __init__(self):
        """Initialize the intelligent Terraform agent"""
        self.reasoning_engine = LocalReasoningEngine()
        self.knowledge_base = self._load_terraform_knowledge()
        self.local_model = None
        self.use_local_model = False
        
        # Disable local model for performance - use fast built-in logic instead
        self.use_local_model = False
        print("🏗️ Intelligent Terraform Agent initialized (using fast built-in logic)")
    
    def _load_terraform_knowledge(self) -> Dict[str, Any]:
        """Load comprehensive Terraform knowledge base"""
        return {
            "aws_patterns": {
                "web_app_basic": {
                    "name": "web_app_basic",
                    "description": "Basic web application with EC2, RDS, and ALB",
                    "components": ["vpc", "subnets", "security_groups", "ec2", "rds", "alb"],
                    "cost_estimate": 150,
                    "complexity": "medium",
                    "scalability": "medium",
                    "security": "medium"
                },
                "web_app_scalable": {
                    "name": "web_app_scalable",
                    "description": "Scalable web application with ECS, RDS, and CloudFront",
                    "components": ["vpc", "ecs", "rds", "cloudfront", "route53", "autoscaling"],
                    "cost_estimate": 300,
                    "complexity": "high",
                    "scalability": "high",
                    "security": "high"
                },
                "serverless_api": {
                    "name": "serverless_api",
                    "description": "Serverless API with Lambda, API Gateway, and DynamoDB",
                    "components": ["lambda", "api_gateway", "dynamodb", "cloudwatch", "iam"],
                    "cost_estimate": 50,
                    "complexity": "low",
                    "scalability": "high",
                    "security": "high"
                },
                "microservices": {
                    "name": "microservices",
                    "description": "Microservices architecture with EKS, RDS, and Redis",
                    "components": ["eks", "rds", "redis", "alb", "vpc", "iam"],
                    "cost_estimate": 500,
                    "complexity": "very_high",
                    "scalability": "very_high",
                    "security": "high"
                },
                "data_analytics": {
                    "name": "data_analytics",
                    "description": "Data analytics platform with EMR, S3, and Redshift",
                    "components": ["emr", "s3", "redshift", "glue", "athena"],
                    "cost_estimate": 800,
                    "complexity": "very_high",
                    "scalability": "very_high",
                    "security": "high"
                }
            },
            "azure_patterns": {
                "web_app_basic": {
                    "name": "web_app_basic",
                    "description": "Basic web application with App Service and SQL Database",
                    "components": ["resource_group", "app_service", "sql_database", "storage_account"],
                    "cost_estimate": 120,
                    "complexity": "medium",
                    "scalability": "medium",
                    "security": "medium"
                },
                "web_app_scalable": {
                    "name": "web_app_scalable",
                    "description": "Scalable web application with AKS and Cosmos DB",
                    "components": ["aks", "cosmos_db", "application_gateway", "key_vault"],
                    "cost_estimate": 400,
                    "complexity": "high",
                    "scalability": "high",
                    "security": "high"
                }
            },
            "gcp_patterns": {
                "web_app_basic": {
                    "name": "web_app_basic",
                    "description": "Basic web application with Compute Engine and Cloud SQL",
                    "components": ["vpc", "compute_engine", "cloud_sql", "load_balancer"],
                    "cost_estimate": 130,
                    "complexity": "medium",
                    "scalability": "medium",
                    "security": "medium"
                },
                "web_app_scalable": {
                    "name": "web_app_scalable",
                    "description": "Scalable web application with GKE and Cloud SQL",
                    "components": ["gke", "cloud_sql", "cloud_load_balancer", "cloud_storage"],
                    "cost_estimate": 350,
                    "complexity": "high",
                    "scalability": "high",
                    "security": "high"
                }
            },
            "best_practices": {
                "security": [
                    "Use least privilege IAM policies",
                    "Enable VPC flow logs",
                    "Use private subnets for databases",
                    "Enable encryption at rest and in transit",
                    "Regular security group reviews"
                ],
                "cost_optimization": [
                    "Use spot instances for non-critical workloads",
                    "Implement auto-scaling",
                    "Use reserved instances for predictable workloads",
                    "Monitor and optimize storage costs",
                    "Use CloudWatch for cost monitoring"
                ],
                "reliability": [
                    "Use multiple availability zones",
                    "Implement health checks",
                    "Use auto-scaling groups",
                    "Implement backup strategies",
                    "Use infrastructure as code"
                ]
            },
            "common_issues": {
                "terraform_errors": {
                    "state_lock": "Use DynamoDB for state locking in team environments",
                    "resource_conflicts": "Use terraform import for existing resources",
                    "dependency_issues": "Use depends_on for explicit dependencies"
                },
                "aws_issues": {
                    "permissions": "Ensure IAM roles have necessary permissions",
                    "quotas": "Check service quotas before deployment",
                    "regions": "Verify resource availability in chosen region"
                }
            }
        }
    
    def process_request(self, request: str, session_id: str = "default") -> AgentResponse:
        """
        Process infrastructure request and generate Terraform solution
        """
        print(f"🏗️ Processing Terraform request: {request}")
        
        # Use reasoning engine to analyze the request
        reasoning_result = self.reasoning_engine.reason_through_problem(request, {})
        
        # Generate Terraform code based on reasoning
        terraform_project = self._generate_terraform_code(reasoning_result, request)
        
        # Create implementation steps
        implementation_steps = self._generate_implementation_steps(terraform_project)
        
        # Calculate cost estimate
        cost_estimate = self._calculate_cost_estimate(terraform_project)
        
        return AgentResponse(
            content=reasoning_result.explanation,
            terraform_code=self._format_terraform_files(terraform_project),
            confidence=reasoning_result.confidence,
            reasoning_steps=reasoning_result.reasoning_steps,
            cost_estimate=cost_estimate,
            implementation_steps=implementation_steps
        )
    
    def _generate_terraform_code(self, reasoning_result, request: str) -> TerraformProject:
        """Generate Terraform code based on reasoning"""
        
        # Determine provider based on request
        provider = self._determine_provider(request)
        
        # Select appropriate pattern
        pattern = self._select_pattern(reasoning_result, provider)
        
        # Generate Terraform files
        files = self._generate_terraform_files(pattern, provider)
        
        # Generate variables and outputs
        variables = self._generate_variables(pattern)
        outputs = self._generate_outputs(pattern)
        
        return TerraformProject(
            name=pattern["name"],
            files=files,
            variables=variables,
            outputs=outputs,
            provider=provider
        )
    
    def _determine_provider(self, request: str) -> str:
        """Determine cloud provider from request"""
        request_lower = request.lower()
        
        if "aws" in request_lower or "amazon" in request_lower:
            return "aws"
        elif "azure" in request_lower or "microsoft" in request_lower:
            return "azure"
        elif "gcp" in request_lower or "google" in request_lower:
            return "gcp"
        else:
            return "aws"  # Default to AWS
    
    def _select_pattern(self, reasoning_result, provider: str) -> Dict[str, Any]:
        """Select appropriate infrastructure pattern"""
        patterns = self.knowledge_base.get(f"{provider}_patterns", {})
        
        # Simple pattern selection based on requirements
        if "serverless" in reasoning_result.decision.solution.name.lower():
            pattern = patterns.get("serverless_api", patterns.get("web_app_basic", {}))
        elif "scalable" in reasoning_result.decision.solution.name.lower():
            pattern = patterns.get("web_app_scalable", patterns.get("web_app_basic", {}))
        else:
            pattern = patterns.get("web_app_basic", {})
        
        # Ensure pattern has required keys
        if not pattern:
            pattern = {
                "name": "basic_web_app",
                "description": "Basic web application",
                "components": ["compute", "database", "networking"],
                "cost_estimate": 100,
                "complexity": "medium"
            }
        
        # Add name if missing
        if "name" not in pattern:
            pattern["name"] = "web_app_basic"
        
        return pattern
    
    def _generate_terraform_files(self, pattern: Dict[str, Any], provider: str) -> List[TerraformFile]:
        """Generate Terraform files based on pattern"""
        files = []
        
        # Generate main.tf
        main_content = self._generate_main_tf(pattern, provider)
        files.append(TerraformFile(
            filename="main.tf",
            content=main_content,
            description="Main Terraform configuration"
        ))
        
        # Generate variables.tf
        variables_content = self._generate_variables_tf(pattern)
        files.append(TerraformFile(
            filename="variables.tf",
            content=variables_content,
            description="Input variables"
        ))
        
        # Generate outputs.tf
        outputs_content = self._generate_outputs_tf(pattern)
        files.append(TerraformFile(
            filename="outputs.tf",
            content=outputs_content,
            description="Output values"
        ))
        
        # Generate terraform.tfvars
        tfvars_content = self._generate_tfvars(pattern)
        files.append(TerraformFile(
            filename="terraform.tfvars",
            content=tfvars_content,
            description="Variable values"
        ))
        
        return files
    
    def _generate_main_tf(self, pattern: Dict[str, Any], provider: str) -> str:
        """Generate main.tf content"""
        if provider == "aws":
            return self._generate_aws_main_tf(pattern)
        elif provider == "azure":
            return self._generate_azure_main_tf(pattern)
        elif provider == "gcp":
            return self._generate_gcp_main_tf(pattern)
        else:
            return "# Provider not supported yet"
    
    def _generate_aws_main_tf(self, pattern: Dict[str, Any]) -> str:
        """Generate AWS main.tf using local model if available"""
        if self.use_local_model and self.local_model:
            return self._generate_aws_main_tf_with_local_model(pattern)
        else:
            return self._generate_aws_main_tf_fallback(pattern)
    
    def _generate_aws_main_tf_with_local_model(self, pattern: Dict[str, Any]) -> str:
        """Generate AWS main.tf using CodeLlama"""
        try:
            prompt = f"""<s>[INST] Generate AWS Terraform code for: {pattern["name"]}

Create basic infrastructure with:
- VPC and subnets
- Security groups
- EC2 instances or load balancer
- Proper tagging

Generate only Terraform code, no explanations.
[/INST]"""
            
            response = self.local_model.generate_response(prompt, max_tokens=800)
            return response
            
        except Exception as e:
            print(f"⚠️ Local model failed for Terraform generation, using fallback: {e}")
            return self._generate_aws_main_tf_fallback(pattern)
    
    def _generate_aws_main_tf_fallback(self, pattern: Dict[str, Any]) -> str:
        """Fallback AWS main.tf generation"""
        return f'''# {pattern["description"]}
# Generated by Intelligent Terraform Agent

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

# VPC
resource "aws_vpc" "main" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name = "${{var.project_name}}-vpc"
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "main" {{
  vpc_id = aws_vpc.main.id

  tags = {{
    Name = "${{var.project_name}}-igw"
  }}
}}

# Public Subnet
resource "aws_subnet" "public" {{
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {{
    Name = "${{var.project_name}}-public-subnet"
  }}
}}

# Security Group for Web Servers
resource "aws_security_group" "web" {{
  name_prefix = "${{var.project_name}}-web-"
  vpc_id      = aws_vpc.main.id

  ingress {{
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  ingress {{
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name = "${{var.project_name}}-web-sg"
  }}
}}

# EC2 Instance
resource "aws_instance" "web" {{
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Hello from ${{var.project_name}}!</h1>" > /var/www/html/index.html
  EOF

  tags = {{
    Name = "${{var.project_name}}-web-server"
  }}
}}

# RDS Subnet Group
resource "aws_db_subnet_group" "main" {{
  name       = "${{var.project_name}}-db-subnet-group"
  subnet_ids = [aws_subnet.public.id]

  tags = {{
    Name = "${{var.project_name}}-db-subnet-group"
  }}
}}

# RDS Instance
resource "aws_db_instance" "main" {{
  identifier = "${{var.project_name}}-db"
  engine     = "mysql"
  engine_version = "8.0"
  instance_class = var.db_instance_class
  allocated_storage = 20
  storage_type = "gp2"
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = true

  tags = {{
    Name = "${{var.project_name}}-database"
  }}
}}

# Security Group for Database
resource "aws_security_group" "db" {{
  name_prefix = "${{var.project_name}}-db-"
  vpc_id      = aws_vpc.main.id

  ingress {{
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }}

  tags = {{
    Name = "${{var.project_name}}-db-sg"
  }}
}}
'''
    
    def _generate_azure_main_tf(self, pattern: Dict[str, Any]) -> str:
        """Generate Azure main.tf"""
        return f'''# {pattern["description"]}
# Generated by Intelligent Terraform Agent

terraform {{
  required_version = ">= 1.0"
  required_providers {{
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }}
  }}
}}

provider "azurerm" {{
  features {{}}
}}

# Resource Group
resource "azurerm_resource_group" "main" {{
  name     = "${{var.project_name}}-rg"
  location = var.location

  tags = {{
    Name = "${{var.project_name}}-resource-group"
  }}
}}

# App Service Plan
resource "azurerm_service_plan" "main" {{
  name                = "${{var.project_name}}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  os_type            = "Linux"
  sku_name           = var.app_service_sku

  tags = {{
    Name = "${{var.project_name}}-app-service-plan"
  }}
}}

# App Service
resource "azurerm_linux_web_app" "main" {{
  name                = "${{var.project_name}}-app"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_service_plan.main.location
  service_plan_id    = azurerm_service_plan.main.id

  site_config {{
    application_stack {{
      node_version = "18-lts"
    }}
  }}

  tags = {{
    Name = "${{var.project_name}}-web-app"
  }}
}}

# SQL Server
resource "azurerm_mssql_server" "main" {{
  name                         = "${{var.project_name}}-sqlserver"
  resource_group_name          = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  version                     = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  tags = {{
    Name = "${{var.project_name}}-sql-server"
  }}
}}

# SQL Database
resource "azurerm_mssql_database" "main" {{
  name           = var.database_name
  server_id      = azurerm_mssql_server.main.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 2
  sku_name       = "Basic"

  tags = {{
    Name = "${{var.project_name}}-database"
  }}
}}
'''
    
    def _generate_gcp_main_tf(self, pattern: Dict[str, Any]) -> str:
        """Generate GCP main.tf"""
        return f'''# {pattern["description"]}
# Generated by Intelligent Terraform Agent

terraform {{
  required_version = ">= 1.0"
  required_providers {{
    google = {{
      source  = "hashicorp/google"
      version = "~> 4.0"
    }}
  }}
}}

provider "google" {{
  project = var.project_id
  region  = var.region
}}

# VPC Network
resource "google_compute_network" "main" {{
  name                    = "${{var.project_name}}-vpc"
  auto_create_subnetworks = false
}}

# Subnet
resource "google_compute_subnetwork" "main" {{
  name          = "${{var.project_name}}-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main.id
}}

# Firewall Rule
resource "google_compute_firewall" "web" {{
  name    = "${{var.project_name}}-web-firewall"
  network = google_compute_network.main.name

  allow {{
    protocol = "tcp"
    ports    = ["80", "443"]
  }}

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
}}

# Compute Instance
resource "google_compute_instance" "web" {{
  name         = "${{var.project_name}}-web"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {{
    initialize_params {{
      image = var.image
    }}
  }}

  network_interface {{
    network    = google_compute_network.main.name
    subnetwork = google_compute_subnetwork.main.name
    access_config {{
      // Ephemeral public IP
    }}
  }}

  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y apache2
    systemctl start apache2
    systemctl enable apache2
    echo "<h1>Hello from ${{var.project_name}}!</h1>" > /var/www/html/index.html
  EOF

  tags = ["web-server"]

  labels = {{
    Name = "${{var.project_name}}-web-server"
  }}
}}

# Cloud SQL Instance
resource "google_sql_database_instance" "main" {{
  name             = "${{var.project_name}}-db"
  database_version = "MYSQL_8_0"
  region           = var.region

  settings {{
    tier = var.db_tier
  }}

  deletion_protection = false
}}

# Cloud SQL Database
resource "google_sql_database" "main" {{
  name     = var.database_name
  instance = google_sql_database_instance.main.name
}}

# Cloud SQL User
resource "google_sql_user" "main" {{
  name     = var.db_username
  instance = google_sql_database_instance.main.name
  password = var.db_password
}}
'''
    
    def _generate_variables_tf(self, pattern: Dict[str, Any]) -> str:
        """Generate variables.tf content"""
        return '''# Input Variables
# Generated by Intelligent Terraform Agent

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "my-web-app"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone"
  type        = string
  default     = "us-east-1a"
}

variable "ami_id" {
  description = "AMI ID for EC2 instance"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Amazon Linux 2
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Name of the AWS key pair"
  type        = string
  default     = "my-key"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "myapp"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  default     = "changeme123"
}
'''
    
    def _generate_outputs_tf(self, pattern: Dict[str, Any]) -> str:
        """Generate outputs.tf content"""
        return '''# Output Values
# Generated by Intelligent Terraform Agent

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "web_server_public_ip" {
  description = "Public IP address of the web server"
  value       = aws_instance.web.public_ip
}

output "web_server_private_ip" {
  description = "Private IP address of the web server"
  value       = aws_instance.web.private_ip
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
}

output "database_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "web_url" {
  description = "URL to access the web application"
  value       = "http://${aws_instance.web.public_ip}"
}
'''
    
    def _generate_tfvars(self, pattern: Dict[str, Any]) -> str:
        """Generate terraform.tfvars content"""
        return '''# Variable Values
# Generated by Intelligent Terraform Agent

project_name = "my-web-app"
aws_region = "us-east-1"
vpc_cidr = "10.0.0.0/16"
public_subnet_cidr = "10.0.1.0/24"
availability_zone = "us-east-1a"
ami_id = "ami-0c02fb55956c7d316"
instance_type = "t3.micro"
key_name = "my-key"
db_instance_class = "db.t3.micro"
db_name = "myapp"
db_username = "admin"
db_password = "changeme123"
'''
    
    def _generate_variables(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate variables dictionary"""
        return {
            "project_name": "my-web-app",
            "aws_region": "us-east-1",
            "instance_type": "t3.micro",
            "db_instance_class": "db.t3.micro"
        }
    
    def _generate_outputs(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Generate outputs dictionary"""
        return {
            "web_url": "http://${aws_instance.web.public_ip}",
            "database_endpoint": "${aws_db_instance.main.endpoint}",
            "vpc_id": "${aws_vpc.main.id}"
        }
    
    def _format_terraform_files(self, project: TerraformProject) -> Dict[str, str]:
        """Format Terraform files as dictionary"""
        files = {}
        for file in project.files:
            files[file.filename] = file.content
        return files
    
    def _generate_implementation_steps(self, project: TerraformProject) -> List[str]:
        """Generate implementation steps"""
        return [
            "1. Initialize Terraform: `terraform init`",
            "2. Review the plan: `terraform plan`",
            "3. Apply the configuration: `terraform apply`",
            "4. Access your application using the web_url output",
            "5. Configure your application to use the database endpoint",
            "6. Set up monitoring and logging",
            "7. Configure backup and disaster recovery"
        ]
    
    def _calculate_cost_estimate(self, project: TerraformProject) -> float:
        """Calculate cost estimate"""
        # Simple cost calculation based on pattern
        base_cost = 100
        if "scalable" in project.name.lower():
            base_cost = 300
        elif "serverless" in project.name.lower():
            base_cost = 50
        
        return base_cost
    
    def validate_terraform_code(self, terraform_code: Dict[str, str]) -> Dict[str, Any]:
        """Validate Terraform code for syntax and best practices"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Check for required files
        required_files = ["main.tf", "variables.tf", "outputs.tf"]
        for file in required_files:
            if file not in terraform_code:
                validation_results["errors"].append(f"Missing required file: {file}")
                validation_results["valid"] = False
        
        # Check main.tf for basic structure
        if "main.tf" in terraform_code:
            main_content = terraform_code["main.tf"]
            
            # Check for provider block
            if "provider" not in main_content:
                validation_results["errors"].append("Missing provider configuration")
                validation_results["valid"] = False
            
            # Check for resource blocks
            if "resource" not in main_content:
                validation_results["errors"].append("No resources defined")
                validation_results["valid"] = False
            
            # Check for security best practices
            if "security_group" in main_content and "0.0.0.0/0" in main_content:
                validation_results["warnings"].append("Security group allows access from anywhere (0.0.0.0/0)")
            
            # Check for tags
            if "tags" not in main_content:
                validation_results["suggestions"].append("Consider adding tags to resources for better organization")
        
        # Check variables.tf
        if "variables.tf" in terraform_code:
            vars_content = terraform_code["variables.tf"]
            if "variable" not in vars_content:
                validation_results["warnings"].append("No variables defined")
        
        return validation_results
    
    def optimize_terraform_code(self, terraform_code: Dict[str, str], requirements: Dict[str, Any]) -> Dict[str, str]:
        """Optimize Terraform code for cost, performance, and security"""
        optimized_code = terraform_code.copy()
        
        # Cost optimization
        if requirements.get("cost_optimization", False):
            optimized_code = self._apply_cost_optimizations(optimized_code)
        
        # Security optimization
        if requirements.get("security_hardening", False):
            optimized_code = self._apply_security_optimizations(optimized_code)
        
        # Performance optimization
        if requirements.get("performance_optimization", False):
            optimized_code = self._apply_performance_optimizations(optimized_code)
        
        return optimized_code
    
    def _apply_cost_optimizations(self, terraform_code: Dict[str, str]) -> Dict[str, str]:
        """Apply cost optimization techniques"""
        optimized = terraform_code.copy()
        
        if "main.tf" in optimized:
            main_content = optimized["main.tf"]
            
            # Add spot instance configuration
            if "aws_instance" in main_content and "spot_price" not in main_content:
                main_content = main_content.replace(
                    'resource "aws_instance"',
                    'resource "aws_spot_instance_request"'
                )
                main_content = main_content.replace(
                    'instance_type          = var.instance_type',
                    'instance_type          = var.instance_type\n  spot_price            = "0.01"\n  wait_for_fulfillment = true'
                )
                optimized["main.tf"] = main_content
        
        return optimized
    
    def _apply_security_optimizations(self, terraform_code: Dict[str, str]) -> Dict[str, str]:
        """Apply security hardening techniques"""
        optimized = terraform_code.copy()
        
        if "main.tf" in optimized:
            main_content = optimized["main.tf"]
            
            # Add VPC flow logs
            if "aws_vpc" in main_content and "aws_flow_log" not in main_content:
                flow_logs = '''
# VPC Flow Logs
resource "aws_flow_log" "vpc_flow_log" {
  iam_role_arn    = aws_iam_role.flow_log_role.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_logs.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id
}

resource "aws_cloudwatch_log_group" "vpc_flow_logs" {
  name              = "/aws/vpc/flowlogs"
  retention_in_days = 30
}

resource "aws_iam_role" "flow_log_role" {
  name = "${var.project_name}-flow-log-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "flow_log_policy" {
  name = "${var.project_name}-flow-log-policy"
  role = aws_iam_role.flow_log_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}
'''
                optimized["main.tf"] = main_content + flow_logs
        
        return optimized
    
    def _apply_performance_optimizations(self, terraform_code: Dict[str, str]) -> Dict[str, str]:
        """Apply performance optimization techniques"""
        optimized = terraform_code.copy()
        
        if "main.tf" in optimized:
            main_content = optimized["main.tf"]
            
            # Add auto-scaling group
            if "aws_instance" in main_content and "aws_autoscaling_group" not in main_content:
                autoscaling = '''
# Auto Scaling Group
resource "aws_launch_template" "web_template" {
  name_prefix   = "${var.project_name}-web-"
  image_id      = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Hello from ${var.project_name}!</h1>" > /var/www/html/index.html
  EOF)

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.project_name}-web-server"
    }
  }
}

resource "aws_autoscaling_group" "web_asg" {
  name                = "${var.project_name}-web-asg"
  vpc_zone_identifier = [aws_subnet.public.id]
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = 2
  max_size         = 10
  desired_capacity = 2

  launch_template {
    id      = aws_launch_template.web_template.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-web-asg"
    propagate_at_launch = false
  }
}

resource "aws_autoscaling_policy" "web_scale_up" {
  name                   = "${var.project_name}-web-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web_asg.name
}

resource "aws_autoscaling_policy" "web_scale_down" {
  name                   = "${var.project_name}-web-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web_asg.name
}
'''
                optimized["main.tf"] = main_content + autoscaling
        
        return optimized
    
    def troubleshoot_terraform_issue(self, issue_description: str, terraform_code: Dict[str, str] = None) -> Dict[str, Any]:
        """Troubleshoot common Terraform issues"""
        troubleshooting_result = {
            "issue_identified": False,
            "root_cause": "",
            "solution": "",
            "prevention": "",
            "related_issues": []
        }
        
        issue_lower = issue_description.lower()
        
        # Common Terraform issues
        if "state" in issue_lower and "lock" in issue_lower:
            troubleshooting_result.update({
                "issue_identified": True,
                "root_cause": "Terraform state is locked, likely by another process or team member",
                "solution": "Use 'terraform force-unlock <lock-id>' or check for running Terraform processes",
                "prevention": "Use remote state backend with DynamoDB for state locking",
                "related_issues": ["Concurrent modifications", "State corruption"]
            })
        
        elif "permission" in issue_lower or "access denied" in issue_lower:
            troubleshooting_result.update({
                "issue_identified": True,
                "root_cause": "Insufficient IAM permissions for the current AWS credentials",
                "solution": "Check IAM policies and ensure required permissions are granted",
                "prevention": "Use least privilege principle and test permissions before deployment",
                "related_issues": ["IAM role issues", "Credential problems"]
            })
        
        elif "resource" in issue_lower and "already exists" in issue_lower:
            troubleshooting_result.update({
                "issue_identified": True,
                "root_cause": "Resource already exists in AWS but not in Terraform state",
                "solution": "Use 'terraform import <resource_type>.<name> <resource_id>' to import existing resource",
                "prevention": "Always use Terraform for resource creation and management",
                "related_issues": ["State drift", "Manual resource creation"]
            })
        
        elif "dependency" in issue_lower or "circular" in issue_lower:
            troubleshooting_result.update({
                "issue_identified": True,
                "root_cause": "Circular dependency or missing dependency between resources",
                "solution": "Use 'depends_on' to explicitly define dependencies or restructure resources",
                "prevention": "Plan resource dependencies carefully and use data sources when possible",
                "related_issues": ["Resource ordering", "Implicit dependencies"]
            })
        
        else:
            troubleshooting_result.update({
                "issue_identified": False,
                "root_cause": "Issue not recognized in common patterns",
                "solution": "Check Terraform documentation, logs, and community resources",
                "prevention": "Follow Terraform best practices and use version control",
                "related_issues": ["Unknown issues", "Complex configurations"]
            })
        
        return troubleshooting_result
    
    def generate_terraform_plan(self, terraform_code: Dict[str, str], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive Terraform deployment plan"""
        plan = {
            "phases": [],
            "estimated_duration": "30-60 minutes",
            "prerequisites": [],
            "post_deployment": [],
            "rollback_plan": []
        }
        
        # Phase 1: Prerequisites
        plan["prerequisites"] = [
            "Install Terraform (>= 1.0)",
            "Configure AWS credentials",
            "Verify AWS permissions",
            "Check service quotas",
            "Review and customize variables"
        ]
        
        # Phase 2: Deployment phases
        plan["phases"] = [
            {
                "name": "Infrastructure Setup",
                "steps": [
                    "Initialize Terraform: terraform init",
                    "Review plan: terraform plan",
                    "Apply infrastructure: terraform apply"
                ],
                "estimated_time": "15-30 minutes"
            },
            {
                "name": "Application Deployment",
                "steps": [
                    "Configure application settings",
                    "Deploy application code",
                    "Configure database connections",
                    "Test application functionality"
                ],
                "estimated_time": "15-30 minutes"
            }
        ]
        
        # Phase 3: Post-deployment
        plan["post_deployment"] = [
            "Verify all resources are running",
            "Test application endpoints",
            "Configure monitoring and alerting",
            "Set up backup procedures",
            "Document infrastructure details"
        ]
        
        # Rollback plan
        plan["rollback_plan"] = [
            "Stop application services",
            "Destroy infrastructure: terraform destroy",
            "Restore from backup if needed",
            "Investigate and fix issues",
            "Redeploy with fixes"
        ]
        
        return plan
