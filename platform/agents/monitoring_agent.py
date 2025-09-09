"""
Monitoring & Observability Agent for the Multi-Agent Infrastructure Intelligence Platform.

This agent specializes in monitoring, observability, alerting, and performance optimization
for infrastructure and applications.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
class MonitoringRule:
    """Represents a monitoring rule or metric."""
    id: str
    name: str
    description: str
    metric_type: str  # cpu, memory, disk, network, custom
    threshold: float
    operator: str  # >, <, >=, <=, ==, !=
    severity: str  # info, warning, critical
    evaluation_interval: int  # seconds
    notification_channels: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Represents a monitoring alert."""
    id: str
    rule_id: str
    name: str
    description: str
    severity: str
    status: str  # active, resolved, acknowledged
    triggered_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dashboard:
    """Represents a monitoring dashboard."""
    id: str
    name: str
    description: str
    panels: List[Dict[str, Any]]
    refresh_interval: int  # seconds
    time_range: str  # 1h, 6h, 24h, 7d, 30d
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringConfiguration:
    """Represents a monitoring configuration."""
    id: str
    name: str
    description: str
    targets: List[str]  # hosts, services, applications
    rules: List[MonitoringRule]
    dashboards: List[Dashboard]
    exporters: List[Dict[str, Any]]  # Prometheus exporters, etc.
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)


