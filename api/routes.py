from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
from pathlib import Path
import uuid
import json

from . import schemas
from agent.terraform_agent import TerraformAgent
from agent.ansible_agent import AnsibleAgent

router = APIRouter()
logger = logging.getLogger(__name__)

# Store active agent instances
active_agents: Dict[str, Any] = {}

def get_agent(agent_id: str):
    """Retrieve an agent instance by ID."""
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return active_agents[agent_id]

@router.post("/agent/create", response_model=schemas.Response)
async def create_agent(request: schemas.BaseRequest):
    """Create a new agent instance."""
    try:
        logger.info(f"Creating new agent with request: {request}")
        agent_id = str(uuid.uuid4())
        work_dir = Path(f"./workspace/{agent_id}")
        
        # Create workspace directory if it doesn't exist
        work_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created workspace directory: {work_dir}")
        
        agent = None
        try:
            if request.agent_type == schemas.AgentType.TERRAFORM:
                logger.info("Initializing Terraform agent")
                agent = TerraformAgent(work_dir=str(work_dir))
            elif request.agent_type == schemas.AgentType.ANSIBLE:
                logger.info("Initializing Ansible agent")
                agent = AnsibleAgent(work_dir=str(work_dir))
            else:
                error_msg = f"Unsupported agent type: {request.agent_type}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Initialize the agent
            logger.info("Initializing agent...")
            agent.initialize()  # Synchronous call
            
            # Store the agent instance
            active_agents[agent_id] = agent
            logger.info(f"Agent created successfully with ID: {agent_id}")
            
            return {
                "success": True,
                "message": f"{request.agent_type.value.capitalize()} agent created successfully",
                "data": {"agent_id": agent_id}
            }
            
        except Exception as e:
            logger.exception(f"Error creating agent: {str(e)}")
            # Clean up workspace if agent creation failed
            if agent and hasattr(agent, 'cleanup'):
                await agent.cleanup()
            raise
            
    except Exception as e:
        logger.exception("Unexpected error in create_agent")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create agent: {str(e)}"
        )

@router.post("/agent/{agent_id}/execute", response_model=schemas.Response)
async def execute_operation(agent_id: str, request: schemas.BaseRequest):
    """Execute an operation using the specified agent."""
    try:
        agent = get_agent(agent_id)
        
        if request.agent_type == schemas.AgentType.TERRAFORM:
            if request.operation == "plan":
                result = await agent.plan(request.config)
            elif request.operation == "apply":
                result = await agent.apply(request.config.get("plan"))
            elif request.operation == "destroy":
                result = await agent.destroy()
            else:
                raise ValueError(f"Unsupported operation: {request.operation}")
        
        elif request.agent_type == schemas.AgentType.ANSIBLE:
            if request.operation == "run_playbook":
                result = await agent.run_playbook(
                    playbook=request.config.get("playbook"),
                    inventory=request.config.get("inventory"),
                    extra_vars=request.config.get("extra_vars")
                )
            else:
                raise ValueError(f"Unsupported operation: {request.operation}")
        
        else:
            raise ValueError(f"Unsupported agent type: {request.agent_type}")
        
        return {
            "success": result.get("success", False),
            "message": f"Operation '{request.operation}' completed",
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Operation failed: {request.operation}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/{agent_id}/state", response_model=schemas.Response)
async def get_agent_state(agent_id: str):
    """Get the current state of an agent."""
    try:
        agent = get_agent(agent_id)
        return {
            "success": True,
            "data": agent.get_state()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get agent state")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agent/{agent_id}", response_model=schemas.Response)
async def delete_agent(agent_id: str):
    """Remove an agent instance."""
    try:
        if agent_id in active_agents:
            # Clean up any resources if needed
            del active_agents[agent_id]
        return {"success": True, "message": "Agent removed successfully"}
    except Exception as e:
        logger.exception("Failed to remove agent")
        raise HTTPException(status_code=500, detail=str(e))
