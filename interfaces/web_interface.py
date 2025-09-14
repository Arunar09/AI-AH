#!/usr/bin/env python3
"""
Web Interface for Intelligent Agents
Provides web-based interface with granular requirement gathering and real-time planning
"""

import sys
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
import threading
import time
import zipfile
import tempfile

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
intelligent_agents_dir = parent_dir / "intelligent-agents"
sys.path.insert(0, str(intelligent_agents_dir))

try:
    from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
    from core.reasoning.local_reasoning_engine import LocalReasoningEngine
except ImportError as e:
    print(f"Warning: Could not import agents: {e}")
    print("Running in demo mode without agent integration")
    IntelligentTerraformAgent = None
    LocalReasoningEngine = None

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

@dataclass
class Requirement:
    """Individual requirement with validation"""
    category: str
    question: str
    answer: str
    validation_rules: List[str]
    is_required: bool = True
    follow_up_questions: List[str] = None

@dataclass
class RequirementSet:
    """Complete set of requirements for a project"""
    project_name: str
    requirements: List[Requirement]
    validation_status: str = "pending"
    completeness_score: float = 0.0

class WebRequirementCollector:
    """Web-based requirement collector"""
    
    def __init__(self):
        self.requirement_templates = self._load_requirement_templates()
    
    def _load_requirement_templates(self) -> Dict[str, List[Dict]]:
        """Load requirement templates for different project types"""
        return {
            "web_application": [
                {
                    "category": "basic_info",
                    "question": "What is the name of your project?",
                    "type": "text",
                    "validation_rules": ["not_empty", "alphanumeric"],
                    "follow_up_questions": [
                        "What is the primary purpose of this application?",
                        "Who are the target users?"
                    ]
                },
                {
                    "category": "infrastructure",
                    "question": "Which cloud provider do you prefer?",
                    "type": "dropdown",
                    "options": ["AWS", "Azure", "GCP", "Multi-cloud"],
                    "validation_rules": ["one_of:aws,azure,gcp,multi-cloud"],
                    "follow_up_questions": [
                        "What is your preferred region?",
                        "Do you have existing infrastructure to integrate with?"
                    ]
                },
                {
                    "category": "scaling",
                    "question": "What is your expected user load?",
                    "type": "number",
                    "validation_rules": ["numeric_range:1-10000000"],
                    "follow_up_questions": [
                        "What is your peak traffic pattern?",
                        "Do you need auto-scaling?"
                    ]
                },
                {
                    "category": "budget",
                    "question": "What is your monthly budget?",
                    "type": "number",
                    "validation_rules": ["numeric_range:10-50000"]
                },
                {
                    "category": "security",
                    "question": "What are your security requirements?",
                    "type": "textarea",
                    "validation_rules": ["not_empty"]
                },
                {
                    "category": "availability",
                    "question": "What is your required uptime?",
                    "type": "dropdown",
                    "options": ["99.0%", "99.5%", "99.9%", "99.95%", "99.99%"],
                    "validation_rules": ["one_of:99.0%,99.5%,99.9%,99.95%,99.99%"]
                },
                {
                    "category": "monitoring",
                    "question": "What monitoring and alerting do you need?",
                    "type": "textarea",
                    "validation_rules": ["not_empty"]
                }
            ],
            "microservices": [
                {
                    "category": "architecture",
                    "question": "How many microservices do you plan to deploy?",
                    "type": "number",
                    "validation_rules": ["numeric_range:1-100"]
                },
                {
                    "category": "containerization",
                    "question": "Which container orchestration platform?",
                    "type": "dropdown",
                    "options": ["EKS", "AKS", "GKE", "ECS"],
                    "validation_rules": ["one_of:eks,aks,gke,ecs"]
                },
                {
                    "category": "communication",
                    "question": "What is the communication pattern between services?",
                    "type": "dropdown",
                    "options": ["REST API", "GraphQL", "gRPC", "Message Queue"],
                    "validation_rules": ["not_empty"]
                }
            ],
            "data_platform": [
                {
                    "category": "data_volume",
                    "question": "What is your expected data volume?",
                    "type": "number",
                    "validation_rules": ["numeric_range:1-1000000"]
                },
                {
                    "category": "analytics",
                    "question": "What type of analytics do you need?",
                    "type": "dropdown",
                    "options": ["Batch", "Streaming", "Interactive", "ML"],
                    "validation_rules": ["one_of:batch,streaming,interactive,ml"]
                },
                {
                    "category": "processing",
                    "question": "What is your data processing latency requirement?",
                    "type": "dropdown",
                    "options": ["Real-time (<1s)", "Near real-time (<1min)", "Batch (<1hour)", "Flexible"],
                    "validation_rules": ["not_empty"]
                }
            ]
        }

