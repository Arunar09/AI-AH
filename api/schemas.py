from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union
from enum import Enum

class AgentType(str, Enum):
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"

class BaseRequest(BaseModel):
    """Base request model for all agent operations."""
    agent_type: AgentType = Field(..., description="Type of agent to use")
    operation: str = Field(..., description="Operation to perform")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Configuration for the operation")

class TerraformPlanRequest(BaseRequest):
    """Request model for Terraform plan operation."""
    agent_type: AgentType = AgentType.TERRAFORM
    operation: str = "plan"
    config: Dict[str, Any] = Field(default_factory=dict, description="Terraform variables")

class TerraformApplyRequest(BaseRequest):
    """Request model for Terraform apply operation."""
    agent_type: AgentType = AgentType.TERRAFORM
    operation: str = "apply"
    plan: Optional[Dict[str, Any]] = Field(default=None, description="Plan to apply (optional)")

class AnsiblePlaybookRequest(BaseRequest):
    """Request model for Ansible playbook operations."""
    agent_type: AgentType = AgentType.ANSIBLE
    operation: str = "run_playbook"
    playbook: Dict[str, Any] = Field(..., description="Ansible playbook content")
    inventory: Optional[Dict[str, Any]] = Field(default=None, description="Inventory configuration")
    extra_vars: Optional[Dict[str, Any]] = Field(default=None, description="Extra variables for the playbook")

class Response(BaseModel):
    """Base response model."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: Optional[str] = Field(None, description="Status message")
    data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Response data")
    error: Optional[str] = Field(None, description="Error message if operation failed")
