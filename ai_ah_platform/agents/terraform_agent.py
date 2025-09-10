"""
Terraform Infrastructure Agent for the Multi-Agent Infrastructure Intelligence Platform.

This agent specializes in Terraform-based infrastructure provisioning,
management, and optimization using AI-driven decision making.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import asyncio
import subprocess
import os
import tempfile
from pathlib import Path
import yaml

from ..core.base_platform import BasePlatformComponent, PlatformConfig, Task, Priority, ComponentStatus, AgentCapability
from ..core.agent_framework import IntelligentAgent, AgentResponse, ConversationType, MemoryType
from ..core.nlp.natural_language_processor import ParsedRequest, IntentType, EntityType
from ..core.intelligence.local_knowledge_base import LocalKnowledgeBase


@dataclass
class TerraformResource:
    """Represents a Terraform resource."""
    type: str
    name: str
    provider: str
    configuration: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TerraformPlan:
    """Represents a Terraform execution plan."""
    id: str
    name: str
    description: str
    resources: List[TerraformResource]
    variables: Dict[str, Any]
    outputs: Dict[str, Any]
    state_file: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TerraformExecution:
    """Represents a Terraform execution."""
    id: str
    plan_id: str
    command: str
    status: str
    output: str
    error: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TerraformAgent(IntelligentAgent):
    """
    Terraform Infrastructure Agent.
    
    Specializes in:
    - Infrastructure provisioning with Terraform
    - Resource management and optimization
    - Cost estimation and optimization
    - Security best practices
    - Multi-cloud deployments
    """
    
    def __init__(self, config: PlatformConfig, workspace_path: str = None):
        super().__init__(config)
        
        self.workspace_path = workspace_path or tempfile.mkdtemp(prefix="terraform_agent_")
        self.plans: Dict[str, TerraformPlan] = {}
        self.executions: Dict[str, TerraformExecution] = {}
        self.resource_templates: Dict[str, Dict[str, Any]] = {}
        self.provider_configs: Dict[str, Dict[str, Any]] = {}
        
        # Initialize local knowledge base for intelligent responses
        self.knowledge_base = LocalKnowledgeBase()
        
        # Terraform-specific capabilities
        self.capabilities = [
            AgentCapability(
                name="infrastructure_provisioning",
                description="Provision infrastructure using Terraform",
                version="1.0.0",
                parameters={"supported_providers": ["aws", "azure", "gcp", "digitalocean"]}
            ),
            AgentCapability(
                name="resource_management",
                description="Manage and optimize Terraform resources",
                version="1.0.0"
            ),
            AgentCapability(
                name="cost_optimization",
                description="Optimize infrastructure costs",
                version="1.0.0"
            ),
            AgentCapability(
                name="security_analysis",
                description="Analyze and enforce security best practices",
                version="1.0.0"
            )
        ]
        
        # Initialize resource templates
        self._initialize_resource_templates()
        self._initialize_provider_configs()
    
    async def _initialize_capabilities(self):
        """Initialize Terraform-specific capabilities."""
        # Add Terraform-specific response handlers
        self.add_response_handler("create_infrastructure", self._handle_create_infrastructure)
        self.add_response_handler("modify_infrastructure", self._handle_modify_infrastructure)
        self.add_response_handler("delete_infrastructure", self._handle_delete_infrastructure)
        self.add_response_handler("get_status", self._handle_get_status)
        
        # Add context processors
        self.add_context_processor(self._process_terraform_context)
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers for Terraform operations."""
        pass  # Already handled in _initialize_capabilities
    
    async def _initialize_context_processors(self):
        """Initialize context processors for Terraform operations."""
        pass  # Already handled in _initialize_capabilities
    
    def _initialize_resource_templates(self):
        """Initialize common Terraform resource templates."""
        self.resource_templates = {
            "aws_ec2_instance": {
                "resource": "aws_instance",
                "required_params": ["ami", "instance_type"],
                "optional_params": ["subnet_id", "security_groups", "key_name", "tags"],
                "defaults": {
                    "tags": {"Name": "{{name}}", "Environment": "{{environment}}"}
                }
            },
            "aws_s3_bucket": {
                "resource": "aws_s3_bucket",
                "required_params": ["bucket"],
                "optional_params": ["versioning", "encryption", "tags"],
                "defaults": {
                    "versioning": {"enabled": True},
                    "encryption": {"algorithm": "AES256"}
                }
            },
            "aws_rds_instance": {
                "resource": "aws_db_instance",
                "required_params": ["identifier", "engine", "instance_class"],
                "optional_params": ["allocated_storage", "storage_type", "backup_retention_period"],
                "defaults": {
                    "backup_retention_period": 7,
                    "storage_type": "gp2"
                }
            },
            "aws_vpc": {
                "resource": "aws_vpc",
                "required_params": ["cidr_block"],
                "optional_params": ["enable_dns_hostnames", "enable_dns_support", "tags"],
                "defaults": {
                    "enable_dns_hostnames": True,
                    "enable_dns_support": True
                }
            },
            "aws_security_group": {
                "resource": "aws_security_group",
                "required_params": ["name", "description"],
                "optional_params": ["vpc_id", "ingress", "egress", "tags"],
                "defaults": {
                    "egress": [{"from_port": 0, "to_port": 0, "protocol": "-1", "cidr_blocks": ["0.0.0.0/0"]}]
                }
            }
        }
    
    def _initialize_provider_configs(self):
        """Initialize provider configurations."""
        self.provider_configs = {
            "aws": {
                "provider": "aws",
                "required_vars": ["region"],
                "optional_vars": ["access_key", "secret_key", "profile"],
                "defaults": {"region": "us-east-1"}
            },
            "azure": {
                "provider": "azurerm",
                "required_vars": ["subscription_id", "client_id", "client_secret", "tenant_id"],
                "optional_vars": ["features"],
                "defaults": {}
            },
            "gcp": {
                "provider": "google",
                "required_vars": ["project", "region"],
                "optional_vars": ["credentials", "zone"],
                "defaults": {"region": "us-central1"}
            }
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a Terraform-related request using local intelligence."""
        try:
            # Use knowledge base to analyze the request
            analysis = self.knowledge_base.analyze_request(request)
            
            # Generate intelligent response based on analysis
            if analysis["confidence"] > 0.7:
                return await self._generate_intelligent_response(analysis, request, context)
            else:
                # Fallback to original parsing for low confidence
                parsed_request = await self._parse_terraform_request(request)
                
                # Fix: Handle intent as dictionary
                intent_type = parsed_request.intent.get("type") if isinstance(parsed_request.intent, dict) else parsed_request.intent.type
                
                if intent_type == IntentType.CREATE_INFRASTRUCTURE:
                    return await self._handle_create_infrastructure(parsed_request, context)
                elif intent_type == IntentType.MODIFY_INFRASTRUCTURE:
                    return await self._handle_modify_infrastructure(parsed_request, context)
                elif intent_type == IntentType.DELETE_INFRASTRUCTURE:
                    return await self._handle_delete_infrastructure(parsed_request, context)
                elif intent_type == IntentType.GET_STATUS:
                    return await self._handle_get_status(parsed_request, context)
                else:
                    return AgentResponse(
                        agent_id=self.config.name,
                        response_type="text",
                        content="I can help you with Terraform infrastructure operations. What would you like to do?",
                        confidence=0.8
                    )
                
        except Exception as e:
            self.logger.error(f"Error processing Terraform request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def _generate_intelligent_response(self, analysis: Dict[str, Any], request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Generate intelligent response using knowledge base analysis."""
        try:
            # Build comprehensive response content
            content_parts = []
            
            # Add main response
            if analysis["recommendations"]:
                content_parts.append("## Infrastructure Analysis\n")
                content_parts.extend([f"• {rec}" for rec in analysis["recommendations"]])
            
            # Add knowledge insights
            if analysis["knowledge"]:
                content_parts.append("\n## Knowledge Insights\n")
                for knowledge in analysis["knowledge"][:2]:  # Show top 2 insights
                    content_parts.append(f"**{knowledge.title}**: {knowledge.content[:200]}...")
            
            # Add best practices
            if analysis["best_practices"]:
                content_parts.append("\n## Best Practices\n")
                content_parts.extend([f"• {practice}" for practice in analysis["best_practices"][:3]])
            
            # Add relevant templates
            if analysis["templates"]:
                content_parts.append("\n## Recommended Templates\n")
                for template in analysis["templates"]:
                    content_parts.append(f"• **{template['name']}**: {template['description']} (Cost: {template['estimated_cost']})")
            
            # Add scenarios
            if analysis["scenarios"]:
                content_parts.append("\n## Similar Scenarios\n")
                for scenario in analysis["scenarios"]:
                    content_parts.append(f"• **{scenario['name']}**: {scenario['description']} (Cost: {scenario['estimated_cost']})")
            
            # Generate plan if it's a creation request
            if analysis["intent"] in ["create_web_server", "create_database", "create_load_balancer"]:
                plan = await self._generate_plan_from_analysis(analysis, request)
                if plan:
                    content_parts.append(f"\n## Generated Plan\n")
                    content_parts.append(f"Plan ID: {plan.id}")
                    content_parts.append(f"Resources: {len(plan.resources)}")
                    content_parts.append(f"Status: {plan.status}")
            
            content = "\n".join(content_parts)
            
            return AgentResponse(
                agent_id=self.config.name,
                response_type="text",
                content=content,
                confidence=analysis["confidence"],
                metadata={
                    "intent": analysis["intent"],
                    "agent_type": analysis["agent_type"],
                    "knowledge_used": len(analysis["knowledge"]),
                    "templates_suggested": len(analysis["templates"]),
                    "best_practices_included": len(analysis["best_practices"])
                },
                suggestions=[
                    "Would you like me to create a detailed plan?",
                    "Should I proceed with the recommended template?",
                    "Do you need help with security configuration?",
                    "Would you like cost optimization recommendations?"
                ]
            )
            
        except Exception as e:
            self.logger.error(f"Error generating intelligent response: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="text",
                content=f"I understand you need help with infrastructure. Let me provide some guidance based on your request.",
                confidence=0.6,
                metadata={"error": str(e)}
            )
    
    async def _generate_plan_from_analysis(self, analysis: Dict[str, Any], request: str) -> Optional[TerraformPlan]:
        """Generate a Terraform plan based on knowledge base analysis."""
        try:
            # Create a new plan
            plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate resources based on intent
            resources = []
            if analysis["intent"] == "create_web_server":
                resources = [
                    TerraformResource(
                        type="aws_instance",
                        name="web_server",
                        provider="aws",
                        configuration={
                            "ami": "ami-12345678",
                            "instance_type": "t3.micro",
                            "security_groups": ["web_sg"]
                        }
                    ),
                    TerraformResource(
                        type="aws_security_group",
                        name="web_sg",
                        provider="aws",
                        configuration={
                            "ingress": [
                                {"from_port": 80, "to_port": 80, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]},
                                {"from_port": 443, "to_port": 443, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]},
                                {"from_port": 22, "to_port": 22, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]}
                            ]
                        }
                    )
                ]
            elif analysis["intent"] == "create_database":
                resources = [
                    TerraformResource(
                        type="aws_db_instance",
                        name="database",
                        provider="aws",
                        configuration={
                            "engine": "mysql",
                            "engine_version": "8.0",
                            "instance_class": "db.t3.micro",
                            "allocated_storage": 20
                        }
                    )
                ]
            
            # Create the plan
            plan = TerraformPlan(
                id=plan_id,
                name=f"Generated Plan for {analysis['intent'].replace('_', ' ').title()}",
                description=f"Auto-generated plan based on: {request[:100]}...",
                resources=resources,
                variables=analysis.get("parameters", {}),
                outputs={},
                status="draft"
            )
            
            # Store the plan
            self.plans[plan_id] = plan
            
            return plan
            
        except Exception as e:
            self.logger.error(f"Error generating plan: {str(e)}")
            return None
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze infrastructure requirements for Terraform."""
        try:
            # Parse requirements
            parsed_request = await self._parse_terraform_request(requirements)
            
            analysis = {
                "intent": parsed_request.intent.type.value,
                "confidence": parsed_request.confidence,
                "entities": [
                    {
                        "type": entity.type.value,
                        "value": entity.value,
                        "confidence": entity.confidence
                    }
                    for entity in parsed_request.entities
                ],
                "resources": [],
                "providers": [],
                "recommendations": []
            }
            
            # Extract resources and providers
            for entity in parsed_request.entities:
                if entity.type == EntityType.SERVICE:
                    if entity.value.lower() in ["ec2", "instance", "server"]:
                        analysis["resources"].append("aws_ec2_instance")
                    elif entity.value.lower() in ["s3", "storage", "bucket"]:
                        analysis["resources"].append("aws_s3_bucket")
                    elif entity.value.lower() in ["rds", "database"]:
                        analysis["resources"].append("aws_rds_instance")
                
                elif entity.type == EntityType.CLOUD_PROVIDER:
                    analysis["providers"].append(entity.value.lower())
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing requirements: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def generate_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a Terraform execution plan."""
        try:
            plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create Terraform plan
            plan = TerraformPlan(
                id=plan_id,
                name=analysis.get("name", f"Infrastructure Plan {plan_id}"),
                description=analysis.get("description", "Generated infrastructure plan"),
                resources=[],
                variables={},
                outputs={}
            )
            
            # Add resources based on analysis
            for resource_type in analysis.get("resources", []):
                if resource_type in self.resource_templates:
                    template = self.resource_templates[resource_type]
                    resource = TerraformResource(
                        type=template["resource"],
                        name=f"{resource_type}_{len(plan.resources) + 1}",
                        provider=template["resource"].split("_")[0],
                        configuration=template["defaults"].copy()
                    )
                    plan.resources.append(resource)
            
            # Add provider configurations
            for provider in analysis.get("providers", []):
                if provider in self.provider_configs:
                    provider_config = self.provider_configs[provider]
                    plan.variables.update(provider_config["defaults"])
            
            # Store plan
            self.plans[plan_id] = plan
            
            # Generate Terraform files
            await self._generate_terraform_files(plan)
            
            return {
                "plan_id": plan_id,
                "status": "created",
                "resources": len(plan.resources),
                "providers": list(set(r.provider for r in plan.resources)),
                "files_generated": True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating plan: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Terraform plan."""
        try:
            plan_id = plan.get("plan_id")
            if not plan_id or plan_id not in self.plans:
                return {"error": "Plan not found", "status": "failed"}
            
            terraform_plan = self.plans[plan_id]
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create execution
            execution = TerraformExecution(
                id=execution_id,
                plan_id=plan_id,
                command="terraform apply",
                status="running"
            )
            
            self.executions[execution_id] = execution
            
            # Execute Terraform commands
            result = await self._execute_terraform_commands(terraform_plan, execution)
            
            execution.status = "completed" if result["success"] else "failed"
            execution.completed_at = datetime.now()
            execution.output = result["output"]
            execution.error = result.get("error")
            
            return {
                "execution_id": execution_id,
                "status": execution.status,
                "output": execution.output,
                "error": execution.error
            }
            
        except Exception as e:
            self.logger.error(f"Error executing plan: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def _parse_terraform_request(self, request: str) -> ParsedRequest:
        """Parse a Terraform-specific request."""
        # This would integrate with the NLP processor
        # For now, we'll do basic parsing
        request_lower = request.lower()
        
        # Simple intent detection
        if any(word in request_lower for word in ["create", "deploy", "provision", "build"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["modify", "update", "change", "scale"]):
            intent_type = IntentType.MODIFY_INFRASTRUCTURE
        elif any(word in request_lower for word in ["delete", "remove", "destroy"]):
            intent_type = IntentType.DELETE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["status", "state", "health"]):
            intent_type = IntentType.GET_STATUS
        else:
            intent_type = IntentType.UNKNOWN
        
        # Simple entity extraction
        entities = []
        if "aws" in request_lower:
            entities.append({"type": EntityType.CLOUD_PROVIDER, "value": "aws"})
        if "ec2" in request_lower or "instance" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "ec2"})
        if "s3" in request_lower or "bucket" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "s3"})
        
        return ParsedRequest(
            original_text=request,
            intent={"type": intent_type, "confidence": 0.8},
            entities=entities,
            confidence=0.8
        )
    
    async def _handle_create_infrastructure(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle infrastructure creation requests."""
        # Analyze requirements
        analysis = await self.analyze_requirements(parsed_request.original_text)
        
        # Generate plan
        plan = await self.generate_plan(analysis)
        
        if plan.get("status") == "created":
            return AgentResponse(
                agent_id=self.config.name,
                response_type="infrastructure_plan",
                content=f"I've created a Terraform plan with {plan['resources']} resources for {', '.join(plan['providers'])} providers.",
                confidence=0.9,
                suggestions=[
                    "Review the generated Terraform files",
                    "Execute the plan to provision infrastructure",
                    "Modify the plan if needed"
                ],
                next_actions=[
                    "terraform_plan_review",
                    "terraform_plan_execute",
                    "terraform_plan_modify"
                ],
                metadata={"plan_id": plan["plan_id"], "analysis": analysis}
            )
        else:
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content="I encountered an error creating the infrastructure plan.",
                confidence=0.0,
                metadata={"error": plan.get("error")}
            )
    
    async def _handle_modify_infrastructure(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle infrastructure modification requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you modify your infrastructure. Let me analyze the current state and propose changes.",
            confidence=0.8,
            suggestions=["Review current infrastructure", "Identify changes needed", "Generate modification plan"]
        )
    
    async def _handle_delete_infrastructure(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle infrastructure deletion requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you safely remove infrastructure. Let me first show you what will be deleted.",
            confidence=0.8,
            suggestions=["Review resources to be deleted", "Confirm deletion", "Execute destruction plan"]
        )
    
    async def _handle_get_status(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle status requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll check the status of your Terraform infrastructure.",
            confidence=0.8,
            suggestions=["Check resource status", "Review recent changes", "Monitor health"]
        )
    
    async def _process_terraform_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context for Terraform operations."""
        processed_context = context.copy()
        
        # Add Terraform-specific context
        processed_context["terraform_workspace"] = self.workspace_path
        processed_context["available_plans"] = list(self.plans.keys())
        processed_context["available_executions"] = list(self.executions.keys())
        
        return processed_context
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Security recommendations
        if "aws_ec2_instance" in analysis["resources"]:
            recommendations.append("Consider using security groups with least privilege access")
            recommendations.append("Enable CloudTrail logging for audit purposes")
        
        # Cost optimization recommendations
        if "aws_rds_instance" in analysis["resources"]:
            recommendations.append("Consider using RDS Reserved Instances for cost savings")
            recommendations.append("Enable automated backups with appropriate retention")
        
        # Performance recommendations
        if "aws_s3_bucket" in analysis["resources"]:
            recommendations.append("Enable versioning for data protection")
            recommendations.append("Configure lifecycle policies for cost optimization")
        
        return recommendations
    
    async def _generate_terraform_files(self, plan: TerraformPlan):
        """Generate Terraform configuration files."""
        plan_dir = Path(self.workspace_path) / plan.id
        plan_dir.mkdir(exist_ok=True)
        
        # Generate main.tf
        main_tf_content = self._generate_main_tf(plan)
        with open(plan_dir / "main.tf", "w") as f:
            f.write(main_tf_content)
        
        # Generate variables.tf
        variables_tf_content = self._generate_variables_tf(plan)
        with open(plan_dir / "variables.tf", "w") as f:
            f.write(variables_tf_content)
        
        # Generate outputs.tf
        outputs_tf_content = self._generate_outputs_tf(plan)
        with open(plan_dir / "outputs.tf", "w") as f:
            f.write(outputs_tf_content)
        
        # Generate terraform.tfvars
        tfvars_content = self._generate_tfvars(plan)
        with open(plan_dir / "terraform.tfvars", "w") as f:
            f.write(tfvars_content)
    
    def _generate_main_tf(self, plan: TerraformPlan) -> str:
        """Generate main.tf content."""
        content = "# Terraform configuration generated by AI-AH Platform\n\n"
        
        # Add provider configurations
        providers = set(r.provider for r in plan.resources)
        for provider in providers:
            if provider == "aws":
                content += '''provider "aws" {
  region = var.aws_region
}

'''
        
        # Add resources
        for resource in plan.resources:
            content += f'resource "{resource.type}" "{resource.name}" {{\n'
            for key, value in resource.configuration.items():
                if isinstance(value, str):
                    content += f'  {key} = "{value}"\n'
                elif isinstance(value, dict):
                    content += f'  {key} = {{\n'
                    for k, v in value.items():
                        content += f'    {k} = "{v}"\n'
                    content += '  }\n'
                else:
                    content += f'  {key} = {value}\n'
            content += '}\n\n'
        
        return content
    
    def _generate_variables_tf(self, plan: TerraformPlan) -> str:
        """Generate variables.tf content."""
        content = "# Variables for Terraform configuration\n\n"
        
        # Add common variables
        variables = {
            "aws_region": {"type": "string", "default": "us-east-1", "description": "AWS region"},
            "environment": {"type": "string", "default": "development", "description": "Environment name"},
            "project_name": {"type": "string", "default": "ai-ah-project", "description": "Project name"}
        }
        
        for var_name, var_config in variables.items():
            content += f'variable "{var_name}" {{\n'
            content += f'  type        = "{var_config["type"]}"\n'
            content += f'  default     = "{var_config["default"]}"\n'
            content += f'  description = "{var_config["description"]}"\n'
            content += '}\n\n'
        
        return content
    
    def _generate_outputs_tf(self, plan: TerraformPlan) -> str:
        """Generate outputs.tf content."""
        content = "# Outputs for Terraform configuration\n\n"
        
        for resource in plan.resources:
            if resource.type == "aws_instance":
                content += f'output "{resource.name}_id" {{\n'
                content += f'  value = {resource.type}.{resource.name}.id\n'
                content += f'  description = "ID of the {resource.name} instance"\n'
                content += '}\n\n'
        
        return content
    
    def _generate_tfvars(self, plan: TerraformPlan) -> str:
        """Generate terraform.tfvars content."""
        content = "# Terraform variables file\n\n"
        content += 'aws_region = "us-east-1"\n'
        content += 'environment = "development"\n'
        content += 'project_name = "ai-ah-project"\n'
        
        return content
    
    async def _execute_terraform_commands(self, plan: TerraformPlan, execution: TerraformExecution) -> Dict[str, Any]:
        """Execute Terraform commands."""
        try:
            plan_dir = Path(self.workspace_path) / plan.id
            
            # Initialize Terraform
            init_result = await self._run_terraform_command(plan_dir, "terraform init")
            if not init_result["success"]:
                return init_result
            
            # Plan Terraform
            plan_result = await self._run_terraform_command(plan_dir, "terraform plan")
            if not plan_result["success"]:
                return plan_result
            
            # Apply Terraform
            apply_result = await self._run_terraform_command(plan_dir, "terraform apply -auto-approve")
            
            return apply_result
            
        except Exception as e:
            return {"success": False, "error": str(e), "output": ""}
    
    async def _run_terraform_command(self, plan_dir: Path, command: str) -> Dict[str, Any]:
        """Run a Terraform command."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=plan_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": stderr.decode() if stderr else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "output": ""}
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.name == "create_infrastructure":
            analysis = await self.analyze_requirements(task.metadata.get("requirements", ""))
            plan = await self.generate_plan(analysis)
            return plan
        elif task.name == "execute_plan":
            return await self.execute_plan(task.metadata)
        elif task.name == "get_status":
            return await self._get_infrastructure_status()
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    async def _get_infrastructure_status(self) -> Dict[str, Any]:
        """Get current infrastructure status."""
        return {
            "plans_count": len(self.plans),
            "executions_count": len(self.executions),
            "active_executions": len([e for e in self.executions.values() if e.status == "running"]),
            "last_activity": max([p.created_at for p in self.plans.values()]) if self.plans else None
        }
