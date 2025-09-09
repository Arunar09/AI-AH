"""
Tests for the core platform framework.

This module contains comprehensive tests for the base platform classes,
agent framework, NLP, and memory management components.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

from platform.core.base_platform import BasePlatform, PlatformConfig, Task, Priority, PlatformStatus
from platform.core.agent_framework import BaseAgent, ConversationManager, MemoryManager, ToolRegistry
from platform.core.nlp.natural_language_processor import NaturalLanguageProcessor
from platform.core.memory.memory_manager import MemoryManager as CoreMemoryManager


class TestPlatformConfig:
    """Test PlatformConfig class."""
    
    def test_platform_config_creation(self):
        """Test platform configuration creation."""
        config = PlatformConfig(
            name="test_platform",
            version="1.0.0",
            description="Test platform"
        )
        
        assert config.name == "test_platform"
        assert config.version == "1.0.0"
        assert config.description == "Test platform"
        assert config.created_at is not None
        assert config.updated_at is not None
    
    def test_platform_config_defaults(self):
        """Test platform configuration defaults."""
        config = PlatformConfig(name="test")
        
        assert config.name == "test"
        assert config.version == "1.0.0"
        assert config.description == ""
        assert config.environment == "development"
        assert config.debug is False


class TestTask:
    """Test Task class."""
    
    def test_task_creation(self):
        """Test task creation."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="Test task description",
            priority=Priority.HIGH
        )
        
        assert task.id == "test_task"
        assert task.name == "Test Task"
        assert task.description == "Test task description"
        assert task.priority == Priority.HIGH
        assert task.status == "pending"
        assert task.created_at is not None
    
    def test_task_priority_enum(self):
        """Test task priority enum values."""
        assert Priority.LOW.value == "low"
        assert Priority.NORMAL.value == "normal"
        assert Priority.HIGH.value == "high"
        assert Priority.CRITICAL.value == "critical"
        assert Priority.EMERGENCY.value == "emergency"


