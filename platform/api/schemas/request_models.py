"""
Request models for the Multi-Agent Infrastructure Intelligence Platform API.

This module defines Pydantic models for API request validation and serialization.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Supported agent types."""
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"
    KUBERNETES = "kubernetes"
    SECURITY = "security"
    MONITORING = "monitoring"


class RequestType(str, Enum):
    """Types of requests."""
    CREATE_INFRASTRUCTURE = "create_infrastructure"
    MODIFY_INFRASTRUCTURE = "modify_infrastructure"
    DELETE_INFRASTRUCTURE = "delete_infrastructure"
    MONITOR_INFRASTRUCTURE = "monitor_infrastructure"
    SECURITY_HARDEN = "security_harden"
    COMPLIANCE_CHECK = "compliance_check"
    VULNERABILITY_SCAN = "vulnerability_scan"
    RISK_ASSESS = "risk_assess"
    SETUP_MONITORING = "setup_monitoring"
    CREATE_DASHBOARD = "create_dashboard"
    CONFIGURE_ALERTS = "configure_alerts"
    ANALYZE_PERFORMANCE = "analyze_performance"


class Priority(str, Enum):
    """Request priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class BaseRequest(BaseModel):
    """Base request model."""
    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Request timestamp")
    priority: Priority = Field(default=Priority.NORMAL, description="Request priority")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class InfrastructureRequest(BaseRequest):
    """Request for infrastructure operations."""
    agent_type: AgentType = Field(..., description="Target agent type")
    request_type: RequestType = Field(..., description="Type of infrastructure request")
    requirements: str = Field(..., description="Natural language requirements")
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Request parameters")


class TerraformRequest(InfrastructureRequest):
    """Terraform-specific request."""
    agent_type: AgentType = Field(default=AgentType.TERRAFORM, description="Terraform agent")
    cloud_provider: Optional[str] = Field(None, description="Target cloud provider")
    region: Optional[str] = Field(None, description="Target region")
    environment: Optional[str] = Field(None, description="Target environment")


class AnsibleRequest(InfrastructureRequest):
    """Ansible-specific request."""
    agent_type: AgentType = Field(default=AgentType.ANSIBLE, description="Ansible agent")
    target_hosts: List[str] = Field(default_factory=list, description="Target hosts")
    playbook_type: Optional[str] = Field(None, description="Type of playbook")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Ansible variables")


class KubernetesRequest(InfrastructureRequest):
    """Kubernetes-specific request."""
    agent_type: AgentType = Field(default=AgentType.KUBERNETES, description="Kubernetes agent")
    namespace: Optional[str] = Field(None, description="Target namespace")
    cluster_context: Optional[str] = Field(None, description="Kubernetes cluster context")
    deployment_type: Optional[str] = Field(None, description="Type of deployment")


class SecurityRequest(InfrastructureRequest):
    """Security-specific request."""
    agent_type: AgentType = Field(default=AgentType.SECURITY, description="Security agent")
    compliance_framework: Optional[str] = Field(None, description="Compliance framework")
    security_level: Optional[str] = Field(None, description="Security level")
    target_components: List[str] = Field(default_factory=list, description="Target components")


class MonitoringRequest(InfrastructureRequest):
    """Monitoring-specific request."""
    agent_type: AgentType = Field(default=AgentType.MONITORING, description="Monitoring agent")
    monitoring_type: Optional[str] = Field(None, description="Type of monitoring")
    target_services: List[str] = Field(default_factory=list, description="Target services")
    metrics: List[str] = Field(default_factory=list, description="Metrics to monitor")


class TaskRequest(BaseModel):
    """Request for task execution."""
    task_id: str = Field(..., description="Task identifier")
    task_name: str = Field(..., description="Task name")
    task_description: str = Field(..., description="Task description")
    agent_type: AgentType = Field(..., description="Target agent type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    priority: Priority = Field(default=Priority.NORMAL, description="Task priority")
    timeout: Optional[int] = Field(None, description="Task timeout in seconds")


class ConversationRequest(BaseModel):
    """Request for conversation with agents."""
    message: str = Field(..., description="User message")
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_type: Optional[AgentType] = Field(None, description="Target agent type")
    context: Dict[str, Any] = Field(default_factory=dict, description="Conversation context")


class HealthCheckRequest(BaseModel):
    """Request for health check."""
    component: Optional[str] = Field(None, description="Component to check")
    include_details: bool = Field(default=False, description="Include detailed information")


class ConfigurationRequest(BaseModel):
    """Request for configuration management."""
    config_type: str = Field(..., description="Configuration type")
    config_name: str = Field(..., description="Configuration name")
    config_data: Dict[str, Any] = Field(..., description="Configuration data")
    agent_type: AgentType = Field(..., description="Target agent type")


class StatusRequest(BaseModel):
    """Request for status information."""
    component: Optional[str] = Field(None, description="Component to get status for")
    include_metrics: bool = Field(default=False, description="Include metrics")
    include_history: bool = Field(default=False, description="Include history")


class WebSocketMessage(BaseModel):
    """WebSocket message model."""
    message_type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")


class BatchRequest(BaseModel):
    """Request for batch operations."""
    requests: List[InfrastructureRequest] = Field(..., description="List of requests")
    parallel: bool = Field(default=False, description="Execute requests in parallel")
    stop_on_error: bool = Field(default=True, description="Stop on first error")


class SearchRequest(BaseModel):
    """Request for searching resources."""
    query: str = Field(..., description="Search query")
    resource_type: Optional[str] = Field(None, description="Resource type to search")
    agent_type: Optional[AgentType] = Field(None, description="Agent type to search")
    limit: int = Field(default=10, description="Maximum number of results")
    offset: int = Field(default=0, description="Offset for pagination")


class FilterRequest(BaseModel):
    """Request for filtering resources."""
    filters: Dict[str, Any] = Field(..., description="Filter criteria")
    resource_type: Optional[str] = Field(None, description="Resource type to filter")
    agent_type: Optional[AgentType] = Field(None, description="Agent type to filter")
    limit: int = Field(default=10, description="Maximum number of results")
    offset: int = Field(default=0, description="Offset for pagination")


class ExportRequest(BaseModel):
    """Request for exporting data."""
    export_type: str = Field(..., description="Export type (json, yaml, csv)")
    resource_type: str = Field(..., description="Resource type to export")
    agent_type: AgentType = Field(..., description="Agent type")
    filters: Optional[Dict[str, Any]] = Field(None, description="Export filters")
    include_metadata: bool = Field(default=True, description="Include metadata")


class ImportRequest(BaseModel):
    """Request for importing data."""
    import_type: str = Field(..., description="Import type (json, yaml, csv)")
    data: Union[str, Dict[str, Any]] = Field(..., description="Data to import")
    agent_type: AgentType = Field(..., description="Target agent type")
    validate_only: bool = Field(default=False, description="Only validate, don't import")


class ValidationRequest(BaseModel):
    """Request for validation."""
    resource_type: str = Field(..., description="Resource type to validate")
    data: Dict[str, Any] = Field(..., description="Data to validate")
    agent_type: AgentType = Field(..., description="Agent type")
    strict: bool = Field(default=True, description="Strict validation")


class TemplateRequest(BaseModel):
    """Request for template operations."""
    template_type: str = Field(..., description="Template type")
    template_name: str = Field(..., description="Template name")
    agent_type: AgentType = Field(..., description="Agent type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Template parameters")


class WorkflowRequest(BaseModel):
    """Request for workflow operations."""
    workflow_name: str = Field(..., description="Workflow name")
    workflow_definition: Dict[str, Any] = Field(..., description="Workflow definition")
    agent_types: List[AgentType] = Field(..., description="Required agent types")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Workflow parameters")
    parallel: bool = Field(default=False, description="Execute steps in parallel")


class NotificationRequest(BaseModel):
    """Request for notifications."""
    notification_type: str = Field(..., description="Notification type")
    recipients: List[str] = Field(..., description="Recipient list")
    message: str = Field(..., description="Notification message")
    priority: Priority = Field(default=Priority.NORMAL, description="Notification priority")
    channels: List[str] = Field(default_factory=list, description="Notification channels")


class AuditRequest(BaseModel):
    """Request for audit operations."""
    audit_type: str = Field(..., description="Audit type")
    target: str = Field(..., description="Audit target")
    agent_type: AgentType = Field(..., description="Agent type")
    include_recommendations: bool = Field(default=True, description="Include recommendations")
    compliance_framework: Optional[str] = Field(None, description="Compliance framework")


class BackupRequest(BaseModel):
    """Request for backup operations."""
    backup_type: str = Field(..., description="Backup type")
    target: str = Field(..., description="Backup target")
    agent_type: AgentType = Field(..., description="Agent type")
    include_configurations: bool = Field(default=True, description="Include configurations")
    include_data: bool = Field(default=False, description="Include data")


class RestoreRequest(BaseModel):
    """Request for restore operations."""
    restore_type: str = Field(..., description="Restore type")
    backup_id: str = Field(..., description="Backup identifier")
    agent_type: AgentType = Field(..., description="Agent type")
    target: Optional[str] = Field(None, description="Restore target")
    validate_only: bool = Field(default=False, description="Only validate, don't restore")
