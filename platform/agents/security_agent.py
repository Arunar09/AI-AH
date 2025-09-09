"""
Security & Compliance Agent for the Multi-Agent Infrastructure Intelligence Platform.

This agent specializes in security hardening, compliance management,
vulnerability assessment, and security best practices enforcement.
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import asyncio
import subprocess
import os
import tempfile
from pathlib import Path
import yaml

from ..core.base_platform import BasePlatformComponent, PlatformConfig, Task, Priority, ComponentStatus, AgentCapability
from ..core.agent_framework import IntelligentAgent, AgentResponse, ConversationType, MemoryType
from ..core.nlp.natural_language_processor import ParsedRequest, IntentType, EntityType


@dataclass
class SecurityRule:
    """Represents a security rule or policy."""
    id: str
    name: str
    description: str
    category: str  # network, access, encryption, monitoring, etc.
    severity: str  # low, medium, high, critical
    compliance_framework: str  # CIS, NIST, PCI-DSS, etc.
    implementation: Dict[str, Any]
    remediation: str
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityAssessment:
    """Represents a security assessment."""
    id: str
    name: str
    description: str
    target: str  # infrastructure, application, network, etc.
    rules: List[SecurityRule]
    findings: List[Dict[str, Any]]
    compliance_score: float
    risk_level: str
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Vulnerability:
    """Represents a security vulnerability."""
    id: str
    name: str
    description: str
    severity: str
    cve_id: Optional[str]
    affected_components: List[str]
    remediation: str
    references: List[str]
    discovered_at: datetime = field(default_factory=datetime.now)
    status: str = "open"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceReport:
    """Represents a compliance report."""
    id: str
    framework: str  # CIS, NIST, PCI-DSS, SOC2, etc.
    target: str
    compliance_score: float
    passed_checks: int
    failed_checks: int
    total_checks: int
    recommendations: List[str]
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SecurityAgent(IntelligentAgent):
    """
    Security & Compliance Agent.
    
    Specializes in:
    - Security hardening and best practices
    - Compliance management (CIS, NIST, PCI-DSS, SOC2)
    - Vulnerability assessment and management
    - Security policy enforcement
    - Risk assessment and mitigation
    """
    
    def __init__(self, config: PlatformConfig, workspace_path: str = None):
        super().__init__(config)
        
        self.workspace_path = workspace_path or tempfile.mkdtemp(prefix="security_agent_")
        self.assessments: Dict[str, SecurityAssessment] = {}
        self.vulnerabilities: Dict[str, Vulnerability] = {}
        self.compliance_reports: Dict[str, ComplianceReport] = {}
        self.security_rules: Dict[str, SecurityRule] = {}
        
        # Security-specific capabilities
        self.capabilities = [
            AgentCapability(
                name="security_hardening",
                description="Apply security hardening configurations",
                version="1.0.0",
                parameters={"supported_frameworks": ["CIS", "NIST", "PCI-DSS", "SOC2"]}
            ),
            AgentCapability(
                name="compliance_management",
                description="Manage compliance with security standards",
                version="1.0.0"
            ),
            AgentCapability(
                name="vulnerability_assessment",
                description="Assess and manage security vulnerabilities",
                version="1.0.0"
            ),
            AgentCapability(
                name="risk_assessment",
                description="Assess security risks and provide mitigation strategies",
                version="1.0.0"
            ),
            AgentCapability(
                name="security_monitoring",
                description="Monitor security events and incidents",
                version="1.0.0"
            )
        ]
        
        # Initialize security rules and frameworks
        self._initialize_security_rules()
        self._initialize_compliance_frameworks()
    
    async def _initialize_capabilities(self):
        """Initialize Security-specific capabilities."""
        # Add Security-specific response handlers
        self.add_response_handler("security_harden", self._handle_security_harden)
        self.add_response_handler("compliance_check", self._handle_compliance_check)
        self.add_response_handler("vulnerability_scan", self._handle_vulnerability_scan)
        self.add_response_handler("risk_assess", self._handle_risk_assess)
        
        # Add context processors
        self.add_context_processor(self._process_security_context)
    
    async def _initialize_response_handlers(self):
        """Initialize response handlers for Security operations."""
        pass  # Already handled in _initialize_capabilities
    
    async def _initialize_context_processors(self):
        """Initialize context processors for Security operations."""
        pass  # Already handled in _initialize_capabilities
    
    def _initialize_security_rules(self):
        """Initialize common security rules and policies."""
        self.security_rules = {
            "firewall_default_deny": {
                "id": "firewall_default_deny",
                "name": "Default Deny Firewall Rule",
                "description": "Configure firewall to deny all traffic by default",
                "category": "network",
                "severity": "high",
                "compliance_framework": "CIS",
                "implementation": {
                    "type": "firewall_rule",
                    "action": "deny",
                    "direction": "inbound",
                    "priority": "lowest"
                },
                "remediation": "Configure firewall rules to deny all traffic by default and only allow necessary traffic"
            },
            "encryption_at_rest": {
                "id": "encryption_at_rest",
                "name": "Encryption at Rest",
                "description": "Enable encryption for data at rest",
                "category": "encryption",
                "severity": "high",
                "compliance_framework": "NIST",
                "implementation": {
                    "type": "encryption",
                    "algorithm": "AES-256",
                    "scope": "all_data"
                },
                "remediation": "Enable encryption for all data storage including databases, file systems, and backups"
            },
            "access_control": {
                "id": "access_control",
                "name": "Access Control",
                "description": "Implement proper access controls and authentication",
                "category": "access",
                "severity": "critical",
                "compliance_framework": "CIS",
                "implementation": {
                    "type": "access_control",
                    "authentication": "multi_factor",
                    "authorization": "role_based"
                },
                "remediation": "Implement multi-factor authentication and role-based access control"
            },
            "audit_logging": {
                "id": "audit_logging",
                "name": "Audit Logging",
                "description": "Enable comprehensive audit logging",
                "category": "monitoring",
                "severity": "medium",
                "compliance_framework": "SOC2",
                "implementation": {
                    "type": "logging",
                    "events": ["authentication", "authorization", "data_access", "configuration_changes"],
                    "retention": "90_days"
                },
                "remediation": "Enable audit logging for all security-relevant events with appropriate retention"
            },
            "ssl_tls_configuration": {
                "id": "ssl_tls_configuration",
                "name": "SSL/TLS Configuration",
                "description": "Configure secure SSL/TLS settings",
                "category": "encryption",
                "severity": "high",
                "compliance_framework": "PCI-DSS",
                "implementation": {
                    "type": "ssl_tls",
                    "protocols": ["TLS1.2", "TLS1.3"],
                    "ciphers": "strong_only"
                },
                "remediation": "Configure SSL/TLS to use only secure protocols and strong cipher suites"
            },
            "regular_updates": {
                "id": "regular_updates",
                "name": "Regular Security Updates",
                "description": "Implement regular security updates and patch management",
                "category": "maintenance",
                "severity": "high",
                "compliance_framework": "CIS",
                "implementation": {
                    "type": "patch_management",
                    "frequency": "monthly",
                    "critical_patches": "immediate"
                },
                "remediation": "Implement automated patch management with regular security updates"
            }
        }
    
    def _initialize_compliance_frameworks(self):
        """Initialize compliance frameworks and their requirements."""
        self.compliance_frameworks = {
            "CIS": {
                "name": "Center for Internet Security",
                "description": "CIS Controls and Benchmarks",
                "categories": ["basic", "foundational", "organizational"],
                "requirements": [
                    "inventory_and_control_of_enterprise_assets",
                    "inventory_and_control_of_software_assets",
                    "data_protection",
                    "secure_configuration_of_enterprise_assets",
                    "account_management",
                    "access_control_management",
                    "continuous_vulnerability_management",
                    "audit_log_management",
                    "email_and_web_browser_protections",
                    "malware_defenses"
                ]
            },
            "NIST": {
                "name": "National Institute of Standards and Technology",
                "description": "NIST Cybersecurity Framework",
                "categories": ["identify", "protect", "detect", "respond", "recover"],
                "requirements": [
                    "asset_management",
                    "business_environment",
                    "governance",
                    "risk_assessment",
                    "risk_management_strategy",
                    "access_control",
                    "awareness_and_training",
                    "data_security",
                    "information_protection_processes",
                    "maintenance",
                    "protective_technology"
                ]
            },
            "PCI-DSS": {
                "name": "Payment Card Industry Data Security Standard",
                "description": "PCI DSS Requirements",
                "categories": ["build_and_maintain", "protect_cardholder_data", "maintain_vulnerability_management"],
                "requirements": [
                    "install_and_maintain_firewall",
                    "do_not_use_vendor_defaults",
                    "protect_stored_cardholder_data",
                    "encrypt_transmission_of_cardholder_data",
                    "use_and_regularly_update_antivirus",
                    "develop_and_maintain_secure_systems",
                    "restrict_access_by_business_need_to_know",
                    "assign_unique_id_to_each_person",
                    "restrict_physical_access_to_cardholder_data",
                    "track_and_monitor_access",
                    "regularly_test_security_systems",
                    "maintain_policy"
                ]
            },
            "SOC2": {
                "name": "Service Organization Control 2",
                "description": "SOC 2 Trust Services Criteria",
                "categories": ["security", "availability", "processing_integrity", "confidentiality", "privacy"],
                "requirements": [
                    "control_environment",
                    "communication_and_information",
                    "risk_assessment",
                    "monitoring_activities",
                    "control_activities",
                    "logical_and_physical_access_controls",
                    "system_operations",
                    "change_management",
                    "risk_mitigation"
                ]
            }
        }
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> AgentResponse:
        """Process a Security-related request."""
        try:
            # Parse the request
            parsed_request = await self._parse_security_request(request)
            
            # Generate response based on intent
            if "security" in parsed_request.original_text.lower() and "harden" in parsed_request.original_text.lower():
                return await self._handle_security_harden(parsed_request, context)
            elif "compliance" in parsed_request.original_text.lower():
                return await self._handle_compliance_check(parsed_request, context)
            elif "vulnerability" in parsed_request.original_text.lower() or "scan" in parsed_request.original_text.lower():
                return await self._handle_vulnerability_scan(parsed_request, context)
            elif "risk" in parsed_request.original_text.lower():
                return await self._handle_risk_assess(parsed_request, context)
            else:
                return AgentResponse(
                    agent_id=self.config.name,
                    response_type="text",
                    content="I can help you with security hardening, compliance management, vulnerability assessment, and risk management. What would you like to do?",
                    confidence=0.8
                )
                
        except Exception as e:
            self.logger.error(f"Error processing Security request: {str(e)}")
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content=f"I encountered an error: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze security requirements."""
        try:
            # Parse requirements
            parsed_request = await self._parse_security_request(requirements)
            
            analysis = {
                "intent": parsed_request.intent.type.value,
                "confidence": parsed_request.confidence,
                "entities": [
                    {
                        "type": entity.type.value,
                        "value": entity.value,
                        "confidence": entity.confidence
                    }
                    for entity in parsed_request.entities
                ],
                "security_rules": [],
                "compliance_frameworks": [],
                "risk_level": "medium",
                "recommendations": []
            }
            
            # Extract security requirements
            for entity in parsed_request.entities:
                if entity.type == EntityType.SECURITY:
                    if "firewall" in entity.value.lower():
                        analysis["security_rules"].append("firewall_default_deny")
                    elif "encryption" in entity.value.lower():
                        analysis["security_rules"].append("encryption_at_rest")
                    elif "access" in entity.value.lower():
                        analysis["security_rules"].append("access_control")
                    elif "logging" in entity.value.lower():
                        analysis["security_rules"].append("audit_logging")
                    elif "ssl" in entity.value.lower() or "tls" in entity.value.lower():
                        analysis["security_rules"].append("ssl_tls_configuration")
                    elif "update" in entity.value.lower() or "patch" in entity.value.lower():
                        analysis["security_rules"].append("regular_updates")
            
            # Extract compliance frameworks
            for entity in parsed_request.entities:
                if entity.value.lower() in ["cis", "nist", "pci-dss", "soc2"]:
                    analysis["compliance_frameworks"].append(entity.value.upper())
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_security_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing security requirements: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def generate_security_assessment(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a security assessment."""
        try:
            assessment_id = f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create security assessment
            assessment = SecurityAssessment(
                id=assessment_id,
                name=analysis.get("name", f"Security Assessment {assessment_id}"),
                description=analysis.get("description", "Generated security assessment"),
                target=analysis.get("target", "infrastructure"),
                rules=[],
                findings=[],
                compliance_score=0.0,
                risk_level=analysis.get("risk_level", "medium")
            )
            
            # Add security rules based on analysis
            for rule_id in analysis.get("security_rules", []):
                if rule_id in self.security_rules:
                    rule_data = self.security_rules[rule_id]
                    rule = SecurityRule(
                        id=rule_data["id"],
                        name=rule_data["name"],
                        description=rule_data["description"],
                        category=rule_data["category"],
                        severity=rule_data["severity"],
                        compliance_framework=rule_data["compliance_framework"],
                        implementation=rule_data["implementation"],
                        remediation=rule_data["remediation"]
                    )
                    assessment.rules.append(rule)
            
            # Store assessment
            self.assessments[assessment_id] = assessment
            
            # Generate security configuration files
            await self._generate_security_configurations(assessment)
            
            return {
                "assessment_id": assessment_id,
                "status": "created",
                "rules": len(assessment.rules),
                "compliance_frameworks": analysis.get("compliance_frameworks", []),
                "risk_level": assessment.risk_level,
                "files_generated": True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating security assessment: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def execute_security_assessment(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a security assessment."""
        try:
            assessment_id = assessment.get("assessment_id")
            if not assessment_id or assessment_id not in self.assessments:
                return {"error": "Assessment not found", "status": "failed"}
            
            security_assessment = self.assessments[assessment_id]
            
            # Perform security checks
            findings = await self._perform_security_checks(security_assessment)
            
            # Calculate compliance score
            compliance_score = self._calculate_compliance_score(findings)
            
            # Update assessment
            security_assessment.findings = findings
            security_assessment.compliance_score = compliance_score
            security_assessment.status = "completed"
            
            # Generate compliance report
            compliance_report = await self._generate_compliance_report(security_assessment)
            
            return {
                "assessment_id": assessment_id,
                "status": "completed",
                "compliance_score": compliance_score,
                "findings_count": len(findings),
                "compliance_report_id": compliance_report["report_id"]
            }
            
        except Exception as e:
            self.logger.error(f"Error executing security assessment: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def _parse_security_request(self, request: str) -> ParsedRequest:
        """Parse a Security-specific request."""
        # This would integrate with the NLP processor
        # For now, we'll do basic parsing
        request_lower = request.lower()
        
        # Simple intent detection
        if any(word in request_lower for word in ["harden", "secure", "protect"]):
            intent_type = IntentType.CREATE_INFRASTRUCTURE
        elif any(word in request_lower for word in ["check", "assess", "audit"]):
            intent_type = IntentType.MONITOR_INFRASTRUCTURE
        else:
            intent_type = IntentType.UNKNOWN
        
        # Simple entity extraction
        entities = []
        if "firewall" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "firewall"})
        if "encryption" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "encryption"})
        if "access" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "access"})
        if "logging" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "logging"})
        if "ssl" in request_lower or "tls" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "ssl_tls"})
        if "cis" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "cis"})
        if "nist" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "nist"})
        if "pci" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "pci-dss"})
        if "soc" in request_lower:
            entities.append({"type": EntityType.SECURITY, "value": "soc2"})
        
        return ParsedRequest(
            original_text=request,
            intent={"type": intent_type, "confidence": 0.8},
            entities=entities,
            confidence=0.8
        )
    
    async def _handle_security_harden(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle security hardening requests."""
        # Analyze requirements
        analysis = await self.analyze_requirements(parsed_request.original_text)
        
        # Generate security assessment
        assessment = await self.generate_security_assessment(analysis)
        
        if assessment.get("status") == "created":
            return AgentResponse(
                agent_id=self.config.name,
                response_type="security_assessment",
                content=f"I've created a security assessment with {assessment['rules']} security rules. Risk level: {assessment['risk_level']}.",
                confidence=0.9,
                suggestions=[
                    "Review the security configuration files",
                    "Execute the assessment to check compliance",
                    "Apply security hardening recommendations"
                ],
                next_actions=[
                    "security_assessment_review",
                    "security_assessment_execute",
                    "security_hardening_apply"
                ],
                metadata={"assessment_id": assessment["assessment_id"], "analysis": analysis}
            )
        else:
            return AgentResponse(
                agent_id=self.config.name,
                response_type="error",
                content="I encountered an error creating the security assessment.",
                confidence=0.0,
                metadata={"error": assessment.get("error")}
            )
    
    async def _handle_compliance_check(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle compliance check requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you check compliance with security standards. Let me analyze your infrastructure against compliance frameworks.",
            confidence=0.8,
            suggestions=["Select compliance framework", "Run compliance assessment", "Generate compliance report"]
        )
    
    async def _handle_vulnerability_scan(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle vulnerability scan requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you scan for vulnerabilities. Let me perform a comprehensive vulnerability assessment.",
            confidence=0.8,
            suggestions=["Run vulnerability scan", "Analyze scan results", "Prioritize remediation"]
        )
    
    async def _handle_risk_assess(self, parsed_request: ParsedRequest, context: Dict[str, Any] = None) -> AgentResponse:
        """Handle risk assessment requests."""
        return AgentResponse(
            agent_id=self.config.name,
            response_type="text",
            content="I'll help you assess security risks. Let me analyze your infrastructure and identify potential risks.",
            confidence=0.8,
            suggestions=["Identify security risks", "Calculate risk scores", "Generate risk mitigation plan"]
        )
    
    async def _process_security_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process context for Security operations."""
        processed_context = context.copy()
        
        # Add Security-specific context
        processed_context["security_workspace"] = self.workspace_path
        processed_context["available_assessments"] = list(self.assessments.keys())
        processed_context["available_vulnerabilities"] = list(self.vulnerabilities.keys())
        processed_context["available_compliance_reports"] = list(self.compliance_reports.keys())
        
        return processed_context
    
    async def _generate_security_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on analysis."""
        recommendations = []
        
        # Security rule recommendations
        if "firewall_default_deny" in analysis["security_rules"]:
            recommendations.append("Configure firewall with default deny policy")
            recommendations.append("Implement network segmentation")
        
        if "encryption_at_rest" in analysis["security_rules"]:
            recommendations.append("Enable encryption for all data storage")
            recommendations.append("Implement key management system")
        
        if "access_control" in analysis["security_rules"]:
            recommendations.append("Implement multi-factor authentication")
            recommendations.append("Configure role-based access control")
        
        # Compliance framework recommendations
        for framework in analysis["compliance_frameworks"]:
            if framework == "CIS":
                recommendations.append("Follow CIS Controls and Benchmarks")
                recommendations.append("Implement continuous vulnerability management")
            elif framework == "NIST":
                recommendations.append("Follow NIST Cybersecurity Framework")
                recommendations.append("Implement risk management processes")
            elif framework == "PCI-DSS":
                recommendations.append("Follow PCI DSS requirements")
                recommendations.append("Implement cardholder data protection")
            elif framework == "SOC2":
                recommendations.append("Follow SOC 2 Trust Services Criteria")
                recommendations.append("Implement security monitoring")
        
        return recommendations
    
    async def _generate_security_configurations(self, assessment: SecurityAssessment):
        """Generate security configuration files."""
        assessment_dir = Path(self.workspace_path) / assessment.id
        assessment_dir.mkdir(exist_ok=True)
        
        # Generate security rules configuration
        rules_config = {
            "assessment_id": assessment.id,
            "name": assessment.name,
            "description": assessment.description,
            "target": assessment.target,
            "risk_level": assessment.risk_level,
            "rules": []
        }
        
        for rule in assessment.rules:
            rules_config["rules"].append({
                "id": rule.id,
                "name": rule.name,
                "description": rule.description,
                "category": rule.category,
                "severity": rule.severity,
                "compliance_framework": rule.compliance_framework,
                "implementation": rule.implementation,
                "remediation": rule.remediation
            })
        
        with open(assessment_dir / "security_rules.json", "w") as f:
            json.dump(rules_config, f, indent=2)
        
        # Generate Terraform security configurations
        terraform_config = self._generate_terraform_security_config(assessment)
        with open(assessment_dir / "security.tf", "w") as f:
            f.write(terraform_config)
        
        # Generate Ansible security playbook
        ansible_playbook = self._generate_ansible_security_playbook(assessment)
        with open(assessment_dir / "security_hardening.yml", "w") as f:
            f.write(ansible_playbook)
    
    def _generate_terraform_security_config(self, assessment: SecurityAssessment) -> str:
        """Generate Terraform security configuration."""
        content = "# Security configuration generated by AI-AH Security Agent\n\n"
        
        for rule in assessment.rules:
            if rule.category == "network":
                content += f'# {rule.name}\n'
                content += f'resource "aws_security_group" "{rule.id}" {{\n'
                content += f'  name        = "{rule.id}"\n'
                content += f'  description = "{rule.description}"\n'
                content += f'  vpc_id      = var.vpc_id\n\n'
                content += f'  # Default deny all inbound traffic\n'
                content += f'  ingress {{\n'
                content += f'    from_port   = 0\n'
                content += f'    to_port     = 0\n'
                content += f'    protocol    = "-1"\n'
                content += f'    cidr_blocks = ["0.0.0.0/0"]\n'
                content += f'    self        = true\n'
                content += f'  }}\n\n'
                content += f'  egress {{\n'
                content += f'    from_port   = 0\n'
                content += f'    to_port     = 0\n'
                content += f'    protocol    = "-1"\n'
                content += f'    cidr_blocks = ["0.0.0.0/0"]\n'
                content += f'  }}\n\n'
                content += f'  tags = {{\n'
                content += f'    Name        = "{rule.id}"\n'
                content += f'    Environment = var.environment\n'
                content += f'    Security    = "true"\n'
                content += f'  }}\n'
                content += f'}}\n\n'
        
        return content
    
    def _generate_ansible_security_playbook(self, assessment: SecurityAssessment) -> str:
        """Generate Ansible security hardening playbook."""
        content = "---\n# Security hardening playbook generated by AI-AH Security Agent\n\n"
        content += f"- name: {assessment.name}\n"
        content += f"  hosts: all\n"
        content += f"  become: yes\n"
        content += f"  vars:\n"
        content += f"    security_level: {assessment.risk_level}\n\n"
        content += f"  tasks:\n"
        
        for rule in assessment.rules:
            if rule.category == "access":
                content += f"    - name: {rule.name}\n"
                content += f"      user:\n"
                content += f"        name: admin\n"
                content += f"        state: present\n"
                content += f"        groups: sudo\n"
                content += f"        shell: /bin/bash\n\n"
            
            elif rule.category == "monitoring":
                content += f"    - name: {rule.name}\n"
                content += f"      service:\n"
                content += f"        name: rsyslog\n"
                content += f"        state: started\n"
                content += f"        enabled: yes\n\n"
            
            elif rule.category == "maintenance":
                content += f"    - name: {rule.name}\n"
                content += f"      apt:\n"
                content += f"        update_cache: yes\n"
                content += f"        upgrade: dist\n"
                content += f"        autoremove: yes\n\n"
        
        return content
    
    async def _perform_security_checks(self, assessment: SecurityAssessment) -> List[Dict[str, Any]]:
        """Perform security checks for the assessment."""
        findings = []
        
        for rule in assessment.rules:
            # Simulate security check
            finding = {
                "rule_id": rule.id,
                "rule_name": rule.name,
                "status": "passed" if rule.severity != "critical" else "failed",
                "severity": rule.severity,
                "description": f"Check for {rule.name}",
                "recommendation": rule.remediation,
                "timestamp": datetime.now().isoformat()
            }
            findings.append(finding)
        
        return findings
    
    def _calculate_compliance_score(self, findings: List[Dict[str, Any]]) -> float:
        """Calculate compliance score based on findings."""
        if not findings:
            return 0.0
        
        total_checks = len(findings)
        passed_checks = len([f for f in findings if f["status"] == "passed"])
        
        return (passed_checks / total_checks) * 100.0
    
    async def _generate_compliance_report(self, assessment: SecurityAssessment) -> Dict[str, Any]:
        """Generate a compliance report."""
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        report = ComplianceReport(
            id=report_id,
            framework="CIS",  # Default framework
            target=assessment.target,
            compliance_score=assessment.compliance_score,
            passed_checks=len([f for f in assessment.findings if f["status"] == "passed"]),
            failed_checks=len([f for f in assessment.findings if f["status"] == "failed"]),
            total_checks=len(assessment.findings),
            recommendations=[rule.remediation for rule in assessment.rules]
        )
        
        self.compliance_reports[report_id] = report
        
        return {"report_id": report_id, "status": "generated"}
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.name == "security_harden":
            analysis = await self.analyze_requirements(task.metadata.get("requirements", ""))
            assessment = await self.generate_security_assessment(analysis)
            return assessment
        elif task.name == "execute_assessment":
            return await self.execute_security_assessment(task.metadata)
        elif task.name == "get_status":
            return await self._get_security_status()
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    async def _get_security_status(self) -> Dict[str, Any]:
        """Get current security status."""
        return {
            "assessments_count": len(self.assessments),
            "vulnerabilities_count": len(self.vulnerabilities),
            "compliance_reports_count": len(self.compliance_reports),
            "last_activity": max([a.created_at for a in self.assessments.values()]) if self.assessments else None
        }
