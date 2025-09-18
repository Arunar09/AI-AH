#!/usr/bin/env python3
"""
Enhanced Web Interface for Multi-Agent AI System
Comprehensive interface with task management, multi-agent support, and advanced requirement collection
"""

import sys
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
import threading
import time
import zipfile
import tempfile
import logging
from datetime import datetime
from enum import Enum

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
intelligent_agents_dir = parent_dir / "intelligent-agents"
sys.path.insert(0, str(intelligent_agents_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
    from core.reasoning.local_reasoning_engine import LocalReasoningEngine
except ImportError as e:
    logger.warning(f"Could not import agents: {e}")
    logger.info("Running in demo mode without agent integration")
    IntelligentTerraformAgent = None
    LocalReasoningEngine = None

app = Flask(__name__)
app.secret_key = 'enhanced-ai-agent-hub-2024'  # Change this in production

# Disable Flask's auto-reloader to prevent excessive reloading
app.config['TEMPLATES_AUTO_RELOAD'] = False

class AgentType(Enum):
    """Available agent types"""
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"
    KUBERNETES = "kubernetes"
    SECURITY = "security"
    MONITORING = "monitoring"
    COST_OPTIMIZATION = "cost_optimization"

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AgentCapability:
    """Agent capability definition"""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    parameters: Dict[str, Any]
    examples: List[str]

@dataclass
class Task:
    """Task definition for agent execution"""
    id: str
    name: str
    description: str
    agent_type: AgentType
    priority: TaskPriority
    status: TaskStatus
    parameters: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

@dataclass
class Project:
    """Project definition"""
    id: str
    name: str
    description: str
    requirements: Dict[str, Any]
    tasks: List[Task]
    created_at: datetime
    updated_at: datetime
    status: str = "active"

@dataclass
class RequirementTemplate:
    """Enhanced requirement template with better validation"""
    id: str
    category: str
    question: str
    description: str
    input_type: str  # text, number, select, multi_select, file, boolean
    options: List[str] = None
    validation_rules: Dict[str, Any] = None
    is_required: bool = True
    dependencies: List[str] = None
    help_text: str = ""
    examples: List[str] = None

class EnhancedWebInterface:
    """Enhanced web interface with comprehensive features"""
    
    def __init__(self):
        self.agents = {}
        self.projects = {}
        self.tasks = {}
        self.requirement_templates = self._load_requirement_templates()
        self.agent_capabilities = self._load_agent_capabilities()
        
        # Initialize available agents
        self._initialize_agents()
        
        # Create workspace directory
        self.workspace_base = Path("interfaces/workspaces")
        self.workspace_base.mkdir(exist_ok=True)
    
    def _initialize_agents(self):
        """Initialize available agents"""
        if IntelligentTerraformAgent:
            self.agents[AgentType.TERRAFORM] = IntelligentTerraformAgent()
            logger.info("✅ Terraform Agent initialized")
        
        # Placeholder for future agents
        self.agents[AgentType.ANSIBLE] = None  # Will be implemented
        self.agents[AgentType.KUBERNETES] = None  # Will be implemented
        self.agents[AgentType.SECURITY] = None  # Will be implemented
        self.agents[AgentType.MONITORING] = None  # Will be implemented
        self.agents[AgentType.COST_OPTIMIZATION] = None  # Will be implemented
    
    def _load_requirement_templates(self) -> Dict[str, RequirementTemplate]:
        """Load comprehensive requirement templates"""
        templates = {
            "project_basic": RequirementTemplate(
                id="project_basic",
                category="Project Information",
                question="Project Name",
                description="Enter a descriptive name for your project",
                input_type="text",
                validation_rules={"min_length": 3, "max_length": 50, "pattern": r"^[a-zA-Z0-9\s\-_]+$"},
                help_text="Use alphanumeric characters, spaces, hyphens, and underscores only",
                examples=["my-web-app", "e-commerce-platform", "data-analytics-system"]
            ),
            "project_description": RequirementTemplate(
                id="project_description",
                category="Project Information",
                question="Project Description",
                description="Describe what your project does and its main purpose",
                input_type="text",
                validation_rules={"min_length": 10, "max_length": 500},
                help_text="Provide a clear, concise description of your project's purpose and functionality",
                examples=["A scalable e-commerce platform for online retail", "A data analytics dashboard for business intelligence"]
            ),
            "cloud_provider": RequirementTemplate(
                id="cloud_provider",
                category="Infrastructure",
                question="Cloud Provider",
                description="Select your preferred cloud provider",
                input_type="select",
                options=["AWS", "Azure", "Google Cloud", "Multi-Cloud"],
                validation_rules={"required": True},
                help_text="Choose the cloud provider where you want to deploy your infrastructure"
            ),
            "deployment_region": RequirementTemplate(
                id="deployment_region",
                category="Infrastructure",
                question="Deployment Region",
                description="Select the primary deployment region",
                input_type="select",
                options=["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "ap-northeast-1"],
                validation_rules={"required": True},
                help_text="Choose the region closest to your users for optimal performance"
            ),
            "user_load": RequirementTemplate(
                id="user_load",
                category="Performance",
                question="Expected User Load",
                description="How many concurrent users do you expect?",
                input_type="select",
                options=["< 100", "100-1,000", "1,000-10,000", "10,000-100,000", "> 100,000"],
                validation_rules={"required": True},
                help_text="This helps determine the appropriate infrastructure scaling"
            ),
            "budget": RequirementTemplate(
                id="budget",
                category="Cost",
                question="Monthly Budget (USD)",
                description="What's your monthly infrastructure budget?",
                input_type="select",
                options=["< $100", "$100-500", "$500-1,000", "$1,000-5,000", "$5,000-10,000", "> $10,000"],
                validation_rules={"required": True},
                help_text="This helps optimize infrastructure costs within your budget"
            ),
            "uptime_requirement": RequirementTemplate(
                id="uptime_requirement",
                category="Reliability",
                question="Uptime Requirement",
                description="What uptime percentage do you need?",
                input_type="select",
                options=["99.0%", "99.5%", "99.9%", "99.95%", "99.99%"],
                validation_rules={"required": True},
                help_text="Higher uptime requirements may require additional redundancy and monitoring"
            ),
            "security_level": RequirementTemplate(
                id="security_level",
                category="Security",
                question="Security Level",
                description="What level of security do you need?",
                input_type="select",
                options=["Basic", "Standard", "High", "Enterprise", "Compliance"],
                validation_rules={"required": True},
                help_text="Higher security levels include additional encryption, monitoring, and compliance features"
            ),
            "compliance_requirements": RequirementTemplate(
                id="compliance_requirements",
                category="Compliance",
                question="Compliance Requirements",
                description="Do you have any compliance requirements?",
                input_type="multi_select",
                options=["GDPR", "HIPAA", "SOC 2", "PCI DSS", "ISO 27001", "None"],
                validation_rules={"required": False},
                help_text="Select all applicable compliance standards"
            ),
            "database_type": RequirementTemplate(
                id="database_type",
                category="Data",
                question="Database Type",
                description="What type of database do you need?",
                input_type="select",
                options=["Relational (PostgreSQL/MySQL)", "NoSQL (MongoDB/DynamoDB)", "Both", "Not sure"],
                validation_rules={"required": True},
                help_text="Choose based on your data structure and query patterns"
            ),
            "storage_requirements": RequirementTemplate(
                id="storage_requirements",
                category="Storage",
                question="Storage Requirements",
                description="What type of storage do you need?",
                input_type="multi_select",
                options=["File Storage", "Object Storage", "Block Storage", "Database Storage", "Backup Storage"],
                validation_rules={"required": True},
                help_text="Select all storage types your application requires"
            ),
            "monitoring_needs": RequirementTemplate(
                id="monitoring_needs",
                category="Monitoring",
                question="Monitoring Requirements",
                description="What do you want to monitor?",
                input_type="multi_select",
                options=["Application Performance", "Infrastructure Health", "Security Events", "Cost Tracking", "User Analytics"],
                validation_rules={"required": False},
                help_text="Select all monitoring capabilities you need"
            )
        }
        return templates
    
    def _load_agent_capabilities(self) -> Dict[AgentType, AgentCapability]:
        """Load agent capabilities"""
        capabilities = {
            AgentType.TERRAFORM: AgentCapability(
                name="Terraform Agent",
                description="Generates and manages infrastructure as code using Terraform",
                input_types=["requirements", "architecture_patterns", "cost_constraints"],
                output_types=["terraform_files", "deployment_scripts", "cost_estimates"],
                parameters={
                    "cloud_provider": "string",
                    "region": "string",
                    "budget": "number",
                    "security_level": "string"
                },
                examples=[
                    "Generate AWS infrastructure for a web application",
                    "Create a multi-tier architecture with load balancers",
                    "Set up auto-scaling groups for high availability"
                ]
            ),
            AgentType.ANSIBLE: AgentCapability(
                name="Ansible Agent",
                description="Manages configuration and deployment automation",
                input_types=["server_configs", "application_deployments", "system_updates"],
                output_types=["playbooks", "inventories", "deployment_scripts"],
                parameters={
                    "target_servers": "list",
                    "configuration_type": "string",
                    "deployment_strategy": "string"
                },
                examples=[
                    "Configure web servers with Nginx and SSL",
                    "Deploy application updates across multiple servers",
                    "Set up monitoring agents on all servers"
                ]
            ),
            AgentType.KUBERNETES: AgentCapability(
                name="Kubernetes Agent",
                description="Manages container orchestration and microservices",
                input_types=["container_images", "service_definitions", "scaling_requirements"],
                output_types=["manifests", "helm_charts", "deployment_configs"],
                parameters={
                    "namespace": "string",
                    "replicas": "number",
                    "resources": "object"
                },
                examples=[
                    "Deploy microservices with auto-scaling",
                    "Set up service mesh for inter-service communication",
                    "Configure ingress controllers and load balancing"
                ]
            )
        }
        return capabilities
    
    def create_project(self, name: str, description: str, requirements: Dict[str, Any]) -> Project:
        """Create a new project"""
        project_id = f"proj_{int(time.time())}"
        project = Project(
            id=project_id,
            name=name,
            description=description,
            requirements=requirements,
            tasks=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.projects[project_id] = project
        return project
    
    def create_task(self, project_id: str, name: str, description: str, 
                   agent_type: AgentType, priority: TaskPriority, 
                   parameters: Dict[str, Any]) -> Task:
        """Create a new task for an agent"""
        task_id = f"task_{int(time.time())}"
        task = Task(
            id=task_id,
            name=name,
            description=description,
            agent_type=agent_type,
            priority=priority,
            status=TaskStatus.PENDING,
            parameters=parameters,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.tasks[task_id] = task
        
        if project_id in self.projects:
            self.projects[project_id].tasks.append(task)
        
        return task
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a task using the appropriate agent"""
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = TaskStatus.IN_PROGRESS
        task.updated_at = datetime.now()
        
        try:
            agent = self.agents.get(task.agent_type)
            if not agent:
                raise Exception(f"Agent {task.agent_type.value} not available")
            
            # Execute task based on agent type
            if task.agent_type == AgentType.TERRAFORM:
                result = self._execute_terraform_task(task)
            else:
                result = {"error": f"Agent {task.agent_type.value} not implemented yet"}
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.updated_at = datetime.now()
            
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.now()
            return {"error": str(e)}
    
    def _execute_terraform_task(self, task: Task) -> Dict[str, Any]:
        """Execute a Terraform task"""
        agent = self.agents[AgentType.TERRAFORM]
        
        # Convert task parameters to agent request format
        request_text = self._format_terraform_request(task.parameters)
        
        # Execute the agent
        response = agent.process_request(request_text)
        
        return {
            "confidence": response.confidence,
            "cost_estimate": response.cost_estimate,
            "terraform_code": response.terraform_code,
            "reasoning": response.reasoning,
            "files_generated": len(response.terraform_code)
        }
    
    def _format_terraform_request(self, parameters: Dict[str, Any]) -> str:
        """Format parameters as a request string for Terraform agent"""
        request_parts = []
        for key, value in parameters.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            request_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(request_parts)

# Initialize the enhanced interface
enhanced_interface = EnhancedWebInterface()

# Flask Routes
@app.route('/')
def index():
    """Main dashboard"""
    return render_template('enhanced_index.html', 
                         agents=enhanced_interface.agents,
                         projects=enhanced_interface.projects,
                         capabilities=enhanced_interface.agent_capabilities)

@app.route('/api/requirement-templates')
def get_requirement_templates():
    """Get all requirement templates"""
    templates = {}
    for template_id, template in enhanced_interface.requirement_templates.items():
        templates[template_id] = asdict(template)
    return jsonify(templates)

@app.route('/api/agent-capabilities')
def get_agent_capabilities():
    """Get all agent capabilities"""
    capabilities = {}
    for agent_type, capability in enhanced_interface.agent_capabilities.items():
        capabilities[agent_type.value] = asdict(capability)
    return jsonify(capabilities)

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    
    project = enhanced_interface.create_project(
        name=data['name'],
        description=data['description'],
        requirements=data['requirements']
    )
    
    return jsonify({
        "success": True,
        "project": asdict(project)
    })

@app.route('/api/projects/<project_id>/tasks', methods=['POST'])
def create_task(project_id):
    """Create a new task for a project"""
    data = request.get_json()
    
    task = enhanced_interface.create_task(
        project_id=project_id,
        name=data['name'],
        description=data['description'],
        agent_type=AgentType(data['agent_type']),
        priority=TaskPriority(data['priority']),
        parameters=data['parameters']
    )
    
    return jsonify({
        "success": True,
        "task": asdict(task)
    })

@app.route('/api/tasks/<task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """Execute a task"""
    result = enhanced_interface.execute_task(task_id)
    return jsonify(result)

@app.route('/api/tasks/<task_id>')
def get_task(task_id):
    """Get task details"""
    if task_id in enhanced_interface.tasks:
        return jsonify(asdict(enhanced_interface.tasks[task_id]))
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/projects')
def get_projects():
    """Get all projects"""
    projects = {}
    for project_id, project in enhanced_interface.projects.items():
        projects[project_id] = asdict(project)
    return jsonify(projects)

@app.route('/api/validate-requirement', methods=['POST'])
def validate_requirement():
    """Validate a requirement value"""
    data = request.get_json()
    template_id = data.get('template_id')
    value = data.get('value')
    
    if template_id not in enhanced_interface.requirement_templates:
        return jsonify({"valid": False, "error": "Template not found"})
    
    template = enhanced_interface.requirement_templates[template_id]
    validation_result = _validate_requirement_value(template, value)
    
    return jsonify(validation_result)

def _validate_requirement_value(template: RequirementTemplate, value: str) -> Dict[str, Any]:
    """Validate a requirement value against its template"""
    if template.is_required and not value:
        return {"valid": False, "error": f"{template.question} is required"}
    
    if not value:
        return {"valid": True}
    
    rules = template.validation_rules or {}
    
    # Check minimum length
    if "min_length" in rules and len(value) < rules["min_length"]:
        return {"valid": False, "error": f"Minimum length is {rules['min_length']} characters"}
    
    # Check maximum length
    if "max_length" in rules and len(value) > rules["max_length"]:
        return {"valid": False, "error": f"Maximum length is {rules['max_length']} characters"}
    
    # Check pattern
    if "pattern" in rules:
        import re
        if not re.match(rules["pattern"], value):
            return {"valid": False, "error": "Invalid format"}
    
    # Check options for select types
    if template.input_type == "select" and template.options:
        if value not in template.options:
            return {"valid": False, "error": f"Must be one of: {', '.join(template.options)}"}
    
    return {"valid": True}

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return '', 204

if __name__ == '__main__':
    print("🚀 Starting Enhanced Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run with debug=False to prevent excessive reloading
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