class MonitoringAgent(IntelligentAgent):
    """
    Monitoring & Observability Agent.
    
    Specializes in:
    - Infrastructure and application monitoring
    - Metrics collection and analysis
    - Alerting and notification management
    - Dashboard creation and management
    - Performance optimization recommendations
    """
    
    def __init__(self, config: PlatformConfig, workspace_path: str = None):
        super().__init__(config)
        
        self.workspace_path = workspace_path or tempfile.mkdtemp(prefix="monitoring_agent_")
        self.configurations: Dict[str, MonitoringConfiguration] = {}
        self.alerts: Dict[str, Alert] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        self.metrics_data: Dict[str, List[Dict[str, Any]]] = {}
        
        # Monitoring-specific capabilities
        self.capabilities = [
            AgentCapability(
                name="infrastructure_monitoring",
                description="Monitor infrastructure components",
                version="1.0.0",
                parameters={"supported_metrics": ["cpu", "memory", "disk", "network", "process"]}
            ),
            AgentCapability(
                name="application_monitoring",
                description="Monitor applications and services",
                version="1.0.0"
            ),
            AgentCapability(
                name="alerting_management",
                description="Manage alerts and notifications",
                version="1.0.0"
            ),
            AgentCapability(
                name="dashboard_creation",
                description="Create and manage monitoring dashboards",
                version="1.0.0"
            ),
            AgentCapability(
                name="performance_optimization",
                description="Analyze performance and provide optimization recommendations",
                version="1.0.0"
            )
        ]
        
        # Initialize monitoring templates
        self._initialize_monitoring_templates()
        self._initialize_metric_templates()
    
    async def _initialize_capabilities(self):
        """Initialize Monitoring-specific capabilities."""
        # Add Monitoring-specific response handlers
        self.add_response_handler("setup_monitoring", self._handle_setup_monitoring)
        self.add_response_handler("create_dashboard", self._handle_create_dashboard)
        self.add_response_handler("configure_alerts", self._handle_configure_alerts)
        self.add_response_handler("analyze_performance", self._handle_analyze_performance)
        
        # Add context processors
        self.add_context_processor(self._process_monitoring_context)
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers for Monitoring operations."""
        pass  # Already handled in _initialize_capabilities
    
    async def _initialize_context_processors(self):
        """Initialize context processors for Monitoring operations."""
        pass  # Already handled in _initialize_capabilities
    
    def _initialize_monitoring_templates(self):
        """Initialize common monitoring templates."""
        self.monitoring_templates = {
            "infrastructure_monitoring": {
                "name": "Infrastructure Monitoring",
                "description": "Monitor infrastructure components",
                "metrics": [
                    {"type": "cpu", "name": "CPU Usage", "threshold": 80, "operator": ">"},
                    {"type": "memory", "name": "Memory Usage", "threshold": 85, "operator": ">"},
                    {"type": "disk", "name": "Disk Usage", "threshold": 90, "operator": ">"},
                    {"type": "network", "name": "Network Traffic", "threshold": 1000, "operator": ">"}
                ],
                "exporters": ["node_exporter", "cadvisor"],
                "dashboards": ["infrastructure_overview", "system_metrics"]
            },
            "application_monitoring": {
                "name": "Application Monitoring",
                "description": "Monitor applications and services",
                "metrics": [
                    {"type": "response_time", "name": "Response Time", "threshold": 1000, "operator": ">"},
                    {"type": "error_rate", "name": "Error Rate", "threshold": 5, "operator": ">"},
                    {"type": "throughput", "name": "Request Throughput", "threshold": 100, "operator": "<"},
                    {"type": "availability", "name": "Service Availability", "threshold": 99, "operator": "<"}
                ],
                "exporters": ["application_exporter", "nginx_exporter"],
                "dashboards": ["application_overview", "service_metrics"]
            },
            "database_monitoring": {
                "name": "Database Monitoring",
                "description": "Monitor database performance",
                "metrics": [
                    {"type": "connection_count", "name": "Connection Count", "threshold": 80, "operator": ">"},
                    {"type": "query_time", "name": "Query Time", "threshold": 5000, "operator": ">"},
                    {"type": "cache_hit_ratio", "name": "Cache Hit Ratio", "threshold": 90, "operator": "<"},
                    {"type": "disk_io", "name": "Disk I/O", "threshold": 1000, "operator": ">"}
                ],
                "exporters": ["mysql_exporter", "postgres_exporter"],
                "dashboards": ["database_overview", "query_performance"]
            },
            "kubernetes_monitoring": {
                "name": "Kubernetes Monitoring",
                "description": "Monitor Kubernetes clusters",
                "metrics": [
                    {"type": "pod_restarts", "name": "Pod Restarts", "threshold": 5, "operator": ">"},
                    {"type": "resource_usage", "name": "Resource Usage", "threshold": 80, "operator": ">"},
                    {"type": "deployment_status", "name": "Deployment Status", "threshold": 1, "operator": "!="},
                    {"type": "service_availability", "name": "Service Availability", "threshold": 99, "operator": "<"}
                ],
                "exporters": ["kube-state-metrics", "cadvisor"],
                "dashboards": ["kubernetes_overview", "pod_metrics", "service_metrics"]
            }
        }
    
    def _initialize_metric_templates(self):
        """Initialize common metric templates."""
        self.metric_templates = {
            "cpu": {
                "name": "CPU Usage",
                "description": "CPU utilization percentage",
                "unit": "percent",
                "type": "gauge",
                "query": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
                "thresholds": {"warning": 70, "critical": 90}
            },
            "memory": {
                "name": "Memory Usage",
                "description": "Memory utilization percentage",
                "unit": "percent",
                "type": "gauge",
                "query": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
                "thresholds": {"warning": 80, "critical": 95}
            },
            "disk": {
                "name": "Disk Usage",
                "description": "Disk utilization percentage",
                "unit": "percent",
                "type": "gauge",
                "query": "100 - ((node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes)",
                "thresholds": {"warning": 85, "critical": 95}
            },
            "network": {
                "name": "Network Traffic",
                "description": "Network traffic rate",
                "unit": "bytes/sec",
                "type": "counter",
                "query": "rate(node_network_receive_bytes_total[5m])",
                "thresholds": {"warning": 1000000000, "critical": 5000000000}  # 1GB/s, 5GB/s
            },
            "response_time": {
                "name": "Response Time",
                "description": "HTTP response time",
                "unit": "milliseconds",
                "type": "histogram",
                "query": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                "thresholds": {"warning": 500, "critical": 2000}
            },
            "error_rate": {
                "name": "Error Rate",
                "description": "HTTP error rate percentage",
                "unit": "percent",
                "type": "gauge",
                "query": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
                "thresholds": {"warning": 1, "critical": 5}
            }
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a Monitoring-related request."""
        try:
            # Parse the request
            parsed_request = await self._parse_monitoring_request(request)
            
            # Generate response based on intent
            if "monitor" in parsed_request.original_text.lower() or "setup" in parsed_request.original_text.lower():
                return await self._handle_setup_monitoring(parsed_request, context)
            elif "dashboard" in parsed_request.original_text.lower():
                return await self._handle_create_dashboard(parsed_request, context)
            elif "alert" in parsed_request.original_text.lower():
                return await self._handle_configure_alerts(parsed_request, context)
            elif "performance" in parsed_request.original_text.lower() or "analyze" in parsed_request.original_text.lower():
                return await self._handle_analyze_performance(parsed_request, context)
            else:
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content="I can help you with monitoring setup, dashboard creation, alerting, and performance analysis. What would you like to do?",
                    confidence=0.8
                )
                
        except Exception as e:
            self.logger.error(f"Error processing Monitoring request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze monitoring requirements."""
        try:
            # Parse requirements
            parsed_request = await self._parse_monitoring_request(requirements)
            
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
                "monitoring_types": [],
                "metrics": [],
                "targets": [],
                "recommendations": []
            }
            
            # Extract monitoring types
            for entity in parsed_request.entities:
                if entity.type == EntityType.SERVICE:
                    if entity.value.lower() in ["infrastructure", "server", "host"]:
                        analysis["monitoring_types"].append("infrastructure_monitoring")
                    elif entity.value.lower() in ["application", "app", "service"]:
                        analysis["monitoring_types"].append("application_monitoring")
                    elif entity.value.lower() in ["database", "db", "mysql", "postgresql"]:
                        analysis["monitoring_types"].append("database_monitoring")
                    elif entity.value.lower() in ["kubernetes", "k8s", "container"]:
                        analysis["monitoring_types"].append("kubernetes_monitoring")
            
            # Extract metrics
            for entity in parsed_request.entities:
                if entity.type == EntityType.MONITORING:
                    if entity.value.lower() in ["cpu", "memory", "disk", "network"]:
                        analysis["metrics"].append(entity.value.lower())
                    elif entity.value.lower() in ["response", "latency", "throughput"]:
                        analysis["metrics"].append("response_time")
                    elif entity.value.lower() in ["error", "availability"]:
                        analysis["metrics"].append("error_rate")
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_monitoring_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing monitoring requirements: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def generate_monitoring_configuration(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a monitoring configuration."""
        try:
            config_id = f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create monitoring configuration
            configuration = MonitoringConfiguration(
                id=config_id,
                name=analysis.get("name", f"Monitoring Configuration {config_id}"),
                description=analysis.get("description", "Generated monitoring configuration"),
                targets=analysis.get("targets", ["localhost"]),
                rules=[],
                dashboards=[],
                exporters=[]
            )
            
            # Add monitoring rules based on analysis
            for monitoring_type in analysis.get("monitoring_types", []):
                if monitoring_type in self.monitoring_templates:
                    template = self.monitoring_templates[monitoring_type]
                    for metric_config in template["metrics"]:
                        rule = MonitoringRule(
                            id=f"{monitoring_type}_{metric_config['type']}",
                            name=metric_config["name"],
                            description=f"Monitor {metric_config['name']}",
                            metric_type=metric_config["type"],
                            threshold=metric_config["threshold"],
                            operator=metric_config["operator"],
                            severity="warning",
                            evaluation_interval=60,
                            notification_channels=["email", "slack"]
                        )
                        configuration.rules.append(rule)
                    
                    # Add exporters
                    for exporter in template["exporters"]:
                        configuration.exporters.append({
                            "name": exporter,
                            "type": "prometheus_exporter",
                            "port": 9100,
                            "enabled": True
                        })
            
            # Store configuration
            self.configurations[config_id] = configuration
            
            # Generate monitoring configuration files
            await self._generate_monitoring_configurations(configuration)
            
            return {
                "config_id": config_id,
                "status": "created",
                "rules": len(configuration.rules),
                "exporters": len(configuration.exporters),
                "targets": configuration.targets,
                "files_generated": True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating monitoring configuration: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def execute_monitoring_setup(self, configuration: Dict[str, Any]) -> Dict[str, Any]:
        """Execute monitoring setup."""
        try:
            config_id = configuration.get("config_id")
            if not config_id or config_id not in self.configurations:
                return {"error": "Configuration not found", "status": "failed"}
            
            monitoring_config = self.configurations[config_id]
            
            # Simulate monitoring setup
            setup_result = await self._setup_monitoring_components(monitoring_config)
            
            # Update configuration status
            monitoring_config.status = "active" if setup_result["success"] else "failed"
            
            return {
                "config_id": config_id,
                "status": monitoring_config.status,
                "setup_result": setup_result,
                "monitoring_active": setup_result["success"]
            }
            
        except Exception as e:
            self.logger.error(f"Error executing monitoring setup: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def _parse_monitoring_request(self, request: str) -> ParsedRequest:
        """Parse a Monitoring-specific request."""
        # This would integrate with the NLP processor
        # For now, we'll do basic parsing
        request_lower = request.lower()
        
        # Simple intent detection
        if any(word in request_lower for word in ["monitor", "setup", "configure"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["dashboard", "visualize", "display"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["alert", "notify", "warning"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        else:
            intent_type = IntentType.UNKNOWN
        
        # Simple entity extraction
        entities = []
        if "infrastructure" in request_lower or "server" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "infrastructure"})
        if "application" in request_lower or "app" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "application"})
        if "database" in request_lower or "db" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "database"})
        if "kubernetes" in request_lower or "k8s" in request_lower:
            entities.append({"type": EntityType.SERVICE, "value": "kubernetes"})
        if "cpu" in request_lower:
            entities.append({"type": EntityType.MONITORING, "value": "cpu"})
        if "memory" in request_lower:
            entities.append({"type": EntityType.MONITORING, "value": "memory"})
        if "disk" in request_lower:
            entities.append({"type": EntityType.MONITORING, "value": "disk"})
        if "network" in request_lower:
            entities.append({"type": EntityType.MONITORING, "value": "network"})
        
        return ParsedRequest(
            original_text=request,
            intent={"type": intent_type, "confidence": 0.8},
            entities=entities,
            confidence=0.8
        )
    
    async def _handle_setup_monitoring(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle monitoring setup requests."""
        # Analyze requirements
        analysis = await self.analyze_requirements(parsed_request.original_text)
        
        # Generate monitoring configuration
        configuration = await self.generate_monitoring_configuration(analysis)
        
        if configuration.get("status") == "created":
            return AgentResponse(
                agent_id=self.config.name,
                response_type="monitoring_configuration",
                content=f"I've created a monitoring configuration with {configuration['rules']} monitoring rules and {configuration['exporters']} exporters for {', '.join(configuration['targets'])} targets.",
                confidence=0.9,
                suggestions=[
                    "Review the monitoring configuration files",
                    "Execute the setup to start monitoring",
                    "Create custom dashboards for visualization"
                ],
                next_actions=[
                    "monitoring_config_review",
                    "monitoring_setup_execute",
                    "dashboard_create"
                ],
                metadata={"config_id": configuration["config_id"], "analysis": analysis}
            )
        else:
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content="I encountered an error creating the monitoring configuration.",
                confidence=0.0,
                metadata={"error": configuration.get("error")}
            )
    
    async def _handle_create_dashboard(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle dashboard creation requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you create monitoring dashboards. Let me analyze your requirements and create custom dashboards.",
            confidence=0.8,
            suggestions=["Select dashboard type", "Configure panels and metrics", "Set up auto-refresh"]
        )
    
    async def _handle_configure_alerts(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle alert configuration requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you configure monitoring alerts. Let me set up alerting rules and notification channels.",
            confidence=0.8,
            suggestions=["Configure alert rules", "Set up notification channels", "Test alert delivery"]
        )
    
    async def _handle_analyze_performance(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle performance analysis requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you analyze performance. Let me collect metrics and provide optimization recommendations.",
            confidence=0.8,
            suggestions=["Collect performance metrics", "Analyze bottlenecks", "Generate optimization recommendations"]
        )
    
    async def _process_monitoring_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context for Monitoring operations."""
        processed_context = context.copy()
        
        # Add Monitoring-specific context
        processed_context["monitoring_workspace"] = self.workspace_path
        processed_context["available_configurations"] = list(self.configurations.keys())
        processed_context["active_alerts"] = len([a for a in self.alerts.values() if a.status == "active"])
        processed_context["available_dashboards"] = list(self.dashboards.keys())
        
        return processed_context
    
    async def _generate_monitoring_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate monitoring recommendations based on analysis."""
        recommendations = []
        
        # Infrastructure monitoring recommendations
        if "infrastructure_monitoring" in analysis["monitoring_types"]:
            recommendations.append("Set up comprehensive infrastructure monitoring")
            recommendations.append("Configure CPU, memory, disk, and network monitoring")
            recommendations.append("Implement automated alerting for critical thresholds")
        
        # Application monitoring recommendations
        if "application_monitoring" in analysis["monitoring_types"]:
            recommendations.append("Monitor application performance metrics")
            recommendations.append("Track response times and error rates")
            recommendations.append("Set up user experience monitoring")
        
        # Database monitoring recommendations
        if "database_monitoring" in analysis["monitoring_types"]:
            recommendations.append("Monitor database performance and health")
            recommendations.append("Track query performance and connection metrics")
            recommendations.append("Set up database backup monitoring")
        
        # Kubernetes monitoring recommendations
        if "kubernetes_monitoring" in analysis["monitoring_types"]:
            recommendations.append("Monitor Kubernetes cluster health")
            recommendations.append("Track pod and service metrics")
            recommendations.append("Set up resource usage monitoring")
        
        return recommendations
    
    async def _generate_monitoring_configurations(self, configuration: MonitoringConfiguration):
        """Generate monitoring configuration files."""
        config_dir = Path(self.workspace_path) / configuration.id
        config_dir.mkdir(exist_ok=True)
        
        # Generate Prometheus configuration
        prometheus_config = self._generate_prometheus_config(configuration)
        with open(config_dir / "prometheus.yml", "w") as f:
            yaml.dump(prometheus_config, f, default_flow_style=False)
        
        # Generate Grafana dashboard configuration
        grafana_config = self._generate_grafana_config(configuration)
        with open(config_dir / "grafana-dashboard.json", "w") as f:
            json.dump(grafana_config, f, indent=2)
        
        # Generate alerting rules
        alerting_rules = self._generate_alerting_rules(configuration)
        with open(config_dir / "alerting-rules.yml", "w") as f:
            yaml.dump(alerting_rules, f, default_flow_style=False)
        
        # Generate Docker Compose for monitoring stack
        docker_compose = self._generate_docker_compose(configuration)
        with open(config_dir / "docker-compose.yml", "w") as f:
            yaml.dump(docker_compose, f, default_flow_style=False)
    
    def _generate_prometheus_config(self, configuration: MonitoringConfiguration) -> Dict[str, Any]:
        """Generate Prometheus configuration."""
        config = {
            "global": {
                "scrape_interval": "15s",
                "evaluation_interval": "15s"
            },
            "rule_files": ["alerting-rules.yml"],
            "scrape_configs": []
        }
        
        # Add scrape configs for exporters
        for exporter in configuration.exporters:
            scrape_config = {
                "job_name": exporter["name"],
                "static_configs": [
                    {
                        "targets": [f"{target}:{exporter['port']}" for target in configuration.targets]
                    }
                ]
            }
            config["scrape_configs"].append(scrape_config)
        
        return config
    
    def _generate_grafana_config(self, configuration: MonitoringConfiguration) -> Dict[str, Any]:
        """Generate Grafana dashboard configuration."""
        dashboard = {
            "dashboard": {
                "id": None,
                "title": configuration.name,
                "description": configuration.description,
                "panels": [],
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "refresh": "30s"
            }
        }
        
        # Add panels for each monitoring rule
        for i, rule in enumerate(configuration.rules):
            panel = {
                "id": i + 1,
                "title": rule.name,
                "type": "graph",
                "targets": [
                    {
                        "expr": self.metric_templates.get(rule.metric_type, {}).get("query", ""),
                        "legendFormat": rule.name
                    }
                ],
                "yAxes": [
                    {
                        "label": self.metric_templates.get(rule.metric_type, {}).get("unit", ""),
                        "min": 0
                    }
                ],
                "thresholds": [
                    {
                        "value": rule.threshold,
                        "colorMode": "critical",
                        "op": rule.operator
                    }
                ]
            }
            dashboard["dashboard"]["panels"].append(panel)
        
        return dashboard
    
    def _generate_alerting_rules(self, configuration: MonitoringConfiguration) -> Dict[str, Any]:
        """Generate alerting rules configuration."""
        groups = [
            {
                "name": "monitoring_alerts",
                "rules": []
            }
        ]
        
        for rule in configuration.rules:
            alert_rule = {
                "alert": rule.name,
                "expr": f"{self.metric_templates.get(rule.metric_type, {}).get('query', '')} {rule.operator} {rule.threshold}",
                "for": "5m",
                "labels": {
                    "severity": rule.severity,
                    "service": "monitoring"
                },
                "annotations": {
                    "summary": f"{rule.name} is {rule.operator} {rule.threshold}",
                    "description": rule.description
                }
            }
            groups[0]["rules"].append(alert_rule)
        
        return {"groups": groups}
    
    def _generate_docker_compose(self, configuration: MonitoringConfiguration) -> Dict[str, Any]:
        """Generate Docker Compose configuration for monitoring stack."""
        services = {
            "prometheus": {
                "image": "prom/prometheus:latest",
                "ports": ["9090:9090"],
                "volumes": [
                    "./prometheus.yml:/etc/prometheus/prometheus.yml",
                    "./alerting-rules.yml:/etc/prometheus/alerting-rules.yml"
                ],
                "command": [
                    "--config.file=/etc/prometheus/prometheus.yml",
                    "--storage.tsdb.path=/prometheus",
                    "--web.console.libraries=/etc/prometheus/console_libraries",
                    "--web.console.templates=/etc/prometheus/consoles"
                ]
            },
            "grafana": {
                "image": "grafana/grafana:latest",
                "ports": ["3000:3000"],
                "environment": {
                    "GF_SECURITY_ADMIN_PASSWORD": "admin"
                },
                "volumes": [
                    "./grafana-dashboard.json:/var/lib/grafana/dashboards/dashboard.json"
                ]
            }
        }
        
        # Add exporters
        for exporter in configuration.exporters:
            if exporter["name"] == "node_exporter":
                services["node_exporter"] = {
                    "image": "prom/node-exporter:latest",
                    "ports": ["9100:9100"],
                    "volumes": ["/proc:/host/proc:ro", "/sys:/host/sys:ro", "/:/rootfs:ro"]
                }
        
        return {
            "version": "3.8",
            "services": services
        }
    
    async def _setup_monitoring_components(self, configuration: MonitoringConfiguration) -> Dict[str, Any]:
        """Setup monitoring components."""
        try:
            # Simulate monitoring setup
            setup_steps = [
                "Installing Prometheus",
                "Configuring exporters",
                "Setting up Grafana",
                "Configuring alerting rules",
                "Starting monitoring services"
            ]
            
            for step in setup_steps:
                self.logger.info(f"Setup step: {step}")
                await asyncio.sleep(0.1)  # Simulate setup time
            
            return {
                "success": True,
                "message": "Monitoring setup completed successfully",
                "components": ["prometheus", "grafana", "exporters", "alerting"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Monitoring setup failed"
            }
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.name == "setup_monitoring":
            analysis = await self.analyze_requirements(task.metadata.get("requirements", ""))
            configuration = await self.generate_monitoring_configuration(analysis)
            return configuration
        elif task.name == "execute_monitoring_setup":
            return await self.execute_monitoring_setup(task.metadata)
        elif task.name == "get_status":
            return await self._get_monitoring_status()
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    async def _get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            "configurations_count": len(self.configurations),
            "active_alerts": len([a for a in self.alerts.values() if a.status == "active"]),
            "dashboards_count": len(self.dashboards),
            "last_activity": max([c.created_at for c in self.configurations.values()]) if self.configurations else None
        }
