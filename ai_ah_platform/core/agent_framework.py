"""
Agent Framework for the Multi-Agent Infrastructure Intelligence Platform.

This module provides the core agent framework with conversation handling,
memory management, and tool integration capabilities.
"""

from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import asyncio
import uuid
from enum import Enum

from .base_platform import BaseAgent, Task, Priority, ComponentStatus, AgentCapability


class ConversationType(Enum):
    """Types of conversations."""
    INFRASTRUCTURE_REQUEST = "infrastructure_request"
    TROUBLESHOOTING = "troubleshooting"
    CONFIGURATION = "configuration"
    MONITORING = "monitoring"
    SECURITY = "security"
    GENERAL = "general"


class MemoryType(Enum):
    """Types of memory storage."""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


@dataclass
class ConversationContext:
    """Context for a conversation."""
    session_id: str
    user_id: str
    conversation_type: ConversationType
    start_time: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Memory:
    """Represents a memory item."""
    id: str
    type: MemoryType
    content: Any
    importance: float  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    """Response from an agent."""
    agent_id: str
    response_type: str
    content: Any
    confidence: float  # 0.0 to 1.0
    suggestions: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class ConversationManager:
    """Manages conversations and context."""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.conversations: Dict[str, ConversationContext] = {}
        self.active_sessions: Dict[str, str] = {}  # user_id -> session_id
    
    def start_conversation(self, user_id: str, conversation_type: ConversationType, 
                          metadata: Dict[str, Any] = None) -> str:
        """Start a new conversation."""
        session_id = str(uuid.uuid4())
        context = ConversationContext(
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
            metadata=metadata or {}
        )
        
        self.conversations[session_id] = context
        self.active_sessions[user_id] = session_id
        
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, 
                   metadata: Dict[str, Any] = None):
        """Add a message to the conversation history."""
        if session_id not in self.conversations:
            raise ValueError(f"Session {session_id} not found")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        context = self.conversations[session_id]
        context.history.append(message)
        context.last_activity = datetime.now()
        
        # Trim history if too long
        if len(context.history) > self.max_history:
            context.history = context.history[-self.max_history:]
    
    def get_conversation_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get conversation context by session ID."""
        return self.conversations.get(session_id)
    
    def get_active_session(self, user_id: str) -> Optional[str]:
        """Get active session for a user."""
        return self.active_sessions.get(user_id)
    
    def end_conversation(self, session_id: str):
        """End a conversation."""
        if session_id in self.conversations:
            context = self.conversations[session_id]
            if context.user_id in self.active_sessions:
                del self.active_sessions[context.user_id]
            del self.conversations[session_id]


class MemoryManager:
    """Manages agent memory and knowledge."""
    
    def __init__(self, max_memories: int = 1000):
        self.max_memories = max_memories
        self.memories: Dict[str, Memory] = {}
        self.memory_index: Dict[str, List[str]] = {}  # tag -> memory_ids
    
    def store_memory(self, content: Any, memory_type: MemoryType, 
                    importance: float = 0.5, tags: List[str] = None,
                    metadata: Dict[str, Any] = None) -> str:
        """Store a memory item."""
        memory_id = str(uuid.uuid4())
        memory = Memory(
            id=memory_id,
            type=memory_type,
            content=content,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.memories[memory_id] = memory
        
        # Update index
        for tag in memory.tags:
            if tag not in self.memory_index:
                self.memory_index[tag] = []
            self.memory_index[tag].append(memory_id)
        
        # Trim memories if too many
        if len(self.memories) > self.max_memories:
            self._trim_memories()
        
        return memory_id
    
    def retrieve_memories(self, tags: List[str] = None, memory_type: MemoryType = None,
                         limit: int = 10) -> List[Memory]:
        """Retrieve memories by tags or type."""
        candidates = []
        
        if tags:
            for tag in tags:
                if tag in self.memory_index:
                    for memory_id in self.memory_index[tag]:
                        if memory_id in self.memories:
                            memory = self.memories[memory_id]
                            memory.last_accessed = datetime.now()
                            memory.access_count += 1
                            candidates.append(memory)
        else:
            candidates = list(self.memories.values())
        
        # Filter by type if specified
        if memory_type:
            candidates = [m for m in candidates if m.type == memory_type]
        
        # Sort by importance and recency
        candidates.sort(key=lambda m: (m.importance, m.last_accessed), reverse=True)
        
        return candidates[:limit]
    
    def _trim_memories(self):
        """Trim old, less important memories."""
        memories = list(self.memories.values())
        memories.sort(key=lambda m: (m.importance, m.last_accessed))
        
        # Remove bottom 20%
        to_remove = memories[:len(memories) // 5]
        for memory in to_remove:
            del self.memories[memory.id]
            # Remove from index
            for tag in memory.tags:
                if tag in self.memory_index:
                    self.memory_index[tag] = [mid for mid in self.memory_index[tag] 
                                            if mid != memory.id]


class ToolRegistry:
    """Registry for managing tools available to agents."""
    
    def __init__(self):
        self.tools: Dict[str, Any] = {}
        self.tool_metadata: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(self, name: str, tool: Any, metadata: Dict[str, Any] = None):
        """Register a tool with the registry."""
        self.tools[name] = tool
        self.tool_metadata[name] = metadata or {}
    
    def get_tool(self, name: str) -> Optional[Any]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tools."""
        return list(self.tools.keys())
    
    def get_tool_metadata(self, name: str) -> Dict[str, Any]:
        """Get metadata for a tool."""
        return self.tool_metadata.get(name, {})


