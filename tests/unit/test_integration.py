"""
Integration tests for the Multi-Agent Infrastructure Intelligence Platform.

This module contains end-to-end integration tests that verify the complete
workflow from user request to agent execution.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from platform.api.main import app
from platform.core.base_platform import PlatformConfig
from platform.agents.terraform_agent import TerraformAgent
from platform.agents.ansible_agent import AnsibleAgent
from platform.agents.kubernetes_agent import KubernetesAgent
from platform.agents.security_agent import SecurityAgent
from platform.agents.monitoring_agent import MonitoringAgent


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers."""
        login_response = client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.mark.asyncio
    async def test_complete_infrastructure_deployment_workflow(self, client, auth_headers):
        """Test complete infrastructure deployment workflow."""
        # Step 1: Terraform - Create infrastructure
        terraform_request = {
            "request_id": "workflow_123",
            "user_id": "test_user",
            "requirements": "Create a web server with nginx on AWS in us-east-1",
            "context": {"cloud_provider": "aws", "region": "us-east-1"}
        }
        
        with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
            # Mock Terraform agent
            mock_terraform = Mock()
            mock_terraform.config.name = "terraform_agent"
            mock_terraform.process_request = AsyncMock(return_value=Mock(
                response_type="plan_generated",
                content={"plan_id": "plan_123", "resources": ["aws_instance.web"]},
                confidence=0.9,
                suggestions=["Consider auto-scaling"],
                next_actions=["Review plan", "Execute plan"],
                metadata={"estimated_cost": 50.0}
            ))
            
            # Mock Ansible agent
            mock_ansible = Mock()
            mock_ansible.config.name = "ansible_agent"
            mock_ansible.process_request = AsyncMock(return_value=Mock(
                response_type="playbook_generated",
                content={"playbook_id": "playbook_123", "tasks": ["configure_nginx"]},
                confidence=0.85,
                suggestions=["Test in staging"],
                next_actions=["Review playbook", "Execute playbook"],
                metadata={"estimated_duration": "15 minutes"}
            ))
            
            # Mock Security agent
            mock_security = Mock()
            mock_security.config.name = "security_agent"
            mock_security.process_request = AsyncMock(return_value=Mock(
                response_type="assessment_generated",
                content={"assessment_id": "assess_123", "score": 90},
                confidence=0.95,
                suggestions=["Enable 2FA"],
                next_actions=["Review findings", "Implement fixes"],
                metadata={"compliance_score": 90.0}
            ))
            
            # Mock Monitoring agent
            mock_monitoring = Mock()
            mock_monitoring.config.name = "monitoring_agent"
            mock_monitoring.process_request = AsyncMock(return_value=Mock(
                response_type="monitoring_configured",
                content={"config_id": "monitor_123", "components": ["Prometheus", "Grafana"]},
                confidence=0.9,
                suggestions=["Set up alerting"],
                next_actions=["Review config", "Deploy monitoring"],
                metadata={"metrics": ["cpu", "memory", "disk"]}
            ))
            
            # Configure mock to return appropriate agent based on request
            def get_agent_side_effect(agent_type):
                if agent_type == "terraform":
                    return mock_terraform
                elif agent_type == "ansible":
                    return mock_ansible
                elif agent_type == "security":
                    return mock_security
                elif agent_type == "monitoring":
                    return mock_monitoring
                else:
                    return mock_terraform  # Default
            
            mock_get_agent.side_effect = get_agent_side_effect
            
            # Execute workflow steps
            # Step 1: Terraform infrastructure creation
            terraform_response = client.post(
                "/api/v1/agents/terraform/request",
                json=terraform_request,
                headers=auth_headers
            )
            assert terraform_response.status_code == 200
            terraform_data = terraform_response.json()
            assert terraform_data["agent_type"] == "terraform"
            assert terraform_data["response_type"] == "plan_generated"
            
            # Step 2: Ansible configuration
            ansible_request = {
                "request_id": "workflow_124",
                "user_id": "test_user",
                "requirements": "Configure nginx with SSL and security hardening",
                "target_hosts": ["web-server-1"]
            }
            
            ansible_response = client.post(
                "/api/v1/agents/ansible/request",
                json=ansible_request,
                headers=auth_headers
            )
            assert ansible_response.status_code == 200
            ansible_data = ansible_response.json()
            assert ansible_data["agent_type"] == "ansible"
            assert ansible_data["response_type"] == "playbook_generated"
            
            # Step 3: Security assessment
            security_request = {
                "request_id": "workflow_125",
                "user_id": "test_user",
                "requirements": "Run comprehensive security assessment",
                "compliance_framework": "CIS"
            }
            
            security_response = client.post(
                "/api/v1/agents/security/request",
                json=security_request,
                headers=auth_headers
            )
            assert security_response.status_code == 200
            security_data = security_response.json()
            assert security_data["agent_type"] == "security"
            assert security_data["response_type"] == "assessment_generated"
            
            # Step 4: Monitoring setup
            monitoring_request = {
                "request_id": "workflow_126",
                "user_id": "test_user",
                "requirements": "Set up comprehensive monitoring",
                "monitoring_type": "infrastructure"
            }
            
            monitoring_response = client.post(
                "/api/v1/agents/monitoring/request",
                json=monitoring_request,
                headers=auth_headers
            )
            assert monitoring_response.status_code == 200
            monitoring_data = monitoring_response.json()
            assert monitoring_data["agent_type"] == "monitoring"
            assert monitoring_data["response_type"] == "monitoring_configured"
    
    @pytest.mark.asyncio
    async def test_kubernetes_deployment_workflow(self, client, auth_headers):
        """Test Kubernetes deployment workflow."""
        # Step 1: Kubernetes deployment
        k8s_request = {
            "request_id": "k8s_workflow_123",
            "user_id": "test_user",
            "requirements": "Deploy scalable web application with 3 replicas and load balancer",
            "namespace": "production"
        }
        
        with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
            # Mock Kubernetes agent
            mock_k8s = Mock()
            mock_k8s.config.name = "kubernetes_agent"
            mock_k8s.process_request = AsyncMock(return_value=Mock(
                response_type="deployment_generated",
                content={
                    "deployment_id": "deploy_123",
                    "manifests": [
                        {"kind": "Deployment", "name": "web-app"},
                        {"kind": "Service", "name": "web-app-service"},
                        {"kind": "Ingress", "name": "web-app-ingress"}
                    ]
                },
                confidence=0.9,
                suggestions=["Set resource limits"],
                next_actions=["Review manifests", "Deploy"],
                metadata={"replicas": 3}
            ))
            
            mock_get_agent.return_value = mock_k8s
            
            # Execute Kubernetes deployment
            k8s_response = client.post(
                "/api/v1/agents/kubernetes/request",
                json=k8s_request,
                headers=auth_headers
            )
            assert k8s_response.status_code == 200
            k8s_data = k8s_response.json()
            assert k8s_data["agent_type"] == "kubernetes"
            assert k8s_data["response_type"] == "deployment_generated"
            
            # Step 2: Security assessment for Kubernetes
            security_request = {
                "request_id": "k8s_security_123",
                "user_id": "test_user",
                "requirements": "Run Kubernetes security assessment",
                "compliance_framework": "CIS_Kubernetes"
            }
            
            # Mock Security agent for Kubernetes
            mock_security = Mock()
            mock_security.config.name = "security_agent"
            mock_security.process_request = AsyncMock(return_value=Mock(
                response_type="assessment_generated",
                content={"assessment_id": "k8s_assess_123", "score": 88},
                confidence=0.9,
                suggestions=["Enable RBAC", "Use network policies"],
                next_actions=["Review findings", "Implement fixes"],
                metadata={"compliance_score": 88.0}
            ))
            
            mock_get_agent.return_value = mock_security
            
            security_response = client.post(
                "/api/v1/agents/security/request",
                json=security_request,
                headers=auth_headers
            )
            assert security_response.status_code == 200
            security_data = security_response.json()
            assert security_data["agent_type"] == "security"
            assert security_data["response_type"] == "assessment_generated"
    
    @pytest.mark.asyncio
    async def test_conversation_workflow(self, client, auth_headers):
        """Test conversation workflow with multiple agents."""
        conversation_requests = [
            {
                "message": "I need to create a web server",
                "user_id": "test_user",
                "session_id": "conversation_123"
            },
            {
                "message": "Make it secure with SSL",
                "user_id": "test_user",
                "session_id": "conversation_123"
            },
            {
                "message": "Set up monitoring for it",
                "user_id": "test_user",
                "session_id": "conversation_123"
            }
        ]
        
        with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
            # Mock agent responses for different conversation turns
            mock_responses = [
                Mock(
                    content="I can help you create a web server. I'll use Terraform to provision the infrastructure.",
                    confidence=0.9,
                    suggestions=["Use AWS", "Consider auto-scaling"],
                    metadata={}
                ),
                Mock(
                    content="I'll configure SSL certificates and security hardening using Ansible.",
                    confidence=0.85,
                    suggestions=["Use Let's Encrypt", "Enable HSTS"],
                    metadata={}
                ),
                Mock(
                    content="I'll set up Prometheus and Grafana for comprehensive monitoring.",
                    confidence=0.9,
                    suggestions=["Set up alerting", "Create dashboards"],
                    metadata={}
                )
            ]
            
            mock_agent = Mock()
            mock_agent.process_request = AsyncMock(side_effect=mock_responses)
            mock_get_agent.return_value = mock_agent
            
            # Execute conversation
            for i, request in enumerate(conversation_requests):
                response = client.post(
                    "/api/v1/agents/conversation",
                    json=request,
                    headers=auth_headers
                )
                assert response.status_code == 200
                data = response.json()
                assert "response" in data
                assert "confidence" in data
                assert "suggestions" in data
                assert data["confidence"] > 0.8


