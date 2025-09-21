"""
Enhanced Terraform Agent with Log^2 Architecture
Intelligent infrastructure as code solutions with learning and adaptation
"""

import os
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys

# Add the intelligent-agents directory to the path
intelligent_agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if intelligent_agents_dir not in sys.path:
    sys.path.insert(0, intelligent_agents_dir)

from core.reasoning.local_reasoning_engine import LocalReasoningEngine
from .terraform_logic_engine import TerraformLogicEngine
from .terraform_log_engine import TerraformLogEngine, TerraformOperationLog
from .terraform_intelligence_engine import TerraformIntelligenceEngine
from .terraform_project_modifier import TerraformProjectModifier
from .terraform_agent_monitoring.enhanced_terraform_agent_monitor import EnhancedTerraformAgentMonitor
from .autonomous_operations.autonomous_terraform_agent import AutonomousTerraformAgent

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
    """Response from Terraform agent"""
    success: bool
    message: str
    project: Optional[TerraformProject] = None
    cost_estimate: Optional[float] = None
    recommendations: List[str] = None
    warnings: List[str] = None
    operation_id: str = None

class EnhancedTerraformAgent:
    """Enhanced Terraform Agent with Log^2 Architecture"""
    
    def __init__(self, workspaces_dir: str = "workspaces"):
        self.workspaces_dir = workspaces_dir
        os.makedirs(workspaces_dir, exist_ok=True)
        
        # Initialize Log^2 components
        self.logic_engine = TerraformLogicEngine()
        self.log_engine = TerraformLogEngine()
        self.intelligence_engine = TerraformIntelligenceEngine()
        self.project_modifier = TerraformProjectModifier(workspaces_dir)
        
        # Initialize existing components
        self.reasoning_engine = LocalReasoningEngine()
        self.monitor = EnhancedTerraformAgentMonitor()
        self.autonomous_agent = AutonomousTerraformAgent()
        
        # Agent state
        self.current_project = None
        self.operation_history = []
        
        print("✅ Enhanced Terraform Agent initialized with Log^2 architecture")
    
    def process_request(self, request: str, user_context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process infrastructure request with Log^2 intelligence"""
        operation_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Log operation start
            self._log_operation_start(operation_id, request, user_context)
            
            # Parse requirements using logic engine
            requirements = self._parse_requirements(request, user_context)
            
            # Analyze infrastructure requirements
            analysis = self.logic_engine.analyze_infrastructure_requirements(requirements)
            
            # Generate infrastructure design
            design = self._generate_infrastructure_design(requirements, analysis)
            
            # Validate design
            validation = self.logic_engine.validate_infrastructure_design(design)
            
            if not validation['valid']:
                return AgentResponse(
                    success=False,
                    message=f"Design validation failed: {', '.join(validation['errors'])}",
                    warnings=validation['warnings'],
                    operation_id=operation_id
                )
            
            # Generate Terraform project
            project = self._generate_terraform_project(design, requirements)
            
            # Get cost estimate
            cost_estimate = design.get('estimated_costs', {}).get('monthly_estimate', 0.0)
            
            # Get optimization recommendations
            recommendations = self.logic_engine.get_optimization_recommendations(design)
            
            # Learn from this operation
            operation_data = {
                'operation_type': 'infrastructure_generation',
                'user_count': requirements.get('user_count', 0),
                'data_volume': requirements.get('data_volume', 0),
                'availability_requirement': requirements.get('availability_requirement', 99.0),
                'security_requirements': requirements.get('security_requirements', False),
                'compliance_required': requirements.get('compliance_required', False),
                'execution_time': time.time() - start_time,
                'success': True,
                'cost_impact': cost_estimate,
                'resource_changes': design.get('suggested_resources', [])
            }
            
            self.intelligence_engine.learn_from_operation(operation_data)
            
            # Log successful operation
            self._log_operation_success(operation_id, operation_data)
            
            return AgentResponse(
                success=True,
                message="Infrastructure design generated successfully",
                project=project,
                cost_estimate=cost_estimate,
                recommendations=[rec['description'] for rec in recommendations],
                warnings=validation['warnings'],
                operation_id=operation_id
            )
            
        except Exception as e:
            # Log operation failure
            self._log_operation_failure(operation_id, str(e))
            
            return AgentResponse(
                success=False,
                message=f"Failed to process request: {str(e)}",
                operation_id=operation_id
            )
    
    def _parse_requirements(self, request: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parse requirements from request using logic engine"""
        requirements = {
            'user_count': 0,
            'data_volume': 0,
            'availability_requirement': 99.0,
            'security_requirements': False,
            'compliance_required': False,
            'budget_limit': 1000.0,
            'region': 'us-east-1',
            'environment': 'production'
        }
        
        # Extract user count
        user_count = self._extract_user_count(request)
        if user_count > 0:
            requirements['user_count'] = user_count
        
        # Extract data volume
        data_volume = self._extract_data_volume(request)
        if data_volume > 0:
            requirements['data_volume'] = data_volume
        
        # Extract availability requirement
        availability = self._extract_availability_requirement(request)
        if availability > 0:
            requirements['availability_requirement'] = availability
        
        # Extract security requirements
        if any(keyword in request.lower() for keyword in ['security', 'encryption', 'compliance', 'audit']):
            requirements['security_requirements'] = True
        
        # Extract compliance requirements
        if any(keyword in request.lower() for keyword in ['compliance', 'soc2', 'gdpr', 'hipaa']):
            requirements['compliance_required'] = True
        
        # Extract budget information
        budget = self._extract_budget(request)
        if budget > 0:
            requirements['budget_limit'] = budget
        
        # Merge with user context
        if user_context:
            requirements.update(user_context)
        
        return requirements
    
    def _extract_user_count(self, request: str) -> int:
        """Extract user count from request"""
        import re
        
        # Look for numbers followed by user-related keywords
        patterns = [
            r'(\d+(?:,\d+)*)\s*(?:users?|people|employees|customers)',
            r'(\d+(?:,\d+)*)\s*(?:concurrent|simultaneous)',
            r'(\d+(?:,\d+)*)\s*(?:daily|monthly)\s*(?:users?|visitors)',
            r'(\d+(?:,\d+)*)\s*(?:active|registered)\s*(?:users?|members)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                number_str = match.group(1).replace(',', '')
                try:
                    return int(number_str)
                except ValueError:
                    continue
        
        return 0
    
    def _extract_data_volume(self, request: str) -> float:
        """Extract data volume from request"""
        import re
        
        # Look for data volume indicators
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:gb|gigabytes?|tb|terabytes?|mb|megabytes?)',
            r'(\d+(?:\.\d+)?)\s*(?:gigabytes?|terabytes?|megabytes?)',
            r'(\d+(?:\.\d+)?)\s*(?:gb|tb|mb)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                number = float(match.group(1))
                unit = match.group(0).lower()
                
                if 'tb' in unit or 'terabyte' in unit:
                    return number * 1000  # Convert TB to GB
                elif 'gb' in unit or 'gigabyte' in unit:
                    return number
                elif 'mb' in unit or 'megabyte' in unit:
                    return number / 1000  # Convert MB to GB
        
        return 0.0
    
    def _extract_availability_requirement(self, request: str) -> float:
        """Extract availability requirement from request"""
        import re
        
        # Look for availability percentages
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:availability|uptime)',
            r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:sla|service level)',
            r'(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:reliability|downtime)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                return float(match.group(1))
        
        return 0.0
    
    def _extract_budget(self, request: str) -> float:
        """Extract budget information from request"""
        import re
        
        # Look for budget amounts
        patterns = [
            r'\$(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:budget|cost|spend)',
            r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:dollars?|usd|budget|cost)',
            r'budget\s*(?:of\s*)?\$?(\d+(?:,\d+)*(?:\.\d+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        return 0.0
    
    def _generate_infrastructure_design(self, requirements: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate infrastructure design based on requirements and analysis"""
        design = {
            'pattern': analysis.get('recommended_pattern'),
            'resources': analysis.get('suggested_resources', []),
            'estimated_costs': analysis.get('estimated_costs', {}),
            'security_considerations': analysis.get('security_considerations', []),
            'scalability_factors': analysis.get('scalability_factors', []),
            'compliance_requirements': analysis.get('compliance_requirements', []),
            'encryption_enabled': requirements.get('security_requirements', False),
            'access_logging_enabled': requirements.get('compliance_required', False),
            'availability_target': requirements.get('availability_requirement', 99.0)
        }
        
        return design
    
    def _generate_terraform_project(self, design: Dict[str, Any], requirements: Dict[str, Any]) -> TerraformProject:
        """Generate Terraform project from design"""
        project_name = f"infrastructure-{int(time.time())}"
        
        # Generate main.tf
        main_tf_content = self._generate_main_tf(design, requirements)
        
        # Generate variables.tf
        variables_tf_content = self._generate_variables_tf(requirements)
        
        # Generate outputs.tf
        outputs_tf_content = self._generate_outputs_tf(design)
        
        # Create project
        project = TerraformProject(
            name=project_name,
            files=[
                TerraformFile("main.tf", main_tf_content, "Main Terraform configuration"),
                TerraformFile("variables.tf", variables_tf_content, "Variable definitions"),
                TerraformFile("outputs.tf", outputs_tf_content, "Output definitions")
            ],
            variables=self._extract_variables(requirements),
            outputs=self._extract_outputs(design),
            provider="aws"
        )
        
        # Save project to workspace
        self._save_project(project)
        
        return project
    
    def _generate_main_tf(self, design: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """Generate main.tf content"""
        content = '''# Terraform configuration generated by Enhanced Terraform Agent
# Generated on: {timestamp}

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

# Data sources
data "aws_availability_zones" "available" {{
  state = "available"
}}

# VPC Configuration
resource "aws_vpc" "main" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name        = "${{var.project_name}}-vpc"
    Environment = var.environment
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "main" {{
  vpc_id = aws_vpc.main.id

  tags = {{
    Name        = "${{var.project_name}}-igw"
    Environment = var.environment
  }}
}}

# Public Subnets
resource "aws_subnet" "public" {{
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {{
    Name        = "${{var.project_name}}-public-subnet-${{count.index + 1}}"
    Environment = var.environment
    Type        = "public"
  }}
}}

# Private Subnets
resource "aws_subnet" "private" {{
  count = length(var.private_subnet_cidrs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {{
    Name        = "${{var.project_name}}-private-subnet-${{count.index + 1}}"
    Environment = var.environment
    Type        = "private"
  }}
}}

# Route Table for Public Subnets
resource "aws_route_table" "public" {{
  vpc_id = aws_vpc.main.id

  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }}

  tags = {{
    Name        = "${{var.project_name}}-public-rt"
    Environment = var.environment
  }}
}}

# Route Table for Private Subnets
resource "aws_route_table" "private" {{
  count = length(var.private_subnet_cidrs)

  vpc_id = aws_vpc.main.id

  tags = {{
    Name        = "${{var.project_name}}-private-rt-${{count.index + 1}}"
    Environment = var.environment
  }}
}}

# Route Table Associations
resource "aws_route_table_association" "public" {{
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}}

resource "aws_route_table_association" "private" {{
  count = length(aws_subnet.private)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}}

# Security Groups
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
    Name        = "${{var.project_name}}-web-sg"
    Environment = var.environment
  }}
}}

resource "aws_security_group" "database" {{
  name_prefix = "${{var.project_name}}-db-"
  vpc_id      = aws_vpc.main.id

  ingress {{
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name        = "${{var.project_name}}-db-sg"
    Environment = var.environment
  }}
}}

# EC2 Instances
resource "aws_instance" "web" {{
  count = var.instance_count

  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public[count.index % length(aws_subnet.public)].id
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${{path.module}}/user_data.sh", {{
    project_name = var.project_name
  }}))

  tags = {{
    Name        = "${{var.project_name}}-web-${{count.index + 1}}"
    Environment = var.environment
  }}
}}

# Application Load Balancer
resource "aws_lb" "main" {{
  name               = "${{var.project_name}}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false

  tags = {{
    Name        = "${{var.project_name}}-alb"
    Environment = var.environment
  }}
}}

resource "aws_lb_target_group" "web" {{
  name     = "${{var.project_name}}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {{
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }}
}}

resource "aws_lb_target_group_attachment" "web" {{
  count            = length(aws_instance.web)
  target_group_arn = aws_lb_target_group.web.arn
  target_id        = aws_instance.web[count.index].id
  port             = 80
}}

resource "aws_lb_listener" "web" {{
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {{
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }}
}}

# RDS Database
resource "aws_db_instance" "main" {{
  identifier = "${{var.project_name}}-db"

  engine         = var.db_engine
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class
  allocated_storage = var.db_allocated_storage

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = var.backup_retention_period
  backup_window          = var.backup_window
  maintenance_window     = var.maintenance_window

  skip_final_snapshot = true

  tags = {{
    Name        = "${{var.project_name}}-db"
    Environment = var.environment
  }}
}}

resource "aws_db_subnet_group" "main" {{
  name       = "${{var.project_name}}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {{
    Name        = "${{var.project_name}}-db-subnet-group"
    Environment = var.environment
  }}
}}

# S3 Bucket for static assets
resource "aws_s3_bucket" "static" {{
  bucket = "${{var.project_name}}-static-${{random_string.bucket_suffix.result}}"

  tags = {{
    Name        = "${{var.project_name}}-static"
    Environment = var.environment
  }}
}}

resource "random_string" "bucket_suffix" {{
  length  = 8
  special = false
  upper   = false
}}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "app" {{
  name              = "/aws/ec2/${{var.project_name}}"
  retention_in_days = var.log_retention_days

  tags = {{
    Name        = "${{var.project_name}}-logs"
    Environment = var.environment
  }}
}}
'''.format(timestamp=datetime.now().isoformat())
        
        return content
    
    def _generate_variables_tf(self, requirements: Dict[str, Any]) -> str:
        """Generate variables.tf content"""
        return '''# Variable definitions

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "terraform-project"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
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

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Amazon Linux 2
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Number of EC2 instances"
  type        = number
  default     = 2
}

variable "db_engine" {
  description = "Database engine"
  type        = string
  default     = "mysql"
}

variable "db_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "8.0"
}

variable "db_instance_class" {
  description = "Database instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Database allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "appdb"
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

variable "backup_retention_period" {
  description = "Database backup retention period in days"
  type        = number
  default     = 7
}

variable "backup_window" {
  description = "Database backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "maintenance_window" {
  description = "Database maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}
'''
    
    def _generate_outputs_tf(self, design: Dict[str, Any]) -> str:
        """Generate outputs.tf content"""
        return '''# Output definitions

output "vpc_id" {
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

output "web_instance_ids" {
  description = "IDs of the web instances"
  value       = aws_instance.web[*].id
}

output "web_instance_public_ips" {
  description = "Public IP addresses of the web instances"
  value       = aws_instance.web[*].public_ip
}

output "load_balancer_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "load_balancer_zone_id" {
  description = "Zone ID of the load balancer"
  value       = aws_lb.main.zone_id
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
}

output "database_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.static.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.static.arn
}
'''
    
    def _extract_variables(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Extract variables from requirements"""
        return {
            'aws_region': requirements.get('region', 'us-east-1'),
            'project_name': f"infrastructure-{int(time.time())}",
            'environment': requirements.get('environment', 'production'),
            'instance_count': 2 if requirements.get('user_count', 0) > 100 else 1,
            'instance_type': 't3.small' if requirements.get('user_count', 0) > 1000 else 't3.micro'
        }
    
    def _extract_outputs(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """Extract outputs from design"""
        return {
            'vpc_id': 'aws_vpc.main.id',
            'load_balancer_dns_name': 'aws_lb.main.dns_name',
            'database_endpoint': 'aws_db_instance.main.endpoint'
        }
    
    def _save_project(self, project: TerraformProject):
        """Save project to workspace"""
        project_dir = os.path.join(self.workspaces_dir, project.name)
        os.makedirs(project_dir, exist_ok=True)
        
        for file in project.files:
            file_path = os.path.join(project_dir, file.filename)
            with open(file_path, 'w') as f:
                f.write(file.content)
        
        # Save project metadata
        metadata = {
            'name': project.name,
            'created_at': datetime.now().isoformat(),
            'variables': project.variables,
            'outputs': project.outputs,
            'provider': project.provider
        }
        
        metadata_path = os.path.join(project_dir, 'project.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _log_operation_start(self, operation_id: str, request: str, user_context: Optional[Dict[str, Any]] = None):
        """Log operation start"""
        operation_log = TerraformOperationLog(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            operation_type="infrastructure_generation",
            operation_id=operation_id,
            user_id=user_context.get('user_id') if user_context else None,
            input_data={'request': request, 'context': user_context},
            output_data={},
            success=False,  # Will be updated when operation completes
            error_message=None,
            execution_time=0.0,
            resource_changes=[],
            cost_impact=0.0,
            security_impact="low",
            performance_metrics={}
        )
        
        self.log_engine.log_operation(operation_log)
    
    def _log_operation_success(self, operation_id: str, operation_data: Dict[str, Any]):
        """Log successful operation"""
        # Update the operation log with success data
        logs = self.log_engine.get_operation_logs(limit=1)
        if logs:
            log = logs[0]
            log.success = True
            log.output_data = operation_data
            log.execution_time = operation_data.get('execution_time', 0.0)
            log.cost_impact = operation_data.get('cost_impact', 0.0)
            log.resource_changes = operation_data.get('resource_changes', [])
            
            self.log_engine.log_operation(log)
    
    def _log_operation_failure(self, operation_id: str, error_message: str):
        """Log operation failure"""
        # Update the operation log with failure data
        logs = self.log_engine.get_operation_logs(limit=1)
        if logs:
            log = logs[0]
            log.success = False
            log.error_message = error_message
            
            self.log_engine.log_operation(log)
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get learning summary from intelligence engine"""
        return self.intelligence_engine.get_learning_summary()
    
    def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """Get optimization suggestions"""
        suggestions = self.intelligence_engine.get_optimization_suggestions()
        return [asdict(suggestion) for suggestion in suggestions]
    
    def get_predictive_insights(self) -> List[Dict[str, Any]]:
        """Get predictive insights"""
        insights = self.intelligence_engine.get_predictive_insights()
        return [asdict(insight) for insight in insights]
    
    def get_operation_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get operation analytics"""
        return self.log_engine.analyze_operation_patterns(days)
    
    def predict_cost(self, requirements: Dict[str, Any]) -> float:
        """Predict cost for given requirements"""
        return self.intelligence_engine.predict_cost(requirements)
    
    def predict_performance(self, requirements: Dict[str, Any]) -> float:
        """Predict performance for given requirements"""
        return self.intelligence_engine.predict_performance(requirements)
    
    def detect_anomaly(self, requirements: Dict[str, Any]) -> bool:
        """Detect if requirements are anomalous"""
        return self.intelligence_engine.detect_anomaly(requirements)
    
    def analyze_existing_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze existing Terraform project"""
        return self.project_modifier.analyze_existing_project(project_path)
    
    def modify_existing_project(self, project_path: str, modification_request: str, precision_level: str = "medium") -> Dict[str, Any]:
        """Modify existing project with precision-based requests"""
        operation_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Log modification start
            self._log_operation_start(operation_id, f"Modify project: {modification_request}", {"project_path": project_path})
            
            # Analyze existing project
            project_analysis = self.project_modifier.analyze_existing_project(project_path)
            if "error" in project_analysis:
                return {"success": False, "error": project_analysis["error"]}
            
            # Apply modifications
            modification_result = self.project_modifier.modify_project(
                project_path, modification_request, precision_level
            )
            
            if "error" in modification_result:
                return {"success": False, "error": modification_result["error"]}
            
            # Apply the modifications to files
            apply_result = self.project_modifier.apply_modifications(project_path, modification_result)
            
            # Learn from this modification
            operation_data = {
                'operation_type': 'project_modification',
                'modification_type': modification_result.get('modification_type', 'unknown'),
                'changes_count': len(modification_result.get('changes', [])),
                'execution_time': time.time() - start_time,
                'success': apply_result.get('success', False),
                'cost_impact': 0.0,  # Modifications typically don't change cost immediately
                'resource_changes': modification_result.get('changes', [])
            }
            
            self.intelligence_engine.learn_from_operation(operation_data)
            
            # Log successful modification
            self._log_operation_success(operation_id, operation_data)
            
            return {
                "success": True,
                "message": f"Project modified successfully with {len(modification_result.get('changes', []))} changes",
                "modification_type": modification_result.get('modification_type'),
                "changes": modification_result.get('changes', []),
                "impact_assessment": modification_result.get('impact_assessment', {}),
                "rollback_plan": modification_result.get('rollback_plan', []),
                "operation_id": operation_id
            }
            
        except Exception as e:
            # Log modification failure
            self._log_operation_failure(operation_id, str(e))
            
            return {
                "success": False,
                "error": f"Failed to modify project: {str(e)}",
                "operation_id": operation_id
            }
    
    def get_project_recommendations(self, project_path: str) -> Dict[str, Any]:
        """Get intelligent recommendations for existing project"""
        try:
            # Analyze project
            analysis = self.project_modifier.analyze_existing_project(project_path)
            if "error" in analysis:
                return {"error": analysis["error"]}
            
            recommendations = {
                'scaling_recommendations': [],
                'security_recommendations': [],
                'cost_optimization': [],
                'performance_improvements': [],
                'compliance_suggestions': []
            }
            
            # Generate recommendations based on analysis
            complexity = analysis.get('complexity_score', 0)
            resource_count = len(analysis.get('resources', []))
            
            # Scaling recommendations
            if resource_count < 5:
                recommendations['scaling_recommendations'].append({
                    'type': 'add_auto_scaling',
                    'description': 'Add auto-scaling groups for better scalability',
                    'priority': 'medium'
                })
            
            # Security recommendations
            security_resources = [r for r in analysis.get('resources', []) if 'security' in r['type'].lower()]
            if len(security_resources) < 2:
                recommendations['security_recommendations'].append({
                    'type': 'add_encryption',
                    'description': 'Add encryption for data at rest and in transit',
                    'priority': 'high'
                })
            
            # Cost optimization
            ec2_resources = [r for r in analysis.get('resources', []) if r['type'] == 'aws_instance']
            if ec2_resources:
                recommendations['cost_optimization'].append({
                    'type': 'right_size_instances',
                    'description': 'Review and right-size EC2 instances for cost optimization',
                    'priority': 'medium'
                })
            
            # Performance improvements
            if not any(r['type'] == 'aws_lb' for r in analysis.get('resources', [])):
                recommendations['performance_improvements'].append({
                    'type': 'add_load_balancer',
                    'description': 'Add load balancer for better performance and availability',
                    'priority': 'high'
                })
            
            # Compliance suggestions
            if not any(r['type'] == 'aws_cloudtrail' for r in analysis.get('resources', [])):
                recommendations['compliance_suggestions'].append({
                    'type': 'add_audit_logging',
                    'description': 'Add CloudTrail for audit logging and compliance',
                    'priority': 'high'
                })
            
            return {
                'project_analysis': analysis,
                'recommendations': recommendations,
                'complexity_score': complexity,
                'modification_readiness': analysis.get('modification_readiness', 'unknown')
            }
            
        except Exception as e:
            return {"error": f"Failed to get project recommendations: {str(e)}"}
    
    def list_existing_projects(self) -> List[Dict[str, Any]]:
        """List all existing projects in workspaces"""
        try:
            projects = []
            
            for project_dir in self.workspaces_dir.iterdir():
                if project_dir.is_dir():
                    # Get basic project info
                    project_info = {
                        'name': project_dir.name,
                        'path': str(project_dir),
                        'created_at': datetime.fromtimestamp(project_dir.stat().st_ctime).isoformat(),
                        'modified_at': datetime.fromtimestamp(project_dir.stat().st_mtime).isoformat()
                    }
                    
                    # Check for project.json metadata
                    metadata_file = project_dir / 'project.json'
                    if metadata_file.exists():
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                                project_info.update(metadata)
                        except:
                            pass
                    
                    # Count Terraform files
                    tf_files = list(project_dir.glob('*.tf'))
                    project_info['terraform_files'] = len(tf_files)
                    
                    # Quick analysis
                    analysis = self.project_modifier.analyze_existing_project(str(project_dir))
                    if 'error' not in analysis:
                        project_info['resource_count'] = len(analysis.get('resources', []))
                        project_info['complexity_score'] = analysis.get('complexity_score', 0)
                        project_info['modification_readiness'] = analysis.get('modification_readiness', 'unknown')
                    
                    projects.append(project_info)
            
            return sorted(projects, key=lambda x: x['modified_at'], reverse=True)
            
        except Exception as e:
            return [{"error": f"Failed to list projects: {str(e)}"}]
