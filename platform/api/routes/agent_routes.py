"""
Agent routes for the Multi-Agent Infrastructure Intelligence Platform API.

This module defines FastAPI routes for interacting with specialized agents.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
import json
import uuid
from datetime import datetime

from ..schemas.request_models import (
    InfrastructureRequest, TerraformRequest, AnsibleRequest, 
    KubernetesRequest, SecurityRequest, MonitoringRequest,
    TaskRequest, ConversationRequest, StatusRequest
)
from ..schemas.response_models import (
    AgentResponse, TaskResponse, SuccessResponse, ErrorResponse,
    StatusResponse, ConversationResponse, CapabilityResponse
)
from ...core.base_platform import PlatformConfig
from ...core.agent_framework import ConversationManager, MemoryManager, ToolRegistry
from ...agents.terraform_agent import TerraformAgent
from ...agents.ansible_agent import AnsibleAgent
from ...agents.kubernetes_agent import KubernetesAgent
from ...agents.security_agent import SecurityAgent
from ...agents.monitoring_agent import MonitoringAgent


# Create router
router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

# Global agent instances (in production, these would be managed by a proper service)
agents: Dict[str, Any] = {}
conversation_manager = ConversationManager()
memory_manager = MemoryManager()
tool_registry = ToolRegistry()


def get_agent(agent_type: str):
    """Get agent instance by type."""
    if agent_type not in agents:
        config = PlatformConfig(name=f"{agent_type}_agent", version="1.0.0")
        
        if agent_type == "terraform":
            agents[agent_type] = TerraformAgent(config)
        elif agent_type == "ansible":
            agents[agent_type] = AnsibleAgent(config)
        elif agent_type == "kubernetes":
            agents[agent_type] = KubernetesAgent(config)
        elif agent_type == "security":
            agents[agent_type] = SecurityAgent(config)
        elif agent_type == "monitoring":
            agents[agent_type] = MonitoringAgent(config)
        else:
            raise HTTPException(status_code=404, detail=f"Agent type {agent_type} not found")
        
        # Initialize agent
        asyncio.create_task(agents[agent_type].initialize())
        asyncio.create_task(agents[agent_type].start())
    
    return agents[agent_type]


@router.post("/terraform/request", response_model=AgentResponse)
async def terraform_request(request: TerraformRequest):
    """Process a Terraform infrastructure request."""
    try:
        agent = get_agent("terraform")
        response = await agent.process_request(request.requirements, request.context)
        
        return AgentResponse(
            agent_id=agent.config.name,
            agent_type="terraform",
            response_type=response.response_type,
            content=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            next_actions=response.next_actions,
            status="success",
            message="Terraform request processed successfully",
            request_id=request.request_id,
            metadata=response.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ansible/request", response_model=AgentResponse)
async def ansible_request(request: AnsibleRequest):
    """Process an Ansible configuration request."""
    try:
        agent = get_agent("ansible")
        response = await agent.process_request(request.requirements, request.context)
        
        return AgentResponse(
            agent_id=agent.config.name,
            agent_type="ansible",
            response_type=response.response_type,
            content=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            next_actions=response.next_actions,
            status="success",
            message="Ansible request processed successfully",
            request_id=request.request_id,
            metadata=response.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kubernetes/request", response_model=AgentResponse)
async def kubernetes_request(request: KubernetesRequest):
    """Process a Kubernetes orchestration request."""
    try:
        agent = get_agent("kubernetes")
        response = await agent.process_request(request.requirements, request.context)
        
        return AgentResponse(
            agent_id=agent.config.name,
            agent_type="kubernetes",
            response_type=response.response_type,
            content=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            next_actions=response.next_actions,
            status="success",
            message="Kubernetes request processed successfully",
            request_id=request.request_id,
            metadata=response.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/request", response_model=AgentResponse)
async def security_request(request: SecurityRequest):
    """Process a security and compliance request."""
    try:
        agent = get_agent("security")
        response = await agent.process_request(request.requirements, request.context)
        
        return AgentResponse(
            agent_id=agent.config.name,
            agent_type="security",
            response_type=response.response_type,
            content=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            next_actions=response.next_actions,
            status="success",
            message="Security request processed successfully",
            request_id=request.request_id,
            metadata=response.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/monitoring/request", response_model=AgentResponse)
async def monitoring_request(request: MonitoringRequest):
    """Process a monitoring and observability request."""
    try:
        agent = get_agent("monitoring")
        response = await agent.process_request(request.requirements, request.context)
        
        return AgentResponse(
            agent_id=agent.config.name,
            agent_type="monitoring",
            response_type=response.response_type,
            content=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            next_actions=response.next_actions,
            status="success",
            message="Monitoring request processed successfully",
            request_id=request.request_id,
            metadata=response.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation", response_model=ConversationResponse)
async def conversation(request: ConversationRequest):
    """Start or continue a conversation with an agent."""
    try:
        # Get or create session
        session_id = request.session_id
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get agent
        agent = get_agent(request.agent_type.value if request.agent_type else "terraform")
        
        # Process conversation
        response = await agent.process_request(request.message, {
            "session_id": session_id,
            "user_id": request.user_id,
            **request.context
        })
        
        return ConversationResponse(
            conversation_id=str(uuid.uuid4()),
            session_id=session_id,
            user_id=request.user_id,
            agent_type=request.agent_type.value if request.agent_type else "terraform",
            message=request.message,
            response=response.content,
            confidence=response.confidence,
            suggestions=response.suggestions,
            status="success",
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task", response_model=TaskResponse)
async def execute_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Execute a task with an agent."""
    try:
        agent = get_agent(request.agent_type.value)
        
        # Create task
        from ...core.base_platform import Task, Priority
        task = Task(
            id=request.task_id,
            name=request.task_name,
            description=request.task_description,
            priority=Priority(request.priority.value),
            metadata=request.parameters
        )
        
        # Execute task in background
        background_tasks.add_task(execute_task_background, agent, task)
        
        return TaskResponse(
            task_id=task.id,
            task_name=task.name,
            task_status="pending",
            progress=0.0,
            started_at=datetime.now(),
            status="success",
            message="Task queued for execution"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def execute_task_background(agent, task):
    """Execute task in background."""
    try:
        result = await agent.execute_task(task)
        # Store result (in production, this would be stored in a database)
        print(f"Task {task.id} completed with result: {result}")
    except Exception as e:
        print(f"Task {task.id} failed with error: {str(e)}")


@router.get("/{agent_type}/status", response_model=StatusResponse)
async def get_agent_status(agent_type: str):
    """Get status of a specific agent."""
    try:
        agent = get_agent(agent_type)
        status = agent.get_status()
        
        return StatusResponse(
            component=agent.config.name,
            status=status["status"],
            metrics=status,
            last_activity=datetime.now(),
            active_tasks=len(agent.tasks),
            total_tasks=len(agent.tasks),
            message="Agent status retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_type}/capabilities", response_model=CapabilityResponse)
async def get_agent_capabilities(agent_type: str):
    """Get capabilities of a specific agent."""
    try:
        agent = get_agent(agent_type)
        capabilities = agent.get_capabilities()
        
        return CapabilityResponse(
            agent_type=agent_type,
            capabilities=[{
                "name": cap.name,
                "description": cap.description,
                "version": cap.version,
                "parameters": cap.parameters,
                "dependencies": cap.dependencies
            } for cap in capabilities],
            version=agent.config.version,
            status=agent.status.value,
            last_updated=datetime.now(),
            message="Agent capabilities retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_type}/health", response_model=StatusResponse)
async def get_agent_health(agent_type: str):
    """Get health status of a specific agent."""
    try:
        agent = get_agent(agent_type)
        health = await agent.health_check()
        
        return StatusResponse(
            component=agent.config.name,
            status=health["status"],
            metrics=health,
            last_activity=datetime.now(),
            message="Agent health check completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/analyze", response_model=SuccessResponse)
async def analyze_requirements(agent_type: str, requirements: str):
    """Analyze requirements with a specific agent."""
    try:
        agent = get_agent(agent_type)
        analysis = await agent.analyze_requirements(requirements)
        
        return SuccessResponse(
            data=analysis,
            status="success",
            message="Requirements analyzed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/generate", response_model=SuccessResponse)
async def generate_plan(agent_type: str, analysis: Dict[str, Any]):
    """Generate a plan with a specific agent."""
    try:
        agent = get_agent(agent_type)
        
        if agent_type == "terraform":
            plan = await agent.generate_plan(analysis)
        elif agent_type == "ansible":
            plan = await agent.generate_playbook(analysis)
        elif agent_type == "kubernetes":
            plan = await agent.generate_deployment(analysis)
        elif agent_type == "security":
            plan = await agent.generate_security_assessment(analysis)
        elif agent_type == "monitoring":
            plan = await agent.generate_monitoring_configuration(analysis)
        else:
            raise HTTPException(status_code=400, detail=f"Plan generation not supported for {agent_type}")
        
        return SuccessResponse(
            data=plan,
            status="success",
            message="Plan generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/execute", response_model=SuccessResponse)
async def execute_plan(agent_type: str, plan: Dict[str, Any]):
    """Execute a plan with a specific agent."""
    try:
        agent = get_agent(agent_type)
        
        if agent_type == "terraform":
            result = await agent.execute_plan(plan)
        elif agent_type == "ansible":
            result = await agent.execute_playbook(plan)
        elif agent_type == "kubernetes":
            result = await agent.execute_deployment(plan)
        elif agent_type == "security":
            result = await agent.execute_security_assessment(plan)
        elif agent_type == "monitoring":
            result = await agent.execute_monitoring_setup(plan)
        else:
            raise HTTPException(status_code=400, detail=f"Plan execution not supported for {agent_type}")
        
        return SuccessResponse(
            data=result,
            status="success",
            message="Plan executed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=SuccessResponse)
async def list_agents():
    """List all available agents."""
    try:
        agent_list = []
        for agent_type in ["terraform", "ansible", "kubernetes", "security", "monitoring"]:
            try:
                agent = get_agent(agent_type)
                agent_list.append({
                    "type": agent_type,
                    "name": agent.config.name,
                    "version": agent.config.version,
                    "status": agent.status.value,
                    "capabilities": len(agent.capabilities)
                })
            except Exception:
                agent_list.append({
                    "type": agent_type,
                    "name": f"{agent_type}_agent",
                    "version": "1.0.0",
                    "status": "not_initialized",
                    "capabilities": 0
                })
        
        return SuccessResponse(
            data={"agents": agent_list},
            status="success",
            message="Agents listed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{agent_type}")
async def stop_agent(agent_type: str):
    """Stop a specific agent."""
    try:
        if agent_type in agents:
            agent = agents[agent_type]
            await agent.stop()
            del agents[agent_type]
            
            return SuccessResponse(
                data={"agent_type": agent_type},
                status="success",
                message="Agent stopped successfully"
            )
        else:
            raise HTTPException(status_code=404, detail=f"Agent {agent_type} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
