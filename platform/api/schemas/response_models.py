"""
Response models for the Multi-Agent Infrastructure Intelligence Platform API.

This module defines Pydantic models for API response serialization and validation.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    """Response status values."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseResponse(BaseModel):
    """Base response model."""
    status: Status = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Original request identifier")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ErrorResponse(BaseResponse):
    """Error response model."""
    status: Status = Field(default=Status.ERROR, description="Error status")
    error_code: str = Field(..., description="Error code")
    error_details: Dict[str, Any] = Field(default_factory=dict, description="Error details")
    suggestions: List[str] = Field(default_factory=list, description="Error resolution suggestions")


class SuccessResponse(BaseResponse):
    """Success response model."""
    status: Status = Field(default=Status.SUCCESS, description="Success status")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")


class AgentResponse(BaseResponse):
    """Agent-specific response model."""
    agent_id: str = Field(..., description="Agent identifier")
    agent_type: str = Field(..., description="Agent type")
    response_type: str = Field(..., description="Response type")
    content: Any = Field(..., description="Response content")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions")
    next_actions: List[str] = Field(default_factory=list, description="Next actions")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")


class TaskResponse(BaseResponse):
    """Task execution response model."""
    task_id: str = Field(..., description="Task identifier")
    task_name: str = Field(..., description="Task name")
    task_status: str = Field(..., description="Task status")
    progress: float = Field(ge=0.0, le=100.0, description="Task progress percentage")
    result: Optional[Any] = Field(None, description="Task result")
    error: Optional[str] = Field(None, description="Task error")
    started_at: datetime = Field(..., description="Task start time")
    completed_at: Optional[datetime] = Field(None, description="Task completion time")
    logs: List[str] = Field(default_factory=list, description="Task logs")


class HealthResponse(BaseResponse):
    """Health check response model."""
    component: str = Field(..., description="Component name")
    health_status: str = Field(..., description="Health status")
    version: str = Field(..., description="Component version")
    uptime: float = Field(..., description="Uptime in seconds")
    last_check: datetime = Field(..., description="Last health check time")
    details: Dict[str, Any] = Field(default_factory=dict, description="Health details")
    dependencies: List[Dict[str, Any]] = Field(default_factory=list, description="Dependency status")


class StatusResponse(BaseResponse):
    """Status response model."""
    component: str = Field(..., description="Component name")
    status: str = Field(..., description="Component status")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Component metrics")
    last_activity: Optional[datetime] = Field(None, description="Last activity time")
    active_tasks: int = Field(default=0, description="Number of active tasks")
    total_tasks: int = Field(default=0, description="Total number of tasks")


class ConfigurationResponse(BaseResponse):
    """Configuration response model."""
    config_id: str = Field(..., description="Configuration identifier")
    config_type: str = Field(..., description="Configuration type")
    config_name: str = Field(..., description="Configuration name")
    config_data: Dict[str, Any] = Field(..., description="Configuration data")
    agent_type: str = Field(..., description="Target agent type")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    version: str = Field(..., description="Configuration version")


class SearchResponse(BaseResponse):
    """Search response model."""
    query: str = Field(..., description="Search query")
    results: List[Dict[str, Any]] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total number of results")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


class ListResponse(BaseResponse):
    """List response model."""
    items: List[Dict[str, Any]] = Field(..., description="List items")
    total_count: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


class ValidationResponse(BaseResponse):
    """Validation response model."""
    is_valid: bool = Field(..., description="Validation result")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")


class ExportResponse(BaseResponse):
    """Export response model."""
    export_id: str = Field(..., description="Export identifier")
    export_type: str = Field(..., description="Export type")
    file_path: Optional[str] = Field(None, description="Exported file path")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    download_url: Optional[str] = Field(None, description="Download URL")
    expires_at: Optional[datetime] = Field(None, description="Download expiration time")


class ImportResponse(BaseResponse):
    """Import response model."""
    import_id: str = Field(..., description="Import identifier")
    import_type: str = Field(..., description="Import type")
    items_imported: int = Field(..., description="Number of items imported")
    items_failed: int = Field(..., description="Number of items failed")
    errors: List[str] = Field(default_factory=list, description="Import errors")
    warnings: List[str] = Field(default_factory=list, description="Import warnings")


class TemplateResponse(BaseResponse):
    """Template response model."""
    template_id: str = Field(..., description="Template identifier")
    template_type: str = Field(..., description="Template type")
    template_name: str = Field(..., description="Template name")
    template_content: Dict[str, Any] = Field(..., description="Template content")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Template parameters")
    agent_type: str = Field(..., description="Target agent type")
    created_at: datetime = Field(..., description="Creation time")


