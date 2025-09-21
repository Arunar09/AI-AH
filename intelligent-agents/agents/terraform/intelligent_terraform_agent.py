"""
Intelligent Terraform Agent
Builds truly intelligent infrastructure as code solutions
"""

import os
import json
import uuid
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys
# Add the intelligent-agents directory to the path
intelligent_agents_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if intelligent_agents_dir not in sys.path:
    sys.path.insert(0, intelligent_agents_dir)

from core.reasoning.local_reasoning_engine import LocalReasoningEngine
from .terraform_agent_monitoring.enhanced_terraform_agent_monitor import EnhancedTerraformAgentMonitor
from .autonomous_operations.autonomous_terraform_agent import AutonomousTerraformAgent

# Local model integration removed - using enhanced built-in intelligence only
LOCAL_MODEL_AVAILABLE = False

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
    design_plan: Dict[str, Any] = None
    implementation_plan: Dict[str, Any] = None
    project_directory: str = None

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
        
        # Initialize enhanced monitoring system with operational intelligence
        self.monitor = EnhancedTerraformAgentMonitor()
        
        # Initialize autonomous operations system
        self.autonomous_agent = AutonomousTerraformAgent()
        
        # For web interface, use enhanced built-in logic for better performance
        # Local model can be slow and cause connection timeouts
        self.use_local_model = False
        print("🏗️ Intelligent Terraform Agent initialized with all 5 phases:")
        print("   ✅ Phase 1-3: Domain Knowledge, Enhanced Intelligence, Advanced Reasoning")
        print("   ✅ Phase 4: Operational Intelligence (Enhanced Monitoring)")
        print("   ✅ Phase 5: Autonomous Operations (Self-healing, Predictive Scaling)")
    
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
                },
                "ml_training_pipeline": {
                    "name": "ml_training_pipeline",
                    "description": "ML model training with SageMaker, EMR, and S3",
                    "components": ["sagemaker", "emr", "s3", "iam", "cloudwatch", "vpc"],
                    "cost_estimate": 1200,
                    "complexity": "very_high",
                    "scalability": "very_high",
                    "security": "high"
                },
                "ml_inference_pipeline": {
                    "name": "ml_inference_pipeline",
                    "description": "Real-time ML inference with Lambda, ECS, and API Gateway",
                    "components": ["lambda", "ecs", "api_gateway", "dynamodb", "cloudwatch"],
                    "cost_estimate": 400,
                    "complexity": "high",
                    "scalability": "very_high",
                    "security": "high"
                },
                "iot_platform": {
                    "name": "iot_platform",
                    "description": "IoT device management with AWS IoT Core and Kinesis",
                    "components": ["iot_core", "kinesis", "lambda", "dynamodb", "s3", "cloudwatch"],
                    "cost_estimate": 300,
                    "complexity": "high",
                    "scalability": "very_high",
                    "security": "high"
                },
                "enterprise_microservices": {
                    "name": "enterprise_microservices",
                    "description": "Enterprise microservices with EKS, service mesh, and monitoring",
                    "components": ["eks", "istio", "prometheus", "grafana", "jaeger", "vpc", "alb"],
                    "cost_estimate": 1500,
                    "complexity": "very_high",
                    "scalability": "very_high",
                    "security": "very_high"
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
        Process infrastructure request and generate Terraform solution with monitoring
        """
        # Generate unique action ID for monitoring
        action_id = str(uuid.uuid4())[:8]
        
        # Start monitoring this Terraform action
        monitoring_context = self.monitor.start_terraform_action_monitoring(
            action_id=action_id,
            action_type="terraform_generation",
            input_request=request
        )
        
        print(f"🏗️ Processing Terraform request: {request}")
        
        try:
            # Collect detailed requirements from user
            requirements = self._collect_project_requirements(request)
            
            # Use reasoning engine to analyze the request
            reasoning_result = self.reasoning_engine.reason_through_problem(request, {})
            
            # Generate architectural design and implementation plan
            design_plan = self._generate_architectural_design(reasoning_result, request)
            implementation_plan = self._generate_implementation_plan(design_plan, reasoning_result)
            
            # Generate Terraform code based on design plan
            terraform_project = self._generate_terraform_code(reasoning_result, request, design_plan)
            
            # Create implementation steps
            implementation_steps = self._generate_implementation_steps(terraform_project)
            
            # Calculate cost estimate
            cost_estimate = self._calculate_cost_estimate(terraform_project)
            
            # Validate the generated Terraform code
            try:
                terraform_files = self._format_terraform_files_with_requirements(terraform_project, requirements)
                domain = self._extract_domain_from_request(request)
                
                # Get terraform content for validation (combine all files)
                terraform_content = ""
                if terraform_files:
                    terraform_content = "\n\n".join(terraform_files.values())
            except Exception as e:
                print(f"Debug: Error in terraform validation - {e}")
                print(f"Debug: terraform_project type: {type(terraform_project)}")
                print(f"Debug: terraform_project attributes: {dir(terraform_project)}")
                terraform_content = ""
                domain = "unknown"
            
            validation_results = self.monitor.validate_terraform_code(
                terraform_content,
                domain
            )
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(terraform_project)
            
            # Complete Terraform monitoring
            self.monitor.complete_terraform_action_monitoring(
                action_id=action_id,
                success=True,
                confidence_score=reasoning_result.confidence,
                cost_estimate=cost_estimate,
                complexity_score=complexity_score,
                validation_results=validation_results,
                domain=domain,
                terraform_files_generated=len(terraform_files),
                implementation_steps=len(implementation_steps)
            )
            
            # Save Terraform files to disk
            project_directory = self._save_terraform_files(terraform_files, requirements['project_name'])
            
            return AgentResponse(
                content=reasoning_result.explanation,
                terraform_code=terraform_files,
                confidence=reasoning_result.confidence,
                reasoning_steps=reasoning_result.reasoning_steps,
                cost_estimate=cost_estimate,
                implementation_steps=implementation_steps,
                design_plan=design_plan,
                implementation_plan=implementation_plan,
                project_directory=project_directory
            )
            
        except Exception as e:
            # Complete Terraform monitoring with error
            self.monitor.complete_terraform_action_monitoring(
                action_id=action_id,
                success=False,
                confidence_score=0.0,
                cost_estimate=0.0,
                complexity_score=0,
                validation_results={"error": str(e)},
                domain="unknown",
                terraform_files_generated=0,
                implementation_steps=0,
                error_message=str(e)
            )
            raise e
    
    def _generate_architectural_design(self, reasoning_result, request: str) -> Dict[str, Any]:
        """Generate comprehensive architectural design plan"""
        print("🎨 Generating architectural design...")
        
        # Parse requirements from request
        requirements = self._parse_requirements_from_request(request)
        
        # Determine architecture pattern
        architecture_pattern = self._determine_architecture_pattern(requirements)
        
        # Design components
        components = self._design_components(requirements, architecture_pattern)
        
        # Design networking
        networking = self._design_networking(requirements)
        
        # Design security
        security = self._design_security(requirements)
        
        # Design monitoring
        monitoring = self._design_monitoring(requirements)
        
        design_plan = {
            "architecture_pattern": architecture_pattern,
            "components": components,
            "networking": networking,
            "security": security,
            "monitoring": monitoring,
            "scalability": self._design_scalability(requirements),
            "cost_optimization": self._design_cost_optimization(requirements),
            "compliance": self._design_compliance(requirements)
        }
        
        return design_plan
    
    def _generate_implementation_plan(self, design_plan: Dict[str, Any], reasoning_result) -> Dict[str, Any]:
        """Generate detailed implementation plan"""
        print("📋 Generating implementation plan...")
        
        implementation_plan = {
            "phases": [
                {
                    "phase": "Phase 1: Foundation Setup",
                    "description": "Set up core infrastructure foundation",
                    "duration": "15-30 minutes",
                    "steps": [
                        "Configure AWS provider and authentication",
                        "Create VPC and networking components",
                        "Set up security groups and NACLs",
                        "Configure IAM roles and policies"
                    ],
                    "dependencies": [],
                    "risk_level": "Low"
                },
                {
                    "phase": "Phase 2: Core Infrastructure",
                    "description": "Deploy core compute and storage resources",
                    "duration": "20-40 minutes",
                    "steps": [
                        "Launch EC2 instances or containers",
                        "Configure load balancers",
                        "Set up database instances",
                        "Configure storage and backups"
                    ],
                    "dependencies": ["Phase 1"],
                    "risk_level": "Medium"
                },
                {
                    "phase": "Phase 3: Application Deployment",
                    "description": "Deploy and configure applications",
                    "duration": "15-30 minutes",
                    "steps": [
                        "Deploy application code",
                        "Configure environment variables",
                        "Set up database connections",
                        "Test application functionality"
                    ],
                    "dependencies": ["Phase 2"],
                    "risk_level": "Medium"
                },
                {
                    "phase": "Phase 4: Monitoring & Security",
                    "description": "Configure monitoring, logging, and security",
                    "duration": "10-20 minutes",
                    "steps": [
                        "Set up CloudWatch monitoring",
                        "Configure log aggregation",
                        "Enable security scanning",
                        "Set up alerting and notifications"
                    ],
                    "dependencies": ["Phase 3"],
                    "risk_level": "Low"
                }
            ],
            "rollback_strategy": {
                "automatic_rollback": True,
                "rollback_triggers": [
                    "Health check failures",
                    "High error rates",
                    "Resource creation failures"
                ],
                "rollback_steps": [
                    "Stop new deployments",
                    "Restore previous version",
                    "Verify system health",
                    "Investigate and fix issues"
                ]
            },
            "testing_strategy": {
                "unit_tests": "Test individual components",
                "integration_tests": "Test component interactions",
                "load_tests": "Test performance under load",
                "security_tests": "Test security configurations"
            },
            "success_criteria": [
                "All resources deployed successfully",
                "Application responds to health checks",
                "Monitoring and alerting functional",
                "Security configurations validated",
                "Performance meets requirements"
            ]
        }
        
        return implementation_plan
    
    def _parse_requirements_from_request(self, request: str) -> Dict[str, Any]:
        """Parse requirements from request text"""
        requirements = {}
        lines = request.split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                requirements[key] = value
        
        return requirements
    
    def _determine_architecture_pattern(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the best architecture pattern based on requirements"""
        user_load = int(requirements.get('user_load', '1000'))
        budget = int(requirements.get('budget', '100'))
        security = requirements.get('security', 'basic')
        
        if user_load < 1000 and budget < 200:
            pattern = "Simple Web Application"
            description = "Single-tier architecture with web server and database"
        elif user_load < 10000 and budget < 500:
            pattern = "Load Balanced Web Application"
            description = "Multi-tier architecture with load balancer, web servers, and database"
        else:
            pattern = "Microservices Architecture"
            description = "Distributed architecture with multiple services, API gateway, and container orchestration"
        
        return {
            "pattern": pattern,
            "description": description,
            "rationale": f"Selected based on user load ({user_load}), budget (${budget}), and security requirements ({security})"
        }
    
    def _design_components(self, requirements: Dict[str, Any], architecture_pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Design system components based on requirements"""
        components = {
            "compute": {
                "web_servers": {
                    "type": "EC2 instances",
                    "count": 2 if int(requirements.get('user_load', '1000')) > 1000 else 1,
                    "instance_type": "t3.micro" if int(requirements.get('budget', '100')) < 200 else "t3.small",
                    "purpose": "Host web application"
                }
            },
            "storage": {
                "database": {
                    "type": "RDS PostgreSQL",
                    "instance_class": "db.t3.micro",
                    "purpose": "Store application data"
                },
                "file_storage": {
                    "type": "S3 bucket",
                    "purpose": "Store static files and backups"
                }
            },
            "networking": {
                "load_balancer": {
                    "type": "Application Load Balancer",
                    "purpose": "Distribute traffic across web servers"
                },
                "cdn": {
                    "type": "CloudFront",
                    "purpose": "Cache static content globally"
                }
            }
        }
        
        return components
    
    def _design_networking(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design networking architecture"""
        return {
            "vpc": {
                "cidr": "10.0.0.0/16",
                "description": "Main VPC for the application"
            },
            "subnets": {
                "public": {
                    "cidr": "10.0.1.0/24",
                    "availability_zone": "us-east-1a",
                    "purpose": "Load balancer and NAT gateway"
                },
                "private": {
                    "cidr": "10.0.2.0/24",
                    "availability_zone": "us-east-1a",
                    "purpose": "Web servers and database"
                }
            },
            "security_groups": {
                "web_sg": {
                    "inbound": ["HTTP (80)", "HTTPS (443)", "SSH (22)"],
                    "outbound": ["All traffic"]
                },
                "db_sg": {
                    "inbound": ["PostgreSQL (5432) from web servers"],
                    "outbound": ["All traffic"]
                }
            }
        }
    
    def _design_security(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design security architecture"""
        security_level = requirements.get('security', 'basic')
        
        security_design = {
            "network_security": {
                "vpc_endpoints": "Enable for AWS services",
                "security_groups": "Restrictive inbound/outbound rules",
                "nacls": "Additional network-level security"
            },
            "access_control": {
                "iam_roles": "Least privilege access",
                "mfa": "Multi-factor authentication enabled",
                "key_rotation": "Regular key rotation policy"
            }
        }
        
        if security_level == 'high':
            security_design.update({
                "encryption": {
                    "at_rest": "AES-256 encryption for all storage",
                    "in_transit": "TLS 1.2+ for all communications"
                },
                "monitoring": {
                    "cloudtrail": "API call logging",
                    "config": "Resource configuration monitoring",
                    "guardduty": "Threat detection"
                }
            })
        
        return security_design
    
    def _design_monitoring(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design monitoring and observability"""
        return {
            "metrics": {
                "cloudwatch": "System and application metrics",
                "custom_metrics": "Business-specific metrics"
            },
            "logging": {
                "cloudwatch_logs": "Centralized log aggregation",
                "log_groups": ["/aws/ec2/web", "/aws/rds/database"]
            },
            "alerting": {
                "sns": "Email and SMS notifications",
                "alarms": ["High CPU", "High memory", "Database connections"]
            },
            "dashboards": {
                "grafana": "Custom monitoring dashboards",
                "cloudwatch": "AWS native dashboards"
            }
        }
    
    def _design_scalability(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design scalability strategy"""
        return {
            "horizontal_scaling": {
                "auto_scaling_groups": "Automatically scale web servers based on demand",
                "target_tracking": "CPU and memory-based scaling policies"
            },
            "vertical_scaling": {
                "instance_types": "Upgrade instance types as needed",
                "database_scaling": "RDS read replicas for read scaling"
            },
            "caching": {
                "elasticache": "Redis for session and data caching",
                "cloudfront": "CDN for static content caching"
            }
        }
    
    def _design_cost_optimization(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design cost optimization strategy"""
        return {
            "compute_optimization": {
                "spot_instances": "Use spot instances for non-critical workloads",
                "reserved_instances": "Reserve instances for predictable workloads",
                "right_sizing": "Regular instance size optimization"
            },
            "storage_optimization": {
                "s3_lifecycle": "Automated data lifecycle management",
                "ebs_optimization": "Use appropriate EBS volume types"
            },
            "monitoring": {
                "cost_explorer": "Regular cost analysis and optimization",
                "budget_alerts": "Set up budget alerts and notifications"
            }
        }
    
    def _design_compliance(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design compliance and governance"""
        return {
            "data_protection": {
                "encryption": "Encrypt data at rest and in transit",
                "backup": "Regular automated backups",
                "retention": "Data retention policies"
            },
            "audit": {
                "cloudtrail": "API call auditing",
                "config": "Resource configuration compliance",
                "access_logs": "User access logging"
            },
            "governance": {
                "tagging": "Consistent resource tagging",
                "policies": "IAM policies for access control",
                "standards": "AWS Well-Architected Framework compliance"
            }
        }

    def _generate_terraform_code(self, reasoning_result, request: str, design_plan: Dict[str, Any] = None) -> TerraformProject:
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
        """Select appropriate infrastructure pattern with intelligent domain recognition"""
        patterns = self.knowledge_base.get(f"{provider}_patterns", {})
        solution_name = reasoning_result.decision.solution.name.lower()
        
        # Intelligent domain recognition
        if any(keyword in solution_name for keyword in ["machine learning", "ml", "ai", "training", "inference"]):
            if "training" in solution_name or "model" in solution_name:
                pattern = patterns.get("ml_training_pipeline", patterns.get("data_analytics", {}))
            else:
                pattern = patterns.get("ml_inference_pipeline", patterns.get("serverless_api", {}))
        elif any(keyword in solution_name for keyword in ["iot", "device", "sensor", "telemetry"]):
            pattern = patterns.get("iot_platform", patterns.get("serverless_api", {}))
        elif any(keyword in solution_name for keyword in ["enterprise", "microservices", "distributed"]):
            pattern = patterns.get("enterprise_microservices", patterns.get("microservices", {}))
        elif any(keyword in solution_name for keyword in ["data", "analytics", "processing", "pipeline"]):
            pattern = patterns.get("data_analytics", patterns.get("web_app_scalable", {}))
        elif "serverless" in solution_name:
            pattern = patterns.get("serverless_api", patterns.get("web_app_basic", {}))
        elif "scalable" in solution_name or "load balanced" in solution_name:
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
        """Generate AWS main.tf using built-in intelligence"""
        # This method is kept for compatibility but always uses fallback
        return self._generate_aws_main_tf_fallback(pattern)
    
    def _generate_aws_main_tf_fallback(self, pattern: Dict[str, Any]) -> str:
        """Generate domain-specific AWS main.tf based on pattern"""
        pattern_name = pattern.get("name", "web_app_basic").lower()
        
        if "ml" in pattern_name or "machine learning" in pattern_name:
            return self._generate_ml_infrastructure(pattern)
        elif "iot" in pattern_name:
            return self._generate_iot_infrastructure(pattern)
        elif "data" in pattern_name or "analytics" in pattern_name:
            return self._generate_data_analytics_infrastructure(pattern)
        elif "enterprise" in pattern_name or "microservices" in pattern_name:
            return self._generate_enterprise_infrastructure(pattern)
        elif "serverless" in pattern_name:
            return self._generate_serverless_infrastructure(pattern)
        else:
            return self._generate_basic_web_infrastructure(pattern)
    
    def _generate_basic_web_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate basic web infrastructure"""
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
    
    def _generate_ml_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate ML-specific infrastructure with SageMaker, EMR, and S3"""
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

# VPC for ML workloads
resource "aws_vpc" "ml_vpc" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name = "${{var.project_name}}-ml-vpc"
    Environment = var.environment
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "ml_igw" {{
  vpc_id = aws_vpc.ml_vpc.id
  tags = {{
    Name = "${{var.project_name}}-ml-igw"
  }}
}}

# Public Subnets for SageMaker
resource "aws_subnet" "ml_public" {{
  count = 2
  vpc_id                  = aws_vpc.ml_vpc.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {{
    Name = "${{var.project_name}}-ml-public-${{count.index + 1}}"
  }}
}}

# Private Subnets for EMR
resource "aws_subnet" "ml_private" {{
  count = 2
  vpc_id            = aws_vpc.ml_vpc.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {{
    Name = "${{var.project_name}}-ml-private-${{count.index + 1}}"
  }}
}}

# S3 Bucket for ML Data
resource "aws_s3_bucket" "ml_data" {{
  bucket = "${{var.project_name}}-ml-data-${{random_id.bucket_suffix.hex}}"

  tags = {{
    Name = "${{var.project_name}}-ml-data"
    Environment = var.environment
  }}
}}

resource "random_id" "bucket_suffix" {{
  byte_length = 4
}}

# SageMaker Domain
resource "aws_sagemaker_domain" "ml_domain" {{
  domain_name = "${{var.project_name}}-ml-domain"
  auth_mode   = "IAM"
  vpc_id      = aws_vpc.ml_vpc.id
  subnet_ids  = aws_subnet.ml_private[*].id

  default_user_settings {{
    execution_role = aws_iam_role.sagemaker_execution_role.arn
  }}

  tags = {{
    Name = "${{var.project_name}}-ml-domain"
  }}
}}

# EMR Cluster for Data Processing
resource "aws_emr_cluster" "ml_processing" {{
  name          = "${{var.project_name}}-ml-emr"
  release_label = "emr-6.15.0"
  applications  = ["Spark", "Hadoop"]

  ec2_attributes {{
    subnet_id                         = aws_subnet.ml_private[0].id
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr_profile.arn
  }}

  master_instance_group {{
    instance_type = var.emr_master_instance_type
    instance_count = 1
  }}

  core_instance_group {{
    instance_type  = var.emr_core_instance_type
    instance_count = var.emr_core_instance_count
  }}

  tags = {{
    Name = "${{var.project_name}}-ml-emr"
  }}
}}

# Security Groups
resource "aws_security_group" "sagemaker_sg" {{
  name_prefix = "${{var.project_name}}-sagemaker-"
  vpc_id      = aws_vpc.ml_vpc.id

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name = "${{var.project_name}}-sagemaker-sg"
  }}
}}

resource "aws_security_group" "emr_master" {{
  name_prefix = "${{var.project_name}}-emr-master-"
  vpc_id      = aws_vpc.ml_vpc.id

  ingress {{
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name = "${{var.project_name}}-emr-master-sg"
  }}
}}

resource "aws_security_group" "emr_slave" {{
  name_prefix = "${{var.project_name}}-emr-slave-"
  vpc_id      = aws_vpc.ml_vpc.id

  ingress {{
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    self      = true
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}

  tags = {{
    Name = "${{var.project_name}}-emr-slave-sg"
  }}
}}

# IAM Roles
resource "aws_iam_role" "sagemaker_execution_role" {{
  name = "${{var.project_name}}-sagemaker-execution-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "sagemaker.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "sagemaker_full_access" {{
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}}

resource "aws_iam_role" "emr_service_role" {{
  name = "${{var.project_name}}-emr-service-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "elasticmapreduce.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "emr_service_policy" {{
  role       = aws_iam_role.emr_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEMRServicePolicy_v2"
}}

resource "aws_iam_instance_profile" "emr_profile" {{
  name = "${{var.project_name}}-emr-profile"
  role = aws_iam_role.emr_ec2_role.name
}}

resource "aws_iam_role" "emr_ec2_role" {{
  name = "${{var.project_name}}-emr-ec2-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "ec2.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "emr_ec2_policy" {{
  role       = aws_iam_role.emr_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEMRforEC2Role"
}}'''
    
    def _generate_iot_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate IoT-specific infrastructure with IoT Core, Kinesis, and Lambda"""
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

# IoT Core Policy
resource "aws_iot_policy" "device_policy" {{
  name = "${{var.project_name}}-device-policy"

  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Effect = "Allow"
        Action = [
          "iot:Connect",
          "iot:Publish",
          "iot:Subscribe",
          "iot:Receive"
        ]
        Resource = "*"
      }}
    ]
  }})
}}

