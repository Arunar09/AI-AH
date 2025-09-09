"""
Pytest configuration and fixtures for the AI-AH Platform test suite.

This module provides shared fixtures and configuration for all tests.
"""

import pytest
import asyncio
import tempfile
import os
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from platform.core.base_platform import PlatformConfig
from platform.agents.terraform_agent import TerraformAgent
from platform.agents.ansible_agent import AnsibleAgent
from platform.agents.kubernetes_agent import KubernetesAgent
from platform.agents.security_agent import SecurityAgent
from platform.agents.monitoring_agent import MonitoringAgent


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def platform_config():
    """Create a test platform configuration."""
    return PlatformConfig(
        name="test_platform",
        version="1.0.0",
        description="Test platform for unit tests",
        environment="test"
    )


@pytest.fixture
def terraform_agent(platform_config):
    """Create a test Terraform agent."""
    return TerraformAgent(platform_config)


@pytest.fixture
def ansible_agent(platform_config):
    """Create a test Ansible agent."""
    return AnsibleAgent(platform_config)


@pytest.fixture
def kubernetes_agent(platform_config):
    """Create a test Kubernetes agent."""
    return KubernetesAgent(platform_config)


@pytest.fixture
def security_agent(platform_config):
    """Create a test Security agent."""
    return SecurityAgent(platform_config)


@pytest.fixture
def monitoring_agent(platform_config):
    """Create a test Monitoring agent."""
    return MonitoringAgent(platform_config)


@pytest.fixture
def all_agents(terraform_agent, ansible_agent, kubernetes_agent, security_agent, monitoring_agent):
    """Create all test agents."""
    return {
        "terraform": terraform_agent,
        "ansible": ansible_agent,
        "kubernetes": kubernetes_agent,
        "security": security_agent,
        "monitoring": monitoring_agent
    }


@pytest.fixture
def mock_terraform_response():
    """Mock Terraform agent response."""
    return Mock(
        response_type="plan_generated",
        content={
            "plan_id": "test_plan_123",
            "resources": ["aws_instance.web", "aws_security_group.web"],
            "estimated_cost": 50.0
        },
        confidence=0.9,
        suggestions=["Consider using auto-scaling", "Enable monitoring"],
        next_actions=["Review plan", "Execute plan"],
        metadata={"estimated_cost": 50.0, "resource_count": 2}
    )


@pytest.fixture
def mock_ansible_response():
    """Mock Ansible agent response."""
    return Mock(
        response_type="playbook_generated",
        content={
            "playbook_id": "test_playbook_123",
            "tasks": [
                {"name": "Install nginx", "module": "apt"},
                {"name": "Configure SSL", "module": "ssl_certificate"},
                {"name": "Security hardening", "module": "security_hardening"}
            ],
            "estimated_duration": "15 minutes"
        },
        confidence=0.85,
        suggestions=["Test in staging first", "Backup configuration"],
        next_actions=["Review playbook", "Execute playbook"],
        metadata={"estimated_duration": "15 minutes", "task_count": 3}
    )


@pytest.fixture
def mock_kubernetes_response():
    """Mock Kubernetes agent response."""
    return Mock(
        response_type="deployment_generated",
        content={
            "deployment_id": "test_deploy_123",
            "manifests": [
                {"kind": "Deployment", "name": "web-app"},
                {"kind": "Service", "name": "web-app-service"},
                {"kind": "Ingress", "name": "web-app-ingress"}
            ],
            "replicas": 3
        },
        confidence=0.9,
        suggestions=["Set resource limits", "Configure health checks"],
        next_actions=["Review manifests", "Deploy"],
        metadata={"replicas": 3, "manifest_count": 3}
    )


@pytest.fixture
def mock_security_response():
    """Mock Security agent response."""
    return Mock(
        response_type="assessment_generated",
        content={
            "assessment_id": "test_assess_123",
            "checks": [
                {"name": "SSL Configuration", "status": "pass"},
                {"name": "Firewall Rules", "status": "fail"},
                {"name": "Access Controls", "status": "pass"}
            ],
            "compliance_score": 85.0,
            "recommendations": ["Update firewall rules", "Enable 2FA"]
        },
        confidence=0.95,
        suggestions=["Address critical vulnerabilities", "Update security policies"],
        next_actions=["Review findings", "Implement fixes"],
        metadata={"compliance_score": 85.0, "check_count": 3}
    )


@pytest.fixture
def mock_monitoring_response():
    """Mock Monitoring agent response."""
    return Mock(
        response_type="monitoring_configured",
        content={
            "config_id": "test_monitor_123",
            "components": [
                {"name": "Prometheus", "type": "metrics_collection"},
                {"name": "Grafana", "type": "visualization"},
                {"name": "AlertManager", "type": "alerting"}
            ],
            "metrics": ["cpu_usage", "memory_usage", "disk_usage"],
            "dashboards": ["infrastructure_overview", "application_metrics"]
        },
        confidence=0.9,
        suggestions=["Set up alerting rules", "Create custom dashboards"],
        next_actions=["Review configuration", "Deploy monitoring"],
        metadata={"component_count": 3, "metric_count": 3}
    )