class TestPlatformIntegration:
    """Test platform-level integration."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers."""
        login_response = client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_platform_startup_and_shutdown(self, client, auth_headers):
        """Test platform startup and shutdown workflow."""
        with patch('platform.api.routes.platform_routes.get_orchestrator') as mock_get_orchestrator:
            mock_orchestrator = Mock()
            mock_orchestrator.start_platform = AsyncMock(return_value=True)
            mock_orchestrator.stop_platform = AsyncMock(return_value=True)
            mock_orchestrator.get_platform_status.return_value = {
                "status": "running",
                "agents_count": 5,
                "active_tasks": 0
            }
            mock_get_orchestrator.return_value = mock_orchestrator
            
            # Start platform
            start_response = client.post("/api/v1/platform/start", headers=auth_headers)
            assert start_response.status_code == 200
            assert start_response.json()["data"]["status"] == "started"
            
            # Check status
            status_response = client.get("/api/v1/platform/status", headers=auth_headers)
            assert status_response.status_code == 200
            assert status_response.json()["status"] == "running"
            
            # Stop platform
            stop_response = client.post("/api/v1/platform/stop", headers=auth_headers)
            assert stop_response.status_code == 200
            assert stop_response.json()["data"]["status"] == "stopped"
    
    def test_agent_lifecycle_management(self, client, auth_headers):
        """Test agent lifecycle management."""
        with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
            mock_agent = Mock()
            mock_agent.config.name = "terraform_agent"
            mock_agent.config.version = "1.0.0"
            mock_agent.status.value = "running"
            mock_agent.get_capabilities.return_value = []
            mock_agent.get_status.return_value = {"status": "running"}
            mock_agent.tasks = []
            mock_get_agent.return_value = mock_agent
            
            # Get agent status
            status_response = client.get(
                "/api/v1/agents/terraform/status",
                headers=auth_headers
            )
            assert status_response.status_code == 200
            assert status_response.json()["component"] == "terraform_agent"
            
            # Get agent capabilities
            capabilities_response = client.get(
                "/api/v1/agents/terraform/capabilities",
                headers=auth_headers
            )
            assert capabilities_response.status_code == 200
            assert capabilities_response.json()["agent_type"] == "terraform"
            
            # List all agents
            list_response = client.get("/api/v1/agents/", headers=auth_headers)
            assert list_response.status_code == 200
            assert len(list_response.json()["data"]["agents"]) == 5
    
    def test_platform_health_monitoring(self, client, auth_headers):
        """Test platform health monitoring."""
        with patch('platform.api.routes.platform_routes.get_orchestrator') as mock_get_orchestrator:
            mock_orchestrator = Mock()
            mock_orchestrator.health_check = AsyncMock(return_value={
                "platform": "healthy",
                "agents": True,
                "tools": True,
                "database": True,
                "cache": True
            })
            mock_get_orchestrator.return_value = mock_orchestrator
            
            # Check platform health
            health_response = client.get("/api/v1/platform/health", headers=auth_headers)
            assert health_response.status_code == 200
            
            health_data = health_response.json()
            assert health_data["component"] == "ai-ah-platform"
            assert health_data["health_status"] == "healthy"
            assert len(health_data["dependencies"]) > 0
    
    def test_data_export_import_workflow(self, client, auth_headers):
        """Test data export and import workflow."""
        # Export data
        export_request = {
            "export_type": "json",
            "resource_type": "infrastructure",
            "agent_type": "terraform",
            "include_metadata": True
        }
        
        export_response = client.post(
            "/api/v1/platform/export",
            json=export_request,
            headers=auth_headers
        )
        assert export_response.status_code == 200
        
        export_data = export_response.json()
        assert "export_id" in export_data
        assert export_data["export_type"] == "json"
        
        # Import data
        import_request = {
            "import_type": "json",
            "data": {"test": "data"},
            "agent_type": "terraform",
            "validate_only": True
        }
        
        import_response = client.post(
            "/api/v1/platform/import",
            json=import_request,
            headers=auth_headers
        )
        assert import_response.status_code == 200
        
        import_data = import_response.json()
        assert "import_id" in import_data
        assert import_data["import_type"] == "json"