class WorkflowResponse(BaseResponse):
    """Workflow response model."""
    workflow_id: str = Field(..., description="Workflow identifier")
    workflow_name: str = Field(..., description="Workflow name")
    workflow_status: str = Field(..., description="Workflow status")
    current_step: int = Field(..., description="Current step number")
    total_steps: int = Field(..., description="Total number of steps")
    progress: float = Field(ge=0.0, le=100.0, description="Workflow progress percentage")
    steps: List[Dict[str, Any]] = Field(..., description="Workflow steps")
    started_at: datetime = Field(..., description="Workflow start time")
    completed_at: Optional[datetime] = Field(None, description="Workflow completion time")


class NotificationResponse(BaseResponse):
    """Notification response model."""
    notification_id: str = Field(..., description="Notification identifier")
    notification_type: str = Field(..., description="Notification type")
    recipients: List[str] = Field(..., description="Recipients")
    message: str = Field(..., description="Notification message")
    status: str = Field(..., description="Notification status")
    sent_at: Optional[datetime] = Field(None, description="Sent time")
    delivered_at: Optional[datetime] = Field(None, description="Delivery time")


class AuditResponse(BaseResponse):
    """Audit response model."""
    audit_id: str = Field(..., description="Audit identifier")
    audit_type: str = Field(..., description="Audit type")
    target: str = Field(..., description="Audit target")
    findings: List[Dict[str, Any]] = Field(..., description="Audit findings")
    compliance_score: float = Field(..., description="Compliance score")
    recommendations: List[str] = Field(..., description="Recommendations")
    generated_at: datetime = Field(..., description="Audit generation time")


class BackupResponse(BaseResponse):
    """Backup response model."""
    backup_id: str = Field(..., description="Backup identifier")
    backup_type: str = Field(..., description="Backup type")
    target: str = Field(..., description="Backup target")
    backup_size: int = Field(..., description="Backup size in bytes")
    backup_path: str = Field(..., description="Backup file path")
    created_at: datetime = Field(..., description="Backup creation time")
    expires_at: Optional[datetime] = Field(None, description="Backup expiration time")


class RestoreResponse(BaseResponse):
    """Restore response model."""
    restore_id: str = Field(..., description="Restore identifier")
    restore_type: str = Field(..., description="Restore type")
    backup_id: str = Field(..., description="Source backup identifier")
    target: str = Field(..., description="Restore target")
    items_restored: int = Field(..., description="Number of items restored")
    items_failed: int = Field(..., description="Number of items failed")
    restored_at: datetime = Field(..., description="Restore completion time")


class MetricsResponse(BaseResponse):
    """Metrics response model."""
    metrics: Dict[str, Any] = Field(..., description="Metrics data")
    timestamp: datetime = Field(..., description="Metrics timestamp")
    time_range: str = Field(..., description="Time range for metrics")
    aggregation: str = Field(..., description="Metrics aggregation type")


class LogResponse(BaseResponse):
    """Log response model."""
    logs: List[Dict[str, Any]] = Field(..., description="Log entries")
    total_count: int = Field(..., description="Total number of log entries")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")


class WebSocketResponse(BaseModel):
    """WebSocket response model."""
    message_type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")


class BatchResponse(BaseResponse):
    """Batch operation response model."""
    batch_id: str = Field(..., description="Batch identifier")
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    results: List[Dict[str, Any]] = Field(..., description="Individual request results")
    started_at: datetime = Field(..., description="Batch start time")
    completed_at: Optional[datetime] = Field(None, description="Batch completion time")


class ConversationResponse(BaseResponse):
    """Conversation response model."""
    conversation_id: str = Field(..., description="Conversation identifier")
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    agent_type: str = Field(..., description="Agent type")
    message: str = Field(..., description="User message")
    response: str = Field(..., description="Agent response")
    confidence: float = Field(..., description="Response confidence")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions")
    timestamp: datetime = Field(..., description="Conversation timestamp")


class CapabilityResponse(BaseResponse):
    """Capability response model."""
    agent_type: str = Field(..., description="Agent type")
    capabilities: List[Dict[str, Any]] = Field(..., description="Agent capabilities")
    version: str = Field(..., description="Agent version")
    status: str = Field(..., description="Agent status")
    last_updated: datetime = Field(..., description="Last update time")