# IoT Thing Type
resource "aws_iot_thing_type" "sensor" {{
  name = "${{var.project_name}}-sensor"
}}

# Kinesis Data Stream
resource "aws_kinesis_stream" "iot_data" {{
  name             = "${{var.project_name}}-iot-data"
  shard_count      = var.kinesis_shard_count
  retention_period = 24

  tags = {{
    Name = "${{var.project_name}}-iot-data-stream"
  }}
}}

# DynamoDB Table for Device State
resource "aws_dynamodb_table" "device_state" {{
  name           = "${{var.project_name}}-device-state"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "device_id"

  attribute {{
    name = "device_id"
    type = "S"
  }}

  tags = {{
    Name = "${{var.project_name}}-device-state"
  }}
}}

# Lambda Function for Data Processing
resource "aws_lambda_function" "iot_processor" {{
  filename         = "iot_processor.zip"
  function_name    = "${{var.project_name}}-iot-processor"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 30

  environment {{
    variables = {{
      DYNAMODB_TABLE = aws_dynamodb_table.device_state.name
    }}
  }}
}}

# IoT Rule for Data Routing
resource "aws_iot_topic_rule" "data_rule" {{
  name        = "${{var.project_name}}-data-rule"
  description = "Route IoT data to Kinesis"

  sql          = "SELECT * FROM 'device/+/data'"
  sql_version  = "2016-03-23"

  kinesis {{
    role_arn    = aws_iam_role.iot_kinesis_role.arn
    stream_name = aws_kinesis_stream.iot_data.name
  }}
}}

