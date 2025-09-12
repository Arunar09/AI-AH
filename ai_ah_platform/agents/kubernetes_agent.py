"""
Kubernetes Orchestration Agent for the Multi-Agent Infrastructure Intelligence Platform.

This agent specializes in Kubernetes cluster management, application deployment,
scaling, and orchestration using AI-driven decision making.
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
class KubernetesResource:
    """Represents a Kubernetes resource."""
    kind: str
    name: str
    namespace: str
    spec: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KubernetesDeployment:
    """Represents a Kubernetes deployment."""
    id: str
    name: str
    description: str
    namespace: str
    resources: List[KubernetesResource]
    replicas: int
    strategy: str
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KubernetesExecution:
    """Represents a Kubernetes execution."""
    id: str
    deployment_id: str
    command: str
    status: str
    output: str
    error: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KubernetesCluster:
    """Represents a Kubernetes cluster."""
    id: str
    name: str
    context: str
    nodes: List[Dict[str, Any]]
    version: str
    status: str
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class KubernetesAgent(IntelligentAgent):
    """
    Kubernetes Orchestration Agent.
    
    Specializes in:
    - Kubernetes cluster management
    - Application deployment and scaling
    - Resource orchestration
    - Service mesh configuration
    - Monitoring and observability
    """
    
    def __init__(self, config: PlatformConfig, workspace_path: str = None):
        super().__init__(config)
        
        self.workspace_path = workspace_path or tempfile.mkdtemp(prefix="kubernetes_agent_")
        self.deployments: Dict[str, KubernetesDeployment] = {}
        self.executions: Dict[str, KubernetesExecution] = {}
        self.clusters: Dict[str, KubernetesCluster] = {}
        self.resources: Dict[str, KubernetesResource] = {}
        
        # Kubernetes-specific capabilities
        self.capabilities = [
            AgentCapability(
                name="cluster_management",
                description="Manage Kubernetes clusters",
                version="1.0.0",
                parameters={"supported_operations": ["create", "scale", "upgrade", "monitor"]}
            ),
            AgentCapability(
                name="application_deployment",
                description="Deploy applications to Kubernetes",
                version="1.0.0"
            ),
            AgentCapability(
                name="resource_orchestration",
                description="Orchestrate Kubernetes resources",
                version="1.0.0"
            ),
            AgentCapability(
                name="scaling_management",
                description="Manage application scaling",
                version="1.0.0"
            ),
            AgentCapability(
                name="service_mesh",
                description="Configure service mesh",
                version="1.0.0"
            )
        ]
        
        # Initialize resource templates
        self._initialize_resource_templates()
        self._initialize_deployment_templates()
    
    async def _initialize_capabilities(self):
        """Initialize Kubernetes-specific capabilities."""
        # Add Kubernetes-specific response handlers
        self.add_response_handler("deploy_application", self._handle_deploy_application)
        self.add_response_handler("scale_application", self._handle_scale_application)
        self.add_response_handler("manage_cluster", self._handle_manage_cluster)
        self.add_response_handler("configure_service", self._handle_configure_service)
        
        # Add context processors
        self.add_context_processor(self._process_kubernetes_context)
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers for Kubernetes operations."""
        pass  # Already handled in _initialize_capabilities
    
    async def _initialize_context_processors(self):
        """Initialize context processors for Kubernetes operations."""
        pass  # Already handled in _initialize_capabilities
    
    def _initialize_resource_templates(self):
        """Initialize common Kubernetes resource templates."""
        self.resource_templates = {
            "deployment": {
                "kind": "Deployment",
                "apiVersion": "apps/v1",
                "required_fields": ["name", "image", "replicas"],
                "optional_fields": ["ports", "env", "resources", "volumes"],
                "defaults": {
                    "replicas": 1,
                    "ports": [{"containerPort": 80}],
                    "resources": {"requests": {"cpu": "100m", "memory": "128Mi"}}
                }
            },
            "service": {
                "kind": "Service",
                "apiVersion": "v1",
                "required_fields": ["name", "selector"],
                "optional_fields": ["type", "ports"],
                "defaults": {
                    "type": "ClusterIP",
                    "ports": [{"port": 80, "targetPort": 80}]
                }
            },
            "configmap": {
                "kind": "ConfigMap",
                "apiVersion": "v1",
                "required_fields": ["name"],
                "optional_fields": ["data"],
                "defaults": {"data": {}}
            },
            "secret": {
                "kind": "Secret",
                "apiVersion": "v1",
                "required_fields": ["name"],
                "optional_fields": ["data", "type"],
                "defaults": {"type": "Opaque", "data": {}}
            },
            "ingress": {
                "kind": "Ingress",
                "apiVersion": "networking.k8s.io/v1",
                "required_fields": ["name", "rules"],
                "optional_fields": ["tls", "annotations"],
                "defaults": {"rules": []}
            },
            "persistentvolumeclaim": {
                "kind": "PersistentVolumeClaim",
                "apiVersion": "v1",
                "required_fields": ["name", "accessModes"],
                "optional_fields": ["resources"],
                "defaults": {
                    "accessModes": ["ReadWriteOnce"],
                    "resources": {"requests": {"storage": "1Gi"}}
                }
            }
        }
    
    def _initialize_deployment_templates(self):
        """Initialize common deployment templates."""
        self.deployment_templates = {
            "web_application": {
                "name": "web_application",
                "description": "Deploy a web application",
                "resources": [
                    {"template": "deployment", "vars": {"name": "web-app", "image": "nginx:latest"}},
                    {"template": "service", "vars": {"name": "web-service", "selector": "app=web-app"}},
                    {"template": "ingress", "vars": {"name": "web-ingress", "rules": [{"host": "example.com", "http": {"paths": [{"path": "/", "backend": {"service": {"name": "web-service", "port": {"number": 80}}}}]}}]}}
                ]
            },
            "database": {
                "name": "database",
                "description": "Deploy a database",
                "resources": [
                    {"template": "deployment", "vars": {"name": "db-app", "image": "mysql:8.0"}},
                    {"template": "service", "vars": {"name": "db-service", "selector": "app=db-app"}},
                    {"template": "persistentvolumeclaim", "vars": {"name": "db-pvc", "accessModes": ["ReadWriteOnce"]}}
                ]
            },
            "microservice": {
                "name": "microservice",
                "description": "Deploy a microservice",
                "resources": [
                    {"template": "deployment", "vars": {"name": "microservice-app", "image": "alpine:latest"}},
                    {"template": "service", "vars": {"name": "microservice-service", "selector": "app=microservice-app"}},
                    {"template": "configmap", "vars": {"name": "microservice-config"}}
                ]
            }
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a Kubernetes-related request."""
        try:
            # Parse the request
            parsed_request = await self._parse_kubernetes_request(request)
            
            # Generate response based on intent
            if parsed_request.intent["type"] == IntentType.CREATE_INFRASTRUCTURE:
                return await self._handle_deploy_application(parsed_request, context)
            elif parsed_request.intent["type"] == IntentType.MODIFY_INFRASTRUCTURE:
                return await self._handle_scale_application(parsed_request, context)
            elif "cluster" in parsed_request.original_text.lower():
                return await self._handle_manage_cluster(parsed_request, context)
            elif "service" in parsed_request.original_text.lower():
                return await self._handle_configure_service(parsed_request, context)
            else:
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content="I can help you with Kubernetes cluster management and application deployment. What would you like to do?",
                    confidence=0.8
                )
                
        except Exception as e:
            self.logger.error(f"Error processing Kubernetes request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze deployment requirements for Kubernetes."""
        try:
            # Parse requirements
            parsed_request = await self._parse_kubernetes_request(requirements)
            
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
                "deployments": [],
                "namespace": "default",
                "recommendations": []
            }
            
            # Extract resources and deployments
            for entity in parsed_request.entities:
                if entity.type == EntityType.SERVICE:
                    if entity.value.lower() in ["web", "nginx", "apache", "http"]:
                        analysis["deployments"].append("web_application")
                    elif entity.value.lower() in ["database", "mysql", "postgresql", "mongodb"]:
                        analysis["deployments"].append("database")
                    elif entity.value.lower() in ["microservice", "api", "service"]:
                        analysis["deployments"].append("microservice")
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing requirements: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def generate_deployment(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a Kubernetes deployment."""
        try:
            deployment_id = f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create Kubernetes deployment
            deployment = KubernetesDeployment(
                id=deployment_id,
                name=analysis.get("name", f"Kubernetes Deployment {deployment_id}"),
                description=analysis.get("description", "Generated Kubernetes deployment"),
                namespace=analysis.get("namespace", "default"),
                resources=[],
                replicas=analysis.get("replicas", 1),
                strategy=analysis.get("strategy", "RollingUpdate")
            )
            
            # Add resources based on analysis
            for deployment_type in analysis.get("deployments", []):
                if deployment_type in self.deployment_templates:
                    template = self.deployment_templates[deployment_type]
                    for resource_template in template["resources"]:
                        resource = self._create_resource_from_template(resource_template, deployment.namespace)
                        deployment.resources.append(resource)
            
            # Store deployment
            self.deployments[deployment_id] = deployment
            
            # Generate Kubernetes manifests
            await self._generate_kubernetes_manifests(deployment)
            
            return {
                "deployment_id": deployment_id,
                "status": "created",
                "resources": len(deployment.resources),
                "namespace": deployment.namespace,
                "replicas": deployment.replicas,
                "files_generated": True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating deployment: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def execute_deployment(self, deployment: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Kubernetes deployment."""
        try:
            deployment_id = deployment.get("deployment_id")
            if not deployment_id or deployment_id not in self.deployments:
                return {"error": "Deployment not found", "status": "failed"}
            
            kubernetes_deployment = self.deployments[deployment_id]
            execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create execution
            execution = KubernetesExecution(
                id=execution_id,
                deployment_id=deployment_id,
                command="kubectl apply",
                status="running"
            )
            
            self.executions[execution_id] = execution
            
            # Execute Kubernetes commands
            result = await self._execute_kubernetes_commands(kubernetes_deployment, execution)
            
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
            self.logger.error(f"Error executing deployment: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def _parse_kubernetes_request(self, request: str) -> ParsedRequest:
        """Parse a Kubernetes-specific request."""
        # This would integrate with the NLP processor
        # For now, we'll do basic parsing
        request_lower = request.lower()
        
        # Simple intent detection
        if any(word in request_lower for word in ["deploy", "create", "launch", "start"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["scale", "resize", "modify", "update"]):
            intent_type = IntentType.MODIFY_INFRASTRUCTURE
        else:
            intent_type = IntentType.UNKNOWN
        
        # Simple entity extraction
        entities = []
        if "kubernetes" in request_lower or "k8s" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "kubernetes"})
        if "web" in request_lower or "nginx" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "web"})
        if "database" in request_lower or "mysql" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "database"})
        if "microservice" in request_lower or "api" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "microservice"})
        
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
        
        # Generate deployment
        deployment = await self.generate_deployment(analysis)
        
        if deployment.get("status") == "created":
            return AgentResponse(
                agent_id=self.config.name,
                response_type="kubernetes_deployment",
                content=f"I've created a Kubernetes deployment with {deployment['resources']} resources in the {deployment['namespace']} namespace.",
                confidence=0.9,
                suggestions=[
                    "Review the generated Kubernetes manifests",
                    "Execute the deployment to deploy the application",
                    "Modify the deployment if needed"
                ],
                next_actions=[
                    "kubernetes_deployment_review",
                    "kubernetes_deployment_execute",
                    "kubernetes_deployment_modify"
                ],
                metadata={"deployment_id": deployment["deployment_id"], "analysis": analysis}
            )
        else:
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content="I encountered an error creating the deployment.",
                confidence=0.0,
                metadata={"error": deployment.get("error")}
            )
    
    async def _handle_scale_application(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle application scaling requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you scale your application. Let me analyze the current deployment and propose scaling changes.",
            confidence=0.8,
            suggestions=["Review current deployment", "Identify scaling requirements", "Generate scaling plan"]
        )
    
    async def _handle_manage_cluster(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle cluster management requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you manage your Kubernetes cluster. Let me check the cluster status and provide management options.",
            confidence=0.8,
            suggestions=["Check cluster health", "Review cluster resources", "Optimize cluster configuration"]
        )
    
    async def _handle_configure_service(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle service configuration requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you configure your Kubernetes services. Let me analyze the requirements and create a service configuration.",
            confidence=0.8,
            suggestions=["Review service requirements", "Generate service configuration", "Deploy service configuration"]
        )
    
    async def _process_kubernetes_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context for Kubernetes operations."""
        processed_context = context.copy()
        
        # Add Kubernetes-specific context
        processed_context["kubernetes_workspace"] = self.workspace_path
        processed_context["available_deployments"] = list(self.deployments.keys())
        processed_context["available_executions"] = list(self.executions.keys())
        processed_context["available_clusters"] = list(self.clusters.keys())
        
        return processed_context
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Resource recommendations
        if "web_application" in analysis["deployments"]:
            recommendations.append("Configure horizontal pod autoscaling")
            recommendations.append("Set up ingress controller")
            recommendations.append("Enable health checks and readiness probes")
        
        # Database recommendations
        if "database" in analysis["deployments"]:
            recommendations.append("Configure persistent volumes for data storage")
            recommendations.append("Set up database backups")
            recommendations.append("Configure resource limits and requests")
        
        # Microservice recommendations
        if "microservice" in analysis["deployments"]:
            recommendations.append("Configure service mesh for communication")
            recommendations.append("Set up monitoring and logging")
            recommendations.append("Implement circuit breakers and retries")
        
        return recommendations
    
    def _create_resource_from_template(self, resource_template: Dict[str, Any], namespace: str) -> KubernetesResource:
        """Create a Kubernetes resource from a template."""
        template_name = resource_template["template"]
        if template_name in self.resource_templates:
            template = self.resource_templates[template_name]
            resource = KubernetesResource(
                kind=template["kind"],
                name=resource_template["vars"]["name"],
                namespace=namespace,
                spec=template["defaults"].copy()
            )
            
            # Apply variables
            if "vars" in resource_template:
                for key, value in resource_template["vars"].items():
                    if key in resource.spec:
                        resource.spec[key] = value
            
            return resource
        
        return KubernetesResource(
            kind="Unknown",
            name="unknown",
            namespace=namespace,
            spec={}
        )
    
    async def _generate_kubernetes_manifests(self, deployment: KubernetesDeployment):
        """Generate Kubernetes manifest files."""
        deployment_dir = Path(self.workspace_path) / deployment.id
        deployment_dir.mkdir(exist_ok=True)
        
        # Generate individual manifest files
        for resource in deployment.resources:
            manifest_content = self._generate_manifest_yaml(resource)
            manifest_file = deployment_dir / f"{resource.name}-{resource.kind.lower()}.yaml"
            with open(manifest_file, "w") as f:
                f.write(manifest_content)
        
        # Generate combined manifest
        combined_content = self._generate_combined_manifest(deployment)
        with open(deployment_dir / "deployment.yaml", "w") as f:
            f.write(combined_content)
    
    def _generate_manifest_yaml(self, resource: KubernetesResource) -> str:
        """Generate YAML manifest for a resource."""
        manifest = {
            "apiVersion": self._get_api_version(resource.kind),
            "kind": resource.kind,
            "metadata": {
                "name": resource.name,
                "namespace": resource.namespace
            },
            "spec": resource.spec
        }
        
        return yaml.dump(manifest, default_flow_style=False)
    
    def _generate_combined_manifest(self, deployment: KubernetesDeployment) -> str:
        """Generate combined manifest for all resources."""
        content = "---\n# Kubernetes deployment generated by AI-AH Platform\n\n"
        
        for resource in deployment.resources:
            content += yaml.dump({
                "apiVersion": self._get_api_version(resource.kind),
                "kind": resource.kind,
                "metadata": {
                    "name": resource.name,
                    "namespace": resource.namespace
                },
                "spec": resource.spec
            }, default_flow_style=False)
            content += "---\n\n"
        
        return content
    
    def _get_api_version(self, kind: str) -> str:
        """Get API version for a resource kind."""
        api_versions = {
            "Deployment": "apps/v1",
            "Service": "v1",
            "ConfigMap": "v1",
            "Secret": "v1",
            "Ingress": "networking.k8s.io/v1",
            "PersistentVolumeClaim": "v1"
        }
        return api_versions.get(kind, "v1")
    
    async def _execute_kubernetes_commands(self, deployment: KubernetesDeployment, execution: KubernetesExecution) -> Dict[str, Any]:
        """Execute Kubernetes commands."""
        try:
            deployment_dir = Path(self.workspace_path) / deployment.id
            
            # Apply manifests
            command = f"kubectl apply -f deployment.yaml"
            result = await self._run_kubectl_command(deployment_dir, command)
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e), "output": ""}
    
    async def _run_kubectl_command(self, deployment_dir: Path, command: str) -> Dict[str, Any]:
        """Run a kubectl command."""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=deployment_dir,
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
            deployment = await self.generate_deployment(analysis)
            return deployment
        elif task.name == "execute_deployment":
            return await self.execute_deployment(task.metadata)
        elif task.name == "get_status":
            return await self._get_kubernetes_status()
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    async def _get_kubernetes_status(self) -> Dict[str, Any]:
        """Get current Kubernetes status."""
        return {
            "deployments_count": len(self.deployments),
            "executions_count": len(self.executions),
            "active_executions": len([e for e in self.executions.values() if e.status == "running"]),
            "last_activity": max([d.created_at for d in self.deployments.values()]) if self.deployments else None
        }
