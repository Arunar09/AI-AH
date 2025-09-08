#!/usr/bin/env python3
"""
Intelligent Infrastructure Query Analyzer
========================================

This module provides advanced analysis of infrastructure requests, including:
- Semantic understanding of requirements
- Identification of missing information
- Generation of clarification questions
- Creation of execution plans
- Multi-cloud environment detection
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Supported deployment environments"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ON_PREMISE = "on_premise"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class InfrastructurePattern(Enum):
    """Common infrastructure patterns"""
    SERVERLESS = "serverless"
    MICROSERVICES = "microservices"
    THREE_TIER = "three_tier"
    EVENT_DRIVEN = "event_driven"
    CONTAINER_BASED = "container_based"
    MONOLITHIC = "monolithic"
    UNKNOWN = "unknown"


@dataclass
class InfrastructureRequirement:
    """Individual infrastructure requirement"""
    component: str
    type: str
    purpose: str
    priority: str  # high, medium, low
    estimated_cost: Optional[str] = None


@dataclass
class ClarificationQuestion:
    """Question to gather missing information"""
    question: str
    category: str
    required: bool
    options: Optional[List[str]] = None
    default: Optional[str] = None
    priority: str = "medium" # Added priority field


@dataclass
class InfrastructurePlan:
    """Complete infrastructure execution plan"""
    pattern: InfrastructurePattern
    environment: Environment
    requirements: List[InfrastructureRequirement]
    missing_info: List[ClarificationQuestion]
    estimated_cost: str
    security_recommendations: List[str]
    deployment_recommendations: List[str]
    original_request: str # Added original_request field


class IntelligentQueryAnalyzer:
    """
    Advanced analyzer for infrastructure requests
    """
    
    def __init__(self):
        """Initialize the intelligent analyzer"""
        self.cloud_keywords = {
            'gcp': ['gcp', 'google', 'google cloud', 'cloud functions', 'firestore', 'compute engine', 'cloud sql', 'cloud storage', 'gke', 'cloud run'],
            'aws': ['aws', 'amazon', 'lambda', 'dynamodb', 'ec2', 's3', 'rds', 'vpc', 'api gateway'],
            'azure': ['azure', 'microsoft', 'azure functions', 'cosmos db', 'vm', 'blob storage', 'sql database'],
            'on_premise': ['on-premise', 'on-prem', 'local', 'datacenter', 'private cloud'],
            'hybrid': ['hybrid', 'multi-cloud', 'cross-platform', 'mixed', 'all three cloud', 'three cloud', 'aws azure gcp', 'multi provider', 'cross cloud']
        }
        
        self.pattern_keywords = {
            InfrastructurePattern.SERVERLESS: ['serverless', 'lambda', 'functions', 'faas', 'stateless', 'cloud functions', 'cloud run'],
            InfrastructurePattern.MICROSERVICES: ['microservices', 'micro-service', 'distributed', 'api gateway', 'service mesh'],
            InfrastructurePattern.THREE_TIER: ['three tier', '3-tier', 'web', 'application', 'database', 'tier', 'web application'],
            InfrastructurePattern.EVENT_DRIVEN: ['event driven', 'event-based', 'streaming', 'kafka', 'sns', 'pub/sub'],
            InfrastructurePattern.CONTAINER_BASED: ['container', 'docker', 'kubernetes', 'k8s', 'orchestration', 'cloud run', 'gke', 'aks', 'eks'],
            InfrastructurePattern.MONOLITHIC: ['monolithic', 'monolith', 'single application', 'unified']
        }
        
        self.component_keywords = {
            'compute': ['lambda', 'functions', 'ec2', 'vm', 'compute', 'server', 'instance'],
            'database': ['dynamodb', 'cosmos', 'firestore', 'rds', 'sql', 'nosql', 'database'],
            'storage': ['s3', 'storage', 'blob', 'bucket', 'file storage'],
            'networking': ['vpc', 'subnet', 'gateway', 'load balancer', 'cdn', 'network'],
            'security': ['iam', 'security group', 'firewall', 'encryption', 'certificate'],
            'monitoring': ['cloudwatch', 'monitoring', 'logging', 'metrics', 'alerts']
        }
    
    def analyze_infrastructure_request(self, query: str, preferences: Dict[str, Any] = None) -> InfrastructurePlan:
        """Analyze an infrastructure request and create a comprehensive plan"""
        if preferences is None:
            preferences = {}
        
        # Detect infrastructure pattern
        pattern = self._detect_pattern(query)
        
        # Detect target environment
        environment = self._detect_environment(query, preferences)
        
        # Extract basic requirements
        requirements = self._extract_requirements(query, pattern, environment)
        
        # Generate detailed, technical questions
        missing_info = self._generate_detailed_questions(pattern)
        
        # Estimate costs based on pattern and requirements
        estimated_cost = self._estimate_cost(pattern, requirements)
        
        # Generate security and compliance recommendations
        security_recommendations = self._generate_security_recommendations(pattern, requirements)
        
        # Generate deployment recommendations
        deployment_recommendations = self._generate_deployment_recommendations(pattern, requirements)
        
        # Create the infrastructure plan
        plan = InfrastructurePlan(
            pattern=pattern,
            environment=environment,
            requirements=requirements,
            missing_info=missing_info,
            estimated_cost=estimated_cost,
            security_recommendations=security_recommendations,
            deployment_recommendations=deployment_recommendations,
            original_request=query # Store original request for intelligent analysis
        )
        
        return plan
    
    def update_plan_based_on_user_input(self, current_plan: InfrastructurePlan, user_input: str) -> InfrastructurePlan:
        """Dynamically update the infrastructure plan based on user input - making it truly intelligent"""
        updated_plan = current_plan
        environment_changed = False
        
        # Parse user input for environment changes
        if any(keyword in user_input.lower() for keyword in ['all three cloud', 'multi-cloud', 'aws azure gcp', 'three cloud', 'hybrid cloud', 'multi provider']):
            updated_plan.environment = Environment.HYBRID
            environment_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User requested multi-cloud, updating environment to HYBRID")
        
        # Parse user input for pattern changes
        pattern_changed = False
        if any(keyword in user_input.lower() for keyword in ['change to', 'switch to', 'instead of', 'rather than', 'i want', 'i need', 'make it']):
            if 'serverless' in user_input.lower():
                updated_plan.pattern = InfrastructurePattern.SERVERLESS
                pattern_changed = True
                print(f"🔍 INTELLIGENT UPDATE: User requested serverless pattern")
            elif 'microservices' in user_input.lower():
                updated_plan.pattern = InfrastructurePattern.MICROSERVICES
                pattern_changed = True
                print(f"🔍 INTELLIGENT UPDATE: User requested microservices pattern")
            elif 'three tier' in user_input.lower() or '3 tier' in user_input.lower():
                updated_plan.pattern = InfrastructurePattern.THREE_TIER
                pattern_changed = True
                print(f"🔍 INTELLIGENT UPDATE: User requested three-tier pattern")
            elif 'container' in user_input.lower() or 'docker' in user_input.lower() or 'kubernetes' in user_input.lower():
                updated_plan.pattern = InfrastructurePattern.CONTAINER_BASED
                pattern_changed = True
                print(f"🔍 INTELLIGENT UPDATE: User requested container-based pattern")
        
        # Regenerate requirements if environment or pattern changed
        if environment_changed or pattern_changed:
            print(f"🔍 INTELLIGENT UPDATE: Regenerating requirements due to environment/pattern change")
            updated_plan.requirements = self._extract_requirements(user_input, updated_plan.pattern, updated_plan.environment)
        
        # Parse user input for cost constraints
        if any(keyword in user_input.lower() for keyword in ['budget', 'cost', 'expensive', 'cheap', 'affordable', 'money', 'price', 'expensive', 'low cost']):
            if any(keyword in user_input.lower() for keyword in ['low', 'cheap', 'affordable', 'budget', 'minimal', 'cost effective']):
                updated_plan.estimated_cost = "$50-150/month (budget-optimized)"
                print(f"🔍 INTELLIGENT UPDATE: User requested budget optimization")
            elif any(keyword in user_input.lower() for keyword in ['high', 'expensive', 'premium', 'enterprise', 'unlimited', 'best']):
                updated_plan.estimated_cost = "$500-2000/month (enterprise-grade)"
                print(f"🔍 INTELLIGENT UPDATE: User requested enterprise-grade configuration")
        
        # Parse user input for security requirements
        if any(keyword in user_input.lower() for keyword in ['security', 'compliance', 'hipaa', 'soc2', 'pci', 'secure', 'encryption', 'audit', 'governance']):
            if any(keyword in user_input.lower() for keyword in ['hipaa', 'soc2', 'pci', 'compliance', 'regulated', 'audit']):
                updated_plan.security_recommendations = self._generate_compliance_security_recommendations(updated_plan.pattern)
                print(f"🔍 INTELLIGENT UPDATE: User requested compliance-focused security")
            elif any(keyword in user_input.lower() for keyword in ['high security', 'military grade', 'banking', 'financial', 'government']):
                updated_plan.security_recommendations = self._generate_enterprise_security_recommendations(updated_plan.pattern)
                print(f"🔍 INTELLIGENT UPDATE: User requested enterprise-grade security")
        
        # Parse user input for performance requirements
        if any(keyword in user_input.lower() for keyword in ['performance', 'fast', 'slow', 'response time', 'latency', 'throughput', 'scalability', 'auto-scaling']):
            if any(keyword in user_input.lower() for keyword in ['fast', 'high performance', 'low latency', 'milliseconds', 'real-time']):
                updated_plan.estimated_cost = "$200-800/month (performance-optimized)"
                print(f"🔍 INTELLIGENT UPDATE: User requested performance optimization")
            elif any(keyword in user_input.lower() for keyword in ['auto-scaling', 'elastic', 'dynamic', 'flexible']):
                print(f"🔍 INTELLIGENT UPDATE: User requested auto-scaling capabilities")
        
        # Parse user input for region/availability requirements
        if any(keyword in user_input.lower() for keyword in ['region', 'global', 'worldwide', 'multi-region', 'disaster recovery', 'backup', 'redundancy']):
            if any(keyword in user_input.lower() for keyword in ['global', 'worldwide', 'multi-region', 'everywhere']):
                updated_plan.estimated_cost = "$300-1200/month (global-distribution)"
                print(f"🔍 INTELLIGENT UPDATE: User requested global distribution")
            elif any(keyword in user_input.lower() for keyword in ['disaster recovery', 'backup', 'redundancy', 'high availability']):
                print(f"🔍 INTELLIGENT UPDATE: User requested disaster recovery capabilities")
        
        # Parse user input for specific cloud preferences
        if 'aws' in user_input.lower() and 'azure' not in user_input.lower() and 'gcp' not in user_input.lower():
            updated_plan.environment = Environment.AWS
            environment_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested AWS-only")
        elif 'azure' in user_input.lower() and 'aws' not in user_input.lower() and 'gcp' not in user_input.lower():
            updated_plan.environment = Environment.AZURE
            environment_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested Azure-only")
        elif 'gcp' in user_input.lower() and 'aws' not in user_input.lower() and 'azure' not in user_input.lower():
            updated_plan.environment = Environment.GCP
            environment_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested GCP-only")
        
        # Regenerate requirements if environment changed due to specific cloud preference
        if environment_changed:
            print(f"🔍 INTELLIGENT UPDATE: Regenerating requirements due to specific cloud preference")
            updated_plan.requirements = self._extract_requirements(user_input, updated_plan.pattern, updated_plan.environment)
        
        # Parse user input for specific service requirements
        if any(keyword in user_input.lower() for keyword in ['lambda', 'function', 'serverless function']):
            updated_plan.pattern = InfrastructurePattern.SERVERLESS
            pattern_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested Lambda/serverless functions")
        elif any(keyword in user_input.lower() for keyword in ['ecs', 'eks', 'kubernetes', 'container orchestration']):
            updated_plan.pattern = InfrastructurePattern.CONTAINER_BASED
            pattern_changed = True
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested container orchestration")
        elif any(keyword in user_input.lower() for keyword in ['rds', 'database', 'sql', 'postgres', 'mysql']):
            print(f"🔍 INTELLIGENT UPDATE: User specifically requested database services")
        
        # Final requirements regeneration if pattern changed
        if pattern_changed:
            print(f"🔍 INTELLIGENT UPDATE: Regenerating requirements due to pattern change")
            updated_plan.requirements = self._extract_requirements(user_input, updated_plan.pattern, updated_plan.environment)
        
        return updated_plan
    
    def _generate_compliance_security_recommendations(self, pattern: InfrastructurePattern) -> List[str]:
        """Generate compliance-focused security recommendations"""
        base_recommendations = [
            "🔒 **Compliance & Security Framework**",
            "   • Implement SOC2 Type II controls",
            "   • Enable HIPAA compliance features",
            "   • Configure PCI-DSS security measures",
            "   • Regular security audits and penetration testing",
            "   • Automated compliance monitoring and reporting"
        ]
        
        if pattern == InfrastructurePattern.SERVERLESS:
            base_recommendations.extend([
                "🔒 **Serverless Compliance**",
                "   • Lambda environment variable encryption",
                "   • API Gateway WAF integration",
                "   • CloudTrail for all API calls",
                "   • VPC isolation for sensitive functions"
            ])
        elif pattern == InfrastructurePattern.MICROSERVICES:
            base_recommendations.extend([
                "🔒 **Microservices Compliance**",
                "   • Service-to-service authentication",
                "   • Network policies and security groups",
                "   • Container security scanning",
                "   • Secrets management integration"
            ])
        
        return base_recommendations
    
    def _generate_enterprise_security_recommendations(self, pattern: InfrastructurePattern) -> List[str]:
        """Generate enterprise-grade security recommendations"""
        base_recommendations = [
            "🔒 **Enterprise-Grade Security**",
            "   • Military-grade encryption for all data",
            "   • Zero-trust architecture across all services",
            "   • Advanced threat detection and prevention",
            "   • Redundant infrastructure across multiple regions",
            "   • 24/7 security operations center"
        ]
        
        if pattern == InfrastructurePattern.SERVERLESS:
            base_recommendations.extend([
                "🔒 **Serverless Enterprise Security**",
                "   • Advanced IAM role management",
                "   • VPC endpoint security",
                "   • API Gateway WAF with OWASP rules",
                "   • CloudTrail with advanced filtering"
            ])
        elif pattern == InfrastructurePattern.MICROSERVICES:
            base_recommendations.extend([
                "🔒 **Microservices Enterprise Security**",
                "   • Advanced service-to-service authentication",
                "   • Network policies and security groups",
                "   • Container scanning and vulnerability management",
                "   • Advanced secrets management"
            ])
        
        return base_recommendations
    
    def _detect_pattern(self, query: str) -> InfrastructurePattern:
        """Detect the infrastructure pattern from the query"""
        for pattern, keywords in self.pattern_keywords.items():
            if any(keyword in query for keyword in keywords):
                return pattern
        return InfrastructurePattern.UNKNOWN
    
    def _detect_environment(self, query: str, context: Dict[str, Any] = None) -> Environment:
        """Detect the target environment from the query and context"""
        query_lower = query.lower()
        
        # First, check for multi-cloud/hybrid requests (highest priority)
        hybrid_keywords = ['all three cloud', 'three cloud', 'aws azure gcp', 'multi provider', 'cross cloud', 'multi-cloud']
        if any(keyword in query_lower for keyword in hybrid_keywords):
            return Environment.HYBRID
        
        # Check for explicit cloud provider keywords
        for provider, keywords in self.cloud_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if provider == 'aws':
                        return Environment.AWS
                    elif provider == 'azure':
                        return Environment.AZURE
                    elif provider == 'gcp':
                        return Environment.GCP
                    elif provider == 'on_premise':
                        return Environment.ON_PREMISE
                    elif provider == 'hybrid':
                        return Environment.HYBRID
        
        # Check context for previous environment preferences
        if context and 'preferred_environment' in context:
            preferred = context['preferred_environment']
            if isinstance(preferred, str):
                if preferred.lower() == 'aws':
                    return Environment.AWS
                elif preferred.lower() == 'azure':
                    return Environment.AZURE
                elif preferred.lower() == 'gcp':
                    return Environment.GCP
                elif preferred.lower() in ['on-premise', 'on_premise']:
                    return Environment.ON_PREMISE
                elif preferred.lower() == 'hybrid':
                    return Environment.HYBRID
        
        return Environment.AWS  # Default to AWS
    
    def _extract_requirements(self, query: str, pattern: InfrastructurePattern = None, environment: Environment = None) -> List[InfrastructureRequirement]:
        """Extract infrastructure requirements from the query and pattern"""
        requirements = []
        
        # Pattern-specific requirements (cloud-agnostic initially)
        if pattern == InfrastructurePattern.SERVERLESS:
            requirements.extend([
                InfrastructureRequirement(
                    component="Compute",
                    type="Serverless Functions",
                    purpose="Serverless application logic execution",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Database",
                    type="NoSQL Database",
                    purpose="NoSQL data storage and retrieval",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="API Gateway",
                    type="REST API Endpoints",
                    purpose="HTTP request routing and management",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Security",
                    type="IAM/Identity Management",
                    purpose="Access control and permissions",
                    priority="high"
                )
            ])
        
        elif pattern == InfrastructurePattern.MICROSERVICES:
            requirements.extend([
                InfrastructureRequirement(
                    component="Compute",
                    type="Container Orchestration",
                    purpose="Containerized service deployment",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Load Balancer",
                    type="Application Load Balancer",
                    purpose="Traffic distribution across services",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Database",
                    type="Managed Database",
                    purpose="Relational data persistence",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Service Discovery",
                    type="Service Discovery",
                    purpose="Service-to-service communication",
                    priority="medium"
                )
            ])
        
        elif pattern == InfrastructurePattern.THREE_TIER:
            requirements.extend([
                InfrastructureRequirement(
                    component="Web Tier",
                    type="Load Balancer + Web Servers",
                    purpose="User interface and request handling",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Application Tier",
                    type="Application Servers",
                    purpose="Business logic and processing",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Database Tier",
                    type="Managed Database",
                    purpose="Data persistence and storage",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Security",
                    type="Network Security Groups",
                    purpose="Network-level security controls",
                    priority="high"
                )
            ])
        
        elif pattern == InfrastructurePattern.CONTAINER_BASED:
            requirements.extend([
                InfrastructureRequirement(
                    component="Compute",
                    type="Container Orchestration",
                    purpose="Containerized application deployment",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Load Balancer",
                    type="Application Load Balancer",
                    purpose="Traffic distribution across containers",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Database",
                    type="Managed Database",
                    purpose="Data persistence and storage",
                    priority="high"
                ),
                InfrastructureRequirement(
                    component="Security",
                    type="Container Security",
                    purpose="Container-level security controls",
                    priority="high"
                )
            ])
        
        # Now map requirements to specific cloud services based on environment
        if environment:
            requirements = self._map_requirements_to_cloud(requirements, environment)
        
        return requirements
    
    def _map_requirements_to_cloud(self, requirements: List[InfrastructureRequirement], environment: Environment) -> List[InfrastructureRequirement]:
        """Map generic requirements to specific cloud provider services"""
        cloud_mappings = {
            Environment.AWS: {
                "Serverless Functions": "AWS Lambda Functions",
                "NoSQL Database": "DynamoDB Tables",
                "REST API Endpoints": "API Gateway",
                "IAM/Identity Management": "IAM Roles and Policies",
                "Container Orchestration": "ECS/EKS",
                "Application Load Balancer": "Application Load Balancer",
                "Managed Database": "RDS",
                "Service Discovery": "Route 53",
                "Web Servers": "EC2 Instances",
                "Application Servers": "EC2 Instances",
                "Network Security Groups": "Security Groups",
                "Persistent Storage": "EBS Volumes",
                "Container Monitoring": "CloudWatch"
            },
            Environment.AZURE: {
                "Serverless Functions": "Azure Functions",
                "NoSQL Database": "Cosmos DB",
                "REST API Endpoints": "API Management",
                "IAM/Identity Management": "Azure AD",
                "Container Orchestration": "AKS",
                "Application Load Balancer": "Azure Load Balancer",
                "Managed Database": "Azure SQL Database",
                "Service Discovery": "Azure Service Bus",
                "Web Servers": "Azure VMs",
                "Application Servers": "Azure VMs",
                "Network Security Groups": "Network Security Groups",
                "Persistent Storage": "Azure Disks",
                "Container Monitoring": "Azure Monitor"
            },
            Environment.GCP: {
                "Serverless Functions": "Cloud Functions",
                "NoSQL Database": "Firestore",
                "REST API Endpoints": "Cloud Endpoints",
                "IAM/Identity Management": "Cloud IAM",
                "Container Orchestration": "GKE",
                "Application Load Balancer": "Cloud Load Balancing",
                "Managed Database": "Cloud SQL",
                "Service Discovery": "Cloud DNS",
                "Web Servers": "Compute Engine VMs",
                "Application Servers": "Compute Engine VMs",
                "Network Security Groups": "Firewall Rules",
                "Persistent Storage": "Persistent Disks",
                "Container Monitoring": "Cloud Monitoring"
            },
            Environment.HYBRID: {
                "Serverless Functions": "Multi-cloud Functions (AWS Lambda + Azure Functions + Cloud Functions)",
                "NoSQL Database": "Multi-cloud Database (DynamoDB + Cosmos DB + Firestore)",
                "REST API Endpoints": "Multi-cloud Gateway (API Gateway + API Management + Cloud Endpoints)",
                "IAM/Identity Management": "Multi-cloud IAM (IAM + Azure AD + Cloud IAM)",
                "Container Orchestration": "Multi-cloud Orchestration (ECS/EKS + AKS + GKE)",
                "Application Load Balancer": "Multi-cloud Load Balancing (ALB + Azure LB + Cloud LB)",
                "Managed Database": "Multi-cloud Database (RDS + Azure SQL + Cloud SQL)",
                "Service Discovery": "Multi-cloud DNS (Route 53 + Azure DNS + Cloud DNS)",
                "Web Servers": "Multi-cloud VMs (EC2 + Azure VMs + Compute Engine)",
                "Application Servers": "Multi-cloud VMs (EC2 + Azure VMs + Compute Engine)",
                "Network Security Groups": "Multi-cloud Security (Security Groups + NSG + Firewall)",
                "Persistent Storage": "Multi-cloud Storage (EBS + Azure Disks + Persistent Disks)",
                "Container Monitoring": "Multi-cloud Monitoring (CloudWatch + Azure Monitor + Cloud Monitoring)"
            }
        }
        
        if environment in cloud_mappings:
            mapping = cloud_mappings[environment]
            for req in requirements:
                if req.type in mapping:
                    req.type = mapping[req.type]
        
        return requirements
    
    def _identify_missing_info(self, pattern: InfrastructurePattern, 
                              environment: Environment, 
                              requirements: List[InfrastructureRequirement],
                              context: Dict[str, Any] = None) -> List[ClarificationQuestion]:
        """Identify missing information that needs to be gathered"""
        questions = []
        
        # Environment-specific questions
        if environment == Environment.UNKNOWN:
            questions.append(ClarificationQuestion(
                question="Which cloud provider or environment would you like to use?",
                category="environment",
                required=True,
                options=["AWS", "Azure", "GCP", "On-premise", "Hybrid"]
            ))
        
        # Pattern-specific questions
        if pattern == InfrastructurePattern.SERVERLESS:
            questions.append(ClarificationQuestion(
                question="What's your expected request volume?",
                category="performance",
                required=False,
                options=["Low (<1000 req/day)", "Medium (1000-10000 req/day)", "High (>10000 req/day)"],
                default="Medium (1000-10000 req/day)"
            ))
        
        # Security questions
        questions.append(ClarificationQuestion(
            question="Do you have any specific security requirements?",
            category="security",
            required=False,
            options=["Standard security", "Enhanced security", "Compliance requirements"],
            default="Standard security"
        ))
        
        # Cost questions
        questions.append(ClarificationQuestion(
            question="What's your budget range for this infrastructure?",
            category="cost",
            required=False,
            options=["Low cost", "Medium cost", "High performance regardless of cost"],
            default="Medium cost"
        ))
        
        return questions
    
    def _generate_detailed_questions(self, pattern: InfrastructurePattern) -> List[ClarificationQuestion]:
        """Generate detailed, technical questions based on infrastructure pattern"""
        questions = []
        
        if pattern == InfrastructurePattern.SERVERLESS:
            questions.extend([
                ClarificationQuestion(
                    question="What's your expected request volume and patterns?",
                    category="performance",
                    required=True,
                    options=[
                        "Low: <1000 req/day, predictable traffic",
                        "Medium: 1000-10000 req/day, some spikes",
                        "High: >10000 req/day, highly variable",
                        "Enterprise: >100k req/day, auto-scaling critical"
                    ],
                    default="Medium: 1000-10000 req/day, some spikes",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What are your latency requirements?",
                    category="performance",
                    required=True,
                    options=[
                        "Relaxed: <500ms response time acceptable",
                        "Standard: <200ms response time required",
                        "Strict: <100ms response time critical",
                        "Real-time: <50ms response time mandatory"
                    ],
                    default="Standard: <200ms response time required",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What data types will you store in your database?",
                    category="data",
                    required=True,
                    options=[
                        "Simple: User profiles, basic metadata",
                        "Complex: Nested objects, arrays, relationships",
                        "Time-series: Logs, metrics, events",
                        "Multi-tenant: Isolated data per customer"
                    ],
                    default="Simple: User profiles, basic metadata",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What's your data retention and backup strategy?",
                    category="data",
                    required=True,
                    options=[
                        "Basic: 30 days retention, daily backups",
                        "Standard: 90 days retention, hourly backups",
                        "Comprehensive: 1 year retention, real-time replication",
                        "Enterprise: 7 years retention, multi-region backup"
                    ],
                    default="Standard: 90 days retention, hourly backups",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What security compliance do you need?",
                    category="security",
                    required=True,
                    options=[
                        "Basic: Standard cloud security",
                        "Enhanced: Encryption, IAM, network isolation",
                        "Compliance: SOC2, HIPAA, PCI-DSS",
                        "Government: FedRAMP, FISMA, DoD"
                    ],
                    default="Enhanced: Encryption, IAM, network isolation",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What monitoring and alerting do you require?",
                    category="operations",
                    required=True,
                    options=[
                        "Basic: Cloud metrics and logs",
                        "Standard: Custom dashboards, alerting",
                        "Advanced: APM, tracing, business metrics",
                        "Enterprise: Full observability, SLO/SLI tracking"
                    ],
                    default="Standard: Custom dashboards, alerting",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What's your disaster recovery strategy?",
                    category="availability",
                    required=True,
                    options=[
                        "Basic: Single region, manual recovery",
                        "Standard: Multi-zone, automated failover",
                        "Advanced: Multi-region, active-active",
                        "Enterprise: Global distribution, zero-downtime"
                    ],
                    default="Standard: Multi-zone, automated failover",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What's your budget range for this infrastructure?",
                    category="cost",
                    required=True,
                    options=[
                        "Budget: <$100/month, cost-optimized",
                        "Standard: $100-500/month, balanced",
                        "Performance: $500-2000/month, optimized",
                        "Enterprise: >$2000/month, premium features"
                    ],
                    default="Standard: $100-500/month, balanced",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What CI/CD and deployment strategy do you prefer?",
                    category="deployment",
                    required=False,
                    options=[
                        "Manual: Terraform apply, manual approvals",
                        "Automated: GitHub Actions, auto-deploy",
                        "Advanced: GitOps, ArgoCD, automated testing",
                        "Enterprise: Full pipeline, security scanning, compliance"
                    ],
                    default="Automated: GitHub Actions, auto-deploy",
                    priority="medium"
                ),
                ClarificationQuestion(
                    question="What team structure will manage this infrastructure?",
                    category="operations",
                    required=False,
                    options=[
                        "Single developer: Full-stack responsibility",
                        "DevOps team: Dedicated infrastructure engineers",
                        "Platform team: SRE, DevOps, security specialists",
                        "Enterprise: Multiple teams, role-based access"
                    ],
                    default="DevOps team: Dedicated infrastructure engineers",
                    priority="medium"
                )
            ])
        
        elif pattern == InfrastructurePattern.MICROSERVICES:
            questions.extend([
                ClarificationQuestion(
                    question="How many microservices do you plan to deploy?",
                    category="architecture",
                    required=True,
                    options=[
                        "Small: 2-5 services, simple architecture",
                        "Medium: 5-15 services, moderate complexity",
                        "Large: 15-50 services, complex orchestration",
                        "Enterprise: 50+ services, service mesh required"
                    ],
                    default="Medium: 5-15 services, moderate complexity",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What container orchestration platform do you prefer?",
                    category="platform",
                    required=True,
                    options=[
                        "ECS: AWS native, managed service",
                        "EKS: Kubernetes, full control",
                        "Fargate: Serverless containers, no management",
                        "Hybrid: Mix of platforms based on service needs"
                    ],
                    default="ECS: AWS native, managed service",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What's your service communication pattern?",
                    category="architecture",
                    required=True,
                    options=[
                        "Synchronous: REST APIs, direct calls",
                        "Asynchronous: Event-driven, message queues",
                        "Hybrid: Mix of sync/async based on service",
                        "Advanced: gRPC, GraphQL, service mesh"
                    ],
                    default="Hybrid: Mix of sync/async based on service",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What database strategy do you need?",
                    category="data",
                    required=True,
                    options=[
                        "Single database: Shared across services",
                        "Database per service: Isolated data stores",
                        "Polyglot persistence: Different DBs per service",
                        "Advanced: CQRS, event sourcing, data mesh"
                    ],
                    default="Database per service: Isolated data stores",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What's your API management strategy?",
                    category="api",
                    required=True,
                    options=[
                        "Basic: API Gateway, simple routing",
                        "Standard: Rate limiting, authentication, monitoring",
                        "Advanced: API versioning, developer portal, analytics",
                        "Enterprise: Full API lifecycle, governance, monetization"
                    ],
                    default="Standard: Rate limiting, authentication, monitoring",
                    priority="high"
                )
            ])
        
        elif pattern == InfrastructurePattern.THREE_TIER:
            questions.extend([
                ClarificationQuestion(
                    question="What web server technology do you prefer?",
                    category="compute",
                    required=True,
                    options=[
                        "Load Balancer: Application load balancer with target groups",
                        "Auto Scaling: Virtual machines with auto-scaling",
                        "Container: Container orchestration with web containers",
                        "Serverless: Serverless functions with API gateway"
                    ],
                    default="Load Balancer: Application load balancer with target groups",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What application server technology?",
                    category="compute",
                    required=True,
                    options=[
                        "Virtual Machines: Traditional VM-based deployment",
                        "Container: Containerized application deployment",
                        "PaaS: Platform-as-a-Service deployment",
                        "Serverless: Function-based deployment"
                    ],
                    default="Virtual Machines: Traditional VM-based deployment",
                    priority="high"
                ),
                ClarificationQuestion(
                    question="What database technology do you need?",
                    category="database",
                    required=True,
                    options=[
                        "RDS MySQL: Managed relational database",
                        "RDS PostgreSQL: Advanced relational features",
                        "Aurora: MySQL/PostgreSQL compatible, high performance",
                        "Custom: Self-managed database on EC2"
                    ],
                    default="RDS MySQL: Managed relational database",
                    priority="critical"
                ),
                ClarificationQuestion(
                    question="What's your backup and recovery strategy?",
                    category="data",
                    required=True,
                    options=[
                        "Basic: Automated backups, manual recovery",
                        "Standard: Point-in-time recovery, read replicas",
                        "Advanced: Multi-region backup, automated failover",
                        "Enterprise: Zero data loss, continuous backup"
                    ],
                    default="Standard: Point-in-time recovery, read replicas",
                    priority="high"
                )
            ])
        
        # Add common questions for all patterns
        questions.extend([
            ClarificationQuestion(
                question="What region do you prefer for deployment?",
                category="deployment",
                required=True,
                options=[
                    "US East: Primary region for US users",
                    "US West: Lower latency for West Coast",
                    "Europe: GDPR compliance, EU users",
                    "Asia Pacific: Lower latency for APAC users",
                    "Multi-region: Global distribution"
                ],
                default="US East: Primary region for US users",
                priority="high"
            ),
            ClarificationQuestion(
                question="What's your expected data transfer volume?",
                category="network",
                required=False,
                options=[
                    "Low: <100 GB/month, minimal transfer",
                    "Medium: 100 GB - 1 TB/month, moderate transfer",
                    "High: 1 TB - 10 TB/month, significant transfer",
                    "Enterprise: >10 TB/month, high bandwidth required"
                ],
                default="Medium: 100 GB - 1 TB/month, moderate transfer",
                priority="medium"
            ),
            ClarificationQuestion(
                question="What compliance and audit requirements do you have?",
                category="compliance",
                required=False,
                options=[
                    "None: Basic security sufficient",
                    "Internal: Company security policies",
                    "Industry: SOC2, ISO 27001, PCI-DSS",
                    "Government: FedRAMP, FISMA, HIPAA"
                ],
                default="Internal: Company security policies",
                priority="high"
            )
        ])
        
        return questions
    
    def _estimate_cost(self, pattern: InfrastructurePattern, requirements: List[InfrastructureRequirement]) -> str:
        """Estimate the cost of the infrastructure"""
        if pattern == InfrastructurePattern.SERVERLESS:
            return "$50-200/month (pay-per-use)"
        elif pattern == InfrastructurePattern.MICROSERVICES:
            return "$200-1000/month"
        elif pattern == InfrastructurePattern.THREE_TIER:
            return "$500-2000/month"
        else:
            return "$100-500/month"
    
    def _generate_security_recommendations(self, pattern: InfrastructurePattern, requirements: List[InfrastructureRequirement]) -> List[str]:
        """Generate security recommendations based on pattern and requirements"""
        recommendations = []
        
        # Base security recommendations
        recommendations.extend([
            "🔒 **Identity & Access Management (IAM)**",
            "   • Use least privilege principle for all IAM roles",
            "   • Enable MFA for all user accounts",
            "   • Regular access reviews and role rotation",
            "   • Use AWS Organizations for multi-account management"
        ])
        
        # Pattern-specific security
        if pattern == InfrastructurePattern.SERVERLESS:
            recommendations.extend([
                "🔒 **Serverless Security**",
                "   • Encrypt Lambda environment variables",
                "   • Use VPC for Lambda when possible",
                "   • Implement proper IAM roles for Lambda execution",
                "   • Enable CloudTrail for API Gateway monitoring"
            ])
        elif pattern == InfrastructurePattern.MICROSERVICES:
            recommendations.extend([
                "🔒 **Microservices Security**",
                "   • Implement service-to-service authentication",
                "   • Use network policies and security groups",
                "   • Encrypt data in transit and at rest",
                "   • Implement API rate limiting and DDoS protection"
            ])
        elif pattern == InfrastructurePattern.THREE_TIER:
            recommendations.extend([
                "🔒 **Three-Tier Security**",
                "   • Use security groups to isolate tiers",
                "   • Implement WAF for web tier protection",
                "   • Encrypt database connections and data",
                "   • Use private subnets for app and database tiers"
            ])
        
        # Compliance recommendations
        recommendations.extend([
            "🔒 **Compliance & Monitoring**",
            "   • Enable CloudTrail for audit logging",
            "   • Implement CloudWatch monitoring and alerting",
            "   • Regular security assessments and penetration testing",
            "   • Automated compliance checking with AWS Config"
        ])
        
        return recommendations
    
    def _generate_deployment_recommendations(self, pattern: InfrastructurePattern, requirements: List[InfrastructureRequirement]) -> List[str]:
        """Generate deployment recommendations based on pattern and requirements"""
        recommendations = []
        
        # Base deployment recommendations
        recommendations.extend([
            "🚀 **Infrastructure as Code**",
            "   • Use Terraform for infrastructure provisioning",
            "   • Version control all infrastructure code",
            "   • Implement proper state management",
            "   • Use workspaces for environment separation"
        ])
        
        # Pattern-specific deployment
        if pattern == InfrastructurePattern.SERVERLESS:
            recommendations.extend([
                "🚀 **Serverless Deployment**",
                "   • Use SAM or Serverless Framework for packaging",
                "   • Implement blue-green deployments for Lambda",
                "   • Use CloudFormation for infrastructure orchestration",
                "   • Automated testing in staging environment"
            ])
        elif pattern == InfrastructurePattern.MICROSERVICES:
            recommendations.extend([
                "🚀 **Microservices Deployment**",
                "   • Use ECS/EKS for container orchestration",
                "   • Implement rolling deployments with health checks",
                "   • Use service discovery and load balancing",
                "   • Automated deployment pipelines with GitOps"
            ])
        elif pattern == InfrastructurePattern.THREE_TIER:
            recommendations.extend([
                "🚀 **Three-Tier Deployment**",
                "   • Use Auto Scaling Groups for scalability",
                "   • Implement blue-green deployment strategy",
                "   • Use RDS for managed database operations",
                "   • Load balancer health checks and failover"
            ])
        
        # CI/CD recommendations
        recommendations.extend([
            "🚀 **CI/CD Pipeline**",
            "   • Automated testing and quality gates",
            "   • Infrastructure testing with Terratest",
            "   • Security scanning in deployment pipeline",
            "   • Rollback capabilities for failed deployments"
        ])
        
        return recommendations

    def determine_required_categories(self, request: str, pattern: InfrastructurePattern, environment: Environment) -> Dict[str, bool]:
        """
        Intelligently determine which requirement categories are needed
        based on the infrastructure request, pattern, and environment
        """
        required_categories = {
            'basic': True,  # Always needed
            'performance': False,
            'security': False,
            'cost': False,
            'compliance': False,
            'advanced': False
        }
        
        request_lower = request.lower()
        
        # Performance requirements - needed for user-facing applications
        if any(keyword in request_lower for keyword in ['web app', 'api', 'website', 'application', 'users', 'traffic', 'load']):
            required_categories['performance'] = True
        
        # Security requirements - needed for sensitive data or production
        if any(keyword in request_lower for keyword in ['production', 'sensitive', 'compliance', 'secure', 'private', 'internal']):
            required_categories['security'] = True
        elif any(keyword in request_lower for keyword in ['development', 'test', 'demo', 'simple', 'basic']):
            required_categories['security'] = False
        else:
            required_categories['security'] = True  # Default to secure
        
        # Cost requirements - needed for budget-conscious projects
        if any(keyword in request_lower for keyword in ['budget', 'cost', 'cheap', 'affordable', 'minimal', 'optimize']):
            required_categories['cost'] = True
        elif any(keyword in request_lower for keyword in ['enterprise', 'production', 'critical', 'high-availability']):
            required_categories['cost'] = False  # Enterprise projects often prioritize features over cost
        else:
            required_categories['cost'] = True  # Default to cost-aware
        
        # Compliance requirements - needed for regulated industries
        if any(keyword in request_lower for keyword in ['healthcare', 'finance', 'banking', 'government', 'soc2', 'hipaa', 'pci', 'gdpr']):
            required_categories['compliance'] = True
        elif any(keyword in request_lower for keyword in ['development', 'test', 'personal', 'demo']):
            required_categories['compliance'] = False
        else:
            required_categories['compliance'] = False  # Default to no compliance needed
        
        # Advanced requirements - needed for complex deployments
        if any(keyword in request_lower for keyword in ['blue-green', 'canary', 'rolling', 'disaster recovery', 'backup', 'monitoring', 'logging']):
            required_categories['advanced'] = True
        elif any(keyword in request_lower for keyword in ['simple', 'basic', 'minimal', 'development']):
            required_categories['advanced'] = False
        else:
            required_categories['advanced'] = False  # Default to simple
        
        # Pattern-specific adjustments
        if pattern == InfrastructurePattern.SERVERLESS:
            required_categories['performance'] = True  # Serverless needs performance config
            required_categories['cost'] = True  # Serverless is cost-sensitive
        elif pattern == InfrastructurePattern.MICROSERVICES:
            required_categories['advanced'] = True  # Microservices need advanced config
            required_categories['performance'] = True  # Microservices need performance tuning
        elif pattern == InfrastructurePattern.MONOLITHIC:
            required_categories['performance'] = True  # Monoliths need performance config
            required_categories['advanced'] = False  # Monoliths are simpler
        
        # Environment-specific adjustments
        if environment == Environment.HYBRID:
            required_categories['advanced'] = True  # Multi-cloud needs advanced config
            required_categories['cost'] = True  # Multi-cloud cost optimization
        elif environment == Environment.ONPREMISE:
            required_categories['advanced'] = True  # On-premise needs advanced config
            required_categories['security'] = True  # On-premise security is critical
        
        return required_categories