@pytest.fixture
def mock_agent_responses(mock_terraform_response, mock_ansible_response, 
                        mock_kubernetes_response, mock_security_response, 
                        mock_monitoring_response):
    """All mock agent responses."""
    return {
        "terraform": mock_terraform_response,
        "ansible": mock_ansible_response,
        "kubernetes": mock_kubernetes_response,
        "security": mock_security_response,
        "monitoring": mock_monitoring_response
    }


@pytest.fixture
def sample_requirements():
    """Sample requirements for testing."""
    return {
        "simple": "Create a web server",
        "complex": "Create a scalable web application with database, load balancer, and monitoring on AWS",
        "security": "Run comprehensive security assessment with CIS benchmarks",
        "monitoring": "Set up monitoring with Prometheus and Grafana for infrastructure and applications",
        "kubernetes": "Deploy a microservices application with 5 services and auto-scaling"
    }


@pytest.fixture
def sample_context():
    """Sample context data for testing."""
    return {
        "aws": {
            "cloud_provider": "aws",
            "region": "us-east-1",
            "environment": "production"
        },
        "azure": {
            "cloud_provider": "azure",
            "region": "eastus",
            "environment": "staging"
        },
        "gcp": {
            "cloud_provider": "gcp",
            "region": "us-central1",
            "environment": "development"
        }
    }


@pytest.fixture
def mock_platform_status():
    """Mock platform status response."""
    return {
        "status": "running",
        "agents_count": 5,
        "active_tasks": 12,
        "alerts": 3,
        "success_rate": 98.5,
        "uptime": 3600,
        "last_activity": datetime.now().isoformat()
    }


@pytest.fixture
def mock_health_check():
    """Mock health check response."""
    return {
        "platform": "healthy",
        "agents": True,
        "tools": True,
        "database": True,
        "cache": True,
        "timestamp": datetime.now().isoformat()
    }


@pytest.fixture
def mock_user_data():
    """Mock user data for authentication tests."""
    return {
        "user_id": "test_user_123",
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "permissions": ["read", "write"],
        "created_at": datetime.now().isoformat(),
        "last_login": datetime.now().isoformat()
    }


@pytest.fixture
def mock_auth_token():
    """Mock authentication token."""
    return "mock_jwt_token_12345"


@pytest.fixture
def mock_conversation_data():
    """Mock conversation data."""
    return {
        "session_id": "test_session_123",
        "user_id": "test_user_123",
        "messages": [
            {
                "role": "user",
                "content": "I need help setting up a web server",
                "timestamp": datetime.now().isoformat()
            },
            {
                "role": "assistant",
                "content": "I can help you set up a web server. What type of server do you need?",
                "timestamp": datetime.now().isoformat()
            }
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


@pytest.fixture
def mock_task_data():
    """Mock task data."""
    return {
        "id": "test_task_123",
        "name": "Test Task",
        "description": "Test task description",
        "status": "pending",
        "priority": "normal",
        "agent_type": "terraform",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "metadata": {"test": True}
    }


@pytest.fixture
def mock_websocket_message():
    """Mock WebSocket message."""
    return {
        "message_type": "agent_update",
        "data": {
            "agent_type": "terraform",
            "status": "running",
            "update": "Task completed successfully"
        },
        "timestamp": datetime.now().isoformat(),
        "user_id": "test_user_123",
        "session_id": "test_session_123"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "websocket: marks tests as WebSocket tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file names
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_api" in item.nodeid:
            item.add_marker(pytest.mark.api)
        elif "websocket" in item.nodeid:
            item.add_marker(pytest.mark.websocket)
        else:
            item.add_marker(pytest.mark.unit)
        
        # Add slow marker for tests that might take longer
        if "performance" in item.nodeid or "concurrent" in item.nodeid:
            item.add_marker(pytest.mark.slow)


# Async test utilities
@pytest.fixture
def async_mock():
    """Create an async mock."""
    return AsyncMock()


@pytest.fixture
def mock_async_agent():
    """Create a mock async agent."""
    agent = AsyncMock()
    agent.config = Mock()
    agent.config.name = "mock_agent"
    agent.config.version = "1.0.0"
    agent.status = Mock()
    agent.status.value = "running"
    agent.capabilities = []
    agent.tasks = []
    return agent


# Test data generators
@pytest.fixture
def generate_test_requirements():
    """Generate test requirements."""
    def _generate(complexity="simple"):
        if complexity == "simple":
            return "Create a web server with nginx"
        elif complexity == "medium":
            return "Create a web application with database and load balancer"
        elif complexity == "complex":
            return "Create a scalable microservices application with monitoring, security, and auto-scaling"
        else:
            return "Create infrastructure"
    return _generate


@pytest.fixture
def generate_test_context():
    """Generate test context."""
    def _generate(provider="aws"):
        contexts = {
            "aws": {"cloud_provider": "aws", "region": "us-east-1"},
            "azure": {"cloud_provider": "azure", "region": "eastus"},
            "gcp": {"cloud_provider": "gcp", "region": "us-central1"}
        }
        return contexts.get(provider, contexts["aws"])
    return _generate


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test files after each test."""
    yield
    # Cleanup logic here if needed
    pass


# Environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment."""
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    yield
    
    # Cleanup environment variables
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]