class TestBasePlatform:
    """Test BasePlatform class."""
    
    @pytest.fixture
    def platform_config(self):
        """Create a test platform configuration."""
        return PlatformConfig(name="test_platform", version="1.0.0")
    
    @pytest.fixture
    def base_platform(self, platform_config):
        """Create a test base platform instance."""
        return BasePlatform(platform_config)
    
    def test_base_platform_initialization(self, base_platform, platform_config):
        """Test base platform initialization."""
        assert base_platform.config == platform_config
        assert base_platform.status == PlatformStatus.STOPPED
        assert base_platform.tasks == []
        assert base_platform.logger is not None
    
    @pytest.mark.asyncio
    async def test_platform_lifecycle(self, base_platform):
        """Test platform lifecycle methods."""
        # Test initialization
        await base_platform.initialize()
        assert base_platform.status == PlatformStatus.INITIALIZED
        
        # Test starting
        await base_platform.start()
        assert base_platform.status == PlatformStatus.RUNNING
        
        # Test stopping
        await base_platform.stop()
        assert base_platform.status == PlatformStatus.STOPPED
    
    @pytest.mark.asyncio
    async def test_platform_health_check(self, base_platform):
        """Test platform health check."""
        await base_platform.initialize()
        await base_platform.start()
        
        health = await base_platform.health_check()
        
        assert "platform" in health
        assert "status" in health
        assert "timestamp" in health
        assert health["platform"] == "healthy"
    
    def test_platform_task_management(self, base_platform):
        """Test platform task management."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="Test task",
            priority=Priority.NORMAL
        )
        
        # Add task
        base_platform.add_task(task)
        assert len(base_platform.tasks) == 1
        assert base_platform.tasks[0] == task
        
        # Get task
        retrieved_task = base_platform.get_task("test_task")
        assert retrieved_task == task
        
        # Remove task
        base_platform.remove_task("test_task")
        assert len(base_platform.tasks) == 0


class TestConversationManager:
    """Test ConversationManager class."""
    
    @pytest.fixture
    def conversation_manager(self):
        """Create a test conversation manager."""
        return ConversationManager()
    
    def test_conversation_manager_initialization(self, conversation_manager):
        """Test conversation manager initialization."""
        assert conversation_manager.conversations == {}
        assert conversation_manager.max_conversations == 100
        assert conversation_manager.max_messages == 50
    
    def test_conversation_creation(self, conversation_manager):
        """Test conversation creation."""
        session_id = "test_session"
        user_id = "test_user"
        
        conversation = conversation_manager.create_conversation(session_id, user_id)
        
        assert conversation.session_id == session_id
        assert conversation.user_id == user_id
        assert conversation.created_at is not None
        assert len(conversation.messages) == 0
    
    def test_conversation_retrieval(self, conversation_manager):
        """Test conversation retrieval."""
        session_id = "test_session"
        user_id = "test_user"
        
        conversation_manager.create_conversation(session_id, user_id)
        conversation = conversation_manager.get_conversation(session_id)
        
        assert conversation is not None
        assert conversation.session_id == session_id
        assert conversation.user_id == user_id
    
    def test_message_adding(self, conversation_manager):
        """Test adding messages to conversation."""
        session_id = "test_session"
        user_id = "test_user"
        
        conversation_manager.create_conversation(session_id, user_id)
        conversation_manager.add_message(session_id, "user", "Hello")
        conversation_manager.add_message(session_id, "assistant", "Hi there!")
        
        conversation = conversation_manager.get_conversation(session_id)
        assert len(conversation.messages) == 2
        assert conversation.messages[0].content == "Hello"
        assert conversation.messages[1].content == "Hi there!"


class TestMemoryManager:
    """Test MemoryManager class."""
    
    @pytest.fixture
    def memory_manager(self):
        """Create a test memory manager."""
        return MemoryManager()
    
    def test_memory_manager_initialization(self, memory_manager):
        """Test memory manager initialization."""
        assert memory_manager.memories == {}
        assert memory_manager.max_memories == 1000
        assert memory_manager.decay_rate == 0.1
    
    def test_memory_storage(self, memory_manager):
        """Test memory storage and retrieval."""
        memory_id = "test_memory"
        content = "Test memory content"
        metadata = {"type": "test"}
        
        memory_manager.store_memory(memory_id, content, metadata)
        
        memory = memory_manager.get_memory(memory_id)
        assert memory is not None
        assert memory.content == content
        assert memory.metadata == metadata
    
    def test_memory_search(self, memory_manager):
        """Test memory search functionality."""
        # Store multiple memories
        memory_manager.store_memory("mem1", "infrastructure setup", {"type": "infrastructure"})
        memory_manager.store_memory("mem2", "security configuration", {"type": "security"})
        memory_manager.store_memory("mem3", "monitoring setup", {"type": "monitoring"})
        
        # Search for memories
        results = memory_manager.search_memories("infrastructure")
        assert len(results) == 1
        assert results[0].content == "infrastructure setup"
        
        results = memory_manager.search_memories("setup")
        assert len(results) == 3  # All memories contain "setup"


class TestToolRegistry:
    """Test ToolRegistry class."""
    
    @pytest.fixture
    def tool_registry(self):
        """Create a test tool registry."""
        return ToolRegistry()
    
    def test_tool_registry_initialization(self, tool_registry):
        """Test tool registry initialization."""
        assert tool_registry.tools == {}
        assert tool_registry.categories == {}
    
    def test_tool_registration(self, tool_registry):
        """Test tool registration."""
        tool = Mock()
        tool.name = "test_tool"
        tool.category = "test"
        tool.description = "Test tool"
        
        tool_registry.register_tool(tool)
        
        assert "test_tool" in tool_registry.tools
        assert tool_registry.tools["test_tool"] == tool
        assert "test" in tool_registry.categories
        assert tool in tool_registry.categories["test"]
    
    def test_tool_retrieval(self, tool_registry):
        """Test tool retrieval."""
        tool = Mock()
        tool.name = "test_tool"
        tool.category = "test"
        tool.description = "Test tool"
        
        tool_registry.register_tool(tool)
        
        retrieved_tool = tool_registry.get_tool("test_tool")
        assert retrieved_tool == tool
        
        tools_in_category = tool_registry.get_tools_by_category("test")
        assert len(tools_in_category) == 1
        assert tools_in_category[0] == tool


class TestNaturalLanguageProcessor:
    """Test NaturalLanguageProcessor class."""
    
    @pytest.fixture
    def nlp(self):
        """Create a test NLP processor."""
        return NaturalLanguageProcessor()
    
    def test_nlp_initialization(self, nlp):
        """Test NLP processor initialization."""
        assert nlp.intent_patterns is not None
        assert nlp.entity_patterns is not None
    
    def test_intent_recognition(self, nlp):
        """Test intent recognition."""
        # Test infrastructure creation intent
        intent = nlp.recognize_intent("I need to create a web server")
        assert intent == "create_infrastructure"
        
        # Test security assessment intent
        intent = nlp.recognize_intent("Run a security scan")
        assert intent == "security_assessment"
        
        # Test monitoring setup intent
        intent = nlp.recognize_intent("Set up monitoring")
        assert intent == "setup_monitoring"
    
    def test_entity_extraction(self, nlp):
        """Test entity extraction."""
        text = "Create a web server with nginx on AWS in us-east-1"
        
        entities = nlp.extract_entities(text)
        
        assert "web server" in entities.get("service_type", [])
        assert "nginx" in entities.get("software", [])
        assert "AWS" in entities.get("cloud_provider", [])
        assert "us-east-1" in entities.get("region", [])
    
    def test_requirement_analysis(self, nlp):
        """Test requirement analysis."""
        requirements = "I need a scalable web application with database and load balancer"
        
        analysis = nlp.analyze_requirements(requirements)
        
        assert "intent" in analysis
        assert "entities" in analysis
        assert "complexity" in analysis
        assert "estimated_effort" in analysis
        assert analysis["intent"] == "create_infrastructure"


class TestCoreMemoryManager:
    """Test CoreMemoryManager class."""
    
    @pytest.fixture
    def core_memory_manager(self):
        """Create a test core memory manager."""
        return CoreMemoryManager()
    
    def test_core_memory_manager_initialization(self, core_memory_manager):
        """Test core memory manager initialization."""
        assert core_memory_manager.memories == {}
        assert core_memory_manager.relationships == {}
        assert core_memory_manager.decay_strategies == {}
    
    def test_memory_storage_with_relationships(self, core_memory_manager):
        """Test memory storage with relationships."""
        memory_id = "test_memory"
        content = "Test memory content"
        metadata = {"type": "test"}
        relationships = ["related_memory_1", "related_memory_2"]
        
        core_memory_manager.store_memory(memory_id, content, metadata, relationships)
        
        memory = core_memory_manager.get_memory(memory_id)
        assert memory is not None
        assert memory.content == content
        assert memory.relationships == relationships
    
    def test_memory_decay(self, core_memory_manager):
        """Test memory decay functionality."""
        memory_id = "test_memory"
        content = "Test memory content"
        
        core_memory_manager.store_memory(memory_id, content)
        
        # Simulate time passage
        memory = core_memory_manager.get_memory(memory_id)
        original_importance = memory.importance
        
        # Apply decay
        core_memory_manager.apply_decay(memory_id, 0.1)
        
        updated_memory = core_memory_manager.get_memory(memory_id)
        assert updated_memory.importance < original_importance


@pytest.mark.asyncio
class TestAsyncOperations:
    """Test asynchronous operations."""
    
    async def test_concurrent_task_execution(self):
        """Test concurrent task execution."""
        platform = BasePlatform(PlatformConfig(name="test"))
        await platform.initialize()
        await platform.start()
        
        # Create multiple tasks
        tasks = []
        for i in range(5):
            task = Task(
                id=f"task_{i}",
                name=f"Task {i}",
                description=f"Test task {i}",
                priority=Priority.NORMAL
            )
            tasks.append(task)
            platform.add_task(task)
        
        # Execute tasks concurrently
        results = await asyncio.gather(*[
            platform.execute_task(task) for task in tasks
        ])
        
        assert len(results) == 5
        for result in results:
            assert result is not None
    
    async def test_platform_orchestration(self):
        """Test platform orchestration."""
        from platform.core.base_platform import PlatformOrchestrator
        
        config = PlatformConfig(name="orchestrator_test")
        orchestrator = PlatformOrchestrator(config)
        
        await orchestrator.initialize()
        await orchestrator.start_platform()
        
        status = orchestrator.get_platform_status()
        assert status["status"] == "running"
        
        await orchestrator.stop_platform()
        status = orchestrator.get_platform_status()
        assert status["status"] == "stopped"


if __name__ == "__main__":
    pytest.main([__file__])