class WebScalingPlanner:
    """Web-based production scaling planner"""
    
    def __init__(self):
        self.scaling_templates = self._load_scaling_templates()
    
    def _load_scaling_templates(self) -> Dict[str, Dict]:
        """Load scaling templates for different scenarios"""
        return {
            "local_to_production": {
                "phases": [
                    {
                        "name": "Local Development Setup",
                        "duration": "1-2 days",
                        "steps": [
                            "Set up local development environment",
                            "Configure local database and services",
                            "Implement basic monitoring",
                            "Set up version control and CI/CD pipeline"
                        ]
                    },
                    {
                        "name": "Staging Environment",
                        "duration": "2-3 days",
                        "steps": [
                            "Deploy to staging environment",
                            "Configure staging infrastructure",
                            "Set up staging monitoring and alerting",
                            "Perform integration testing",
                            "Validate security configurations"
                        ]
                    },
                    {
                        "name": "Production Deployment",
                        "duration": "3-5 days",
                        "steps": [
                            "Deploy to production with blue-green strategy",
                            "Configure production monitoring",
                            "Set up backup and disaster recovery",
                            "Implement auto-scaling policies",
                            "Configure security hardening"
                        ]
                    },
                    {
                        "name": "Post-Production Optimization",
                        "duration": "1-2 weeks",
                        "steps": [
                            "Monitor performance and optimize",
                            "Implement cost optimization",
                            "Set up advanced monitoring",
                            "Configure alerting and incident response",
                            "Document operational procedures"
                        ]
                    }
                ]
            }
        }
    
    def generate_scaling_plan(self, requirements: Dict) -> Dict:
        """Generate production scaling plan"""
        scaling_needs = self._analyze_scaling_needs(requirements)
        
        plan = {
            "current_state": "local",
            "target_state": "production",
            "scaling_needs": scaling_needs,
            "phases": self._customize_phases(scaling_needs),
            "estimated_duration": self._calculate_duration(scaling_needs),
            "cost_implications": self._calculate_cost_implications(scaling_needs),
            "risk_assessment": self._assess_risks(scaling_needs),
            "success_metrics": self._define_success_metrics(scaling_needs)
        }
        
        return plan
    
    def _analyze_scaling_needs(self, requirements: Dict) -> Dict:
        """Analyze requirements to determine scaling needs"""
        needs = {
            "infrastructure_complexity": "low",
            "security_requirements": "standard",
            "availability_requirements": "standard",
            "monitoring_needs": "basic",
            "compliance_requirements": "none"
        }
        
        for req in requirements.get('requirements', []):
            if req.get('category') == "security" and any(keyword in req.get('answer', '').lower() for keyword in ["compliance", "hipaa", "pci", "soc2"]):
                needs["security_requirements"] = "high"
                needs["compliance_requirements"] = "required"
            
            if req.get('category') == "availability" and "99.9" in req.get('answer', ''):
                needs["availability_requirements"] = "high"
            
            if req.get('category') == "monitoring" and any(keyword in req.get('answer', '').lower() for keyword in ["advanced", "apm", "ml"]):
                needs["monitoring_needs"] = "advanced"
        
        return needs
    
    def _customize_phases(self, scaling_needs: Dict) -> List[Dict]:
        """Customize phases based on scaling needs"""
        base_phases = self.scaling_templates["local_to_production"]["phases"]
        
        if scaling_needs["security_requirements"] == "high":
            base_phases.insert(2, {
                "name": "Security Hardening",
                "duration": "2-3 days",
                "steps": [
                    "Implement security controls",
                    "Configure compliance monitoring",
                    "Set up security scanning",
                    "Validate security configurations"
                ]
            })
        
        if scaling_needs["monitoring_needs"] == "advanced":
            base_phases.append({
                "name": "Advanced Monitoring Setup",
                "duration": "1-2 days",
                "steps": [
                    "Configure APM tools",
                    "Set up ML-based monitoring",
                    "Implement predictive alerting",
                    "Configure log analysis"
                ]
            })
        
        return base_phases
    
    def _calculate_duration(self, scaling_needs: Dict) -> str:
        """Calculate estimated duration"""
        base_days = 7
        
        if scaling_needs["security_requirements"] == "high":
            base_days += 3
        
        if scaling_needs["monitoring_needs"] == "advanced":
            base_days += 2
        
        if scaling_needs["availability_requirements"] == "high":
            base_days += 2
        
        return f"{base_days}-{base_days + 3} days"
    
    def _calculate_cost_implications(self, scaling_needs: Dict) -> Dict:
        """Calculate cost implications"""
        return {
            "development_cost": "$5,000 - $15,000",
            "infrastructure_cost": "$500 - $2,000/month",
            "monitoring_cost": "$100 - $500/month",
            "security_cost": "$200 - $1,000/month" if scaling_needs["security_requirements"] == "high" else "$50 - $200/month"
        }
    
    def _assess_risks(self, scaling_needs: Dict) -> List[str]:
        """Assess risks"""
        risks = [
            "Data migration complexity",
            "Downtime during deployment",
            "Performance degradation",
            "Security vulnerabilities"
        ]
        
        if scaling_needs["availability_requirements"] == "high":
            risks.append("High availability configuration complexity")
        
        if scaling_needs["compliance_requirements"] == "required":
            risks.append("Compliance validation requirements")
        
        return risks
    
    def _define_success_metrics(self, scaling_needs: Dict) -> List[str]:
        """Define success metrics"""
        metrics = [
            "Zero data loss during migration",
            "99.9% uptime during deployment",
            "Performance within 10% of baseline",
            "All security controls implemented"
        ]
        
        if scaling_needs["availability_requirements"] == "high":
            metrics.append("99.99% uptime achieved")
        
        return metrics

