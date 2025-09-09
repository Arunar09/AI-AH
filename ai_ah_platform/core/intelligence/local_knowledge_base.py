"""
Local Knowledge Base for AI-AH Platform

This module provides a local intelligence system with datasets and logic
that doesn't require external LLM services. It uses rule-based intelligence
with a comprehensive knowledge base for infrastructure management.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """Represents a knowledge entry in the local knowledge base."""
    id: str
    category: str
    title: str
    content: str
    tags: List[str]
    confidence: float
    created_at: datetime
    updated_at: datetime


@dataclass
class InfrastructurePattern:
    """Represents an infrastructure pattern for matching."""
    pattern: str
    regex: str
    agent_type: str
    action: str
    confidence: float
    parameters: Dict[str, Any]


class LocalKnowledgeBase:
    """
    Local knowledge base with infrastructure intelligence.
    
    This class provides intelligent responses based on:
    1. Infrastructure patterns and templates
    2. Best practices and recommendations
    3. Common infrastructure scenarios
    4. Rule-based decision making
    """
    
    def __init__(self):
        self.knowledge_entries: Dict[str, KnowledgeEntry] = {}
        self.infrastructure_patterns: List[InfrastructurePattern] = []
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.best_practices: Dict[str, List[str]] = {}
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        
        self._initialize_knowledge_base()
        self._initialize_patterns()
        self._initialize_templates()
        self._initialize_best_practices()
        self._initialize_scenarios()
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with infrastructure knowledge."""
        
        # Infrastructure Knowledge Entries
        knowledge_data = [
            {
                "id": "web_server_basics",
                "category": "infrastructure",
                "title": "Web Server Infrastructure Basics",
                "content": "A web server infrastructure typically includes: 1) Load balancer for traffic distribution, 2) Web servers (Apache/Nginx) for serving content, 3) Application servers for business logic, 4) Database servers for data storage, 5) Caching layer (Redis/Memcached), 6) CDN for static content delivery, 7) Monitoring and logging systems.",
                "tags": ["web", "server", "infrastructure", "basics"],
                "confidence": 0.95
            },
            {
                "id": "security_hardening",
                "category": "security",
                "title": "Server Security Hardening",
                "content": "Security hardening includes: 1) Regular security updates, 2) Firewall configuration, 3) SSH key authentication, 4) Disable unnecessary services, 5) Implement fail2ban, 6) Regular security audits, 7) Backup encryption, 8) Network segmentation, 9) Access control policies, 10) Monitoring and alerting.",
                "tags": ["security", "hardening", "server", "best-practices"],
                "confidence": 0.98
            },
            {
                "id": "scalability_patterns",
                "category": "scalability",
                "title": "Infrastructure Scalability Patterns",
                "content": "Scalability patterns include: 1) Horizontal scaling (add more servers), 2) Vertical scaling (upgrade server specs), 3) Load balancing, 4) Database sharding, 5) Caching strategies, 6) CDN implementation, 7) Microservices architecture, 8) Auto-scaling groups, 9) Container orchestration, 10) Performance monitoring.",
                "tags": ["scalability", "performance", "architecture", "patterns"],
                "confidence": 0.92
            },
            {
                "id": "monitoring_essentials",
                "category": "monitoring",
                "title": "Infrastructure Monitoring Essentials",
                "content": "Essential monitoring includes: 1) System metrics (CPU, memory, disk, network), 2) Application metrics (response time, throughput, errors), 3) Business metrics (user activity, revenue), 4) Log aggregation and analysis, 5) Alerting and notification systems, 6) Health checks and uptime monitoring, 7) Performance profiling, 8) Capacity planning metrics.",
                "tags": ["monitoring", "observability", "metrics", "alerting"],
                "confidence": 0.94
            },
            {
                "id": "cost_optimization",
                "category": "cost",
                "title": "Cloud Cost Optimization Strategies",
                "content": "Cost optimization strategies: 1) Right-sizing instances, 2) Reserved instances for predictable workloads, 3) Spot instances for flexible workloads, 4) Auto-scaling to match demand, 5) Storage optimization (lifecycle policies), 6) Network optimization, 7) Resource tagging for cost tracking, 8) Regular cost audits, 9) Eliminate unused resources, 10) Use cost-effective regions.",
                "tags": ["cost", "optimization", "cloud", "budget"],
                "confidence": 0.90
            }
        ]
        
        for entry_data in knowledge_data:
            entry = KnowledgeEntry(
                id=entry_data["id"],
                category=entry_data["category"],
                title=entry_data["title"],
                content=entry_data["content"],
                tags=entry_data["tags"],
                confidence=entry_data["confidence"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.knowledge_entries[entry.id] = entry
    
    def _initialize_patterns(self):
        """Initialize infrastructure patterns for intent recognition."""
        
        patterns = [
            # Web Server Patterns
            InfrastructurePattern(
                pattern="create web server",
                regex=r"(create|setup|deploy|build).*(web|http|apache|nginx).*(server|site|website)",
                agent_type="terraform",
                action="create_web_server",
                confidence=0.9,
                parameters={"server_type": "web", "default_port": 80}
            ),
            InfrastructurePattern(
                pattern="database setup",
                regex=r"(create|setup|deploy|install).*(database|db|mysql|postgres|mongodb)",
                agent_type="terraform",
                action="create_database",
                confidence=0.9,
                parameters={"db_type": "mysql", "default_port": 3306}
            ),
            InfrastructurePattern(
                pattern="load balancer",
                regex=r"(create|setup|deploy|configure).*(load.?balancer|lb|nginx|haproxy)",
                agent_type="terraform",
                action="create_load_balancer",
                confidence=0.85,
                parameters={"lb_type": "application", "health_check": True}
            ),
            
            # Security Patterns
            InfrastructurePattern(
                pattern="security scan",
                regex=r"(security|vulnerability|scan|audit|check).*(security|vulnerabilities|issues)",
                agent_type="security",
                action="security_scan",
                confidence=0.9,
                parameters={"scan_type": "comprehensive", "auto_fix": False}
            ),
            InfrastructurePattern(
                pattern="firewall configuration",
                regex=r"(configure|setup|create).*(firewall|security.?group|iptables)",
                agent_type="security",
                action="configure_firewall",
                confidence=0.85,
                parameters={"default_deny": True, "allow_ssh": True}
            ),
            
            # Monitoring Patterns
            InfrastructurePattern(
                pattern="monitoring setup",
                regex=r"(setup|configure|create|install).*(monitoring|metrics|alerting|grafana|prometheus)",
                agent_type="monitoring",
                action="setup_monitoring",
                confidence=0.9,
                parameters={"monitoring_type": "comprehensive", "alerting": True}
            ),
            InfrastructurePattern(
                pattern="health check",
                regex=r"(check|monitor|status|health).*(system|server|infrastructure|status)",
                agent_type="monitoring",
                action="health_check",
                confidence=0.8,
                parameters={"check_type": "comprehensive", "detailed": True}
            ),
            
            # Configuration Management
            InfrastructurePattern(
                pattern="server configuration",
                regex=r"(configure|setup|manage|automate).*(server|system|configuration|ansible)",
                agent_type="ansible",
                action="configure_server",
                confidence=0.85,
                parameters={"config_type": "comprehensive", "backup": True}
            ),
            InfrastructurePattern(
                pattern="application deployment",
                regex=r"(deploy|release|update|rollout).*(application|app|service|container)",
                agent_type="kubernetes",
                action="deploy_application",
                confidence=0.9,
                parameters={"deployment_type": "rolling", "health_check": True}
            )
        ]
        
        self.infrastructure_patterns = patterns
    
    def _initialize_templates(self):
        """Initialize infrastructure templates."""
        
        self.templates = {
            "web_server": {
                "name": "Basic Web Server",
                "description": "A simple web server with Apache/Nginx",
                "resources": [
                    {"type": "aws_instance", "name": "web_server", "instance_type": "t3.micro"},
                    {"type": "aws_security_group", "name": "web_sg", "ports": [80, 443, 22]}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$10-20/month"
            },
            "web_app_with_db": {
                "name": "Web Application with Database",
                "description": "Complete web application with database backend",
                "resources": [
                    {"type": "aws_instance", "name": "web_server", "instance_type": "t3.small"},
                    {"type": "aws_db_instance", "name": "database", "engine": "mysql"},
                    {"type": "aws_security_group", "name": "app_sg", "ports": [80, 443, 22, 3306]}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$50-100/month"
            },
            "scalable_web_app": {
                "name": "Scalable Web Application",
                "description": "High-availability web application with load balancer",
                "resources": [
                    {"type": "aws_lb", "name": "app_lb", "type": "application"},
                    {"type": "aws_autoscaling_group", "name": "web_asg", "min_size": 2},
                    {"type": "aws_db_instance", "name": "database", "engine": "mysql", "multi_az": True}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$200-500/month"
            },
            "containerized_app": {
                "name": "Containerized Application",
                "description": "Kubernetes deployment for containerized applications",
                "resources": [
                    {"type": "kubernetes_deployment", "name": "app_deployment", "replicas": 3},
                    {"type": "kubernetes_service", "name": "app_service", "type": "LoadBalancer"},
                    {"type": "kubernetes_configmap", "name": "app_config"}
                ],
                "agent_type": "kubernetes",
                "estimated_cost": "$100-300/month"
            }
        }
    
    def _initialize_best_practices(self):
        """Initialize best practices for different infrastructure scenarios."""
        
        self.best_practices = {
            "security": [
                "Always use SSH keys instead of passwords",
                "Implement regular security updates and patches",
                "Configure firewall to deny all by default",
                "Use HTTPS for all web traffic",
                "Implement proper access controls and RBAC",
                "Regular security audits and vulnerability scans",
                "Encrypt data at rest and in transit",
                "Implement backup and disaster recovery plans"
            ],
            "performance": [
                "Use CDN for static content delivery",
                "Implement caching at multiple levels",
                "Optimize database queries and indexing",
                "Use load balancers for traffic distribution",
                "Monitor and optimize resource utilization",
                "Implement auto-scaling for variable workloads",
                "Use appropriate instance types for workloads",
                "Regular performance testing and optimization"
            ],
            "reliability": [
                "Implement health checks and monitoring",
                "Use multiple availability zones",
                "Implement proper backup strategies",
                "Design for failure and implement circuit breakers",
                "Use infrastructure as code for consistency",
                "Implement proper logging and alerting",
                "Regular disaster recovery testing",
                "Use managed services where appropriate"
            ],
            "cost_optimization": [
                "Right-size instances based on actual usage",
                "Use reserved instances for predictable workloads",
                "Implement auto-scaling to match demand",
                "Regular cost audits and optimization reviews",
                "Use spot instances for flexible workloads",
                "Implement proper resource tagging",
                "Eliminate unused resources regularly",
                "Use cost-effective regions and services"
            ]
        }
    
    def _initialize_scenarios(self):
        """Initialize common infrastructure scenarios."""
        
        self.scenarios = {
            "ecommerce": {
                "name": "E-commerce Platform",
                "description": "Complete e-commerce infrastructure with high availability",
                "components": ["web_servers", "database", "cache", "cdn", "monitoring"],
                "estimated_cost": "$500-2000/month",
                "scalability": "high",
                "security_level": "high"
            },
            "blog": {
                "name": "Blog/Content Management",
                "description": "Simple blog or CMS infrastructure",
                "components": ["web_server", "database", "backup"],
                "estimated_cost": "$20-50/month",
                "scalability": "medium",
                "security_level": "medium"
            },
            "api_service": {
                "name": "API Service",
                "description": "RESTful API service infrastructure",
                "components": ["api_servers", "database", "cache", "monitoring"],
                "estimated_cost": "$100-500/month",
                "scalability": "high",
                "security_level": "high"
            },
            "development": {
                "name": "Development Environment",
                "description": "Development and testing infrastructure",
                "components": ["dev_server", "database", "monitoring"],
                "estimated_cost": "$10-30/month",
                "scalability": "low",
                "security_level": "low"
            }
        }
    
    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and determine the best response.
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Dictionary with analysis results, recommendations, and actions
        """
        user_input_lower = user_input.lower()
        
        # Find matching patterns
        matched_patterns = []
        for pattern in self.infrastructure_patterns:
            if re.search(pattern.regex, user_input_lower, re.IGNORECASE):
                matched_patterns.append(pattern)
        
        # Sort by confidence
        matched_patterns.sort(key=lambda x: x.confidence, reverse=True)
        
        if not matched_patterns:
            return self._handle_general_query(user_input)
        
        best_match = matched_patterns[0]
        
        # Get relevant knowledge entries
        relevant_knowledge = self._get_relevant_knowledge(best_match.agent_type, user_input)
        
        # Get best practices
        best_practices = self._get_best_practices(best_match.agent_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(best_match, user_input)
        
        return {
            "intent": best_match.action,
            "agent_type": best_match.agent_type,
            "confidence": best_match.confidence,
            "parameters": best_match.parameters,
            "knowledge": relevant_knowledge,
            "best_practices": best_practices,
            "recommendations": recommendations,
            "templates": self._get_relevant_templates(best_match.agent_type),
            "scenarios": self._get_relevant_scenarios(user_input)
        }
    
    def _handle_general_query(self, user_input: str) -> Dict[str, Any]:
        """Handle general queries that don't match specific patterns."""
        
        # Check for general infrastructure terms
        if any(term in user_input.lower() for term in ["infrastructure", "server", "cloud", "deployment"]):
            return {
                "intent": "general_infrastructure",
                "agent_type": "terraform",
                "confidence": 0.6,
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I can help you with infrastructure setup, security, monitoring, and optimization.",
                    "Please specify what type of infrastructure you need (web server, database, etc.).",
                    "I can provide templates and best practices for your use case."
                ],
                "templates": list(self.templates.values())[:2],  # Show first 2 templates
                "scenarios": list(self.scenarios.values())[:2]   # Show first 2 scenarios
            }
        
        return {
            "intent": "general_help",
            "agent_type": "general",
            "confidence": 0.5,
            "parameters": {},
            "knowledge": [],
            "best_practices": [],
            "recommendations": [
                "I'm an AI infrastructure assistant. I can help you with:",
                "• Infrastructure setup and management",
                "• Security hardening and compliance",
                "• Monitoring and observability",
                "• Cost optimization",
                "• Best practices and recommendations",
                "Please ask me about specific infrastructure needs!"
            ],
            "templates": [],
            "scenarios": []
        }
    
    def _get_relevant_knowledge(self, agent_type: str, user_input: str) -> List[KnowledgeEntry]:
        """Get knowledge entries relevant to the agent type and user input."""
        relevant = []
        
        for entry in self.knowledge_entries.values():
            # Check if entry is relevant to agent type
            if agent_type in entry.tags or any(tag in user_input.lower() for tag in entry.tags):
                relevant.append(entry)
        
        return relevant[:3]  # Return top 3 most relevant
    
    def _get_best_practices(self, agent_type: str) -> List[str]:
        """Get best practices relevant to the agent type."""
        practices = []
        
        # Map agent types to practice categories
        category_mapping = {
            "terraform": ["reliability", "cost_optimization"],
            "security": ["security"],
            "monitoring": ["performance", "reliability"],
            "ansible": ["reliability", "performance"],
            "kubernetes": ["performance", "reliability"]
        }
        
        categories = category_mapping.get(agent_type, ["reliability"])
        for category in categories:
            practices.extend(self.best_practices.get(category, []))
        
        return practices[:5]  # Return top 5 practices
    
    def _generate_recommendations(self, pattern: InfrastructurePattern, user_input: str) -> List[str]:
        """Generate specific recommendations based on the matched pattern."""
        recommendations = []
        
        if pattern.action == "create_web_server":
            recommendations = [
                "I'll help you create a web server infrastructure.",
                "Recommended: Start with a basic web server template and scale as needed.",
                "Consider implementing load balancing for high availability.",
                "Don't forget to configure security groups and SSL certificates."
            ]
        elif pattern.action == "create_database":
            recommendations = [
                "I'll help you set up a database infrastructure.",
                "Recommended: Use managed database services for better reliability.",
                "Implement proper backup and monitoring for your database.",
                "Consider read replicas for better performance."
            ]
        elif pattern.action == "security_scan":
            recommendations = [
                "I'll perform a comprehensive security assessment.",
                "This will include vulnerability scanning and configuration review.",
                "I'll provide recommendations for security improvements.",
                "Consider implementing automated security monitoring."
            ]
        elif pattern.action == "setup_monitoring":
            recommendations = [
                "I'll set up comprehensive monitoring for your infrastructure.",
                "This includes system metrics, application metrics, and alerting.",
                "I'll configure dashboards for better visibility.",
                "Set up automated alerts for critical issues."
            ]
        else:
            recommendations = [
                f"I'll help you with {pattern.action.replace('_', ' ')}.",
                "Let me analyze your requirements and provide the best solution.",
                "I'll include best practices and security considerations."
            ]
        
        return recommendations
    
    def _get_relevant_templates(self, agent_type: str) -> List[Dict[str, Any]]:
        """Get templates relevant to the agent type."""
        relevant = []
        
        for template in self.templates.values():
            if template["agent_type"] == agent_type:
                relevant.append(template)
        
        return relevant[:2]  # Return top 2 templates
    
    def _get_relevant_scenarios(self, user_input: str) -> List[Dict[str, Any]]:
        """Get scenarios relevant to the user input."""
        relevant = []
        
        for scenario in self.scenarios.values():
            if any(term in user_input.lower() for term in scenario["name"].lower().split()):
                relevant.append(scenario)
        
        return relevant[:2]  # Return top 2 scenarios
    
    def get_knowledge_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Get all knowledge entries for a specific category."""
        return [entry for entry in self.knowledge_entries.values() if entry.category == category]
    
    def add_knowledge_entry(self, entry: KnowledgeEntry):
        """Add a new knowledge entry to the knowledge base."""
        self.knowledge_entries[entry.id] = entry
        logger.info(f"Added knowledge entry: {entry.id}")
    
    def update_knowledge_entry(self, entry_id: str, updates: Dict[str, Any]):
        """Update an existing knowledge entry."""
        if entry_id in self.knowledge_entries:
            entry = self.knowledge_entries[entry_id]
            for key, value in updates.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            entry.updated_at = datetime.now()
            logger.info(f"Updated knowledge entry: {entry_id}")
    
    def search_knowledge(self, query: str) -> List[KnowledgeEntry]:
        """Search knowledge entries by query."""
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge_entries.values():
            # Search in title, content, and tags
            if (query_lower in entry.title.lower() or 
                query_lower in entry.content.lower() or 
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
        
        # Sort by relevance (simple scoring)
        results.sort(key=lambda x: (
            query_lower in x.title.lower(),
            query_lower in x.content.lower(),
            x.confidence
        ), reverse=True)
        
        return results[:10]  # Return top 10 results
