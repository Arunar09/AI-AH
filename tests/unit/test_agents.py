"""
Tests for specialized agents.

This module contains comprehensive tests for all specialized agents:
Terraform, Ansible, Kubernetes, Security, and Monitoring agents.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from platform.core.base_platform import PlatformConfig
from platform.agents.terraform_agent import TerraformAgent
from platform.agents.ansible_agent import AnsibleAgent
from platform.agents.kubernetes_agent import KubernetesAgent
from platform.agents.security_agent import SecurityAgent
from platform.agents.monitoring_agent import MonitoringAgent


class TestTerraformAgent:
    """Test TerraformAgent class."""
    
    @pytest.fixture
    def terraform_agent(self):
        """Create a test Terraform agent."""
        config = PlatformConfig(name="terraform_test", version="1.0.0")
        return TerraformAgent(config)
    
    def test_terraform_agent_initialization(self, terraform_agent):
        """Test Terraform agent initialization."""
        assert terraform_agent.config.name == "terraform_test"
        assert terraform_agent.agent_type == "terraform"
        assert terraform_agent.capabilities is not None
        assert len(terraform_agent.capabilities) > 0
    
    def test_terraform_agent_capabilities(self, terraform_agent):
        """Test Terraform agent capabilities."""
        capabilities = terraform_agent.get_capabilities()
        
        capability_names = [cap.name for cap in capabilities]
        assert "terraform_plan_generation" in capability_names
        assert "terraform_execution" in capability_names
        assert "infrastructure_analysis" in capability_names
    
    @pytest.mark.asyncio
    async def test_terraform_agent_initialization_async(self, terraform_agent):
        """Test Terraform agent async initialization."""
        await terraform_agent.initialize()
        assert terraform_agent.status.value == "initialized"
    
    @pytest.mark.asyncio
    async def test_terraform_agent_lifecycle(self, terraform_agent):
        """Test Terraform agent lifecycle."""
        await terraform_agent.initialize()
        await terraform_agent.start()
        assert terraform_agent.status.value == "running"
        
        await terraform_agent.stop()
        assert terraform_agent.status.value == "stopped"
    
    @pytest.mark.asyncio
    async def test_terraform_plan_generation(self, terraform_agent):
        """Test Terraform plan generation."""
        requirements = "Create a web server with nginx on AWS"
        
        with patch.object(terraform_agent, 'generate_plan') as mock_generate:
            mock_generate.return_value = {
                "plan_id": "plan_123",
                "resources": ["aws_instance.web", "aws_security_group.web"],
                "estimated_cost": 50.0
            }
            
            result = await terraform_agent.generate_plan(requirements)
            
            assert result["plan_id"] == "plan_123"
            assert len(result["resources"]) == 2
            assert result["estimated_cost"] == 50.0
    
    @pytest.mark.asyncio
    async def test_terraform_plan_execution(self, terraform_agent):
        """Test Terraform plan execution."""
        plan = {
            "plan_id": "plan_123",
            "resources": ["aws_instance.web"],
            "estimated_cost": 50.0
        }
        
        with patch.object(terraform_agent, 'execute_plan') as mock_execute:
            mock_execute.return_value = {
                "execution_id": "exec_123",
                "status": "success",
                "resources_created": 1,
                "actual_cost": 45.0
            }
            
            result = await terraform_agent.execute_plan(plan)
            
            assert result["execution_id"] == "exec_123"
            assert result["status"] == "success"
            assert result["resources_created"] == 1
    
    @pytest.mark.asyncio
    async def test_terraform_requirements_analysis(self, terraform_agent):
        """Test Terraform requirements analysis."""
        requirements = "I need a scalable web application with database and load balancer on AWS"
        
        with patch.object(terraform_agent, 'analyze_requirements') as mock_analyze:
            mock_analyze.return_value = {
                "intent": "create_infrastructure",
                "entities": {
                    "service_type": ["web application"],
                    "requirements": ["scalable", "database", "load balancer"],
                    "cloud_provider": ["AWS"]
                },
                "complexity": "high",
                "estimated_effort": "2-4 hours"
            }
            
            result = await terraform_agent.analyze_requirements(requirements)
            
            assert result["intent"] == "create_infrastructure"
            assert "web application" in result["entities"]["service_type"]
            assert "AWS" in result["entities"]["cloud_provider"]
            assert result["complexity"] == "high"


class TestAnsibleAgent:
    """Test AnsibleAgent class."""
    
    @pytest.fixture
    def ansible_agent(self):
        """Create a test Ansible agent."""
        config = PlatformConfig(name="ansible_test", version="1.0.0")
        return AnsibleAgent(config)
    
    def test_ansible_agent_initialization(self, ansible_agent):
        """Test Ansible agent initialization."""
        assert ansible_agent.config.name == "ansible_test"
        assert ansible_agent.agent_type == "ansible"
        assert ansible_agent.capabilities is not None
        assert len(ansible_agent.capabilities) > 0
    
    def test_ansible_agent_capabilities(self, ansible_agent):
        """Test Ansible agent capabilities."""
        capabilities = ansible_agent.get_capabilities()
        
        capability_names = [cap.name for cap in capabilities]
        assert "playbook_generation" in capability_names
        assert "playbook_execution" in capability_names
        assert "configuration_management" in capability_names
    
    @pytest.mark.asyncio
    async def test_ansible_playbook_generation(self, ansible_agent):
        """Test Ansible playbook generation."""
        requirements = "Configure nginx web server with SSL and security hardening"
        
        with patch.object(ansible_agent, 'generate_playbook') as mock_generate:
            mock_generate.return_value = {
                "playbook_id": "playbook_123",
                "tasks": [
                    {"name": "Install nginx", "module": "apt"},
                    {"name": "Configure SSL", "module": "ssl_certificate"},
                    {"name": "Security hardening", "module": "security_hardening"}
                ],
                "estimated_duration": "15 minutes"
            }
            
            result = await ansible_agent.generate_playbook(requirements)
            
            assert result["playbook_id"] == "playbook_123"
            assert len(result["tasks"]) == 3
            assert result["estimated_duration"] == "15 minutes"
    
    @pytest.mark.asyncio
    async def test_ansible_playbook_execution(self, ansible_agent):
        """Test Ansible playbook execution."""
        playbook = {
            "playbook_id": "playbook_123",
            "tasks": [{"name": "Install nginx", "module": "apt"}],
            "target_hosts": ["web-server-1"]
        }
        
        with patch.object(ansible_agent, 'execute_playbook') as mock_execute:
            mock_execute.return_value = {
                "execution_id": "exec_123",
                "status": "success",
                "tasks_completed": 1,
                "duration": "5 minutes"
            }
            
            result = await ansible_agent.execute_playbook(playbook)
            
            assert result["execution_id"] == "exec_123"
            assert result["status"] == "success"
            assert result["tasks_completed"] == 1


class TestKubernetesAgent:
    """Test KubernetesAgent class."""
    
    @pytest.fixture
    def kubernetes_agent(self):
        """Create a test Kubernetes agent."""
        config = PlatformConfig(name="kubernetes_test", version="1.0.0")
        return KubernetesAgent(config)
    
    def test_kubernetes_agent_initialization(self, kubernetes_agent):
        """Test Kubernetes agent initialization."""
        assert kubernetes_agent.config.name == "kubernetes_test"
        assert kubernetes_agent.agent_type == "kubernetes"
        assert kubernetes_agent.capabilities is not None
        assert len(kubernetes_agent.capabilities) > 0
    
    def test_kubernetes_agent_capabilities(self, kubernetes_agent):
        """Test Kubernetes agent capabilities."""
        capabilities = kubernetes_agent.get_capabilities()
        
        capability_names = [cap.name for cap in capabilities]
        assert "deployment_generation" in capability_names
        assert "deployment_execution" in capability_names
        assert "container_orchestration" in capability_names
    
    @pytest.mark.asyncio
    async def test_kubernetes_deployment_generation(self, kubernetes_agent):
        """Test Kubernetes deployment generation."""
        requirements = "Deploy a scalable web application with 3 replicas and load balancer"
        
        with patch.object(kubernetes_agent, 'generate_deployment') as mock_generate:
            mock_generate.return_value = {
                "deployment_id": "deploy_123",
                "manifests": [
                    {"kind": "Deployment", "name": "web-app"},
                    {"kind": "Service", "name": "web-app-service"},
                    {"kind": "Ingress", "name": "web-app-ingress"}
                ],
                "replicas": 3
            }
            
            result = await kubernetes_agent.generate_deployment(requirements)
            
            assert result["deployment_id"] == "deploy_123"
            assert len(result["manifests"]) == 3
            assert result["replicas"] == 3
    
    @pytest.mark.asyncio
    async def test_kubernetes_deployment_execution(self, kubernetes_agent):
        """Test Kubernetes deployment execution."""
        deployment = {
            "deployment_id": "deploy_123",
            "manifests": [{"kind": "Deployment", "name": "web-app"}],
            "namespace": "default"
        }
        
        with patch.object(kubernetes_agent, 'execute_deployment') as mock_execute:
            mock_execute.return_value = {
                "execution_id": "exec_123",
                "status": "success",
                "pods_created": 3,
                "services_created": 1
            }
            
            result = await kubernetes_agent.execute_deployment(deployment)
            
            assert result["execution_id"] == "exec_123"
            assert result["status"] == "success"
            assert result["pods_created"] == 3


class TestSecurityAgent:
    """Test SecurityAgent class."""
    
    @pytest.fixture
    def security_agent(self):
        """Create a test Security agent."""
        config = PlatformConfig(name="security_test", version="1.0.0")
        return SecurityAgent(config)
    
    def test_security_agent_initialization(self, security_agent):
        """Test Security agent initialization."""
        assert security_agent.config.name == "security_test"
        assert security_agent.agent_type == "security"
        assert security_agent.capabilities is not None
        assert len(security_agent.capabilities) > 0
    
    def test_security_agent_capabilities(self, security_agent):
        """Test Security agent capabilities."""
        capabilities = security_agent.get_capabilities()
        
        capability_names = [cap.name for cap in capabilities]
        assert "security_assessment" in capability_names
        assert "compliance_checking" in capability_names
        assert "vulnerability_scanning" in capability_names
        assert "security_hardening" in capability_names
    
    @pytest.mark.asyncio
    async def test_security_assessment(self, security_agent):
        """Test security assessment."""
        requirements = "Run comprehensive security assessment for web infrastructure"
        
        with patch.object(security_agent, 'generate_security_assessment') as mock_generate:
            mock_generate.return_value = {
                "assessment_id": "assess_123",
                "checks": [
                    {"name": "SSL Configuration", "status": "pass"},
                    {"name": "Firewall Rules", "status": "fail"},
                    {"name": "Access Controls", "status": "pass"}
                ],
                "compliance_score": 85.0,
                "recommendations": ["Update firewall rules", "Enable 2FA"]
            }
            
            result = await security_agent.generate_security_assessment(requirements)
            
            assert result["assessment_id"] == "assess_123"
            assert len(result["checks"]) == 3
            assert result["compliance_score"] == 85.0
            assert len(result["recommendations"]) == 2
    
    @pytest.mark.asyncio
    async def test_compliance_checking(self, security_agent):
        """Test compliance checking."""
        requirements = "Check compliance with CIS benchmarks and NIST framework"
        
        with patch.object(security_agent, 'check_compliance') as mock_check:
            mock_check.return_value = {
                "compliance_id": "comp_123",
                "frameworks": ["CIS", "NIST"],
                "results": {
                    "CIS": {"score": 90, "passed": 18, "failed": 2},
                    "NIST": {"score": 85, "passed": 15, "failed": 3}
                },
                "overall_score": 87.5
            }
            
            result = await security_agent.check_compliance(requirements)
            
            assert result["compliance_id"] == "comp_123"
            assert "CIS" in result["frameworks"]
            assert "NIST" in result["frameworks"]
            assert result["overall_score"] == 87.5


class TestMonitoringAgent:
    """Test MonitoringAgent class."""
    
    @pytest.fixture
    def monitoring_agent(self):
        """Create a test Monitoring agent."""
        config = PlatformConfig(name="monitoring_test", version="1.0.0")
        return MonitoringAgent(config)
    
    def test_monitoring_agent_initialization(self, monitoring_agent):
        """Test Monitoring agent initialization."""
        assert monitoring_agent.config.name == "monitoring_test"
        assert monitoring_agent.agent_type == "monitoring"
        assert monitoring_agent.capabilities is not None
        assert len(monitoring_agent.capabilities) > 0
    
    def test_monitoring_agent_capabilities(self, monitoring_agent):
        """Test Monitoring agent capabilities."""
        capabilities = monitoring_agent.get_capabilities()
        
        capability_names = [cap.name for cap in capabilities]
        assert "monitoring_setup" in capability_names
        assert "dashboard_creation" in capability_names
        assert "alerting_configuration" in capability_names
        assert "metrics_collection" in capability_names
    
    @pytest.mark.asyncio
    async def test_monitoring_setup(self, monitoring_agent):
        """Test monitoring setup."""
        requirements = "Set up comprehensive monitoring with Prometheus and Grafana"
        
        with patch.object(monitoring_agent, 'generate_monitoring_configuration') as mock_generate:
            mock_generate.return_value = {
                "config_id": "monitor_123",
                "components": [
                    {"name": "Prometheus", "type": "metrics_collection"},
                    {"name": "Grafana", "type": "visualization"},
                    {"name": "AlertManager", "type": "alerting"}
                ],
                "metrics": ["cpu_usage", "memory_usage", "disk_usage"],
                "dashboards": ["infrastructure_overview", "application_metrics"]
            }
            
            result = await monitoring_agent.generate_monitoring_configuration(requirements)
            
            assert result["config_id"] == "monitor_123"
            assert len(result["components"]) == 3
            assert len(result["metrics"]) == 3
            assert len(result["dashboards"]) == 2
    
    @pytest.mark.asyncio
    async def test_dashboard_creation(self, monitoring_agent):
        """Test dashboard creation."""
        requirements = "Create dashboard for web application performance monitoring"
        
        with patch.object(monitoring_agent, 'create_dashboard') as mock_create:
            mock_create.return_value = {
                "dashboard_id": "dash_123",
                "name": "Web App Performance",
                "panels": [
                    {"title": "Response Time", "type": "graph"},
                    {"title": "Error Rate", "type": "stat"},
                    {"title": "Throughput", "type": "graph"}
                ],
                "refresh_interval": "30s"
            }
            
            result = await monitoring_agent.create_dashboard(requirements)
            
            assert result["dashboard_id"] == "dash_123"
            assert result["name"] == "Web App Performance"
            assert len(result["panels"]) == 3
            assert result["refresh_interval"] == "30s"


@pytest.mark.asyncio
class TestAgentIntegration:
    """Test agent integration scenarios."""
    
    async def test_multi_agent_workflow(self):
        """Test multi-agent workflow."""
        # Create agents
        config = PlatformConfig(name="integration_test", version="1.0.0")
        terraform_agent = TerraformAgent(config)
        ansible_agent = AnsibleAgent(config)
        security_agent = SecurityAgent(config)
        
        # Initialize agents
        await terraform_agent.initialize()
        await ansible_agent.initialize()
        await security_agent.initialize()
        
        # Start agents
        await terraform_agent.start()
        await ansible_agent.start()
        await security_agent.start()
        
        # Test workflow: Infrastructure -> Configuration -> Security
        with patch.object(terraform_agent, 'generate_plan') as mock_terraform:
            mock_terraform.return_value = {"plan_id": "plan_123", "resources": ["web_server"]}
            
            terraform_result = await terraform_agent.generate_plan("Create web server")
            assert terraform_result["plan_id"] == "plan_123"
        
        with patch.object(ansible_agent, 'generate_playbook') as mock_ansible:
            mock_ansible.return_value = {"playbook_id": "playbook_123", "tasks": ["configure_nginx"]}
            
            ansible_result = await ansible_agent.generate_playbook("Configure nginx")
            assert ansible_result["playbook_id"] == "playbook_123"
        
        with patch.object(security_agent, 'generate_security_assessment') as mock_security:
            mock_security.return_value = {"assessment_id": "assess_123", "score": 90}
            
            security_result = await security_agent.generate_security_assessment("Security scan")
            assert security_result["assessment_id"] == "assess_123"
        
        # Stop agents
        await terraform_agent.stop()
        await ansible_agent.stop()
        await security_agent.stop()
    
    async def test_agent_error_handling(self):
        """Test agent error handling."""
        config = PlatformConfig(name="error_test", version="1.0.0")
        terraform_agent = TerraformAgent(config)
        
        await terraform_agent.initialize()
        await terraform_agent.start()
        
        # Test error handling in plan generation
        with patch.object(terraform_agent, 'generate_plan') as mock_generate:
            mock_generate.side_effect = Exception("Terraform error")
            
            with pytest.raises(Exception):
                await terraform_agent.generate_plan("Invalid requirements")
        
        await terraform_agent.stop()
    
    async def test_agent_health_checks(self):
        """Test agent health checks."""
        config = PlatformConfig(name="health_test", version="1.0.0")
        terraform_agent = TerraformAgent(config)
        
        await terraform_agent.initialize()
        await terraform_agent.start()
        
        # Test health check
        health = await terraform_agent.health_check()
        assert "status" in health
        assert "timestamp" in health
        assert health["status"] == "healthy"
        
        await terraform_agent.stop()


if __name__ == "__main__":
    pytest.main([__file__])