# Initialize components
requirement_collector = WebRequirementCollector()
scaling_planner = WebScalingPlanner()
agents = {}
if IntelligentTerraformAgent:
    agents["terraform"] = IntelligentTerraformAgent()

# Workspace management
WORKSPACE_BASE = Path(__file__).parent / "workspaces"
WORKSPACE_BASE.mkdir(exist_ok=True)

def create_project_workspace(project_name: str, terraform_code: Dict[str, str], requirements: Dict, scaling_plan: Dict = None) -> str:
    """Create a project workspace with all files"""
    # Clean project name for filesystem
    safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_').lower()
    
    # Create project directory
    project_dir = WORKSPACE_BASE / safe_name
    project_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    terraform_dir = project_dir / "terraform"
    docs_dir = project_dir / "docs"
    scripts_dir = project_dir / "scripts"
    
    terraform_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)
    scripts_dir.mkdir(exist_ok=True)
    
    # Save Terraform files with proper formatting
    for filename, content in terraform_code.items():
        terraform_file = terraform_dir / filename
        
        # Clean and format the content
        formatted_content = content.strip()
        
        # Ensure proper line endings and indentation
        lines = formatted_content.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            # Adjust indentation based on Terraform syntax
            if line.endswith('{'):
                formatted_lines.append('  ' * indent_level + line)
                indent_level += 1
            elif line.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('  ' * indent_level + line)
            else:
                formatted_lines.append('  ' * indent_level + line)
        
        formatted_content = '\n'.join(formatted_lines)
        
        with open(terraform_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
    
    # Save project requirements
    requirements_file = docs_dir / "requirements.json"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        json.dump(requirements, f, indent=2)
    
    # Save scaling plan if provided
    if scaling_plan:
        scaling_file = docs_dir / "scaling_plan.json"
        with open(scaling_file, 'w', encoding='utf-8') as f:
            json.dump(scaling_plan, f, indent=2)
    
    # Create README
    readme_content = f"""# {project_name}

## Project Overview
This project was generated by the Intelligent Infrastructure Agent.

## Files Structure
```
{project_name}/
├── terraform/           # Terraform configuration files
│   ├── main.tf         # Main infrastructure definition
│   ├── variables.tf    # Variable definitions
│   ├── outputs.tf      # Output definitions
│   └── terraform.tfvars # Variable values
├── docs/               # Documentation
│   ├── requirements.json # Project requirements
│   └── scaling_plan.json # Production scaling plan
├── scripts/            # Deployment scripts
└── README.md          # This file
```

## Quick Start

1. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review the plan:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

## Requirements
- Terraform >= 1.0
- AWS CLI configured
- Appropriate AWS permissions

## Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    readme_file = project_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create deployment script
    deploy_script = f"""#!/bin/bash
# Deployment script for {project_name}
# Generated by Intelligent Infrastructure Agent

set -e

echo "🚀 Deploying {project_name}..."

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install Terraform first."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Navigate to terraform directory
cd terraform

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan

# Ask for confirmation
read -p "Do you want to apply this configuration? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏗️ Applying configuration..."
    terraform apply -auto-approve
    echo "✅ Deployment completed!"
    
    # Show outputs
    echo "📊 Infrastructure outputs:"
    terraform output
else
    echo "❌ Deployment cancelled."
fi
"""
    
    deploy_file = scripts_dir / "deploy.sh"
    with open(deploy_file, 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    # Make deploy script executable
    os.chmod(deploy_file, 0o755)
    
    return str(project_dir)

def create_project_zip(project_dir: str) -> str:
    """Create a zip file of the project"""
    project_path = Path(project_dir)
    zip_path = f"{project_dir}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Create relative path from project directory
                arcname = os.path.relpath(file_path, project_path.parent)
                zipf.write(file_path, arcname)
    
    return zip_path

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Favicon route"""
    return '', 204  # No content

@app.route('/project-types')
def project_types():
    """Get available project types"""
    return jsonify({
        "project_types": list(requirement_collector.requirement_templates.keys())
    })

@app.route('/requirements/<project_type>')
def get_requirements(project_type):
    """Get requirements for a project type"""
    try:
        if project_type not in requirement_collector.requirement_templates:
            return jsonify({"error": "Invalid project type"}), 400
        
        return jsonify({
            "requirements": requirement_collector.requirement_templates[project_type]
        })
    except Exception as e:
        return jsonify({"error": f"Error loading requirements: {str(e)}"}), 500

@app.route('/validate-requirement', methods=['POST'])
def validate_requirement():
    """Validate a single requirement"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        answer = data.get('answer', '')
        validation_rules = data.get('validation_rules', [])
        
        is_valid = _validate_answer(answer, validation_rules)
        
        return jsonify({
            "is_valid": is_valid,
            "message": "Valid" if is_valid else "Invalid"
        })
    except Exception as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 500

def _validate_answer(answer: str, rules: List[str]) -> bool:
    """Validate answer against rules"""
    if not answer and "not_empty" in rules:
        return False
    
    for rule in rules:
        if rule.startswith("one_of:"):
            options = rule.split(":")[1].split(",")
            # Normalize both answer and options for comparison
            answer_normalized = answer.strip().lower()
            options_normalized = [opt.strip().lower() for opt in options]
            
            if answer_normalized not in options_normalized:
                return False
        elif rule.startswith("numeric_range:"):
            try:
                # Remove percentage symbols for numeric validation
                clean_answer = answer.replace('%', '').strip()
                value = float(clean_answer)
                range_str = rule.split(":")[1]
                min_val, max_val = map(float, range_str.split("-"))
                if not (min_val <= value <= max_val):
                    return False
            except ValueError:
                return False
    
    return True

@app.route('/process-requirements', methods=['POST'])
def process_requirements():
    """Process requirements with agent"""
    data = request.json
    project_type = data.get('project_type')
    requirements = data.get('requirements', [])
    
    if not agents:
        return jsonify({
            "error": "No agents available",
            "demo_mode": True,
            "message": "This would normally process your requirements with an intelligent agent."
        })
    
    # Generate request from requirements
    request_parts = []
    
    # Handle both list format and dict format
    if isinstance(requirements, dict):
        # Convert dict to list format
        for key, value in requirements.items():
            if value:
                request_parts.append(f"{key.replace('_', ' ').title()}: {value}")
    else:
        # Handle list format
        for req in requirements:
            if isinstance(req, dict) and req.get('answer'):
                request_parts.append(f"{req['question']}: {req['answer']}")
    
    request_text = "\n".join(request_parts)
    
    # Process with agent
    try:
        agent = agents["terraform"]
        response = agent.process_request(request_text)
        
        return jsonify({
            "success": True,
            "response": {
                "cost_estimate": response.cost_estimate,
                "confidence": response.confidence,
                "implementation_steps": response.implementation_steps,
                "terraform_code": response.terraform_code,
                "content": response.content,
                "reasoning_steps": response.reasoning_steps
            }
        })
    except Exception as e:
        return jsonify({
            "error": f"Agent processing failed: {str(e)}"
        }), 500

@app.route('/generate-scaling-plan', methods=['POST'])
def generate_scaling_plan():
    """Generate production scaling plan"""
    data = request.json
    requirements = data.get('requirements', {})
    
    try:
        scaling_plan = scaling_planner.generate_scaling_plan(requirements)
        return jsonify({
            "success": True,
            "scaling_plan": scaling_plan
        })
    except Exception as e:
        return jsonify({
            "error": f"Scaling plan generation failed: {str(e)}"
        }), 500

@app.route('/troubleshooting')
def troubleshooting():
    """Troubleshooting page"""
    return render_template('troubleshooting.html')

@app.route('/troubleshooting-categories')
def troubleshooting_categories():
    """Get troubleshooting categories"""
    categories = {
        "infrastructure": [
            "Terraform state is locked",
            "Resource already exists error",
            "Permission denied errors",
            "Circular dependency error"
        ],
        "deployment": [
            "Build pipeline failures",
            "Deployment timeouts",
            "Service startup issues",
            "Environment configuration"
        ],
        "performance": [
            "Slow response times",
            "High CPU usage",
            "Memory leaks",
            "Database performance"
        ],
        "security": [
            "Access control issues",
            "Certificate problems",
            "Compliance violations",
            "Vulnerability scanning"
        ],
        "cost": [
            "Unexpected charges",
            "Resource optimization",
            "Budget overruns",
            "Cost analysis"
        ]
    }
    
    return jsonify(categories)

@app.route('/troubleshooting-solution/<category>/<issue>')
def get_troubleshooting_solution(category, issue):
    """Get troubleshooting solution for specific issue"""
    solutions = {
        "Terraform state is locked": {
            "diagnosis": "Terraform state is locked, likely by another process or team member",
            "solutions": [
                "Check for running Terraform processes: `ps aux | grep terraform`",
                "Use force unlock: `terraform force-unlock <lock-id>`",
                "Check with team members if they're running Terraform",
                "Verify no CI/CD pipeline is running Terraform"
            ],
            "prevention": [
                "Use remote state with locking (S3 + DynamoDB)",
                "Implement proper CI/CD pipeline coordination",
                "Use Terraform workspaces for team collaboration"
            ]
        },
        "Resource already exists error": {
            "diagnosis": "Resource already exists in AWS but not in Terraform state",
            "solutions": [
                "Import existing resource: `terraform import <resource_type>.<name> <resource_id>`",
                "Check AWS console for existing resources",
                "Use `terraform plan` to see what will be created",
                "Consider using data sources instead of resources"
            ],
            "prevention": [
                "Always use `terraform plan` before `terraform apply`",
                "Keep Terraform state in sync with actual infrastructure",
                "Use consistent naming conventions"
            ]
        }
    }
    
    solution = solutions.get(issue, {
        "diagnosis": "This is a complex issue that requires detailed analysis",
        "solutions": [
            "Gather more information about the specific error",
            "Check logs and monitoring data",
            "Consult documentation and best practices",
            "Contact support if needed"
        ],
        "prevention": [
            "Follow best practices and guidelines",
            "Implement proper monitoring and alerting",
            "Regular testing and validation",
            "Keep documentation up to date"
        ]
    })
    
    return jsonify(solution)

@app.route('/create-workspace', methods=['POST'])
def create_workspace():
    """Create a project workspace with all files"""
    try:
        data = request.json
        project_name = data.get('project_name', 'untitled_project')
        terraform_code = data.get('terraform_code', {})
        requirements = data.get('requirements', {})
        scaling_plan = data.get('scaling_plan')
        
        # Create workspace
        project_dir = create_project_workspace(project_name, terraform_code, requirements, scaling_plan)
        
        return jsonify({
            "success": True,
            "workspace_path": project_dir,
            "message": f"Workspace created successfully at {project_dir}"
        })
    except Exception as e:
        return jsonify({
            "error": f"Failed to create workspace: {str(e)}"
        }), 500

@app.route('/download-project/<project_name>')
def download_project(project_name):
    """Download project as zip file"""
    try:
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        project_dir = WORKSPACE_BASE / safe_name
        
        if not project_dir.exists():
            return jsonify({"error": "Project not found"}), 404
        
        # Create zip file
        zip_path = create_project_zip(str(project_dir))
        
        # Check if zip file was created successfully
        if not os.path.exists(zip_path):
            return jsonify({"error": "Failed to create zip file"}), 500
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{safe_name}.zip",
            mimetype='application/zip'
        )
    except Exception as e:
        return jsonify({"error": f"Failed to download project: {str(e)}"}), 500

@app.route('/list-projects')
def list_projects():
    """List all created projects"""
    try:
        projects = []
        for project_dir in WORKSPACE_BASE.iterdir():
            if project_dir.is_dir():
                readme_file = project_dir / "README.md"
                created_time = project_dir.stat().st_ctime
                
                projects.append({
                    "name": project_dir.name,
                    "path": str(project_dir),
                    "created": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_time)),
                    "has_readme": readme_file.exists()
                })
        
        return jsonify({
            "success": True,
            "projects": projects
        })
    except Exception as e:
        return jsonify({"error": f"Failed to list projects: {str(e)}"}), 500

@app.route('/project/<project_name>')
def get_project_details(project_name):
    """Get project details and file structure"""
    try:
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_').lower()
        
        project_dir = WORKSPACE_BASE / safe_name
        
        if not project_dir.exists():
            return jsonify({"error": "Project not found"}), 404
        
        # Get file structure
        files = []
        for root, dirs, filenames in os.walk(project_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, project_dir)
                files.append({
                    "name": filename,
                    "path": rel_path,
                    "size": os.path.getsize(file_path)
                })
        
        return jsonify({
            "success": True,
            "project_name": safe_name,
            "project_path": str(project_dir),
            "files": files
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get project details: {str(e)}"}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Create static directory if it doesn't exist
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
