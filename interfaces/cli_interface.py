#!/usr/bin/env python3
"""
CLI Interface for Intelligent Agents
Provides interactive command-line interface with granular requirement gathering
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

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

class RequirementCollector:
    """Collects and validates requirements through interactive CLI"""
    
    def __init__(self):
        self.requirement_templates = self._load_requirement_templates()
        self.current_requirements = []
        
    def _load_requirement_templates(self) -> Dict[str, List[Dict]]:
        """Load requirement templates for different project types"""
        return {
            "web_application": [
                {
                    "category": "basic_info",
                    "question": "What is the name of your project?",
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
                    "validation_rules": ["numeric_range:1-10000000"],
                    "follow_up_questions": [
                        "What is your peak traffic pattern?",
                        "Do you need auto-scaling?",
                        "What is your growth projection for the next 12 months?"
                    ]
                },
                {
                    "category": "budget",
                    "question": "What is your monthly budget?",
                    "validation_rules": ["numeric_range:10-50000"],
                    "follow_up_questions": [
                        "Are there any cost optimization requirements?",
                        "Do you need reserved instances or spot instances?"
                    ]
                },
                {
                    "category": "security",
                    "question": "What are your security requirements?",
                    "validation_rules": ["not_empty"],
                    "follow_up_questions": [
                        "Do you need compliance certifications? (SOC2, HIPAA, PCI-DSS)",
                        "What is your data classification level?",
                        "Do you need encryption at rest and in transit?"
                    ]
                },
                {
                    "category": "availability",
                    "question": "What is your required uptime?",
                    "type": "dropdown",
                    "options": ["99.0%", "99.5%", "99.9%", "99.95%", "99.99%"],
                    "validation_rules": ["one_of:99.0,99.5,99.9,99.95,99.99"],
                    "follow_up_questions": [
                        "Do you need multi-region deployment?",
                        "What is your disaster recovery requirement?",
                        "What is your maximum acceptable downtime?"
                    ]
                },
                {
                    "category": "monitoring",
                    "question": "What monitoring and alerting do you need?",
                    "validation_rules": ["not_empty"],
                    "follow_up_questions": [
                        "Do you need application performance monitoring?",
                        "What are your key performance indicators?",
                        "Do you need log aggregation and analysis?"
                    ]
                }
            ],
            "microservices": [
                {
                    "category": "architecture",
                    "question": "How many microservices do you plan to deploy?",
                    "validation_rules": ["numeric_range:1-100"],
                    "follow_up_questions": [
                        "What is the communication pattern between services?",
                        "Do you need service mesh?",
                        "What is your API gateway requirement?"
                    ]
                },
                {
                    "category": "containerization",
                    "question": "Which container orchestration platform? (EKS/AKS/GKE/ECS)",
                    "validation_rules": ["one_of:eks,aks,gke,ecs"],
                    "follow_up_questions": [
                        "What is your container registry preference?",
                        "Do you need container security scanning?",
                        "What is your CI/CD pipeline requirement?"
                    ]
                }
            ],
            "data_platform": [
                {
                    "category": "data_volume",
                    "question": "What is your expected data volume?",
                    "validation_rules": ["numeric_range:1-1000000"],
                    "follow_up_questions": [
                        "What is your data growth rate?",
                        "Do you need real-time processing?",
                        "What is your data retention policy?"
                    ]
                },
                {
                    "category": "analytics",
                    "question": "What type of analytics do you need?",
                    "validation_rules": ["one_of:batch,streaming,interactive,ml"],
                    "follow_up_questions": [
                        "Do you need machine learning capabilities?",
                        "What is your data processing latency requirement?",
                        "Do you need data visualization tools?"
                    ]
                }
            ]
        }
    
    def collect_requirements(self, project_type: str) -> RequirementSet:
        """Collect requirements interactively"""
        print(f"\n🔍 Collecting Requirements for {project_type.replace('_', ' ').title()}")
        print("=" * 60)
        
        if project_type not in self.requirement_templates:
            raise ValueError(f"Unknown project type: {project_type}")
        
        requirements = []
        template = self.requirement_templates[project_type]
        
        for req_template in template:
            requirement = self._collect_single_requirement(req_template)
            requirements.append(requirement)
            
            # Ask follow-up questions
            if requirement.follow_up_questions:
                for follow_up in requirement.follow_up_questions:
                    follow_up_req = self._collect_follow_up_requirement(follow_up, requirement.category)
                    requirements.append(follow_up_req)
        
        # Calculate completeness score
        total_questions = len(requirements)
        answered_questions = sum(1 for req in requirements if req.answer.strip())
        completeness_score = (answered_questions / total_questions) * 100
        
        return RequirementSet(
            project_name=requirements[0].answer if requirements else "Unknown",
            requirements=requirements,
            completeness_score=completeness_score
        )
    
    def _collect_single_requirement(self, template: Dict) -> Requirement:
        """Collect a single requirement with validation"""
        while True:
            print(f"\n❓ {template['question']}")
            
            # Show dropdown options if available
            if template.get('type') == 'dropdown' and template.get('options'):
                print("   Available options:")
                for i, option in enumerate(template['options'], 1):
                    print(f"   {i}. {option}")
                print("   Or type the option directly")
            
            if template.get('validation_rules'):
                print(f"   Validation: {', '.join(template['validation_rules'])}")
            
            answer = input("💬 Your answer: ").strip()
            
            # Handle dropdown selection by number
            if template.get('type') == 'dropdown' and template.get('options') and answer.isdigit():
                try:
                    option_index = int(answer) - 1
                    if 0 <= option_index < len(template['options']):
                        answer = template['options'][option_index]
                except (ValueError, IndexError):
                    pass
            
            if self._validate_answer(answer, template['validation_rules']):
                return Requirement(
                    category=template['category'],
                    question=template['question'],
                    answer=answer,
                    validation_rules=template['validation_rules'],
                    follow_up_questions=template.get('follow_up_questions', [])
                )
            else:
                print("❌ Invalid answer. Please try again.")
    
    def _collect_follow_up_requirement(self, question: str, category: str) -> Requirement:
        """Collect follow-up requirement"""
        print(f"\n   🔍 Follow-up: {question}")
        answer = input("   💬 Your answer: ").strip()
        
        return Requirement(
            category=category,
            question=question,
            answer=answer,
            validation_rules=["not_empty"],
            is_required=False
        )
    
    def _validate_answer(self, answer: str, rules: List[str]) -> bool:
        """Validate answer against rules"""
        if not answer and "not_empty" in rules:
            return False
        
        for rule in rules:
            if rule.startswith("one_of:"):
                options = rule.split(":")[1].split(",")
                if answer.lower() not in [opt.lower() for opt in options]:
                    return False
            elif rule.startswith("numeric_range:"):
                try:
                    value = float(answer)
                    range_str = rule.split(":")[1]
                    min_val, max_val = map(float, range_str.split("-"))
                    if not (min_val <= value <= max_val):
                        return False
                except ValueError:
                    return False
        
        return True

class ProductionScalingPlanner:
    """Generates production scaling plans from local to production"""
    
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
                            "Configure security hardening",
                            "Set up compliance monitoring"
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
    
    def generate_scaling_plan(self, requirements: RequirementSet, current_state: str = "local") -> Dict:
        """Generate production scaling plan"""
        print(f"\n📈 Generating Production Scaling Plan")
        print("=" * 60)
        
        # Analyze requirements to determine scaling needs
        scaling_needs = self._analyze_scaling_needs(requirements)
        
        # Generate customized plan
        plan = {
            "current_state": current_state,
            "target_state": "production",
            "scaling_needs": scaling_needs,
            "phases": self._customize_phases(scaling_needs),
            "estimated_duration": self._calculate_duration(scaling_needs),
            "cost_implications": self._calculate_cost_implications(scaling_needs),
            "risk_assessment": self._assess_risks(scaling_needs),
            "success_metrics": self._define_success_metrics(scaling_needs)
        }
        
        return plan
    
    def _analyze_scaling_needs(self, requirements: RequirementSet) -> Dict:
        """Analyze requirements to determine scaling needs"""
        needs = {
            "infrastructure_complexity": "low",
            "security_requirements": "standard",
            "availability_requirements": "standard",
            "monitoring_needs": "basic",
            "compliance_requirements": "none"
        }
        
        for req in requirements.requirements:
            if req.category == "security" and any(keyword in req.answer.lower() for keyword in ["compliance", "hipaa", "pci", "soc2"]):
                needs["security_requirements"] = "high"
                needs["compliance_requirements"] = "required"
            
            if req.category == "availability" and "99.9" in req.answer:
                needs["availability_requirements"] = "high"
            
            if req.category == "monitoring" and any(keyword in req.answer.lower() for keyword in ["advanced", "apm", "ml"]):
                needs["monitoring_needs"] = "advanced"
        
        return needs
    
    def _customize_phases(self, scaling_needs: Dict) -> List[Dict]:
        """Customize phases based on scaling needs"""
        base_phases = self.scaling_templates["local_to_production"]["phases"]
        
        # Add additional phases based on needs
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
        base_days = 7  # Base duration
        
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

class CLIInterface:
    """Main CLI interface for interacting with agents"""
    
    def __init__(self):
        self.requirement_collector = RequirementCollector()
        self.scaling_planner = ProductionScalingPlanner()
        self.agents = {}
        if IntelligentTerraformAgent:
            self.agents["terraform"] = IntelligentTerraformAgent()
        self.current_project = None
    
    def run(self):
        """Main CLI loop"""
        print("🚀 Intelligent Infrastructure Agent CLI")
        print("=" * 50)
        
        while True:
            try:
                self._show_main_menu()
                choice = input("\n💬 Enter your choice: ").strip()
                
                if choice == "1":
                    self._create_new_project()
                elif choice == "2":
                    self._load_existing_project()
                elif choice == "3":
                    self._interact_with_agent()
                elif choice == "4":
                    self._generate_scaling_plan()
                elif choice == "5":
                    self._show_troubleshooting_menu()
                elif choice == "6":
                    self._export_project()
                elif choice == "0":
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_main_menu(self):
        """Show main menu"""
        print("\n📋 Main Menu:")
        print("1. Create New Project")
        print("2. Load Existing Project")
        print("3. Interact with Agent")
        print("4. Generate Production Scaling Plan")
        print("5. Troubleshooting Tools")
        print("6. Export Project")
        print("0. Exit")
    
    def _create_new_project(self):
        """Create new project with requirement collection"""
        print("\n🆕 Creating New Project")
        print("=" * 30)
        
        # Select project type
        project_types = list(self.requirement_collector.requirement_templates.keys())
        print("\n📋 Available Project Types:")
        for i, ptype in enumerate(project_types, 1):
            print(f"{i}. {ptype.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input(f"\n💬 Select project type (1-{len(project_types)}): "))
                if 1 <= choice <= len(project_types):
                    project_type = project_types[choice - 1]
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Collect requirements
        requirements = self.requirement_collector.collect_requirements(project_type)
        
        # Save project
        self.current_project = {
            "type": project_type,
            "requirements": requirements,
            "created_at": str(Path.cwd()),
            "status": "requirements_collected"
        }
        
        print(f"\n✅ Project created successfully!")
        print(f"📊 Completeness: {requirements.completeness_score:.1f}%")
        print(f"📁 Project: {requirements.project_name}")
    
    def _load_existing_project(self):
        """Load existing project"""
        print("\n📂 Load Existing Project")
        print("=" * 30)
        
        # List available projects
        projects_dir = Path("projects")
        if not projects_dir.exists():
            print("❌ No projects directory found.")
            return
        
        project_files = list(projects_dir.glob("*.json"))
        if not project_files:
            print("❌ No existing projects found.")
            return
        
        print("\n📋 Available Projects:")
        for i, project_file in enumerate(project_files, 1):
            print(f"{i}. {project_file.stem}")
        
        while True:
            try:
                choice = int(input(f"\n💬 Select project (1-{len(project_files)}): "))
                if 1 <= choice <= len(project_files):
                    project_file = project_files[choice - 1]
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Load project
        try:
            with open(project_file, 'r') as f:
                self.current_project = json.load(f)
            print(f"✅ Project loaded: {project_file.stem}")
        except Exception as e:
            print(f"❌ Error loading project: {e}")
    
    def _interact_with_agent(self):
        """Interact with selected agent"""
        if not self.current_project:
            print("❌ No project loaded. Please create or load a project first.")
            return
        
        print("\n🤖 Agent Interaction")
        print("=" * 30)
        
        if not self.agents:
            print("❌ No agents available. Running in demo mode.")
            print("📝 This would normally process your requirements with an intelligent agent.")
            request = self._generate_request_from_requirements()
            print(f"📝 Generated request: {request}")
            print("✅ In full mode, this would generate Terraform code and deployment plans.")
            return
        
        # Select agent
        print("\n📋 Available Agents:")
        for i, agent_name in enumerate(self.agents.keys(), 1):
            print(f"{i}. {agent_name.title()}")
        
        while True:
            try:
                choice = int(input(f"\n💬 Select agent (1-{len(self.agents)}): "))
                if 1 <= choice <= len(self.agents):
                    agent_name = list(self.agents.keys())[choice - 1]
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        agent = self.agents[agent_name]
        
        # Generate request from requirements
        request = self._generate_request_from_requirements()
        
        print(f"\n🏗️ Processing request with {agent_name} agent...")
        print(f"📝 Request: {request}")
        
        # Process with agent
        response = agent.process_request(request)
        
        # Display results
        self._display_agent_response(response)
        
        # Save results to project
        if "results" not in self.current_project:
            self.current_project["results"] = {}
        self.current_project["results"][agent_name] = {
            "request": request,
            "response": asdict(response)
        }
    
    def _generate_request_from_requirements(self) -> str:
        """Generate request string from collected requirements"""
        if not self.current_project or "requirements" not in self.current_project:
            return "Basic infrastructure setup"
        
        # Handle both RequirementSet object and dict format
        if hasattr(self.current_project["requirements"], 'requirements'):
            requirements = self.current_project["requirements"].requirements
        else:
            requirements = self.current_project["requirements"]["requirements"]
        
        request_parts = []
        
        for req in requirements:
            if hasattr(req, 'answer'):
                answer = req.answer
                question = req.question
            else:
                answer = req["answer"]
                question = req["question"]
            
            if answer:
                request_parts.append(f"{question}: {answer}")
        
        return "\n".join(request_parts)
    
    def _display_agent_response(self, response):
        """Display agent response in formatted way"""
        print(f"\n✅ Agent Response:")
        print("=" * 50)
        print(f"💰 Cost Estimate: ${response.cost_estimate}/month")
        print(f"🎯 Confidence: {response.confidence * 100}%")
        
        print(f"\n📋 Implementation Steps:")
        for i, step in enumerate(response.implementation_steps, 1):
            print(f"  {i}. {step}")
        
        print(f"\n📁 Generated Files:")
        for filename in response.terraform_code.keys():
            print(f"  ✅ {filename}")
        
        print(f"\n📝 Detailed Explanation:")
        print(response.content)
    
    def _generate_scaling_plan(self):
        """Generate production scaling plan"""
        if not self.current_project:
            print("❌ No project loaded. Please create or load a project first.")
            return
        
        print("\n📈 Production Scaling Plan")
        print("=" * 30)
        
        # Convert requirements to RequirementSet object
        req_data = self.current_project["requirements"]
        
        # Handle both RequirementSet object and dict format
        if hasattr(req_data, 'project_name'):
            requirements = req_data
        else:
            requirements = RequirementSet(
                project_name=req_data["project_name"],
                requirements=[Requirement(**req) for req in req_data["requirements"]],
                completeness_score=req_data["completeness_score"]
            )
        
        # Generate scaling plan
        scaling_plan = self.scaling_planner.generate_scaling_plan(requirements)
        
        # Display plan
        print(f"\n📊 Scaling Plan for: {requirements.project_name}")
        print("=" * 50)
        print(f"⏱️  Estimated Duration: {scaling_plan['estimated_duration']}")
        
        print(f"\n📋 Phases:")
        for i, phase in enumerate(scaling_plan['phases'], 1):
            print(f"\n  Phase {i}: {phase['name']}")
            print(f"    Duration: {phase['duration']}")
            print(f"    Steps:")
            for j, step in enumerate(phase['steps'], 1):
                print(f"      {j}. {step}")
        
        print(f"\n💰 Cost Implications:")
        for cost_type, cost_range in scaling_plan['cost_implications'].items():
            print(f"  {cost_type.replace('_', ' ').title()}: {cost_range}")
        
        print(f"\n⚠️  Risk Assessment:")
        for risk in scaling_plan['risk_assessment']:
            print(f"  • {risk}")
        
        print(f"\n🎯 Success Metrics:")
        for metric in scaling_plan['success_metrics']:
            print(f"  • {metric}")
        
        # Save scaling plan to project
        self.current_project["scaling_plan"] = scaling_plan
    
    def _show_troubleshooting_menu(self):
        """Show troubleshooting menu"""
        print("\n🔧 Troubleshooting Tools")
        print("=" * 30)
        
        print("1. Infrastructure Issues")
        print("2. Deployment Problems")
        print("3. Performance Issues")
        print("4. Security Concerns")
        print("5. Cost Optimization")
        print("0. Back to Main Menu")
        
        choice = input("\n💬 Select troubleshooting category: ").strip()
        
        if choice == "1":
            self._troubleshoot_infrastructure()
        elif choice == "2":
            self._troubleshoot_deployment()
        elif choice == "3":
            self._troubleshoot_performance()
        elif choice == "4":
            self._troubleshoot_security()
        elif choice == "5":
            self._troubleshoot_cost()
        elif choice == "0":
            return
        else:
            print("❌ Invalid choice.")
    
    def _troubleshoot_infrastructure(self):
        """Troubleshoot infrastructure issues"""
        print("\n🏗️ Infrastructure Troubleshooting")
        print("=" * 40)
        
        issues = [
            "Terraform state is locked",
            "Resource already exists error",
            "Permission denied errors",
            "Circular dependency error",
            "VPC configuration issues",
            "Security group problems",
            "Load balancer configuration",
            "Database connection issues"
        ]
        
        print("\n📋 Common Infrastructure Issues:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        choice = input("\n💬 Select issue to troubleshoot: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(issues):
            issue = issues[int(choice) - 1]
            self._provide_troubleshooting_solution(issue, "infrastructure")
        else:
            print("❌ Invalid choice.")
    
    def _provide_troubleshooting_solution(self, issue: str, category: str):
        """Provide troubleshooting solution"""
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
        
        if issue in solutions:
            solution = solutions[issue]
            print(f"\n🔍 Diagnosis: {solution['diagnosis']}")
            
            print(f"\n✅ Solutions:")
            for i, sol in enumerate(solution['solutions'], 1):
                print(f"  {i}. {sol}")
            
            print(f"\n🛡️ Prevention:")
            for i, prev in enumerate(solution['prevention'], 1):
                print(f"  {i}. {prev}")
        else:
            print(f"\n❓ Issue: {issue}")
            print("This is a complex issue that requires detailed analysis.")
            print("Please provide more context or contact support.")
    
    def _troubleshoot_deployment(self):
        """Troubleshoot deployment issues"""
        print("\n🚀 Deployment Troubleshooting")
        print("=" * 40)
        print("Deployment troubleshooting features coming soon...")
    
    def _troubleshoot_performance(self):
        """Troubleshoot performance issues"""
        print("\n⚡ Performance Troubleshooting")
        print("=" * 40)
        print("Performance troubleshooting features coming soon...")
    
    def _troubleshoot_security(self):
        """Troubleshoot security issues"""
        print("\n🔒 Security Troubleshooting")
        print("=" * 40)
        print("Security troubleshooting features coming soon...")
    
    def _troubleshoot_cost(self):
        """Troubleshoot cost issues"""
        print("\n💰 Cost Optimization")
        print("=" * 40)
        print("Cost optimization features coming soon...")
    
    def _export_project(self):
        """Export project to files"""
        if not self.current_project:
            print("❌ No project loaded.")
            return
        
        print("\n📤 Export Project")
        print("=" * 30)
        
        # Create projects directory
        projects_dir = Path("projects")
        projects_dir.mkdir(exist_ok=True)
        
        # Generate filename
        project_name = self.current_project["requirements"]["project_name"]
        filename = f"{project_name.replace(' ', '_').lower()}.json"
        filepath = projects_dir / filename
        
        # Save project
        try:
            with open(filepath, 'w') as f:
                json.dump(self.current_project, f, indent=2, default=str)
            print(f"✅ Project exported to: {filepath}")
        except Exception as e:
            print(f"❌ Error exporting project: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Intelligent Infrastructure Agent CLI")
    parser.add_argument("--project", help="Load specific project file")
    parser.add_argument("--agent", help="Use specific agent")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    cli = CLIInterface()
    
    if args.project:
        # Load specific project
        try:
            with open(args.project, 'r') as f:
                cli.current_project = json.load(f)
            print(f"✅ Project loaded: {args.project}")
        except Exception as e:
            print(f"❌ Error loading project: {e}")
            return
    
    if args.interactive or not args.project:
        cli.run()
    else:
        # Non-interactive mode
        if args.agent and args.agent in cli.agents:
            agent = cli.agents[args.agent]
            request = cli._generate_request_from_requirements()
            response = agent.process_request(request)
            cli._display_agent_response(response)

if __name__ == "__main__":
    main()
