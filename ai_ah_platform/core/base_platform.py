"""
Base platform classes for the Multi-Agent Infrastructure Intelligence Platform.

This module provides the foundational classes and interfaces that all platform
components inherit from, ensuring consistency and interoperability.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging
import asyncio
from enum import Enum


class ComponentStatus(Enum):
    """Status enumeration for platform components."""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"


class Priority(Enum):
    """Priority levels for tasks and operations."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


@dataclass
class PlatformConfig:
    """Base configuration for platform components."""
    name: str
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 300
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    """Represents a task in the platform."""
    id: str
    name: str
    description: str
    priority: Priority = Priority.NORMAL
    status: ComponentStatus = ComponentStatus.INITIALIZING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class AgentCapability:
    """Represents a capability of an agent."""
    name: str
    description: str
    version: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)


class BasePlatformComponent(ABC):
    """
    Base class for all platform components.
    
    Provides common functionality for initialization, lifecycle management,
    logging, and error handling.
    """
    
    def __init__(self, config: PlatformConfig):
        self.config = config
        self.status = ComponentStatus.INITIALIZING
        self.logger = self._setup_logger()
        self.tasks: Dict[str, Task] = {}
        self.capabilities: List[AgentCapability] = []
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the component."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.config.name}")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the component."""
        pass
    
    @abstractmethod
    async def start(self) -> bool:
        """Start the component."""
        pass
    
    @abstractmethod
    async def stop(self) -> bool:
        """Stop the component."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the component."""
        pass
    
    async def execute_task(self, task: Task) -> Task:
        """Execute a task with proper error handling and logging."""
        try:
            self.logger.info(f"Starting task: {task.name} (ID: {task.id})")
            task.status = ComponentStatus.RUNNING
            task.updated_at = datetime.now()
            
            result = await self._execute_task_impl(task)
            
            task.result = result
            task.status = ComponentStatus.READY
            task.updated_at = datetime.now()
            
            self.logger.info(f"Task completed successfully: {task.name}")
            return task
            
        except Exception as e:
            self.logger.error(f"Task failed: {task.name} - {str(e)}")
            task.error = str(e)
            task.status = ComponentStatus.ERROR
            task.updated_at = datetime.now()
            return task
    
    @abstractmethod
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the component."""
        return {
            "name": self.config.name,
            "status": self.status.value,
            "version": self.config.version,
            "environment": self.config.environment,
            "tasks_count": len(self.tasks),
            "capabilities_count": len(self.capabilities),
            "last_updated": datetime.now().isoformat()
        }
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to the component."""
        self.capabilities.append(capability)
        self.logger.info(f"Added capability: {capability.name}")
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Get all capabilities of the component."""
        return self.capabilities.copy()


class BaseAgent(BasePlatformComponent):
    """
    Base class for all AI agents in the platform.
    
    Extends BasePlatformComponent with agent-specific functionality
    including conversation handling, tool integration, and learning.
    """
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.conversation_history: List[Dict[str, Any]] = []
        self.tools: Dict[str, Any] = {}
        self.knowledge_base: Dict[str, Any] = {}
        
    @abstractmethod
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user request and return a response."""
        pass
    
    @abstractmethod
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze infrastructure requirements."""
        pass
    
    @abstractmethod
    async def generate_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an execution plan based on analysis."""
        pass
    
    @abstractmethod
    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the generated plan."""
        pass
    
    async def learn_from_feedback(self, feedback: Dict[str, Any]):
        """Learn from user feedback to improve future responses."""
        self.logger.info(f"Learning from feedback: {feedback}")
        # Implementation specific to each agent
    
    def add_tool(self, name: str, tool: Any):
        """Add a tool to the agent's toolkit."""
        self.tools[name] = tool
        self.logger.info(f"Added tool: {name}")
    
    def get_tools(self) -> Dict[str, Any]:
        """Get all tools available to the agent."""
        return self.tools.copy()
    
    def add_to_knowledge_base(self, key: str, value: Any):
        """Add information to the agent's knowledge base."""
        self.knowledge_base[key] = value
        self.logger.info(f"Added to knowledge base: {key}")
    
    def get_from_knowledge_base(self, key: str) -> Any:
        """Retrieve information from the agent's knowledge base."""
        return self.knowledge_base.get(key)


class BaseTool(BasePlatformComponent):
    """
    Base class for all tools in the platform.
    
    Tools are specialized components that provide specific functionality
    to agents, such as Terraform operations, Ansible playbooks, etc.
    """
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.operations: List[str] = []
        
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for the tool."""
        pass
    
    @abstractmethod
    async def execute_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific operation with the tool."""
        pass
    
    def add_operation(self, operation: str):
        """Add a supported operation to the tool."""
        self.operations.append(operation)
        self.logger.info(f"Added operation: {operation}")
    
    def get_operations(self) -> List[str]:
        """Get all supported operations of the tool."""
        return self.operations.copy()


class PlatformOrchestrator:
    """
    Orchestrates the entire platform, managing agents, tools, and workflows.
    
    This is the main coordinator that ensures all components work together
    seamlessly and provides the unified interface for the platform.
    """
    
    def __init__(self, config: PlatformConfig):
        self.config = config
        self.agents: Dict[str, BaseAgent] = {}
        self.tools: Dict[str, BaseTool] = {}
        self.workflows: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"PlatformOrchestrator.{config.name}")
        
    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent with the platform."""
        try:
            await agent.initialize()
            self.agents[agent.config.name] = agent
            self.logger.info(f"Registered agent: {agent.config.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent.config.name}: {str(e)}")
            return False
    
    async def register_tool(self, tool: BaseTool) -> bool:
        """Register a tool with the platform."""
        try:
            await tool.initialize()
            self.tools[tool.config.name] = tool
            self.logger.info(f"Registered tool: {tool.config.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register tool {tool.config.name}: {str(e)}")
            return False
    
    async def start_platform(self) -> bool:
        """Start all registered components."""
        try:
            # Start all tools first
            for tool in self.tools.values():
                await tool.start()
            
            # Start all agents
            for agent in self.agents.values():
                await agent.start()
            
            self.logger.info("Platform started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start platform: {str(e)}")
            return False
    
    async def stop_platform(self) -> bool:
        """Stop all registered components."""
        try:
            # Stop all agents first
            for agent in self.agents.values():
                await agent.stop()
            
            # Stop all tools
            for tool in self.tools.values():
                await tool.stop()
            
            self.logger.info("Platform stopped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop platform: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components."""
        health_status = {
            "platform": "healthy",
            "agents": {},
            "tools": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Check agents
        for name, agent in self.agents.items():
            try:
                health_status["agents"][name] = await agent.health_check()
            except Exception as e:
                health_status["agents"][name] = {"status": "error", "error": str(e)}
        
        # Check tools
        for name, tool in self.tools.items():
            try:
                health_status["tools"][name] = await tool.health_check()
            except Exception as e:
                health_status["tools"][name] = {"status": "error", "error": str(e)}
        
        return health_status
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get overall platform status."""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "environment": self.config.environment,
            "agents_count": len(self.agents),
            "tools_count": len(self.tools),
            "workflows_count": len(self.workflows),
            "status": "running" if self.agents and self.tools else "stopped"
        }