# IAM Roles
resource "aws_iam_role" "lambda_role" {{
  name = "${{var.project_name}}-lambda-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "lambda.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "lambda_basic" {{
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}}

resource "aws_iam_role_policy" "lambda_dynamodb" {{
  name = "${{var.project_name}}-lambda-dynamodb"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.device_state.arn
      }}
    ]
  }})
}}

resource "aws_iam_role" "iot_kinesis_role" {{
  name = "${{var.project_name}}-iot-kinesis-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "iot.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy" "iot_kinesis_policy" {{
  name = "${{var.project_name}}-iot-kinesis-policy"
  role = aws_iam_role.iot_kinesis_role.id

  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Effect = "Allow"
        Action = [
          "kinesis:PutRecord"
        ]
        Resource = aws_kinesis_stream.iot_data.arn
      }}
    ]
  }})
}}'''
    
    def _generate_data_analytics_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate data analytics infrastructure"""
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

# S3 Data Lake
resource "aws_s3_bucket" "data_lake" {{
  bucket = "${{var.project_name}}-data-lake-${{random_id.bucket_suffix.hex}}"

  tags = {{
    Name = "${{var.project_name}}-data-lake"
  }}
}}

resource "random_id" "bucket_suffix" {{
  byte_length = 4
}}

# Redshift Cluster
resource "aws_redshift_cluster" "analytics" {{
  cluster_identifier = "${{var.project_name}}-analytics"
  database_name      = var.redshift_database_name
  master_username    = var.redshift_master_username
  master_password    = var.redshift_master_password
  node_type          = var.redshift_node_type
  cluster_type       = "single-node"

  tags = {{
    Name = "${{var.project_name}}-analytics"
  }}
}}

# EMR Cluster for Data Processing
resource "aws_emr_cluster" "data_processing" {{
  name          = "${{var.project_name}}-data-processing"
  release_label = "emr-6.15.0"
  applications  = ["Spark", "Hadoop", "Hive"]

  ec2_attributes {{
    instance_profile = aws_iam_instance_profile.emr_profile.arn
  }}

  master_instance_group {{
    instance_type = var.emr_master_instance_type
    instance_count = 1
  }}

  core_instance_group {{
    instance_type  = var.emr_core_instance_type
    instance_count = var.emr_core_instance_count
  }}

  tags = {{
    Name = "${{var.project_name}}-data-processing"
  }}
}}

# Glue Crawler
resource "aws_glue_crawler" "data_crawler" {{
  database_name = aws_glue_catalog_database.analytics.name
  name          = "${{var.project_name}}-data-crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {{
    path = "s3://${{aws_s3_bucket.data_lake.bucket}}/raw/"
  }}
}}

# Glue Catalog Database
resource "aws_glue_catalog_database" "analytics" {{
  name = "${{var.project_name}}-analytics-db"
}}

# Athena Workgroup
resource "aws_athena_workgroup" "analytics" {{
  name = "${{var.project_name}}-analytics"

  configuration {{
    result_configuration {{
      output_location = "s3://${{aws_s3_bucket.data_lake.bucket}}/athena-results/"
    }}
  }}
}}

# IAM Roles
resource "aws_iam_role" "glue_role" {{
  name = "${{var.project_name}}-glue-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "glue.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "glue_service_role" {{
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}}'''
    
    def _generate_enterprise_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate enterprise infrastructure with EKS, RDS, and monitoring"""
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

# VPC for Enterprise
resource "aws_vpc" "enterprise_vpc" {{
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {{
    Name = "${{var.project_name}}-enterprise-vpc"
  }}
}}

# EKS Cluster
resource "aws_eks_cluster" "enterprise" {{
  name     = "${{var.project_name}}-enterprise"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {{
    subnet_ids = aws_subnet.enterprise_private[*].id
  }}

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
  ]}}

# EKS Node Group
resource "aws_eks_node_group" "enterprise" {{
  cluster_name    = aws_eks_cluster.enterprise.name
  node_group_name = "${{var.project_name}}-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.enterprise_private[*].id

  scaling_config {{
    desired_size = var.eks_desired_size
    max_size     = var.eks_max_size
    min_size     = var.eks_min_size
  }}

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
  ]}}

# RDS Cluster
resource "aws_rds_cluster" "enterprise" {{
  cluster_identifier      = "${{var.project_name}}-enterprise-db"
  engine                   = "aurora-mysql"
  engine_version           = "8.0.mysql_aurora.3.02.0"
  database_name            = var.database_name
  master_username          = var.database_username
  master_password          = var.database_password
  backup_retention_period  = 7
  preferred_backup_window  = "07:00-09:00"
  skip_final_snapshot      = true

  tags = {{
    Name = "${{var.project_name}}-enterprise-db"
  }}
}}

# IAM Roles for EKS
resource "aws_iam_role" "eks_cluster_role" {{
  name = "${{var.project_name}}-eks-cluster-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "eks.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}}

resource "aws_iam_role" "eks_node_role" {{
  name = "${{var.project_name}}-eks-node-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "ec2.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {{
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}}'''
    
    def _generate_serverless_infrastructure(self, pattern: Dict[str, Any]) -> str:
        """Generate serverless infrastructure with Lambda, API Gateway, and DynamoDB"""
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

# API Gateway
resource "aws_api_gateway_rest_api" "serverless_api" {{
  name        = "${{var.project_name}}-api"
  description = "Serverless API for ${{var.project_name}}"
}}

# Lambda Function
resource "aws_lambda_function" "api_handler" {{
  filename         = "api_handler.zip"
  function_name    = "${{var.project_name}}-api-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 30

  environment {{
    variables = {{
      DYNAMODB_TABLE = aws_dynamodb_table.serverless_data.name
    }}
  }}
}}

# DynamoDB Table
resource "aws_dynamodb_table" "serverless_data" {{
  name           = "${{var.project_name}}-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {{
    name = "id"
    type = "S"
  }}

  tags = {{
    Name = "${{var.project_name}}-data"
  }}
}}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {{
  name = "${{var.project_name}}-lambda-role"

  assume_role_policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {{
          Service = "lambda.amazonaws.com"
        }}
      }}
    ]
  }})
}}

resource "aws_iam_role_policy_attachment" "lambda_basic" {{
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}}'''
    
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
    
    def _format_terraform_files_with_requirements(self, project: TerraformProject, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Format Terraform files with collected requirements"""
        try:
            files = {}
            
            # Main configuration file (use existing logic)
            if project.files:
                for file in project.files:
                    files[file.filename] = file.content
            else:
                # Use domain-specific generation with requirements
                files["main.tf"] = self._generate_aws_main_tf_fallback({
                    "name": requirements.get('project_name', 'web_app'),
                    "description": f"Infrastructure for {requirements.get('project_name', 'web_app')}"
                })
            
            # Variables file with collected requirements
            files["variables.tf"] = f'''# Input Variables
# Generated by Intelligent Terraform Agent

variable "project_name" {{
  description = "Name of the project"
  type        = string
  default     = "{requirements.get('project_name', 'my-web-app')}"
}}

variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "{requirements.get('aws_region', 'us-east-1')}"
}}

variable "environment" {{
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "{requirements.get('environment', 'dev')}"
}}

variable "vpc_cidr" {{
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}}

variable "public_subnet_cidr" {{
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}}

variable "availability_zone" {{
  description = "Availability zone"
  type        = string
  default     = "{requirements.get('aws_region', 'us-east-1')}a"
}}

variable "ami_id" {{
  description = "AMI ID for EC2 instance"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Amazon Linux 2
}}

variable "instance_type" {{
  description = "EC2 instance type"
  type        = string
  default     = "{requirements.get('instance_type', 't3.micro')}"
}}

variable "key_name" {{
  description = "Name of the AWS key pair"
  type        = string
  default     = "{requirements.get('key_name', 'default-key')}"
}}

variable "db_instance_class" {{
  description = "RDS instance class"
  type        = string
  default     = "{requirements.get('db_class', 'db.t3.micro')}"
}}

variable "db_name" {{
  description = "Name of the database"
  type        = string
  default     = "{requirements.get('db_name', 'app_db')}"
}}

variable "db_username" {{
  description = "Database username"
  type        = string
  default     = "{requirements.get('db_username', 'admin')}"
}}

variable "db_password" {{
  description = "Database password"
  type        = string
  sensitive   = true
  default     = "{requirements.get('db_password', 'changeme123')}"
}}

variable "high_availability" {{
  description = "Enable high availability"
  type        = bool
  default     = {str(requirements.get('high_availability', False)).lower()}
}}

variable "monitoring" {{
  description = "Enable monitoring and logging"
  type        = bool
  default     = {str(requirements.get('monitoring', True)).lower()}
}}

variable "backup" {{
  description = "Enable automated backups"
  type        = bool
  default     = {str(requirements.get('backup', True)).lower()}
}}'''
            
            # Outputs file
            files["outputs.tf"] = '''# Output Values
# Generated by Intelligent Terraform Agent

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.web.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.web.public_dns
}

output "project_name" {
  description = "Name of the project"
  value       = var.project_name
}

output "environment" {
  description = "Environment"
  value       = var.environment
}'''
            
            # Terraform.tfvars file with collected requirements
            files["terraform.tfvars"] = f'''# Variable Values
# Generated by Intelligent Terraform Agent

project_name = "{requirements.get('project_name', 'my-web-app')}"
aws_region = "{requirements.get('aws_region', 'us-east-1')}"
environment = "{requirements.get('environment', 'dev')}"
vpc_cidr = "10.0.0.0/16"
public_subnet_cidr = "10.0.1.0/24"
availability_zone = "{requirements.get('aws_region', 'us-east-1')}a"
ami_id = "ami-0c02fb55956c7d316"
instance_type = "{requirements.get('instance_type', 't3.micro')}"
key_name = "{requirements.get('key_name', 'default-key')}"
db_instance_class = "{requirements.get('db_class', 'db.t3.micro')}"
db_name = "{requirements.get('db_name', 'app_db')}"
db_username = "{requirements.get('db_username', 'admin')}"
db_password = "{requirements.get('db_password', 'changeme123')}"
high_availability = {str(requirements.get('high_availability', False)).lower()}
monitoring = {str(requirements.get('monitoring', True)).lower()}
backup = {str(requirements.get('backup', True)).lower()}'''
            
            return files
            
        except Exception as e:
            print(f"Debug: Error formatting terraform files with requirements - {e}")
            return {"main.tf": "# Error generating Terraform files"}
    
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
    
    def _extract_domain_from_request(self, request: str) -> str:
        """Extract domain from request for monitoring"""
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ["machine learning", "ml", "ai", "training", "inference"]):
            return "ml"
        elif any(keyword in request_lower for keyword in ["iot", "device", "sensor", "telemetry"]):
            return "iot"
        elif any(keyword in request_lower for keyword in ["data", "analytics", "processing", "pipeline"]):
            return "analytics"
        elif any(keyword in request_lower for keyword in ["enterprise", "microservices", "distributed"]):
            return "enterprise"
        else:
            return "web"
    
    def _calculate_complexity_score(self, terraform_project) -> int:
        """Calculate complexity score for monitoring"""
        score = 0
        
        # Handle TerraformProject object
        if hasattr(terraform_project, 'files'):
            # Count resources, modules, and data sources from TerraformProject
            for file in terraform_project.files:
                if hasattr(file, 'content'):
                    content = file.content
                    score += content.count('resource "')
                    score += content.count('module "')
                    score += content.count('data "')
                    
                    # Complexity based on services used
                    services = ['aws_ecs', 'aws_eks', 'aws_emr', 'aws_sagemaker', 'aws_iot']
                    for service in services:
                        if service in content:
                            score += 2
        else:
            # Handle dictionary format (fallback)
            for file_content in terraform_project.values():
                if isinstance(file_content, str):
                    score += file_content.count('resource "')
                    score += file_content.count('module "')
                    score += file_content.count('data "')
                    
                    # Complexity based on services used
                    services = ['aws_ecs', 'aws_eks', 'aws_emr', 'aws_sagemaker', 'aws_iot']
                    for service in services:
                        if service in file_content:
                            score += 2
        
        return min(score, 10)  # Cap at 10 for simplicity
    
    def _collect_project_requirements(self, request: str) -> Dict[str, Any]:
        """Intelligently analyze request and collect requirements with smart suggestions"""
        print("\n🧠 **INTELLIGENT REQUIREMENT ANALYSIS**")
        print("=" * 60)
        
        # Analyze the request to understand the scenario
        scenario = self._analyze_request_scenario(request)
        requirements = self._extract_requirements_from_request(request)
        
        print(f"🎯 **Detected Scenario**: {scenario['type']}")
        print(f"📋 **Initial Analysis**: {scenario['description']}")
        
        # For automated testing, use intelligent defaults instead of interactive input
        if scenario['type'] == 'new_infrastructure':
            requirements = self._collect_new_infrastructure_requirements_automated(request, requirements)
        elif scenario['type'] == 'modify_existing':
            requirements = self._collect_modification_requirements_automated(request, requirements)
        elif scenario['type'] == 'add_components':
            requirements = self._collect_addition_requirements_automated(request, requirements)
        elif scenario['type'] == 'optimize_existing':
            requirements = self._collect_optimization_requirements_automated(request, requirements)
        else:
            requirements = self._collect_general_requirements(request, requirements)
        
        # Validate and suggest improvements
        requirements = self._validate_and_suggest_improvements(requirements, scenario)
        
        print("\n✅ **Intelligent Requirements Analysis Complete!**")
        print(f"📋 **Final Requirements**: {self._format_requirements_summary(requirements)}")
        print("=" * 60)
        
        return requirements
    
    def _analyze_request_scenario(self, request: str) -> Dict[str, Any]:
        """Analyze the request to understand what type of scenario this is"""
        request_lower = request.lower()
        
        # New infrastructure indicators
        new_indicators = ['create', 'build', 'deploy', 'set up', 'new', 'fresh', 'from scratch']
        # Modification indicators  
        modify_indicators = ['modify', 'update', 'change', 'edit', 'alter', 'adjust']
        # Addition indicators
        add_indicators = ['add', 'include', 'extend', 'expand', 'integrate', 'connect']
        # Optimization indicators
        optimize_indicators = ['optimize', 'improve', 'enhance', 'tune', 'scale', 'performance']
        
        if any(indicator in request_lower for indicator in new_indicators):
            return {
                'type': 'new_infrastructure',
                'description': 'Creating new infrastructure from scratch',
                'confidence': 0.9
            }
        elif any(indicator in request_lower for indicator in modify_indicators):
            return {
                'type': 'modify_existing', 
                'description': 'Modifying existing infrastructure',
                'confidence': 0.8
            }
        elif any(indicator in request_lower for indicator in add_indicators):
            return {
                'type': 'add_components',
                'description': 'Adding components to existing infrastructure', 
                'confidence': 0.8
            }
        elif any(indicator in request_lower for indicator in optimize_indicators):
            return {
                'type': 'optimize_existing',
                'description': 'Optimizing existing infrastructure',
                'confidence': 0.7
            }
        else:
            return {
                'type': 'general',
                'description': 'General infrastructure request',
                'confidence': 0.5
            }
    
    def _extract_requirements_from_request(self, request: str) -> Dict[str, Any]:
        """Extract requirements that are already mentioned in the request"""
        requirements = {}
        request_lower = request.lower()
        
        # Extract budget information
        import re
        budget_match = re.search(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:per\s*month|/month|monthly)', request_lower)
        if budget_match:
            requirements['budget'] = float(budget_match.group(1).replace(',', ''))
        
        # Extract scale information
        scale_indicators = {
            'small': {'instance_type': 't3.micro', 'db_class': 'db.t3.micro'},
            'medium': {'instance_type': 't3.small', 'db_class': 'db.t3.small'}, 
            'large': {'instance_type': 't3.medium', 'db_class': 'db.t3.medium'},
            'enterprise': {'instance_type': 't3.large', 'db_class': 'db.t3.large'}
        }
        
        for scale, config in scale_indicators.items():
            if scale in request_lower:
                requirements.update(config)
                break
        
        # Extract domain information
        if 'ml' in request_lower or 'machine learning' in request_lower:
            requirements['domain'] = 'ml'
        elif 'iot' in request_lower or 'internet of things' in request_lower:
            requirements['domain'] = 'iot'
        elif 'data' in request_lower or 'analytics' in request_lower:
            requirements['domain'] = 'data'
        elif 'enterprise' in request_lower or 'microservices' in request_lower:
            requirements['domain'] = 'enterprise'
        elif 'serverless' in request_lower:
            requirements['domain'] = 'serverless'
        else:
            requirements['domain'] = 'web'
        
        # Extract availability requirements
        if 'high availability' in request_lower or 'ha' in request_lower:
            requirements['high_availability'] = True
        if '99.9' in request_lower or '99.99' in request_lower:
            requirements['high_availability'] = True
        
        # Extract security requirements
        if 'security' in request_lower or 'secure' in request_lower:
            requirements['security_focus'] = True
        
        return requirements
    
    def _collect_new_infrastructure_requirements_automated(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Automated version of new infrastructure requirements collection"""
        # Use intelligent defaults based on request analysis
        requirements.update({
            'project_name': self._suggest_project_name(request),
            'aws_region': 'us-east-1',  # Default region
            'environment': 'dev',  # Default environment
            'instance_type': 't3.micro',  # Default instance type
            'db_name': 'maindb',
            'db_username': 'admin',
            'db_password': 'SecurePass123!',
            'key_name': 'terraform-key',
            'high_availability': False,
            'monitoring': True,
            'backup': True
        })
        return requirements
    
    def _collect_modification_requirements_automated(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Automated version of modification requirements collection"""
        requirements.update({
            'existing_project': 'existing-project',
            'modification_type': '1',  # Scaling
            'current_size': 't3.micro',
            'new_size': 't3.small'
        })
        return requirements
    
    def _collect_addition_requirements_automated(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Automated version of addition requirements collection"""
        requirements.update({
            'existing_project': 'existing-project',
            'addition_type': '1'  # Database
        })
        return requirements
    
    def _collect_optimization_requirements_automated(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Automated version of optimization requirements collection"""
        requirements.update({
            'existing_project': 'existing-project',
            'optimization_type': '1'  # Performance
        })
        return requirements
    
    def _collect_new_infrastructure_requirements(self, request: str, base_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collect requirements for new infrastructure with intelligent suggestions"""
        print("\n🏗️ **NEW INFRASTRUCTURE SETUP**")
        print("I'll help you design a complete infrastructure from scratch.")
        
        requirements = base_requirements.copy()
        
        # Project identification
        print("\n📝 **Project Identification**")
        if 'project_name' not in requirements:
            suggested_name = self._suggest_project_name(request)
            while True:
                project_name = input(f"Project name (suggested: '{suggested_name}'): ").strip()
                if project_name:
                    requirements['project_name'] = project_name
                    break
                elif project_name == '':
                    # User pressed enter, use suggestion
                    requirements['project_name'] = suggested_name
                    print(f"✅ Using suggested project name: {suggested_name}")
                    break
                print("❌ Project name is required!")
        
        # Environment and region
        print("\n🌍 **Environment & Region**")
        if 'aws_region' not in requirements:
            region_suggestion = self._suggest_aws_region(request)
            print(f"💡 **Suggestion**: {region_suggestion['reason']}")
            print("Available regions:")
            for i, region in enumerate(region_suggestion['options'], 1):
                print(f"{i}. {region['name']} - {region['description']}")
            
            while True:
                choice = input(f"Choose region (1-{len(region_suggestion['options'])}, or custom): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(region_suggestion['options']):
                    requirements['aws_region'] = region_suggestion['options'][int(choice)-1]['code']
                    break
                elif choice.lower() == 'custom':
                    while True:
                        custom_region = input("Enter custom region: ").strip()
                        if custom_region:
                            requirements['aws_region'] = custom_region
                            break
                        print("❌ Custom region is required!")
                    break
                else:
                    print(f"❌ Please choose 1-{len(region_suggestion['options'])} or 'custom'!")
        
        # Environment type
        if 'environment' not in requirements:
            env_suggestion = self._suggest_environment(request)
            print(f"💡 **Suggestion**: {env_suggestion['reason']}")
            env_choice = input(f"Environment (1=dev, 2=staging, 3=prod) [default: {env_suggestion['default']}]: ").strip()
            env_map = {'1': 'dev', '2': 'staging', '3': 'prod'}
            requirements['environment'] = env_map.get(env_choice, env_suggestion['default'])
        
        # Infrastructure sizing
        print("\n💰 **Infrastructure Sizing**")
        if 'instance_type' not in requirements:
            size_suggestion = self._suggest_infrastructure_size(request, requirements)
            print(f"💡 **Suggestion**: {size_suggestion['reason']}")
            print("Size options:")
            for i, option in enumerate(size_suggestion['options'], 1):
                print(f"{i}. {option['name']} - {option['description']} ({option['cost']})")
            
            while True:
                choice = input(f"Choose size (1-{len(size_suggestion['options'])}): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(size_suggestion['options']):
                    selected = size_suggestion['options'][int(choice)-1]
                    requirements.update(selected['config'])
                    break
                else:
                    print(f"❌ Please choose 1-{len(size_suggestion['options'])}!")
        
        # Database requirements
        print("\n🗄️ **Database Requirements**")
        if 'db_name' not in requirements:
            db_suggestion = self._suggest_database_config(request, requirements)
            print(f"💡 **Suggestion**: {db_suggestion['reason']}")
            
            while True:
                db_name = input(f"Database name (suggested: '{db_suggestion['name']}'): ").strip()
                if db_name:
                    requirements['db_name'] = db_name
                    break
                elif db_name == '':
                    # User pressed enter, use suggestion
                    requirements['db_name'] = db_suggestion['name']
                    print(f"✅ Using suggested database name: {db_suggestion['name']}")
                    break
                print("❌ Database name is required!")
            
            while True:
                db_username = input(f"Database username (suggested: '{db_suggestion['username']}'): ").strip()
                if db_username:
                    requirements['db_username'] = db_username
                    break
                elif db_username == '':
                    # User pressed enter, use suggestion
                    requirements['db_username'] = db_suggestion['username']
                    print(f"✅ Using suggested username: {db_suggestion['username']}")
                    break
                print("❌ Database username is required!")
            
            while True:
                db_password = input("Database password (min 12 chars, include numbers & symbols): ").strip()
                if len(db_password) >= 12 and any(c.isdigit() for c in db_password) and any(c in "!@#$%^&*" for c in db_password):
                    requirements['db_password'] = db_password
                    break
                print("❌ Password must be at least 12 characters with numbers and symbols!")
        
        # Security and access
        print("\n🔐 **Security & Access**")
        if 'key_name' not in requirements:
            key_suggestion = self._suggest_ssh_key_config(requirements)
            print(f"💡 **Suggestion**: {key_suggestion['reason']}")
            
            while True:
                key_choice = input("SSH key (1=existing, 2=new) [default: 2]: ").strip()
                if key_choice in ['1', '2', '']:
                    break
                print("❌ Please choose 1 or 2!")
            
            if key_choice == '1':
                while True:
                    existing_key = input("Enter existing key pair name: ").strip()
                    if existing_key:
                        requirements['key_name'] = existing_key
                        break
                    print("❌ Key pair name is required!")
            else:
                while True:
                    new_key = input(f"New key pair name (suggested: '{key_suggestion['name']}'): ").strip()
                    if new_key:
                        requirements['key_name'] = new_key
                        break
                    elif new_key == '':
                        # User pressed enter, use suggestion
                        requirements['key_name'] = key_suggestion['name']
                        print(f"✅ Using suggested key name: {key_suggestion['name']}")
                        break
                    print("❌ Key pair name is required!")
        
        # Advanced features
        print("\n⚡ **Advanced Features**")
        if 'high_availability' not in requirements:
            ha_suggestion = self._suggest_high_availability(request, requirements)
            print(f"💡 **Suggestion**: {ha_suggestion['reason']}")
            while True:
                ha_choice = input(f"High availability? (y/N) [suggested: {ha_suggestion['default']}]: ").strip().lower()
                if ha_choice in ['y', 'yes', 'n', 'no', '']:
                    requirements['high_availability'] = ha_choice in ['y', 'yes'] if ha_choice else ha_suggestion['default']
                    break
                print("❌ Please answer 'y' for yes or 'n' for no!")
        
        if 'monitoring' not in requirements:
            while True:
                monitoring_choice = input("Enable monitoring and logging? (Y/n): ").strip().lower()
                if monitoring_choice in ['y', 'yes', 'n', 'no', '']:
                    requirements['monitoring'] = monitoring_choice not in ['n', 'no']
                    break
                print("❌ Please answer 'y' for yes or 'n' for no!")
        
        if 'backup' not in requirements:
            while True:
                backup_choice = input("Enable automated backups? (Y/n): ").strip().lower()
                if backup_choice in ['y', 'yes', 'n', 'no', '']:
                    requirements['backup'] = backup_choice not in ['n', 'no']
                    break
                print("❌ Please answer 'y' for yes or 'n' for no!")
        
        return requirements
    
    def _collect_modification_requirements(self, request: str, base_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collect requirements for modifying existing infrastructure"""
        print("\n🔧 **MODIFYING EXISTING INFRASTRUCTURE**")
        print("I'll help you modify your existing infrastructure.")
        
        requirements = base_requirements.copy()
        
        # Ask about existing infrastructure
        print("\n📋 **Existing Infrastructure Details**")
        existing_project = input("What's the name of your existing project? ").strip()
        if existing_project:
            requirements['existing_project'] = existing_project
        
        # Ask what needs to be modified
        print("\n🎯 **What needs to be modified?**")
        print("1. Scale up/down resources")
        print("2. Add new components")
        print("3. Update configurations")
        print("4. Security improvements")
        print("5. Performance optimization")
        
        modification_type = input("Choose modification type (1-5): ").strip()
        requirements['modification_type'] = modification_type
        
        # Collect specific modification requirements
        if modification_type == '1':
            print("\n📈 **Scaling Requirements**")
            current_size = input("Current instance type (e.g., t3.micro): ").strip()
            new_size = input("New instance type (e.g., t3.small): ").strip()
            requirements['current_size'] = current_size
            requirements['new_size'] = new_size
        
        return requirements
    
    def _collect_addition_requirements(self, request: str, base_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collect requirements for adding components to existing infrastructure"""
        print("\n➕ **ADDING COMPONENTS TO EXISTING INFRASTRUCTURE**")
        print("I'll help you add new components to your existing setup.")
        
        requirements = base_requirements.copy()
        
        # Ask about existing infrastructure
        print("\n📋 **Existing Infrastructure**")
        existing_project = input("What's the name of your existing project? ").strip()
        if existing_project:
            requirements['existing_project'] = existing_project
        
        # Ask what to add
        print("\n🎯 **What would you like to add?**")
        print("1. Database")
        print("2. Load balancer")
        print("3. Monitoring")
        print("4. Security components")
        print("5. Caching layer")
        print("6. CDN")
        
        addition_type = input("Choose component to add (1-6): ").strip()
        requirements['addition_type'] = addition_type
        
        return requirements
    
    def _collect_optimization_requirements(self, request: str, base_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collect requirements for optimizing existing infrastructure"""
        print("\n⚡ **OPTIMIZING EXISTING INFRASTRUCTURE**")
        print("I'll help you optimize your existing infrastructure.")
        
        requirements = base_requirements.copy()
        
        # Ask about current issues
        print("\n🔍 **Current Infrastructure Issues**")
        print("1. Performance issues")
        print("2. High costs")
        print("3. Security concerns")
        print("4. Scalability problems")
        print("5. All of the above")
        
        optimization_focus = input("What's your main concern? (1-5): ").strip()
        requirements['optimization_focus'] = optimization_focus
        
        return requirements
    
    def _collect_general_requirements(self, request: str, base_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Collect requirements for general infrastructure requests"""
        print("\n🏗️ **GENERAL INFRASTRUCTURE REQUEST**")
        print("I'll help you with your infrastructure needs.")
        
        requirements = base_requirements.copy()
        
        # Ask for clarification
        print("\n❓ **Clarification Needed**")
        print("Could you provide more details about:")
        print("1. What type of infrastructure you need?")
        print("2. What's your budget range?")
        print("3. What's your expected scale?")
        print("4. Any specific requirements?")
        
        return requirements
    
    def _suggest_project_name(self, request: str) -> str:
        """Suggest a project name based on the request"""
        request_lower = request.lower()
        
        if 'ml' in request_lower or 'machine learning' in request_lower:
            return 'ml-platform'
        elif 'iot' in request_lower:
            return 'iot-platform'
        elif 'data' in request_lower or 'analytics' in request_lower:
            return 'data-analytics-platform'
        elif 'enterprise' in request_lower:
            return 'enterprise-platform'
        elif 'web' in request_lower or 'app' in request_lower:
            return 'web-application'
        else:
            return 'infrastructure-project'
    
    def _suggest_aws_region(self, request: str) -> Dict[str, Any]:
        """Suggest AWS region based on requirements"""
        request_lower = request.lower()
        
        if 'europe' in request_lower or 'eu' in request_lower:
            return {
                'reason': 'Europe-based requirements detected',
                'options': [
                    {'name': 'eu-west-1 (Ireland)', 'code': 'eu-west-1', 'description': 'Lowest latency for Europe'},
                    {'name': 'eu-central-1 (Frankfurt)', 'code': 'eu-central-1', 'description': 'GDPR compliance'},
                    {'name': 'eu-west-2 (London)', 'code': 'eu-west-2', 'description': 'UK-specific requirements'}
                ]
            }
        elif 'asia' in request_lower or 'singapore' in request_lower:
            return {
                'reason': 'Asia-Pacific requirements detected',
                'options': [
                    {'name': 'ap-southeast-1 (Singapore)', 'code': 'ap-southeast-1', 'description': 'Best for Southeast Asia'},
                    {'name': 'ap-northeast-1 (Tokyo)', 'code': 'ap-northeast-1', 'description': 'Best for Japan/Korea'},
                    {'name': 'ap-south-1 (Mumbai)', 'code': 'ap-south-1', 'description': 'Best for India'}
                ]
            }
        else:
            return {
                'reason': 'Default to US regions for best service availability',
                'options': [
                    {'name': 'us-east-1 (N. Virginia)', 'code': 'us-east-1', 'description': 'Most services, lowest cost'},
                    {'name': 'us-west-2 (Oregon)', 'code': 'us-west-2', 'description': 'West coast, good for global'},
                    {'name': 'us-east-2 (Ohio)', 'code': 'us-east-2', 'description': 'Alternative to N. Virginia'}
                ]
            }
    
    def _suggest_environment(self, request: str) -> Dict[str, Any]:
        """Suggest environment based on request"""
        request_lower = request.lower()
        
        if 'production' in request_lower or 'prod' in request_lower:
            return {'reason': 'Production environment detected in request', 'default': 'prod'}
        elif 'staging' in request_lower or 'stage' in request_lower:
            return {'reason': 'Staging environment detected in request', 'default': 'staging'}
        else:
            return {'reason': 'Starting with development for safety', 'default': 'dev'}
    
    def _suggest_infrastructure_size(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest infrastructure size based on requirements"""
        request_lower = request.lower()
        budget = requirements.get('budget', 0)
        
        if budget > 0:
            if budget >= 1000:
                recommended = 'enterprise'
            elif budget >= 500:
                recommended = 'large'
            elif budget >= 100:
                recommended = 'medium'
            else:
                recommended = 'small'
        elif 'enterprise' in request_lower or 'large scale' in request_lower:
            recommended = 'enterprise'
        elif 'small' in request_lower or 'basic' in request_lower:
            recommended = 'small'
        else:
            recommended = 'medium'
        
        options = [
            {
                'name': 'Small',
                'description': 'Basic setup for development/testing',
                'cost': '~$20-50/month',
                'config': {'instance_type': 't3.micro', 'db_class': 'db.t3.micro'}
            },
            {
                'name': 'Medium', 
                'description': 'Production-ready for small teams',
                'cost': '~$50-150/month',
                'config': {'instance_type': 't3.small', 'db_class': 'db.t3.small'}
            },
            {
                'name': 'Large',
                'description': 'High-performance for growing applications',
                'cost': '~$150-500/month', 
                'config': {'instance_type': 't3.medium', 'db_class': 'db.t3.medium'}
            },
            {
                'name': 'Enterprise',
                'description': 'Mission-critical with high availability',
                'cost': '~$500+/month',
                'config': {'instance_type': 't3.large', 'db_class': 'db.t3.large'}
            }
        ]
        
        return {
            'reason': f'Based on your requirements, I recommend {recommended} size infrastructure',
            'options': options
        }
    
    def _suggest_database_config(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest database configuration"""
        project_name = requirements.get('project_name', 'app')
        domain = requirements.get('domain', 'web')
        
        if domain == 'ml':
            return {
                'reason': 'ML workloads benefit from descriptive database names',
                'name': f'{project_name}-ml-data',
                'username': 'ml_admin'
            }
        elif domain == 'iot':
            return {
                'reason': 'IoT applications need descriptive database naming',
                'name': f'{project_name}-iot-data',
                'username': 'iot_admin'
            }
        else:
            return {
                'reason': 'Standard database configuration for web applications',
                'name': f'{project_name}-db',
                'username': 'admin'
            }
    
    def _suggest_ssh_key_config(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest SSH key configuration"""
        project_name = requirements.get('project_name', 'project')
        environment = requirements.get('environment', 'dev')
        
        return {
            'reason': f'SSH key should match your project and environment',
            'name': f'{project_name}-{environment}-key'
        }
    
    def _suggest_high_availability(self, request: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest high availability configuration"""
        request_lower = request.lower()
        
        if '99.9' in request_lower or '99.99' in request_lower or 'high availability' in request_lower:
            return {
                'reason': 'High availability requirements detected in your request',
                'default': True
            }
        elif requirements.get('environment') == 'prod':
            return {
                'reason': 'Production environment should have high availability',
                'default': True
            }
        else:
            return {
                'reason': 'Development environment typically doesn\'t need HA',
                'default': False
            }
    
    def _validate_and_suggest_improvements(self, requirements: Dict[str, Any], scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Validate requirements and suggest improvements"""
        print("\n🔍 **VALIDATION & IMPROVEMENTS**")
        
        # Check for missing critical requirements
        missing = []
        if 'project_name' not in requirements:
            missing.append('project_name')
        if 'aws_region' not in requirements:
            missing.append('aws_region')
        if 'instance_type' not in requirements:
            missing.append('instance_type')
        
        if missing:
            print(f"⚠️ Missing critical requirements: {', '.join(missing)}")
            print("💡 I'll use intelligent defaults for missing values...")
            
            # Apply intelligent defaults
            if 'project_name' not in requirements:
                requirements['project_name'] = self._suggest_project_name("")
            if 'aws_region' not in requirements:
                requirements['aws_region'] = 'us-east-1'
            if 'instance_type' not in requirements:
                requirements['instance_type'] = 't3.micro'
        
        # Suggest improvements based on scenario
        improvements = []
        
        if scenario['type'] == 'new_infrastructure' and not requirements.get('monitoring'):
            improvements.append("Consider enabling monitoring for new infrastructure")
        
        if requirements.get('environment') == 'prod' and not requirements.get('high_availability'):
            improvements.append("Production environments should have high availability")
        
        if requirements.get('budget', 0) > 500 and not requirements.get('backup'):
            improvements.append("High-budget projects should include automated backups")
        
        if improvements:
            print("💡 **Suggested Improvements**:")
            for improvement in improvements:
                print(f"   • {improvement}")
        
        return requirements
    
    def _format_requirements_summary(self, requirements: Dict[str, Any]) -> str:
        """Format requirements into a readable summary"""
        summary_parts = []
        
        if 'project_name' in requirements:
            summary_parts.append(f"Project: {requirements['project_name']}")
        if 'aws_region' in requirements:
            summary_parts.append(f"Region: {requirements['aws_region']}")
        if 'environment' in requirements:
            summary_parts.append(f"Environment: {requirements['environment']}")
        if 'instance_type' in requirements:
            summary_parts.append(f"Size: {requirements['instance_type']}")
        if 'high_availability' in requirements:
            summary_parts.append(f"HA: {'Yes' if requirements['high_availability'] else 'No'}")
        
        return ", ".join(summary_parts)
    
    def _save_terraform_files(self, terraform_files: Dict[str, str], project_name: str) -> str:
        """Save Terraform files to disk"""
        try:
            # Create safe project name
            safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            safe_name = safe_name.replace('__', '_')  # Remove double underscores
            
            # Check for existing project and handle conflicts
            project_dir = os.path.join("workspaces", safe_name)
            if os.path.exists(project_dir):
                print(f"⚠️ Project directory '{safe_name}' already exists!")
                print("Options:")
                print("1. Overwrite existing project")
                print("2. Create new project with timestamp")
                print("3. Create new project with different name")
                
                while True:
                    choice = input("Choose option (1-3): ").strip()
                    if choice == '1':
                        print(f"✅ Overwriting existing project: {safe_name}")
                        break
                    elif choice == '2':
                        import datetime
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_name = f"{safe_name}_{timestamp}"
                        project_dir = os.path.join("workspaces", safe_name)
                        print(f"✅ Creating new project: {safe_name}")
                        break
                    elif choice == '3':
                        while True:
                            new_name = input("Enter new project name: ").strip()
                            if new_name:
                                safe_name = "".join(c for c in new_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                safe_name = safe_name.replace(' ', '_').lower()
                                safe_name = safe_name.replace('__', '_')
                                project_dir = os.path.join("workspaces", safe_name)
                                print(f"✅ Creating new project: {safe_name}")
                                break
                            print("❌ Project name is required!")
                        break
                    else:
                        print("❌ Please choose 1, 2, or 3!")
            
            # Create project directory
            os.makedirs(project_dir, exist_ok=True)
            
            # Create terraform subdirectory
            terraform_dir = os.path.join(project_dir, "terraform")
            os.makedirs(terraform_dir, exist_ok=True)
            
            # Save each Terraform file
            for filename, content in terraform_files.items():
                file_path = os.path.join(terraform_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"💾 Saved: {file_path}")
            
            # Create README
            readme_path = os.path.join(project_dir, "README.md")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {project_name}\n\n")
                f.write("## Generated Infrastructure\n\n")
                f.write("This project contains Terraform code generated by the Intelligent Terraform Agent.\n\n")
                f.write("## Files\n\n")
                for filename in terraform_files.keys():
                    f.write(f"- `terraform/{filename}`\n")
                f.write("\n## Usage\n\n")
                f.write("```bash\n")
                f.write("cd terraform\n")
                f.write("terraform init\n")
                f.write("terraform plan\n")
                f.write("terraform apply\n")
                f.write("```\n")
            
            print(f"📁 Project saved to: {project_dir}")
            return project_dir
            
        except Exception as e:
            print(f"❌ Failed to save files: {e}")
            return None
    
    # ============================================================================
    # PHASE 5: AUTONOMOUS OPERATIONS INTEGRATION
    # ============================================================================
    
    def start_autonomous_operations(self):
        """Start autonomous operations for continuous infrastructure management"""
        try:
            self.autonomous_agent.start_autonomous_engine()
            print("🤖 Autonomous operations started - infrastructure will be continuously monitored and optimized")
            return True
        except Exception as e:
            print(f"❌ Failed to start autonomous operations: {e}")
            return False
    
    def stop_autonomous_operations(self):
        """Stop autonomous operations"""
        try:
            self.autonomous_agent.stop_autonomous_engine()
            print("🛑 Autonomous operations stopped")
            return True
        except Exception as e:
            print(f"❌ Failed to stop autonomous operations: {e}")
            return False
    
    def get_infrastructure_health(self):
        """Get current infrastructure health status"""
        try:
            health = self.autonomous_agent.get_infrastructure_health()
            return health
        except Exception as e:
            print(f"❌ Failed to get infrastructure health: {e}")
            return None
    
    def trigger_self_healing(self, issue_description: str):
        """Trigger self-healing for a specific issue"""
        try:
            result = self.autonomous_agent.self_heal_infrastructure(issue_description)
            return result
        except Exception as e:
            print(f"❌ Failed to trigger self-healing: {e}")
            return None
    
    def predict_and_scale(self, workload_pattern: str):
        """Predict scaling needs and implement scaling"""
        try:
            result = self.autonomous_agent.predict_and_scale(workload_pattern)
            return result
        except Exception as e:
            print(f"❌ Failed to predict and scale: {e}")
            return None
    
    def optimize_costs(self):
        """Trigger cost optimization"""
        try:
            result = self.autonomous_agent.optimize_costs()
            return result
        except Exception as e:
            print(f"❌ Failed to optimize costs: {e}")
            return None
    
    def harden_security(self):
        """Trigger security hardening"""
        try:
            result = self.autonomous_agent.harden_security()
            return result
        except Exception as e:
            print(f"❌ Failed to harden security: {e}")
            return None
    
    def tune_performance(self):
        """Trigger performance tuning"""
        try:
            result = self.autonomous_agent.tune_performance()
            return result
        except Exception as e:
            print(f"❌ Failed to tune performance: {e}")
            return None
    
    def check_compliance(self):
        """Trigger compliance check"""
        try:
            result = self.autonomous_agent.check_compliance()
            return result
        except Exception as e:
            print(f"❌ Failed to check compliance: {e}")
            return None
    
    def get_autonomous_operations_status(self):
        """Get status of all autonomous operations"""
        try:
            status = self.autonomous_agent.get_operations_status()
            return status
        except Exception as e:
            print(f"❌ Failed to get autonomous operations status: {e}")
            return None
    
    # ============================================================================
    # PHASE 4: OPERATIONAL INTELLIGENCE INTEGRATION
    # ============================================================================
    
    def get_operational_intelligence(self):
        """Get comprehensive operational intelligence insights"""
        try:
            intelligence = self.monitor.get_operational_intelligence()
            return intelligence
        except Exception as e:
            print(f"❌ Failed to get operational intelligence: {e}")
            return None
    
    def get_enhanced_metrics(self):
        """Get enhanced monitoring metrics"""
        try:
            metrics = self.monitor.get_enhanced_metrics()
            return metrics
        except Exception as e:
            print(f"❌ Failed to get enhanced metrics: {e}")
            return None
    
    def generate_operational_report(self):
        """Generate comprehensive operational report"""
        try:
            report = self.monitor.generate_operational_report()
            return report
        except Exception as e:
            print(f"❌ Failed to generate operational report: {e}")
            return None
