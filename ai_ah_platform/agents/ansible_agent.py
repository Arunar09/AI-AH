"""
Ansible Configuration Agent for the Multi-Agent Infrastructure Intelligence Platform.

This agent specializes in Ansible-based configuration management,
application deployment, and infrastructure automation.
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


@dataclass
class AnsiblePlaybook:
    """Represents an Ansible playbook."""
    id: str
    name: str
    description: str
    hosts: List[str]
    tasks: List[Dict[str, Any]]
    variables: Dict[str, Any]
    handlers: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnsibleExecution:
    """Represents an Ansible execution."""
    id: str
    playbook_id: str
    command: str
    status: str
    output: str
    error: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnsibleInventory:
    """Represents an Ansible inventory."""
    id: str
    name: str
    hosts: Dict[str, Dict[str, Any]]
    groups: Dict[str, List[str]] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AnsibleAgent(IntelligentAgent):
    """
    Ansible Configuration Agent.
    
    Specializes in:
    - Configuration management with Ansible
    - Application deployment and orchestration
    - Infrastructure automation
    - Security hardening
    - Compliance management
    """
    
    def __init__(self, config: PlatformConfig, workspace_path: str = None):
        super().__init__(config)
        
        self.workspace_path = workspace_path or tempfile.mkdtemp(prefix="ansible_agent_")
        self.playbooks: Dict[str, AnsiblePlaybook] = {}
        self.executions: Dict[str, AnsibleExecution] = {}
        self.inventories: Dict[str, AnsibleInventory] = {}
        self.roles: Dict[str, Dict[str, Any]] = {}
        
        # Ansible-specific capabilities
        self.capabilities = [
            AgentCapability(
                name="configuration_management",
                description="Manage system configurations using Ansible",
                version="1.0.0",
                parameters={"supported_modules": ["package", "service", "file", "template", "user"]}
            ),
            AgentCapability(
                name="application_deployment",
                description="Deploy applications using Ansible",
                version="1.0.0"
            ),
            AgentCapability(
                name="infrastructure_automation",
                description="Automate infrastructure tasks",
                version="1.0.0"
            ),
            AgentCapability(
                name="security_hardening",
                description="Apply security hardening configurations",
                version="1.0.0"
            ),
            AgentCapability(
                name="compliance_management",
                description="Ensure compliance with security standards",
                version="1.0.0"
            )
        ]
        
        # Initialize task templates
        self._initialize_task_templates()
        self._initialize_role_templates()
    
    async def _initialize_capabilities(self):
        """Initialize Ansible-specific capabilities."""
        # Add Ansible-specific response handlers
        self.add_response_handler("deploy_application", self._handle_deploy_application)
        self.add_response_handler("configure_system", self._handle_configure_system)
        self.add_response_handler("security_harden", self._handle_security_harden)
        self.add_response_handler("compliance_check", self._handle_compliance_check)
        
        # Add context processors
        self.add_context_processor(self._process_ansible_context)
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers for Ansible operations."""
        pass  # Already handled in _initialize_capabilities
    
    async def _initialize_context_processors(self):
        """Initialize context processors for Ansible operations."""
        pass  # Already handled in _initialize_capabilities
    
    def _initialize_task_templates(self):
        """Initialize common Ansible task templates."""
        self.task_templates = {
            "install_package": {
                "module": "package",
                "parameters": {
                    "name": "{{package_name}}",
                    "state": "present"
                },
                "description": "Install a package"
            },
            "start_service": {
                "module": "service",
                "parameters": {
                    "name": "{{service_name}}",
                    "state": "started",
                    "enabled": True
                },
                "description": "Start and enable a service"
            },
            "create_file": {
                "module": "file",
                "parameters": {
                    "path": "{{file_path}}",
                    "state": "touch",
                    "mode": "{{file_mode | default('0644')}}"
                },
                "description": "Create a file"
            },
            "copy_file": {
                "module": "copy",
                "parameters": {
                    "src": "{{source_path}}",
                    "dest": "{{destination_path}}",
                    "mode": "{{file_mode | default('0644')}}"
                },
                "description": "Copy a file"
            },
            "create_user": {
                "module": "user",
                "parameters": {
                    "name": "{{username}}",
                    "state": "present",
                    "shell": "{{user_shell | default('/bin/bash')}}"
                },
                "description": "Create a user"
            },
            "configure_firewall": {
                "module": "ufw",
                "parameters": {
                    "rule": "{{firewall_rule}}",
                    "port": "{{port_number}}",
                    "proto": "{{protocol | default('tcp')}}"
                },
                "description": "Configure firewall rules"
            },
            "update_system": {
                "module": "apt",
                "parameters": {
                    "update_cache": True,
                    "upgrade": "dist"
                },
                "description": "Update system packages"
            }
        }
    
    def _initialize_role_templates(self):
        """Initialize common Ansible role templates."""
        self.role_templates = {
            "web_server": {
                "name": "web_server",
                "description": "Configure a web server",
                "tasks": [
                    {"template": "install_package", "vars": {"package_name": "nginx"}},
                    {"template": "start_service", "vars": {"service_name": "nginx"}},
                    {"template": "create_file", "vars": {"file_path": "/etc/nginx/sites-available/default"}}
                ],
                "handlers": [
                    {"name": "restart nginx", "module": "service", "parameters": {"name": "nginx", "state": "restarted"}}
                ]
            },
            "database_server": {
                "name": "database_server",
                "description": "Configure a database server",
                "tasks": [
                    {"template": "install_package", "vars": {"package_name": "mysql-server"}},
                    {"template": "start_service", "vars": {"service_name": "mysql"}},
                    {"template": "create_user", "vars": {"username": "dbuser"}}
                ],
                "handlers": [
                    {"name": "restart mysql", "module": "service", "parameters": {"name": "mysql", "state": "restarted"}}
                ]
            },
            "security_hardening": {
                "name": "security_hardening",
                "description": "Apply security hardening",
                "tasks": [
                    {"template": "update_system"},
                    {"template": "configure_firewall", "vars": {"firewall_rule": "allow", "port_number": "22"}},
                    {"template": "configure_firewall", "vars": {"firewall_rule": "allow", "port_number": "80"}},
                    {"template": "configure_firewall", "vars": {"firewall_rule": "allow", "port_number": "443"}}
                ],
                "handlers": []
            }
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process an Ansible-related request using local intelligence."""
        try:
            # Get session context for conversation memory
            session_id = context.get("session_id", "default") if context else "default"
            conv_context = self._get_conversation_context(session_id)
            conv_context["message_count"] += 1
            conv_context["conversation_history"].append(request)
            
            # Use knowledge base to analyze the request
            analysis = self.knowledge_base.analyze_request(request)
            
            # Check for repeated intents
            current_intent = analysis.get("intent")
            if current_intent == conv_context["last_intent"]:
                conv_context["repeated_intents"] += 1
            else:
                conv_context["repeated_intents"] = 0
            conv_context["last_intent"] = current_intent
            
            # Generate intelligent response based on analysis
            if analysis["confidence"] > 0.4:  # Lower threshold to use intelligent responses more often
                return await self._generate_intelligent_response(analysis, request, context, conv_context)
            else:
                # Fallback to original parsing for low confidence
                parsed_request = await self._parse_ansible_request(request)
                
                # Generate response based on intent
                if parsed_request.intent.type == IntentType.CREATE_INFRASTRUCTURE:
                    return await self._handle_deploy_application(parsed_request, context)
                elif parsed_request.intent.type == IntentType.MODIFY_INFRASTRUCTURE:
                    return await self._handle_configure_system(parsed_request, context)
                elif "security" in parsed_request.original_text.lower():
                    return await self._handle_security_harden(parsed_request, context)
                elif "compliance" in parsed_request.original_text.lower():
                    return await self._handle_compliance_check(parsed_request, context)
                else:
                    return AgentResponse(
                        agent_id=self.config.name,
                        response_type="text",
                        content="I can help you with Ansible configuration management and deployment. What would you like to do?",
                        confidence=0.8
                    )
                
        except Exception as e:
            self.logger.error(f"Error processing Ansible request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def _generate_intelligent_response(self, analysis: Dict[str, Any], request: str, context: Dict[str, Any] = None, conv_context: Dict[str, Any] = None) -> AgentResponse:
        """Generate professional infrastructure assistant response using knowledge base analysis."""
        try:
            # Build structured response content following professional guidelines
            content_parts = []
            
            # Brief summary of user's request
            intent_type = analysis.get("intent", "general_infrastructure")
            if intent_type == "explain_technology":
                # Handle technology explanation requests
                technology = analysis.get("parameters", {}).get("technology", "unknown")
                knowledge_entries = analysis.get("knowledge", [])
                
                if knowledge_entries:
                    # Use the comprehensive knowledge from our enhanced knowledge base
                    entry = knowledge_entries[0]  # Get the most relevant entry
                    content_parts.append(f"## {entry.title}")
                    content_parts.append(f"{entry.content}")
                    
                    # Add best practices if available
                    best_practices = analysis.get("best_practices", [])
                    if best_practices:
                        content_parts.append("\n## **Best Practices**")
                        for practice in best_practices[:5]:  # Show top 5
                            content_parts.append(f"• {practice}")
                    
                    # Add recommendations if available
                    recommendations = analysis.get("recommendations", [])
                    if recommendations:
                        content_parts.append("\n## **Recommendations**")
                        for rec in recommendations[:3]:  # Show top 3
                            content_parts.append(f"• {rec}")
                else:
                    # Fallback if no knowledge found
                    content_parts.append(f"## {technology.upper()} Overview")
                    content_parts.append(f"I'd be happy to explain {technology} in detail!")
                    content_parts.append("Let me provide you with comprehensive information about this technology.")
                
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=analysis.get("confidence", 0.8),
                    metadata={"intent": intent_type, "technology": technology, "format": "comprehensive"}
                )
            else:
                # Default response for other intents
                content_parts.append("## Ansible Configuration Management")
                content_parts.append("I'll help you with Ansible automation and configuration management.")
                
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=analysis.get("confidence", 0.7),
                    metadata={"intent": intent_type, "format": "professional"}
                )
                
        except Exception as e:
            self.logger.error(f"Error generating intelligent response: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"Error generating response: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze configuration requirements for Ansible."""
        try:
            # Parse requirements
            parsed_request = await self._parse_ansible_request(requirements)
            
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
                "tasks": [],
                "roles": [],
                "hosts": [],
                "recommendations": []
            }
            
            # Extract tasks and roles
            for entity in parsed_request.entities:
                if entity.type == EntityType.SERVICE:
                    if entity.value.lower() in ["nginx", "apache", "web", "http"]:
                        analysis["roles"].append("web_server")
                    elif entity.value.lower() in ["mysql", "postgresql", "database", "db"]:
                        analysis["roles"].append("database_server")
                    elif entity.value.lower() in ["security", "firewall", "hardening"]:
                        analysis["roles"].append("security_hardening")
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing requirements: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def generate_playbook(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an Ansible playbook."""
        try:
            playbook_id = f"playbook_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create Ansible playbook
            playbook = AnsiblePlaybook(
                id=playbook_id,
                name=analysis.get("name", f"Configuration Playbook {playbook_id}"),
                description=analysis.get("description", "Generated configuration playbook"),
                hosts=analysis.get("hosts", ["all"]),
                tasks=[],
                variables=analysis.get("variables", {})
            )
            
            # Add tasks based on analysis
            for role_name in analysis.get("roles", []):
                if role_name in self.role_templates:
                    role = self.role_templates[role_name]
                    for task_template in role["tasks"]:
                        task = self._create_task_from_template(task_template)
                        playbook.tasks.append(task)
                    
                    # Add handlers
                    for handler_template in role["handlers"]:
                        handler = self._create_handler_from_template(handler_template)
                        playbook.handlers.append(handler)
            
            # Store playbook
            self.playbooks[playbook_id] = playbook
            
            # Generate Ansible files
            await self._generate_ansible_files(playbook)
            
            return {
                "playbook_id": playbook_id,
                "status": "created",
                "tasks": len(playbook.tasks),
                "handlers": len(playbook.handlers),
                "hosts": playbook.hosts,
                "files_generated": True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating playbook: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def execute_playbook(self, playbook: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an Ansible playbook."""
        try:
            playbook_id = playbook.get("playbook_id")
            if not playbook_id or playbook_id not in self.playbooks:
                return {"error": "Playbook not found", "status": "failed"}
            
            ansible_playbook = self.playbooks[playbook_id]
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create execution
            execution = AnsibleExecution(
                id=execution_id,
                playbook_id=playbook_id,
                command="ansible-playbook",
                status="running"
            )
            
            self.executions[execution_id] = execution
            
            # Execute Ansible commands
            result = await self._execute_ansible_commands(ansible_playbook, execution)
            
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
            self.logger.error(f"Error executing playbook: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def _parse_ansible_request(self, request: str) -> ParsedRequest:
        """Parse an Ansible-specific request."""
        # This would integrate with the NLP processor
        # For now, we'll do basic parsing
        request_lower = request.lower()
        
        # Simple intent detection
        if any(word in request_lower for word in ["deploy", "install", "configure", "setup"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["modify", "update", "change", "adjust"]):
            intent_type = IntentType.MODIFY_INFRASTRUCTURE
        else:
            intent_type = IntentType.UNKNOWN
        
        # Simple entity extraction
        entities = []
        if "nginx" in request_lower or "web" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "nginx"})
        if "mysql" in request_lower or "database" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "mysql"})
        if "security" in request_lower or "firewall" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "security"})
        
        return ParsedRequest(
            original_text=request,
            intent={"type": intent_type, "confidence": 0.8},
            entities=entities,
            confidence=0.8
        )
    
    async def _handle_deploy_application(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle application deployment requests."""
        # Analyze requirements
        analysis = await self.analyze_requirements(parsed_request.original_text)
        
        # Generate playbook
        playbook = await self.generate_playbook(analysis)
        
        if playbook.get("status") == "created":
            return AgentResponse(
                agent_id=self.config.name,
                response_type="ansible_playbook",
                content=f"I've created an Ansible playbook with {playbook['tasks']} tasks for {', '.join(playbook['hosts'])} hosts.",
                confidence=0.9,
                suggestions=[
                    "Review the generated playbook",
                    "Execute the playbook to deploy the application",
                    "Modify the playbook if needed"
                ],
                next_actions=[
                    "ansible_playbook_review",
                    "ansible_playbook_execute",
                    "ansible_playbook_modify"
                ],
                metadata={"playbook_id": playbook["playbook_id"], "analysis": analysis}
            )
        else:
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content="I encountered an error creating the playbook.",
                confidence=0.0,
                metadata={"error": playbook.get("error")}
            )
    
    async def _handle_configure_system(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle system configuration requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you configure your system. Let me analyze the requirements and create a configuration plan.",
            confidence=0.8,
            suggestions=["Review current configuration", "Identify changes needed", "Generate configuration plan"]
        )
    
    async def _handle_security_harden(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle security hardening requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you apply security hardening. Let me create a security configuration plan.",
            confidence=0.8,
            suggestions=["Review security requirements", "Generate hardening playbook", "Execute security configuration"]
        )
    
    async def _handle_compliance_check(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle compliance check requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you check compliance. Let me analyze your system against compliance standards.",
            confidence=0.8,
            suggestions=["Review compliance requirements", "Run compliance checks", "Generate compliance report"]
        )
    
    async def _process_ansible_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context for Ansible operations."""
        processed_context = context.copy()
        
        # Add Ansible-specific context
        processed_context["ansible_workspace"] = self.workspace_path
        processed_context["available_playbooks"] = list(self.playbooks.keys())
        processed_context["available_executions"] = list(self.executions.keys())
        processed_context["available_inventories"] = list(self.inventories.keys())
        
        return processed_context
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Security recommendations
        if "security_hardening" in analysis["roles"]:
            recommendations.append("Enable firewall and configure rules")
            recommendations.append("Update system packages regularly")
            recommendations.append("Configure user access controls")
        
        # Performance recommendations
        if "web_server" in analysis["roles"]:
            recommendations.append("Configure SSL/TLS certificates")
            recommendations.append("Enable gzip compression")
            recommendations.append("Set up monitoring and logging")
        
        # Database recommendations
        if "database_server" in analysis["roles"]:
            recommendations.append("Configure database backups")
            recommendations.append("Set up database monitoring")
            recommendations.append("Apply database security hardening")
        
        return recommendations
    
    def _create_task_from_template(self, task_template: Dict[str, Any]) -> Dict[str, Any]:
        """Create a task from a template."""
        template_name = task_template["template"]
        if template_name in self.task_templates:
            template = self.task_templates[template_name]
            task = {
                "name": template["description"],
                template["module"]: template["parameters"].copy()
            }
            
            # Apply variables
            if "vars" in task_template:
                for key, value in task_template["vars"].items():
                    if key in task["module"]:
                        task["module"][key] = value
            
            return task
        
        return task_template
    
    def _create_handler_from_template(self, handler_template: Dict[str, Any]) -> Dict[str, Any]:
        """Create a handler from a template."""
        return {
            "name": handler_template["name"],
            handler_template["module"]: handler_template["parameters"]
        }
    
    async def _generate_ansible_files(self, playbook: AnsiblePlaybook):
        """Generate Ansible configuration files."""
        playbook_dir = Path(self.workspace_path) / playbook.id
        playbook_dir.mkdir(exist_ok=True)
        
        # Generate playbook.yml
        playbook_content = self._generate_playbook_yml(playbook)
        with open(playbook_dir / "playbook.yml", "w") as f:
            f.write(playbook_content)
        
        # Generate inventory.ini
        inventory_content = self._generate_inventory_ini(playbook)
        with open(playbook_dir / "inventory.ini", "w") as f:
            f.write(inventory_content)
        
        # Generate group_vars/all.yml
        group_vars_content = self._generate_group_vars(playbook)
        group_vars_dir = playbook_dir / "group_vars"
        group_vars_dir.mkdir(exist_ok=True)
        with open(group_vars_dir / "all.yml", "w") as f:
            f.write(group_vars_content)
    
    def _generate_playbook_yml(self, playbook: AnsiblePlaybook) -> str:
        """Generate playbook.yml content."""
        content = f"---\n# Ansible playbook generated by AI-AH Platform\n\n"
        content += f"- name: {playbook.name}\n"
        content += f"  hosts: {', '.join(playbook.hosts)}\n"
        content += f"  become: yes\n"
        content += f"  vars:\n"
        
        for key, value in playbook.variables.items():
            content += f"    {key}: {value}\n"
        
        content += f"  tasks:\n"
        
        for task in playbook.tasks:
            content += f"    - name: {task['name']}\n"
            for module, parameters in task.items():
                if module != "name":
                    content += f"      {module}:\n"
                    for param_key, param_value in parameters.items():
                        content += f"        {param_key}: {param_value}\n"
        
        if playbook.handlers:
            content += f"  handlers:\n"
            for handler in playbook.handlers:
                content += f"    - name: {handler['name']}\n"
                for module, parameters in handler.items():
                    if module != "name":
                        content += f"      {module}:\n"
                        for param_key, param_value in parameters.items():
                            content += f"        {param_key}: {param_value}\n"
        
        return content
    
    def _generate_inventory_ini(self, playbook: AnsiblePlaybook) -> str:
        """Generate inventory.ini content."""
        content = "# Ansible inventory generated by AI-AH Platform\n\n"
        
        for host in playbook.hosts:
            if host != "all":
                content += f"[{host}]\n"
                content += f"{host} ansible_host=localhost ansible_connection=local\n\n"
        
        return content
    
    def _generate_group_vars(self, playbook: AnsiblePlaybook) -> str:
        """Generate group_vars/all.yml content."""
        content = "# Group variables for Ansible playbook\n\n"
        
        for key, value in playbook.variables.items():
            content += f"{key}: {value}\n"
        
        return content
    
    async def _execute_ansible_commands(self, playbook: AnsiblePlaybook, execution: AnsibleExecution) -> Dict[str, Any]:
        """Execute Ansible commands."""
        try:
            playbook_dir = Path(self.workspace_path) / playbook.id
            
            # Run ansible-playbook
            command = f"ansible-playbook -i inventory.ini playbook.yml"
            result = await self._run_ansible_command(playbook_dir, command)
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e), "output": ""}
    
    async def _run_ansible_command(self, playbook_dir: Path, command: str) -> Dict[str, Any]:
        """Run an Ansible command."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=playbook_dir,
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
        if task.name == "deploy_application":
            analysis = await self.analyze_requirements(task.metadata.get("requirements", ""))
            playbook = await self.generate_playbook(analysis)
            return playbook
        elif task.name == "execute_playbook":
            return await self.execute_playbook(task.metadata)
        elif task.name == "get_status":
            return await self._get_ansible_status()
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    async def _get_ansible_status(self) -> Dict[str, Any]:
        """Get current Ansible status."""
        return {
            "playbooks_count": len(self.playbooks),
            "executions_count": len(self.executions),
            "active_executions": len([e for e in self.executions.values() if e.status == "running"]),
            "last_activity": max([p.created_at for p in self.playbooks.values()]) if self.playbooks else None
        }