class IntelligentAgent(BaseAgent):
    """
    Enhanced base agent with conversation management, memory, and tool integration.
    
    This class extends BaseAgent with advanced capabilities for handling
    conversations, managing memory, and integrating with tools.
    """
    
    def __init__(self, config, conversation_manager: ConversationManager = None,
                 memory_manager: MemoryManager = None, tool_registry: ToolRegistry = None):
        super().__init__(config)
        
        self.conversation_manager = conversation_manager or ConversationManager()
        self.memory_manager = memory_manager or MemoryManager()
        self.tool_registry = tool_registry or ToolRegistry()
        
        self.response_handlers: Dict[str, Callable] = {}
        self.context_processors: List[Callable] = []
        
    async def initialize(self) -> bool:
        """Initialize the intelligent agent."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info(f"Initializing {self.config.name}")
            
            # Initialize base capabilities
            await self._initialize_capabilities()
            
            # Initialize response handlers
            await self._initialize_response_handlers()
            
            # Initialize context processors
            await self._initialize_context_processors()
            
            self.status = ComponentStatus.READY
            self.logger.info(f"{self.config.name} initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.config.name}: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the intelligent agent."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info(f"{self.config.name} started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start {self.config.name}: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the intelligent agent."""
        try:
            self.status = ComponentStatus.STOPPED
            self.logger.info(f"{self.config.name} stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop {self.config.name}: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the agent."""
        return {
            "status": self.status.value,
            "conversations": len(self.conversation_manager.conversations),
            "memories": len(self.memory_manager.memories),
            "tools": len(self.tool_registry.tools),
            "capabilities": len(self.capabilities),
            "last_check": datetime.now().isoformat()
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a user request and return a response."""
        try:
            # Get or create conversation context
            session_id = context.get('session_id') if context else None
            if not session_id:
                user_id = context.get('user_id', 'anonymous') if context else 'anonymous'
                session_id = self.conversation_manager.start_conversation(
                    user_id, ConversationType.INFRASTRUCTURE_REQUEST, context
                )
            
            # Add user message to conversation
            self.conversation_manager.add_message(session_id, "user", request, context)
            
            # Process context
            processed_context = await self._process_context(session_id, context or {})
            
            # Generate response
            response = await self._generate_response(request, processed_context)
            
            # Add agent response to conversation
            self.conversation_manager.add_message(
                session_id, "assistant", response.content, response.metadata
            )
            
            # Store important information in memory
            await self._store_conversation_memory(session_id, request, response)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze infrastructure requirements."""
        # This will be implemented by specific agents
        return {"status": "not_implemented", "message": "Override in specific agent"}
    
    async def generate_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an execution plan based on analysis."""
        # This will be implemented by specific agents
        return {"status": "not_implemented", "message": "Override in specific agent"}
    
    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the generated plan."""
        # This will be implemented by specific agents
        return {"status": "not_implemented", "message": "Override in specific agent"}
    
    async def _initialize_capabilities(self):
        """Initialize agent capabilities."""
        # Override in specific agents
        pass
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers."""
        # Override in specific agents
        pass
    
    async def _initialize_context_processors(self):
        """Initialize context processors."""
        # Override in specific agents
        pass
    
    async def _process_context(self, session_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process conversation context."""
        processed_context = context.copy()
        
        # Get conversation history
        conv_context = self.conversation_manager.get_conversation_context(session_id)
        if conv_context:
            processed_context["conversation_history"] = conv_context.history
            processed_context["conversation_type"] = conv_context.conversation_type.value
        
        # Retrieve relevant memories
        relevant_memories = self.memory_manager.retrieve_memories(limit=5)
        processed_context["relevant_memories"] = [
            {"content": m.content, "importance": m.importance, "tags": m.tags}
            for m in relevant_memories
        ]
        
        # Apply context processors
        for processor in self.context_processors:
            processed_context = await processor(processed_context)
        
        return processed_context
    
    async def _generate_response(self, request: str, context: Dict[str, Any]) -> AgentResponse:
        """Generate response based on request and context."""
        # This will be implemented by specific agents
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'm ready to help with infrastructure tasks.",
            confidence=0.8
        )
    
    async def _store_conversation_memory(self, session_id: str, request: str, response: AgentResponse):
        """Store important conversation information in memory."""
        # Store the request-response pair if it's important
        if response.confidence > 0.7:
            memory_content = {
                "request": request,
                "response": response.content,
                "session_id": session_id
            }
            
            self.memory_manager.store_memory(
                content=memory_content,
                memory_type=MemoryType.EPISODIC,
                importance=response.confidence,
                tags=["conversation", "infrastructure"],
                metadata=response.metadata
            )
    
    def add_response_handler(self, response_type: str, handler: Callable):
        """Add a response handler for specific response types."""
        self.response_handlers[response_type] = handler
    
    def add_context_processor(self, processor: Callable):
        """Add a context processor."""
        self.context_processors.append(processor)
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        # This will be implemented by specific agents
        return {"status": "completed", "task_id": task.id}