class TestErrorRecovery:
    """Test error recovery and resilience."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers."""
        login_response = client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_agent_failure_recovery(self, client, auth_headers):
        """Test agent failure and recovery."""
        with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
            # Simulate agent failure
            mock_get_agent.side_effect = Exception("Agent initialization failed")
            
            # Request should handle failure gracefully
            request_data = {
                "request_id": "failure_test_123",
                "user_id": "test_user",
                "requirements": "Create infrastructure"
            }
            
            response = client.post(
                "/api/v1/agents/terraform/request",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 500  # Should return error, not crash
    
    def test_platform_graceful_degradation(self, client, auth_headers):
        """Test platform graceful degradation."""
        with patch('platform.api.routes.platform_routes.get_orchestrator') as mock_get_orchestrator:
            # Simulate partial platform failure
            mock_orchestrator = Mock()
            mock_orchestrator.health_check = AsyncMock(return_value={
                "platform": "degraded",
                "agents": False,  # Agents down
                "tools": True,    # Tools still working
                "database": True,
                "cache": False    # Cache down
            })
            mock_get_orchestrator.return_value = mock_orchestrator
            
            # Platform should still respond with degraded status
            health_response = client.get("/api/v1/platform/health", headers=auth_headers)
            assert health_response.status_code == 200
            
            health_data = health_response.json()
            assert health_data["health_status"] == "unhealthy"  # Should reflect degraded state
    
    def test_concurrent_request_handling(self, client, auth_headers):
        """Test concurrent request handling."""
        import threading
        import time
        
        results = []
        
        def make_request():
            request_data = {
                "request_id": f"concurrent_{threading.current_thread().ident}",
                "user_id": "test_user",
                "requirements": "Create infrastructure"
            }
            
            with patch('platform.api.routes.agent_routes.get_agent') as mock_get_agent:
                mock_agent = Mock()
                mock_agent.config.name = "terraform_agent"
                mock_agent.process_request = AsyncMock(return_value=Mock(
                    response_type="plan_generated",
                    content={"plan_id": "plan_123"},
                    confidence=0.9,
                    suggestions=[],
                    next_actions=[],
                    metadata={}
                ))
                mock_get_agent.return_value = mock_agent
                
                response = client.post(
                    "/api/v1/agents/terraform/request",
                    json=request_data,
                    headers=auth_headers
                )
                results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(results) == 5
        assert all(status == 200 for status in results)


class TestPerformanceIntegration:
    """Test performance and scalability."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers."""
        login_response = client.post("/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_response_times(self, client, auth_headers):
        """Test response times for various endpoints."""
        import time
        
        endpoints = [
            ("/health", "GET"),
            ("/api/v1/platform/status", "GET"),
            ("/api/v1/agents/", "GET"),
            ("/api/v1/platform/info", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            
            if method == "GET":
                response = client.get(endpoint, headers=auth_headers)
            else:
                response = client.post(endpoint, headers=auth_headers)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 1.0  # Should respond within 1 second
    
    def test_memory_usage_stability(self, client, auth_headers):
        """Test memory usage stability under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Make multiple requests
        for i in range(100):
            response = client.get("/api/v1/platform/status", headers=auth_headers)
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__])
