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
from ..core.intelligence.reasoning_engine import IntelligentReasoningEngine


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
        self.conversation_memory = {}  # Store conversation context per session
        self.response_variants = {
            "greeting": [
                "Hello! 👋 I'm your AI infrastructure assistant. How can I help you today?",
                "Hi there! 🚀 Ready to build some infrastructure? What can I help you with?",
                "Greetings! 💻 I'm here to assist with your infrastructure needs. What's on your mind?",
                "Hello! 🏗️ Let's design some amazing infrastructure together. What do you need?"
            ],
            "capabilities": [
                "I'm trained to support you with cloud architecture, DevOps, and infrastructure management.",
                "I specialize in infrastructure automation, security, and optimization.",
                "I can help you with everything from basic setups to complex cloud architectures.",
                "I'm your go-to expert for infrastructure design, deployment, and management."
            ]
        }
        self.resource_templates: Dict[str, Dict[str, Any]] = {}
        self.provider_configs: Dict[str, Dict[str, Any]] = {}
        
        # Initialize local knowledge base for intelligent responses
        self.knowledge_base = LocalKnowledgeBase()
        self.reasoning_engine = IntelligentReasoningEngine()
    
    def _get_conversation_context(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context for a session"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = {
                "message_count": 0,
                "last_intent": None,
                "repeated_intents": 0,
                "conversation_history": []
            }
        return self.conversation_memory[session_id]
    
    def _get_varied_response(self, response_type: str, context: Dict[str, Any]) -> str:
        """Get a varied response based on conversation context"""
        variants = self.response_variants.get(response_type, [])
        if not variants:
            return ""
        
        # Use message count to cycle through variants
        variant_index = context["message_count"] % len(variants)
        return variants[variant_index]
        
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
            
            # Use reasoning engine for intelligent response generation
            reasoning_result = self.reasoning_engine.reason_through_request(request, context)
            
            # Generate response based on reasoning
            if reasoning_result.confidence > 0.3:
                return await self._generate_reasoned_response(reasoning_result, request, context, conv_context)
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
    
    async def _generate_reasoned_response(self, reasoning_result, request: str, context: Dict[str, Any] = None, conv_context: Dict[str, Any] = None) -> AgentResponse:
        """Generate response based on reasoning engine results."""
        try:
            # Use the curated response from reasoning engine
            content = reasoning_result.final_recommendation
            
            # Add reasoning metadata for transparency
            metadata = {
                "reasoning_confidence": reasoning_result.confidence,
                "reasoning_steps": len(reasoning_result.steps),
                "reasoning_chain": reasoning_result.reasoning_chain,
                "format": "reasoned_response"
            }
            
            return AgentResponse(
                agent_id=self.config.name,
                response_type="text",
                content=content,
                confidence=reasoning_result.confidence,
                metadata=metadata
            )
            
        except Exception as e:
            self.logger.error(f"Error generating reasoned response: {str(e)}")
            # Fallback to simple response
            return AgentResponse(
                agent_id=self.config.name,
                response_type="text",
                content=f"I analyzed your request: {request}. Let me provide you with a comprehensive response.",
                confidence=0.5,
                metadata={"error": str(e), "fallback": True}
            )

    async def _generate_intelligent_response(self, analysis: Dict[str, Any], request: str, context: Dict[str, Any] = None, conv_context: Dict[str, Any] = None) -> AgentResponse:
        """Generate professional infrastructure assistant response using knowledge base analysis."""
        try:
            # Build structured response content following professional guidelines
            content_parts = []
            
            # Brief summary of user's request
            intent_type = analysis.get("intent", "general_infrastructure")
            if intent_type == "greeting":
                # Handle repeated greetings with different responses
                if conv_context and conv_context["repeated_intents"] > 0:
                    content_parts.append("## I'm still here! 😊")
                    content_parts.append("I see you're saying hello again. Is there something specific you'd like to work on?")
                    content_parts.append("\n## **Quick Actions**")
                    content_parts.append("• 'list me terraform' - See Terraform capabilities")
                    content_parts.append("• 'create a web server' - Get infrastructure examples")
                    content_parts.append("• 'help me optimize costs' - Cost optimization guidance")
                    content_parts.append("• 'what else' - See more options")
                else:
                    # First greeting - use varied response
                    greeting_text = self._get_varied_response("greeting", conv_context) if conv_context else "Hello! 👋 I'm your AI infrastructure assistant. How can I help you today?"
                    content_parts.append(f"## {greeting_text}")
                    content_parts.append("\n## **What I Can Help You With**")
                    content_parts.append("• **Infrastructure Setup**: Web servers, databases, load balancers")
                    content_parts.append("• **Security & Compliance**: Hardening, vulnerability scanning, IAM policies")
                    content_parts.append("• **Monitoring & Observability**: Prometheus, Grafana, ELK stack")
                    content_parts.append("• **Cost Optimization**: Rightsizing, reserved instances, auto-scaling")
                    content_parts.append("\n## **Quick Start**")
                    content_parts.append("• Ask me about specific technologies (e.g., 'list me terraform')")
                    content_parts.append("• Request infrastructure examples (e.g., 'create a web server')")
                    content_parts.append("• Get help with optimization (e.g., 'help me optimize costs')")
                    content_parts.append("\n## **What would you like to work on today?**")
                
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional", "conversation_context": conv_context}
                )
            elif intent_type == "explain_technology":
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
            elif intent_type == "list_terraform":
                content_parts.append("## Terraform Infrastructure Management")
                content_parts.append("I'll provide you with Terraform capabilities and examples.")
                content_parts.append("\n## **Terraform Capabilities**")
                content_parts.append("• **Infrastructure as Code**: Define and manage cloud resources")
                content_parts.append("• **Multi-Cloud Support**: AWS, Azure, GCP, and 100+ providers")
                content_parts.append("• **State Management**: Track and manage infrastructure changes")
                content_parts.append("• **Plan & Apply**: Preview changes before execution")
                content_parts.append("\n## **Common Terraform Operations**")
                content_parts.append("• **Web Servers**: EC2 instances, load balancers, auto-scaling")
                content_parts.append("• **Databases**: RDS, managed databases, backup strategies")
                content_parts.append("• **Networking**: VPCs, subnets, security groups, routes")
                content_parts.append("• **Storage**: S3 buckets, EBS volumes, file systems")
                content_parts.append("\n## **Implementation Examples**")
                content_parts.append("### Basic Web Server")
                content_parts.append("```hcl")
                content_parts.append("resource \"aws_instance\" \"web_server\" {")
                content_parts.append("  ami           = \"ami-0c02fb55956c7d316\"")
                content_parts.append("  instance_type = \"t3.micro\"")
                content_parts.append("  security_groups = [aws_security_group.web_sg.name]")
                content_parts.append("}")
                content_parts.append("```")
                content_parts.append("\n## **Next Steps**")
                content_parts.append("• Specify your infrastructure requirements")
                content_parts.append("• Choose your cloud provider (AWS, Azure, GCP)")
                content_parts.append("• Define your resource needs and constraints")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            elif intent_type == "show_more_options":
                content_parts.append("## Additional Infrastructure Capabilities")
                content_parts.append("Here are additional capabilities and options I can help you with:")
                content_parts.append("\n## **Advanced Infrastructure**")
                content_parts.append("• **Microservices**: Service mesh, API gateways, container orchestration")
                content_parts.append("• **Serverless**: AWS Lambda, Azure Functions, Google Cloud Functions")
                content_parts.append("• **Edge Computing**: CDN, edge locations, distributed processing")
                content_parts.append("\n## **DevOps Automation**")
                content_parts.append("• **CI/CD Pipelines**: Jenkins, GitLab CI, GitHub Actions")
                content_parts.append("• **Deployment Strategies**: Blue-green, canary, rolling deployments")
                content_parts.append("• **Testing**: Infrastructure testing, security scanning, performance testing")
                content_parts.append("\n## **Cloud Migration & Optimization**")
                content_parts.append("• **Migration Strategies**: Lift-and-shift, refactoring, hybrid cloud")
                content_parts.append("• **Disaster Recovery**: Backup strategies, failover, business continuity")
                content_parts.append("• **Performance Tuning**: Optimization, scaling, load testing")
                content_parts.append("\n## **Next Steps**")
                content_parts.append("• Ask about specific technologies or use cases")
                content_parts.append("• Request detailed implementation examples")
                content_parts.append("• Get help with your specific infrastructure challenges")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            elif intent_type == "explain_behavior":
                content_parts.append("## Understanding My Responses")
                content_parts.append("I understand your concern about repetitive responses. Let me explain:")
                content_parts.append("\n## **My Approach**")
                content_parts.append("• I provide consistent, professional infrastructure guidance")
                content_parts.append("• Each response is tailored to your specific query and context")
                content_parts.append("• I can provide more detailed, specific information if you ask targeted questions")
                content_parts.append("• Try asking about specific technologies, use cases, or implementation details")
                content_parts.append("\n## **For More Specific Responses**")
                content_parts.append("• 'Show me terraform examples for AWS'")
                content_parts.append("• 'How do I set up monitoring with Prometheus?'")
                content_parts.append("• 'What's the best way to secure my Kubernetes cluster?'")
                content_parts.append("• 'Compare different database options for my application'")
                content_parts.append("• 'Help me design a microservices architecture'")
                content_parts.append("\n## **Next Steps**")
                content_parts.append("• Ask specific questions about your infrastructure needs")
                content_parts.append("• Request code examples and implementation details")
                content_parts.append("• Get help with your particular use case or technology stack")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            elif intent_type == "explain_agent_functionality":
                content_parts.append("## 🤖 How I Work - AI Infrastructure Assistant")
                content_parts.append("")
                content_parts.append("## **My Intelligence System**")
                content_parts.append("• **Natural Language Processing**: I analyze your queries using keyword extraction and pattern matching")
                content_parts.append("• **Local Knowledge Base**: I have a comprehensive database of infrastructure patterns, best practices, and scenarios")
                content_parts.append("• **Context-Aware Responses**: I remember our conversation and provide contextual, non-repetitive responses")
                content_parts.append("• **Multi-Agent Architecture**: I can route requests to specialized agents (Terraform, Ansible, Kubernetes, Security, Monitoring)")
                content_parts.append("")
                content_parts.append("## **My Capabilities**")
                content_parts.append("• **Infrastructure Analysis**: I understand complex infrastructure requirements and provide detailed recommendations")
                content_parts.append("• **Technology Expertise**: Deep knowledge of cloud platforms, DevOps tools, and infrastructure patterns")
                content_parts.append("• **Cost Optimization**: I can analyze costs and suggest optimization strategies")
                content_parts.append("• **Security & Compliance**: I provide security hardening and compliance guidance")
                content_parts.append("")
                content_parts.append("## **How to Get the Best Results**")
                content_parts.append("• Ask specific questions about technologies or use cases")
                content_parts.append("• Provide context about your infrastructure needs")
                content_parts.append("• Ask follow-up questions for deeper insights")
                content_parts.append("• Use clear, descriptive language about your requirements")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            elif intent_type == "follow_up_question":
                # Handle follow-up questions with specific recommendations
                recommendations = analysis.get("recommendations", [])
                if recommendations:
                    content_parts.append("## Request Summary")
                    content_parts.append(f"Analyzing your infrastructure request: {request}")
                    content_parts.append("\n## **Setup & Architecture**")
                    for rec in recommendations[:3]:  # Limit to top 3
                        content_parts.append(f"• {rec}")
                    content_parts.append("\n## **Best Practices**")
                    content_parts.append("• Implement health checks and monitoring")
                    content_parts.append("• Use multiple availability zones")
                    content_parts.append("• Implement proper backup strategies")
                    content_parts.append("\n## **Key Insights**")
                    knowledge = analysis.get("knowledge", [])
                    if knowledge:
                        for k in knowledge[:2]:  # Limit to top 2
                            title = getattr(k, 'title', 'Infrastructure Insight')
                            content = getattr(k, 'content', '')
                            content_parts.append(f"• {title}: {content[:100]}...")
                    content_parts.append("\n## **Next Steps**")
                    content_parts.append("• Review the recommended architecture")
                    content_parts.append("• Implement security hardening measures")
                    content_parts.append("• Set up monitoring and alerting")
                    content_parts.append("• Plan for disaster recovery and backup")
                else:
                    content_parts.append("## Request Summary")
                    content_parts.append(f"Analyzing your infrastructure request: {request}")
                    content_parts.append("\n## **Setup & Architecture**")
                    content_parts.append("• I'd be happy to provide more details! Could you please specify:")
                    content_parts.append("•   • What specific aspect would you like me to explain further?")
                    content_parts.append("•   • Are you looking for implementation details, best practices, or cost estimates?")
                    content_parts.append("\n## **Best Practices**")
                    content_parts.append("• Implement health checks and monitoring")
                    content_parts.append("• Use multiple availability zones")
                    content_parts.append("• Implement proper backup strategies")
                    content_parts.append("\n## **Key Insights**")
                    content_parts.append("• Web Server Infrastructure Basics: A web server infrastructure typically includes: 1) Load balancer for traffic distribution, 2) Web servers (Apache/Nginx) for serving content, 3) Application servers for business logic, 4) Database servers for data storage, 5) CDN for content delivery, 6) Security layers (firewalls, SSL certificates), 7) Monitoring and logging systems, 8) Backup and disaster recovery systems, 9) Auto-scaling capabilities, 10) Load balancing strategies")
                    content_parts.append("• Server Security Hardening: Security hardening includes: 1) Regular security updates and patches, 2) Firewall configuration and network segmentation, 3) SSH key authentication and disable password login, 4) Disable unnecessary services and ports, 5) Implement fail2ban for intrusion prevention, 6) Regular security audits and vulnerability scanning, 7) User access control and privilege management, 8) File system permissions and ownership, 9) Log monitoring and analysis, 10) Incident response and backup strategies")
                    content_parts.append("\n## **Next Steps**")
                    content_parts.append("• Review the recommended architecture")
                    content_parts.append("• Implement security hardening measures")
                    content_parts.append("• Set up monitoring and alerting")
                    content_parts.append("• Plan for disaster recovery and backup")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.8,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            elif intent_type in ["show_capabilities", "general_help"]:
                content_parts.append("## AI Infrastructure Assistant Capabilities")
                content_parts.append("I'm trained to support you with cloud architecture, DevOps, and infrastructure management.")
                content_parts.append("\n## **Core Capabilities**")
                content_parts.append("• **Infrastructure Management**: Terraform, Ansible, Kubernetes")
                content_parts.append("• **Security & Compliance**: Hardening, vulnerability scanning, IAM policies")
                content_parts.append("• **Monitoring & Observability**: Prometheus, Grafana, ELK stack")
                content_parts.append("• **Cost Optimization**: Rightsizing, reserved instances, auto-scaling")
                content_parts.append("\n## **Next Steps**")
                content_parts.append("• Specify your infrastructure requirements")
                content_parts.append("• Choose your preferred cloud provider (AWS, Azure, GCP)")
                content_parts.append("• Define your security and compliance needs")
                content = "\n".join(content_parts)
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content=content,
                    confidence=0.9,
                    metadata={"intent": intent_type, "format": "professional"}
                )
            else:
                content_parts.append(f"## Request Summary")
                content_parts.append(f"Analyzing your infrastructure request: {request[:100]}{'...' if len(request) > 100 else ''}")
            
            # Main recommendations with structured sections
            if analysis["recommendations"]:
                content_parts.append("\n## **Setup & Architecture**")
                # Limit to top 3 recommendations to avoid clutter
                for rec in analysis["recommendations"][:3]:
                    if rec.startswith("##"):
                        content_parts.append(rec)  # Keep existing headers
                    else:
                        content_parts.append(f"• {rec}")
            
            # Technical analysis and reasoning
            if analysis.get("reasoning"):
                content_parts.append("\n## **Technical Analysis**")
                # Limit to top 2 reasoning points to avoid clutter
                for reason in analysis["reasoning"][:2]:
                    content_parts.append(f"• {reason}")
            
            # Security considerations
            keywords = analysis.get("keywords", {})
            security_keywords = keywords.get("security", []) if isinstance(keywords.get("security"), list) else []
            if ("security" in str(analysis.get("intent", "")).lower() or 
                any("security" in str(kw).lower() for kw in security_keywords)):
                content_parts.append("\n## **Security**")
                content_parts.append("• Implement IAM policies with least privilege access")
                content_parts.append("• Enable encryption at rest and in transit")
                content_parts.append("• Configure network security groups and firewalls")
                content_parts.append("• Set up security monitoring and alerting")
            
            # Monitoring and observability
            monitoring_keywords = keywords.get("monitoring", []) if isinstance(keywords.get("monitoring"), list) else []
            if ("monitoring" in str(analysis.get("intent", "")).lower() or 
                any("monitoring" in str(kw).lower() for kw in monitoring_keywords)):
                content_parts.append("\n## **Monitoring**")
                content_parts.append("• Deploy Prometheus for metrics collection")
                content_parts.append("• Configure Grafana dashboards for visualization")
                content_parts.append("• Set up log aggregation with ELK stack")
                content_parts.append("• Implement health checks and alerting")
            
            # Cost optimization
            cost_keywords = keywords.get("cost", []) if isinstance(keywords.get("cost"), list) else []
            if ("cost" in str(analysis.get("intent", "")).lower() or 
                any("cost" in str(kw).lower() for kw in cost_keywords)):
                content_parts.append("\n## **Cost Optimization**")
                content_parts.append("• Right-size instances based on actual usage")
                content_parts.append("• Implement reserved instances for predictable workloads")
                content_parts.append("• Use spot instances for flexible workloads")
                content_parts.append("• Set up automated scaling policies")
            
            # Add technical examples and commands
            if analysis.get("intent") in ["create_web_server", "create_database", "create_load_balancer"]:
                content_parts.append("\n## **Implementation Examples**")
                
                if "web_server" in str(analysis.get("intent", "")):
                    content_parts.append("### Terraform Configuration")
                    content_parts.append("```hcl")
                    content_parts.append("# Web server with load balancer")
                    content_parts.append("resource \"aws_instance\" \"web_server\" {")
                    content_parts.append("  ami           = \"ami-0c02fb55956c7d316\"")
                    content_parts.append("  instance_type = \"t3.micro\"")
                    content_parts.append("  security_groups = [aws_security_group.web_sg.name]")
                    content_parts.append("  user_data = file(\"user_data.sh\")")
                    content_parts.append("}")
                    content_parts.append("```")
                
                if "database" in str(analysis.get("intent", "")):
                    content_parts.append("### Database Setup")
                    content_parts.append("```bash")
                    content_parts.append("# Install and configure PostgreSQL")
                    content_parts.append("sudo apt update")
                    content_parts.append("sudo apt install postgresql postgresql-contrib")
                    content_parts.append("sudo systemctl start postgresql")
                    content_parts.append("sudo systemctl enable postgresql")
                    content_parts.append("```")
            
            # Best practices
            if analysis["best_practices"]:
                content_parts.append("\n## **Best Practices**")
                for practice in analysis["best_practices"][:3]:
                    content_parts.append(f"• {practice}")
            
            # Knowledge insights (condensed)
            if analysis["knowledge"]:
                content_parts.append("\n## **Key Insights**")
                for knowledge in analysis["knowledge"][:1]:  # Show top 1 insight
                    content = knowledge.content
                    if len(content) > 150:
                        content = content[:150] + "..."
                    content_parts.append(f"• **{knowledge.title}**: {content}")
            
            # Next steps
            content_parts.append("\n## **Next Steps**")
            if analysis.get("intent") == "show_capabilities":
                content_parts.append("• Specify your infrastructure requirements")
                content_parts.append("• Choose your preferred cloud provider (AWS, Azure, GCP)")
                content_parts.append("• Define your security and compliance needs")
            else:
                content_parts.append("• Review the recommended architecture")
                content_parts.append("• Implement security hardening measures")
                content_parts.append("• Set up monitoring and alerting")
                content_parts.append("• Plan for disaster recovery and backup")
            
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
                    "templates_suggested": len(analysis.get("templates", [])),
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
