"""
Local Knowledge Base for AI-AH Platform

This module provides a local intelligence system with datasets and logic
that doesn't require external LLM services. It uses rule-based intelligence
with a comprehensive knowledge base for infrastructure management.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Optional imports for enhanced components
try:
    from ..search.vector_search import VectorSearchEngine
    from ..nlp.enhanced_nlp_processor import EnhancedNLPProcessor
    ENHANCED_COMPONENTS_AVAILABLE = True
except ImportError:
    ENHANCED_COMPONENTS_AVAILABLE = False
    VectorSearchEngine = None
    EnhancedNLPProcessor = None

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """Represents a knowledge entry in the local knowledge base."""
    id: str
    category: str
    title: str
    content: str
    tags: List[str]
    confidence: float
    created_at: datetime
    updated_at: datetime


@dataclass
class InfrastructurePattern:
    """Represents an infrastructure pattern for matching."""
    pattern: str
    regex: str
    agent_type: str
    action: str
    confidence: float
    parameters: Dict[str, Any]


class LocalKnowledgeBase:
    """
    Local knowledge base with infrastructure intelligence.
    
    This class provides intelligent responses based on:
    1. Infrastructure patterns and templates
    2. Best practices and recommendations
    3. Common infrastructure scenarios
    4. Rule-based decision making
    """
    
    def __init__(self, vector_search_engine: Optional[Any] = None, 
                 nlp_processor: Optional[Any] = None):
        self.knowledge_entries: Dict[str, KnowledgeEntry] = {}
        self.infrastructure_patterns: List[InfrastructurePattern] = []
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.best_practices: Dict[str, List[str]] = {}
        self.scenarios: Dict[str, Dict[str, Any]] = {}
        
        # Enhanced components (only if available)
        self.vector_search_engine = vector_search_engine if ENHANCED_COMPONENTS_AVAILABLE else None
        self.nlp_processor = nlp_processor if ENHANCED_COMPONENTS_AVAILABLE else None
        
        self._initialize_knowledge_base()
        self._initialize_patterns()
        self._initialize_templates()
        self._initialize_best_practices()
        self._initialize_scenarios()
        
        # Note: Vector search initialization will be done separately when needed
    
    async def _initialize_vector_search(self):
        """Initialize vector search with knowledge base entries."""
        try:
            # Create infrastructure index if it doesn't exist
            if "infrastructure" not in self.vector_search_engine.indexes:
                await self.vector_search_engine.create_index("infrastructure", "flat", "Infrastructure knowledge base")
            
            # Convert knowledge entries to documents
            documents = []
            for entry in self.knowledge_entries.values():
                doc = {
                    'id': entry.id,
                    'content': f"{entry.title} {entry.content}",
                    'metadata': {
                        'category': entry.category,
                        'tags': entry.tags,
                        'confidence': entry.confidence,
                        'created_at': entry.created_at.isoformat()
                    }
                }
                documents.append(doc)
            
            # Add documents to vector search
            if documents:
                await self.vector_search_engine.add_documents("infrastructure", documents)
                logger.info(f"Added {len(documents)} knowledge entries to vector search")
                
        except Exception as e:
            logger.error(f"Failed to initialize vector search: {str(e)}")
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with infrastructure knowledge."""
        
        # Infrastructure Knowledge Entries
        knowledge_data = [
            {
                "id": "web_server_basics",
                "category": "infrastructure",
                "title": "Web Server Infrastructure Basics",
                "content": "A web server infrastructure typically includes: 1) Load balancer for traffic distribution, 2) Web servers (Apache/Nginx) for serving content, 3) Application servers for business logic, 4) Database servers for data storage, 5) Caching layer (Redis/Memcached), 6) CDN for static content delivery, 7) Monitoring and logging systems.",
                "tags": ["web", "server", "infrastructure", "basics"],
                "confidence": 0.95
            },
            {
                "id": "security_hardening",
                "category": "security",
                "title": "Server Security Hardening",
                "content": "Security hardening includes: 1) Regular security updates, 2) Firewall configuration, 3) SSH key authentication, 4) Disable unnecessary services, 5) Implement fail2ban, 6) Regular security audits, 7) Backup encryption, 8) Network segmentation, 9) Access control policies, 10) Monitoring and alerting.",
                "tags": ["security", "hardening", "server", "best-practices"],
                "confidence": 0.98
            },
            {
                "id": "scalability_patterns",
                "category": "scalability",
                "title": "Infrastructure Scalability Patterns",
                "content": "Scalability patterns include: 1) Horizontal scaling (add more servers), 2) Vertical scaling (upgrade server specs), 3) Load balancing, 4) Database sharding, 5) Caching strategies, 6) CDN implementation, 7) Microservices architecture, 8) Auto-scaling groups, 9) Container orchestration, 10) Performance monitoring.",
                "tags": ["scalability", "performance", "architecture", "patterns"],
                "confidence": 0.92
            },
            {
                "id": "monitoring_essentials",
                "category": "monitoring",
                "title": "Infrastructure Monitoring Essentials",
                "content": "Essential monitoring includes: 1) System metrics (CPU, memory, disk, network), 2) Application metrics (response time, throughput, errors), 3) Business metrics (user activity, revenue), 4) Log aggregation and analysis, 5) Alerting and notification systems, 6) Health checks and uptime monitoring, 7) Performance profiling, 8) Capacity planning metrics.",
                "tags": ["monitoring", "observability", "metrics", "alerting"],
                "confidence": 0.94
            },
            {
                "id": "cost_optimization",
                "category": "cost",
                "title": "Cloud Cost Optimization Strategies",
                "content": "Cost optimization strategies: 1) Right-sizing instances, 2) Reserved instances for predictable workloads, 3) Spot instances for flexible workloads, 4) Auto-scaling to match demand, 5) Storage optimization (lifecycle policies), 6) Network optimization, 7) Resource tagging for cost tracking, 8) Regular cost audits, 9) Eliminate unused resources, 10) Use cost-effective regions.",
                "tags": ["cost", "optimization", "cloud", "budget"],
                "confidence": 0.90
            },
            # Advanced Infrastructure Knowledge
            {
                "id": "microservices_architecture",
                "category": "architecture",
                "title": "Microservices Architecture Patterns",
                "content": "Microservices architecture includes: 1) Service decomposition by business capability, 2) API gateway for external communication, 3) Service mesh for inter-service communication, 4) Container orchestration (Kubernetes), 5) Distributed data management, 6) Event-driven architecture, 7) Circuit breakers for fault tolerance, 8) Distributed tracing and logging, 9) Service discovery and registration, 10) Configuration management.",
                "tags": ["microservices", "architecture", "containers", "kubernetes"],
                "confidence": 0.95
            },
            {
                "id": "container_orchestration",
                "category": "containers",
                "title": "Container Orchestration Best Practices",
                "content": "Container orchestration best practices: 1) Use Kubernetes for production workloads, 2) Implement health checks and readiness probes, 3) Use rolling deployments for zero-downtime updates, 4) Implement resource limits and requests, 5) Use namespaces for multi-tenancy, 6) Implement network policies for security, 7) Use persistent volumes for stateful applications, 8) Implement auto-scaling based on metrics, 9) Use secrets management for sensitive data, 10) Implement monitoring and observability.",
                "tags": ["containers", "kubernetes", "orchestration", "devops"],
                "confidence": 0.94
            },
            {
                "id": "serverless_architecture",
                "category": "serverless",
                "title": "Serverless Architecture Patterns",
                "content": "Serverless architecture patterns: 1) Function-as-a-Service (FaaS) for compute, 2) Event-driven architecture with triggers, 3) API Gateway for HTTP endpoints, 4) Database-as-a-Service for data storage, 5) Storage services for file and object storage, 6) Message queues for asynchronous processing, 7) Step functions for workflow orchestration, 8) Event sourcing and CQRS patterns, 9) Cold start optimization strategies, 10) Cost optimization with pay-per-use model.",
                "tags": ["serverless", "lambda", "functions", "event-driven"],
                "confidence": 0.93
            },
            {
                "id": "zero_trust_security",
                "category": "security",
                "title": "Zero Trust Security Model",
                "content": "Zero Trust security model: 1) Never trust, always verify principle, 2) Identity-based access control, 3) Multi-factor authentication (MFA), 4) Least privilege access, 5) Network segmentation and micro-segmentation, 6) Continuous monitoring and validation, 7) Encryption in transit and at rest, 8) Device compliance and health checks, 9) Behavioral analytics and anomaly detection, 10) Automated response to security incidents.",
                "tags": ["security", "zero-trust", "identity", "access-control"],
                "confidence": 0.96
            },
            {
                "id": "compliance_frameworks",
                "category": "compliance",
                "title": "Compliance Frameworks and Standards",
                "content": "Major compliance frameworks: 1) GDPR for data privacy in EU, 2) HIPAA for healthcare data protection, 3) SOX for financial reporting, 4) PCI DSS for payment card data, 5) ISO 27001 for information security management, 6) NIST Cybersecurity Framework, 7) CIS Controls for security best practices, 8) SOC 2 for service organizations, 9) FedRAMP for government cloud services, 10) CCPA for California privacy rights.",
                "tags": ["compliance", "gdpr", "hipaa", "pci", "security"],
                "confidence": 0.97
            },
            {
                "id": "performance_optimization",
                "category": "performance",
                "title": "Performance Optimization Strategies",
                "content": "Performance optimization strategies: 1) Application-level caching (Redis, Memcached), 2) Database query optimization and indexing, 3) CDN implementation for static content, 4) Image and asset optimization, 5) Code splitting and lazy loading, 6) Connection pooling and database optimization, 7) Load balancing and traffic distribution, 8) Auto-scaling based on demand, 9) Performance monitoring and profiling, 10) Regular performance testing and benchmarking.",
                "tags": ["performance", "optimization", "caching", "scalability"],
                "confidence": 0.94
            },
            {
                "id": "high_availability",
                "category": "reliability",
                "title": "High Availability Architecture",
                "content": "High availability architecture: 1) Multi-region deployment, 2) Multi-availability zone setup, 3) Load balancing across instances, 4) Database replication and failover, 5) Health checks and auto-recovery, 6) Circuit breakers and bulkheads, 7) Graceful degradation strategies, 8) Disaster recovery planning, 9) Backup and restore procedures, 10) Monitoring and alerting systems.",
                "tags": ["high-availability", "reliability", "disaster-recovery", "fault-tolerance"],
                "confidence": 0.95
            },
            {
                "id": "data_architecture",
                "category": "data",
                "title": "Modern Data Architecture Patterns",
                "content": "Modern data architecture: 1) Data lake for raw data storage, 2) Data warehouse for structured analytics, 3) ETL/ELT pipelines for data processing, 4) Real-time streaming with Kafka/Kinesis, 5) Data mesh for decentralized data management, 6) Data catalog and governance, 7) Machine learning pipelines, 8) Data quality and validation, 9) Data lineage and metadata management, 10) Privacy-preserving analytics.",
                "tags": ["data", "analytics", "data-lake", "data-warehouse"],
                "confidence": 0.93
            },
            {
                "id": "database_optimization",
                "category": "database",
                "title": "Database Performance and Optimization",
                "content": "Database optimization strategies: 1) Query optimization and indexing, 2) Connection pooling and management, 3) Read replicas for scaling reads, 4) Database sharding and partitioning, 5) Caching strategies (Redis, Memcached), 6) Database monitoring and profiling, 7) Regular maintenance and cleanup, 8) Backup and recovery procedures, 9) Database versioning and migration, 10) Security and access control.",
                "tags": ["database", "optimization", "performance", "scalability"],
                "confidence": 0.94
            },
            {
                "id": "observability_stack",
                "category": "observability",
                "title": "Modern Observability Stack",
                "content": "Modern observability stack: 1) Metrics collection (Prometheus, CloudWatch), 2) Log aggregation (ELK Stack, Splunk), 3) Distributed tracing (Jaeger, Zipkin), 4) APM tools (New Relic, Datadog), 5) Alerting systems (PagerDuty, OpsGenie), 6) Dashboard and visualization (Grafana, Kibana), 7) Synthetic monitoring, 8) Real user monitoring (RUM), 9) Error tracking (Sentry, Rollbar), 10) Infrastructure as Code monitoring.",
                "tags": ["observability", "monitoring", "tracing", "apm"],
                "confidence": 0.95
            },
            {
                "id": "devops_practices",
                "category": "devops",
                "title": "DevOps Best Practices",
                "content": "DevOps best practices: 1) Infrastructure as Code (Terraform, CloudFormation), 2) Continuous Integration/Continuous Deployment (CI/CD), 3) Configuration management (Ansible, Puppet), 4) Container orchestration (Kubernetes), 5) Monitoring and observability, 6) Security in the pipeline (DevSecOps), 7) Automated testing and quality gates, 8) Feature flags and canary deployments, 9) Incident response and post-mortems, 10) Team collaboration and communication.",
                "tags": ["devops", "ci-cd", "automation", "infrastructure-as-code"],
                "confidence": 0.93
            },
            {
                "id": "disaster_recovery",
                "category": "disaster-recovery",
                "title": "Disaster Recovery Planning",
                "content": "Disaster recovery planning: 1) Business impact analysis (BIA), 2) Recovery Time Objective (RTO) and Recovery Point Objective (RPO), 3) Backup strategies and testing, 4) Multi-region deployment, 5) Data replication and synchronization, 6) Failover and failback procedures, 7) Communication plans during incidents, 8) Regular disaster recovery testing, 9) Documentation and runbooks, 10) Continuous improvement and lessons learned.",
                "tags": ["disaster-recovery", "backup", "business-continuity", "rto-rpo"],
                "confidence": 0.94
            },
            {
                "id": "elk_stack_deployment",
                "category": "monitoring",
                "title": "ELK Stack Deployment and Clustering",
                "content": "ELK Stack deployment with Elasticsearch clustering: 1) Elasticsearch cluster setup with master, data, and coordinating nodes, 2) Index templates and shard allocation strategies, 3) Logstash pipeline configuration for data ingestion, 4) Kibana dashboard creation and visualization, 5) Beats agents for log collection, 6) Cluster health monitoring and alerting, 7) Index lifecycle management (ILM) policies, 8) Security configuration with X-Pack, 9) Backup and restore strategies, 10) Performance tuning and optimization.",
                "tags": ["elk", "elasticsearch", "logstash", "kibana", "clustering", "monitoring"],
                "confidence": 0.96
            },
            {
                "id": "kubernetes_service_mesh",
                "category": "kubernetes",
                "title": "Kubernetes Service Mesh with Istio",
                "content": "Kubernetes service mesh implementation with Istio: 1) Istio control plane installation and configuration, 2) Sidecar proxy injection for microservices, 3) Traffic management with VirtualServices and DestinationRules, 4) Security policies with mTLS and authorization, 5) Observability with metrics, logs, and distributed tracing, 6) Canary deployments and traffic splitting, 7) Circuit breakers and fault injection, 8) Multi-cluster service mesh setup, 9) Performance optimization and resource tuning, 10) Monitoring and troubleshooting strategies.",
                "tags": ["kubernetes", "istio", "service-mesh", "microservices", "observability"],
                "confidence": 0.95
            },
            {
                "id": "terraform_multi_region",
                "category": "terraform",
                "title": "Multi-Region Terraform Setup",
                "content": "Multi-region Terraform setup: 1) Remote state management with S3 and DynamoDB, 2) State locking and versioning strategies, 3) Provider configuration for multiple regions, 4) Module structure for region-specific resources, 5) Workspace management for environment separation, 6) Cross-region resource dependencies, 7) State migration and backup procedures, 8) CI/CD pipeline integration, 9) Security best practices for state files, 10) Disaster recovery and state restoration.",
                "tags": ["terraform", "multi-region", "state-management", "infrastructure-as-code"],
                "confidence": 0.94
            },
            {
                "id": "zero_trust_architecture",
                "category": "security",
                "title": "Zero Trust Security Architecture",
                "content": "Zero Trust security architecture implementation: 1) Identity and access management (IAM) with multi-factor authentication, 2) Network segmentation and micro-segmentation, 3) Device trust and compliance verification, 4) Application-level security with API gateways, 5) Data encryption at rest and in transit, 6) Continuous monitoring and behavioral analytics, 7) Least privilege access principles, 8) Security automation and orchestration, 9) Incident response and threat detection, 10) Compliance and audit frameworks.",
                "tags": ["zero-trust", "security", "iam", "network-security", "compliance"],
                "confidence": 0.97
            },
            {
                "id": "finops_practices",
                "category": "cost-optimization",
                "title": "FinOps Practices for Cloud Cost Optimization",
                "content": "FinOps practices for cloud cost optimization: 1) Cost allocation and chargeback models, 2) Budget management and alerting systems, 3) Right-sizing instances and resources, 4) Reserved instances and savings plans, 5) Spot instances for flexible workloads, 6) Auto-scaling and resource optimization, 7) Cost monitoring and reporting dashboards, 8) Tagging strategies for cost tracking, 9) Unused resource identification and cleanup, 10) Cost governance and approval workflows.",
                "tags": ["finops", "cost-optimization", "cloud-economics", "budget-management"],
                "confidence": 0.95
            },
            {
                "id": "prometheus_grafana_monitoring",
                "category": "monitoring",
                "title": "Comprehensive Monitoring with Prometheus and Grafana",
                "content": "Comprehensive monitoring setup with Prometheus and Grafana: 1) Prometheus server configuration and service discovery, 2) Grafana dashboard creation and visualization, 3) AlertManager configuration for notifications, 4) Custom metrics and exporters setup, 5) Log aggregation with ELK stack integration, 6) Distributed tracing with Jaeger, 7) APM tools integration, 8) SLA/SLO monitoring and alerting, 9) Capacity planning and forecasting, 10) Incident response and runbook automation.",
                "tags": ["prometheus", "grafana", "monitoring", "observability", "alerting"],
                "confidence": 0.96
            },
            {
                "id": "cicd_pipeline_implementation",
                "category": "devops",
                "title": "CI/CD Pipeline Implementation with GitLab CI",
                "content": "CI/CD pipeline implementation with GitLab CI: 1) GitLab CI/CD configuration with .gitlab-ci.yml, 2) Pipeline stages and job definitions, 3) Docker containerization and registry integration, 4) Automated testing and quality gates, 5) Security scanning and vulnerability assessment, 6) Deployment strategies (blue-green, canary, rolling), 7) Environment management and promotion, 8) Artifact management and versioning, 9) Monitoring and notification integration, 10) Pipeline optimization and performance tuning.",
                "tags": ["cicd", "gitlab-ci", "devops", "automation", "deployment"],
                "confidence": 0.95
            },
            {
                "id": "multi_cloud_architecture_design",
                "category": "architecture",
                "title": "Multi-Cloud Architecture Design",
                "content": "Multi-cloud architecture design: 1) Cloud provider selection and vendor lock-in avoidance, 2) Hybrid cloud connectivity and networking, 3) Data synchronization and replication strategies, 4) Application portability and containerization, 5) Load balancing and traffic distribution, 6) Disaster recovery and business continuity, 7) Cost optimization across providers, 8) Security and compliance management, 9) Monitoring and observability across clouds, 10) Governance and policy enforcement.",
                "tags": ["multi-cloud", "architecture", "hybrid-cloud", "cloud-strategy"],
                "confidence": 0.94
            },
            {
                "id": "application_performance_optimization",
                "category": "performance",
                "title": "Application Performance and Scalability Optimization",
                "content": "Application performance and scalability optimization: 1) Performance profiling and bottleneck identification, 2) Caching strategies (Redis, Memcached, CDN), 3) Database optimization and query tuning, 4) Load balancing and horizontal scaling, 5) Auto-scaling and resource management, 6) Code optimization and algorithm improvements, 7) Network optimization and latency reduction, 8) Memory management and garbage collection tuning, 9) Performance monitoring and alerting, 10) Capacity planning and forecasting.",
                "tags": ["performance", "scalability", "optimization", "caching", "monitoring"],
                "confidence": 0.95
            },
            # Comprehensive Technology Knowledge
            {
                "id": "ansible_comprehensive",
                "category": "automation",
                "title": "Ansible Complete Guide",
                "content": "Ansible is a powerful automation platform for IT infrastructure. Core Components: 1) Inventory Management - Define hosts in INI/YAML format with groups and variables, 2) Playbooks - YAML files describing automation workflows with tasks, handlers, and roles, 3) Roles - Reusable collections of tasks, variables, files, and templates, 4) Modules - Built-in and custom modules for system operations (system, cloud, network, database), 5) Variables - Dynamic values using facts, group_vars, host_vars, and vault, 6) Templates - Jinja2 templating for dynamic configuration files, 7) Handlers - Tasks triggered by changes (restart services, reload configs), 8) Vault - Encrypt sensitive data like passwords and API keys, 9) Galaxy - Community repository for pre-built roles and collections, 10) Best Practices - Idempotency, error handling, testing with molecule, and proper variable management. Common Use Cases: Server provisioning, application deployment, configuration drift remediation, security hardening, and compliance automation.",
                "tags": ["ansible", "automation", "configuration-management", "devops", "infrastructure"],
                "confidence": 0.98
            },
            {
                "id": "terraform_comprehensive",
                "category": "infrastructure",
                "title": "Terraform Infrastructure as Code",
                "content": "Terraform is HashiCorp's Infrastructure as Code tool for building, changing, and versioning infrastructure safely. Core Concepts: 1) Providers - Plugins that interact with APIs (AWS, Azure, GCP, Kubernetes), 2) Resources - Infrastructure components defined in configuration files, 3) State Management - Tracks current infrastructure state and enables planning, 4) Modules - Reusable components for organizing and sharing configurations, 5) Variables - Input, output, and local variables for dynamic values, 6) Data Sources - Fetch information from external systems, 7) Workspaces - Multiple state files for different environments, 8) Remote State - Shared state storage with locking (S3, Consul), 9) Terraform Cloud - Managed service for collaboration and state management, 10) Best Practices - Version pinning, state locking, modular design, and proper resource tagging. Advanced Features: Import existing resources, taint/untaint for targeted updates, provisioners for local/remote execution, and policy as code with Sentinel.",
                "tags": ["terraform", "infrastructure-as-code", "iac", "aws", "azure", "gcp"],
                "confidence": 0.98
            },
            {
                "id": "kubernetes_comprehensive",
                "category": "orchestration",
                "title": "Kubernetes Container Orchestration",
                "content": "Kubernetes is a container orchestration platform for automating deployment, scaling, and management of containerized applications. Core Components: 1) Control Plane - API Server, etcd, Scheduler, Controller Manager, 2) Nodes - Worker machines running kubelet, kube-proxy, and container runtime, 3) Pods - Smallest deployable units containing one or more containers, 4) Services - Stable network endpoints for pod access, 5) Deployments - Manage replica sets and rolling updates, 6) ConfigMaps/Secrets - Configuration and sensitive data management, 7) Ingress - External access to services with routing rules, 8) Persistent Volumes - Storage abstraction for stateful applications, 9) Namespaces - Virtual clusters for resource isolation, 10) RBAC - Role-based access control for security. Advanced Features: Helm for package management, Operators for application-specific controllers, Service Mesh (Istio) for microservices communication, and GitOps workflows with ArgoCD/Flux.",
                "tags": ["kubernetes", "k8s", "containers", "orchestration", "microservices"],
                "confidence": 0.98
            },
            {
                "id": "aws_comprehensive",
                "category": "cloud",
                "title": "Amazon Web Services (AWS) Platform",
                "content": "AWS is the leading cloud platform offering 200+ services. Core Services: 1) Compute - EC2, Lambda, ECS, EKS, Fargate for application hosting, 2) Storage - S3, EBS, EFS, Glacier for data storage and backup, 3) Database - RDS, DynamoDB, ElastiCache, Redshift for data management, 4) Networking - VPC, CloudFront, Route 53, ALB/NLB for connectivity, 5) Security - IAM, KMS, Secrets Manager, WAF for access control, 6) Monitoring - CloudWatch, X-Ray, CloudTrail for observability, 7) DevOps - CodePipeline, CodeBuild, CodeDeploy for CI/CD, 8) Analytics - Kinesis, EMR, Athena for big data processing, 9) AI/ML - SageMaker, Rekognition, Comprehend for machine learning, 10) Cost Management - Cost Explorer, Budgets, Trusted Advisor for optimization. Best Practices: Well-Architected Framework, security by design, cost optimization, and automation with Infrastructure as Code.",
                "tags": ["aws", "amazon", "cloud", "ec2", "s3", "lambda"],
                "confidence": 0.98
            },
            {
                "id": "azure_comprehensive",
                "category": "cloud",
                "title": "Microsoft Azure Cloud Platform",
                "content": "Azure is Microsoft's cloud platform with comprehensive services for enterprise workloads. Core Services: 1) Compute - Virtual Machines, App Service, Functions, Container Instances, AKS, 2) Storage - Blob Storage, Files, Disks, Archive for data management, 3) Database - SQL Database, Cosmos DB, Redis Cache, Synapse Analytics, 4) Networking - Virtual Network, CDN, DNS, Load Balancer, Application Gateway, 5) Security - Azure AD, Key Vault, Security Center, Sentinel for identity and security, 6) Monitoring - Monitor, Application Insights, Log Analytics for observability, 7) DevOps - DevOps Pipelines, Boards, Repos, Artifacts for development lifecycle, 8) Analytics - Data Factory, Stream Analytics, HDInsight for big data, 9) AI/ML - Machine Learning, Cognitive Services, Bot Framework, 10) Cost Management - Cost Management + Billing, Advisor for optimization. Enterprise Features: Hybrid cloud with Azure Arc, multi-cloud with Azure Lighthouse, and compliance with various standards (SOC, ISO, HIPAA).",
                "tags": ["azure", "microsoft", "cloud", "vm", "app-service", "aks"],
                "confidence": 0.98
            },
            {
                "id": "gcp_comprehensive",
                "category": "cloud",
                "title": "Google Cloud Platform (GCP)",
                "content": "GCP is Google's cloud platform known for data analytics and machine learning capabilities. Core Services: 1) Compute - Compute Engine, App Engine, Cloud Functions, GKE for application hosting, 2) Storage - Cloud Storage, Persistent Disk, Filestore for data management, 3) Database - Cloud SQL, Firestore, Bigtable, Spanner for data storage, 4) Networking - VPC, Cloud CDN, Cloud DNS, Load Balancing for connectivity, 5) Security - Identity and Access Management, Secret Manager, Security Command Center, 6) Monitoring - Cloud Monitoring, Cloud Logging, Cloud Trace for observability, 7) DevOps - Cloud Build, Cloud Deploy, Artifact Registry for CI/CD, 8) Analytics - BigQuery, Dataflow, Pub/Sub, Dataproc for big data, 9) AI/ML - Vertex AI, AutoML, AI Platform for machine learning, 10) Cost Management - Cost Management, Recommender for optimization. Unique Features: Global network infrastructure, advanced AI/ML services, and strong data analytics capabilities with BigQuery.",
                "tags": ["gcp", "google", "cloud", "bigquery", "gke", "cloud-functions"],
                "confidence": 0.98
            },
            {
                "id": "docker_comprehensive",
                "category": "containers",
                "title": "Docker Containerization Platform",
                "content": "Docker is a containerization platform that packages applications and dependencies into portable containers. Core Concepts: 1) Images - Read-only templates containing application code and dependencies, 2) Containers - Running instances of Docker images, 3) Dockerfile - Text file with instructions to build images, 4) Registry - Repository for storing and sharing images (Docker Hub, ECR, ACR), 5) Volumes - Persistent data storage for containers, 6) Networks - Communication between containers and external systems, 7) Compose - Multi-container application definition and orchestration, 8) Swarm - Native clustering and orchestration solution, 9) Security - Image scanning, secrets management, and runtime protection, 10) Best Practices - Multi-stage builds, minimal base images, proper layer caching, and security scanning. Advanced Features: BuildKit for faster builds, Docker Desktop for local development, and integration with Kubernetes and cloud platforms.",
                "tags": ["docker", "containers", "containerization", "devops", "microservices"],
                "confidence": 0.98
            },
            {
                "id": "monitoring_comprehensive",
                "category": "observability",
                "title": "Comprehensive Monitoring and Observability",
                "content": "Modern monitoring stack for full-stack observability: 1) Metrics - Prometheus for time-series data collection, Grafana for visualization and alerting, 2) Logging - ELK Stack (Elasticsearch, Logstash, Kibana) or EFK (Fluentd) for centralized logging, 3) Tracing - Jaeger, Zipkin, or OpenTelemetry for distributed request tracing, 4) APM - New Relic, Datadog, or AppDynamics for application performance monitoring, 5) Infrastructure - CloudWatch, Azure Monitor, or Stackdriver for cloud resource monitoring, 6) Alerting - PagerDuty, OpsGenie, or AlertManager for incident management, 7) Synthetic Monitoring - Pingdom, UptimeRobot for external availability testing, 8) Real User Monitoring - Browser and mobile app performance tracking, 9) Error Tracking - Sentry, Rollbar, or Bugsnag for application error monitoring, 10) Security Monitoring - SIEM tools like Splunk, QRadar, or Azure Sentinel. Best Practices: Three pillars of observability (metrics, logs, traces), proper alerting thresholds, and correlation across monitoring tools.",
                "tags": ["monitoring", "observability", "prometheus", "grafana", "elk", "jaeger"],
                "confidence": 0.98
            },
            {
                "id": "security_comprehensive",
                "category": "security",
                "title": "Infrastructure Security Best Practices",
                "content": "Comprehensive security framework for infrastructure: 1) Identity and Access Management - Multi-factor authentication, least privilege access, and regular access reviews, 2) Network Security - VPCs, security groups, firewalls, and network segmentation, 3) Data Protection - Encryption at rest and in transit, key management, and data classification, 4) Vulnerability Management - Regular scanning, patch management, and security updates, 5) Compliance - SOC 2, ISO 27001, PCI DSS, and industry-specific requirements, 6) Security Monitoring - SIEM, threat detection, and incident response, 7) DevSecOps - Security integration in CI/CD pipelines, SAST/DAST testing, 8) Container Security - Image scanning, runtime protection, and secure base images, 9) Cloud Security - Shared responsibility model, cloud security posture management, 10) Incident Response - Playbooks, forensics, and recovery procedures. Tools: AWS Security Hub, Azure Security Center, GCP Security Command Center, and third-party solutions like Prisma Cloud.",
                "tags": ["security", "compliance", "iam", "encryption", "vulnerability", "devsecops"],
                "confidence": 0.98
            },
            {
                "id": "cicd_comprehensive",
                "category": "devops",
                "title": "CI/CD Pipeline Best Practices",
                "content": "Complete CI/CD pipeline implementation: 1) Source Control - Git workflows, branching strategies, and code review processes, 2) Build Automation - Automated compilation, testing, and artifact generation, 3) Testing - Unit, integration, security, and performance testing automation, 4) Code Quality - Static analysis, code coverage, and quality gates, 5) Security Scanning - SAST, DAST, dependency scanning, and container image scanning, 6) Deployment Strategies - Blue-green, canary, rolling, and feature flag deployments, 7) Infrastructure Provisioning - Infrastructure as Code with Terraform, CloudFormation, or ARM templates, 8) Configuration Management - Environment-specific configurations and secrets management, 9) Monitoring - Deployment monitoring, rollback triggers, and health checks, 10) Feedback Loops - Automated notifications, metrics collection, and continuous improvement. Popular Tools: Jenkins, GitLab CI, GitHub Actions, Azure DevOps, AWS CodePipeline, and cloud-native solutions.",
                "tags": ["ci-cd", "devops", "automation", "jenkins", "gitlab", "github-actions"],
                "confidence": 0.98
            }
        ]
        
        for entry_data in knowledge_data:
            entry = KnowledgeEntry(
                id=entry_data["id"],
                category=entry_data["category"],
                title=entry_data["title"],
                content=entry_data["content"],
                tags=entry_data["tags"],
                confidence=entry_data["confidence"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.knowledge_entries[entry.id] = entry
    
    def _initialize_patterns(self):
        """Initialize infrastructure patterns for intent recognition."""
        
        patterns = [
            # Web Server Patterns
            InfrastructurePattern(
                pattern="create web server",
                regex=r"(create|setup|deploy|build).*(web|http|apache|nginx).*(server|site|website)",
                agent_type="terraform",
                action="create_web_server",
                confidence=0.9,
                parameters={"server_type": "web", "default_port": 80}
            ),
            InfrastructurePattern(
                pattern="database setup",
                regex=r"(create|setup|deploy|install).*(database|db|mysql|postgres|mongodb)",
                agent_type="terraform",
                action="create_database",
                confidence=0.9,
                parameters={"db_type": "mysql", "default_port": 3306}
            ),
            InfrastructurePattern(
                pattern="load balancer",
                regex=r"(create|setup|deploy|configure).*(load.?balancer|lb|nginx|haproxy)",
                agent_type="terraform",
                action="create_load_balancer",
                confidence=0.85,
                parameters={"lb_type": "application", "health_check": True}
            ),
            
            # Security Patterns
            InfrastructurePattern(
                pattern="security scan",
                regex=r"(security|vulnerability|scan|audit|check|hardening).*(security|vulnerabilities|issues|hardening|hardening)",
                agent_type="security",
                action="security_scan",
                confidence=0.9,
                parameters={"scan_type": "comprehensive", "auto_fix": False}
            ),
            InfrastructurePattern(
                pattern="firewall configuration",
                regex=r"(configure|setup|create).*(firewall|security.?group|iptables)",
                agent_type="security",
                action="configure_firewall",
                confidence=0.85,
                parameters={"default_deny": True, "allow_ssh": True}
            ),
            
            # Monitoring Patterns
            InfrastructurePattern(
                pattern="monitoring setup",
                regex=r"(setup|configure|create|install|monitoring).*(monitoring|metrics|alerting|grafana|prometheus|setup)",
                agent_type="monitoring",
                action="setup_monitoring",
                confidence=0.9,
                parameters={"monitoring_type": "comprehensive", "alerting": True}
            ),
            InfrastructurePattern(
                pattern="health check",
                regex=r"(check|monitor|status|health).*(system|server|infrastructure|status)",
                agent_type="monitoring",
                action="health_check",
                confidence=0.8,
                parameters={"check_type": "comprehensive", "detailed": True}
            ),
            
            # ELK Stack Patterns
            InfrastructurePattern(
                pattern="elk stack deployment",
                regex=r"(elk|elasticsearch|logstash|kibana|elastic).*(deploy|setup|configure|clustering|cluster)",
                agent_type="monitoring",
                action="elk_deployment",
                confidence=0.95,
                parameters={"elk_type": "full_stack", "clustering": True}
            ),
            InfrastructurePattern(
                pattern="elasticsearch clustering",
                regex=r"(elasticsearch|elastic).*(cluster|clustering|node|shard|replica)",
                agent_type="monitoring",
                action="elasticsearch_cluster",
                confidence=0.9,
                parameters={"cluster_type": "multi_node", "replication": True}
            ),
            
            # Kubernetes Patterns
            InfrastructurePattern(
                pattern="kubernetes service mesh",
                regex=r"(kubernetes|k8s|service.?mesh|istio|linkerd).*(service.?mesh|mesh|istio|linkerd)",
                agent_type="kubernetes",
                action="service_mesh",
                confidence=0.95,
                parameters={"mesh_type": "istio", "security": True}
            ),
            InfrastructurePattern(
                pattern="kubernetes microservices",
                regex=r"(kubernetes|k8s|microservices|microservice).*(deploy|setup|architecture)",
                agent_type="kubernetes",
                action="microservices_deployment",
                confidence=0.9,
                parameters={"architecture": "microservices", "scaling": True}
            ),
            
            # Terraform Patterns
            InfrastructurePattern(
                pattern="terraform multi-region",
                regex=r"(terraform|multi.?region|multi.?region).*(setup|deploy|create|state)",
                agent_type="terraform",
                action="multi_region_setup",
                confidence=0.9,
                parameters={"regions": "multiple", "state_management": True}
            ),
            
            # Security Patterns
            InfrastructurePattern(
                pattern="zero trust security",
                regex=r"(zero.?trust|zero.?trust).*(security|architecture|implementation)",
                agent_type="security",
                action="zero_trust_architecture",
                confidence=0.95,
                parameters={"trust_model": "zero_trust", "verification": "continuous"}
            ),
            
            # FinOps Patterns
            InfrastructurePattern(
                pattern="finops cost optimization",
                regex=r"(finops|cost.?optimization|cloud.?cost).*(optimization|management|practices)",
                agent_type="monitoring",
                action="finops_optimization",
                confidence=0.9,
                parameters={"optimization_type": "comprehensive", "automation": True}
            ),
            
            # CI/CD Patterns
            InfrastructurePattern(
                pattern="cicd pipeline",
                regex=r"(ci.?cd|continuous.?integration|continuous.?deployment|pipeline|gitlab.?ci|jenkins|github.?actions).*(pipeline|deploy|integration|deployment)",
                agent_type="terraform",
                action="cicd_pipeline",
                confidence=0.95,
                parameters={"pipeline_type": "comprehensive", "automation": True}
            ),
            
            # Multi-cloud Patterns
            InfrastructurePattern(
                pattern="multi-cloud architecture",
                regex=r"(multi.?cloud|multi.?cloud|hybrid.?cloud).*(architecture|design|setup|implementation)",
                agent_type="terraform",
                action="multi_cloud_architecture",
                confidence=0.95,
                parameters={"cloud_providers": "multiple", "integration": True}
            ),
            
            # Performance Patterns
            InfrastructurePattern(
                pattern="performance optimization",
                regex=r"(performance|optimization|scalability|scaling).*(optimization|performance|scalability|scaling)",
                agent_type="monitoring",
                action="performance_optimization",
                confidence=0.9,
                parameters={"optimization_type": "comprehensive", "monitoring": True}
            ),
            
            # Cost Optimization Patterns
            InfrastructurePattern(
                pattern="cost optimization",
                regex=r"(cost|optimize|optimization|budget|save|reduce).*(cost|optimization|budget|money|expense)",
                agent_type="terraform",
                action="cost_optimization",
                confidence=0.9,
                parameters={"optimization_type": "comprehensive", "include_recommendations": True}
            ),
            
            # Configuration Management
            InfrastructurePattern(
                pattern="server configuration",
                regex=r"(configure|setup|manage|automate).*(server|system|configuration|ansible)",
                agent_type="ansible",
                action="configure_server",
                confidence=0.85,
                parameters={"config_type": "comprehensive", "backup": True}
            ),
            InfrastructurePattern(
                pattern="application deployment",
                regex=r"(deploy|release|update|rollout).*(application|app|service|container)",
                agent_type="kubernetes",
                action="deploy_application",
                confidence=0.9,
                parameters={"deployment_type": "rolling", "health_check": True}
            ),
            # Technology Explanation Patterns
            InfrastructurePattern(
                pattern="ansible explanation",
                regex=r"(explain|tell|about|what|how|ansible)",
                agent_type="ansible",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "ansible", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="terraform explanation",
                regex=r"(explain|tell|about|what|how|terraform)",
                agent_type="terraform",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "terraform", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="kubernetes explanation",
                regex=r"(explain|tell|about|what|how|kubernetes|k8s)",
                agent_type="kubernetes",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "kubernetes", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="aws explanation",
                regex=r"(explain|tell|about|what|how|aws|amazon)",
                agent_type="aws",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "aws", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="azure explanation",
                regex=r"(explain|tell|about|what|how|azure|microsoft)",
                agent_type="azure",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "azure", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="gcp explanation",
                regex=r"(explain|tell|about|what|how|gcp|google)",
                agent_type="gcp",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "gcp", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="docker explanation",
                regex=r"(explain|tell|about|what|how|docker)",
                agent_type="docker",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "docker", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="monitoring explanation",
                regex=r"(explain|tell|about|what|how|monitoring|prometheus|grafana|elk)",
                agent_type="monitoring",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "monitoring", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="security explanation",
                regex=r"(explain|tell|about|what|how|security|compliance|iam)",
                agent_type="security",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "security", "detail_level": "comprehensive"}
            ),
            InfrastructurePattern(
                pattern="cicd explanation",
                regex=r"(explain|tell|about|what|how|ci.?cd|devops|jenkins|gitlab)",
                agent_type="cicd",
                action="explain_technology",
                confidence=0.95,
                parameters={"technology": "cicd", "detail_level": "comprehensive"}
            )
        ]
        
        self.infrastructure_patterns = patterns
    
    def _initialize_templates(self):
        """Initialize infrastructure templates."""
        
        self.templates = {
            "web_server": {
                "name": "Basic Web Server",
                "description": "A simple web server with Apache/Nginx",
                "resources": [
                    {"type": "aws_instance", "name": "web_server", "instance_type": "t3.micro"},
                    {"type": "aws_security_group", "name": "web_sg", "ports": [80, 443, 22]}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$10-20/month"
            },
            "web_app_with_db": {
                "name": "Web Application with Database",
                "description": "Complete web application with database backend",
                "resources": [
                    {"type": "aws_instance", "name": "web_server", "instance_type": "t3.small"},
                    {"type": "aws_db_instance", "name": "database", "engine": "mysql"},
                    {"type": "aws_security_group", "name": "app_sg", "ports": [80, 443, 22, 3306]}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$50-100/month"
            },
            "scalable_web_app": {
                "name": "Scalable Web Application",
                "description": "High-availability web application with load balancer",
                "resources": [
                    {"type": "aws_lb", "name": "app_lb", "type": "application"},
                    {"type": "aws_autoscaling_group", "name": "web_asg", "min_size": 2},
                    {"type": "aws_db_instance", "name": "database", "engine": "mysql", "multi_az": True}
                ],
                "agent_type": "terraform",
                "estimated_cost": "$200-500/month"
            },
            "containerized_app": {
                "name": "Containerized Application",
                "description": "Kubernetes deployment for containerized applications",
                "resources": [
                    {"type": "kubernetes_deployment", "name": "app_deployment", "replicas": 3},
                    {"type": "kubernetes_service", "name": "app_service", "type": "LoadBalancer"},
                    {"type": "kubernetes_configmap", "name": "app_config"}
                ],
                "agent_type": "kubernetes",
                "estimated_cost": "$100-300/month"
            }
        }
    
    def _initialize_best_practices(self):
        """Initialize best practices for different infrastructure scenarios."""
        
        self.best_practices = {
            "security": [
                "Always use SSH keys instead of passwords",
                "Implement regular security updates and patches",
                "Configure firewall to deny all by default",
                "Use HTTPS for all web traffic",
                "Implement proper access controls and RBAC",
                "Regular security audits and vulnerability scans",
                "Encrypt data at rest and in transit",
                "Implement backup and disaster recovery plans"
            ],
            "performance": [
                "Use CDN for static content delivery",
                "Implement caching at multiple levels",
                "Optimize database queries and indexing",
                "Use load balancers for traffic distribution",
                "Monitor and optimize resource utilization",
                "Implement auto-scaling for variable workloads",
                "Use appropriate instance types for workloads",
                "Regular performance testing and optimization"
            ],
            "reliability": [
                "Implement health checks and monitoring",
                "Use multiple availability zones",
                "Implement proper backup strategies",
                "Design for failure and implement circuit breakers",
                "Use infrastructure as code for consistency",
                "Implement proper logging and alerting",
                "Regular disaster recovery testing",
                "Use managed services where appropriate"
            ],
            "cost_optimization": [
                "Right-size instances based on actual usage",
                "Use reserved instances for predictable workloads",
                "Implement auto-scaling to match demand",
                "Regular cost audits and optimization reviews",
                "Use spot instances for flexible workloads",
                "Implement proper resource tagging",
                "Eliminate unused resources regularly",
                "Use cost-effective regions and services"
            ]
        }
    
    def _initialize_scenarios(self):
        """Initialize common infrastructure scenarios."""
        
        self.scenarios = {
            "ecommerce": {
                "name": "E-commerce Platform",
                "description": "Complete e-commerce infrastructure with high availability",
                "components": ["web_servers", "database", "cache", "cdn", "monitoring"],
                "estimated_cost": "$500-2000/month",
                "scalability": "high",
                "security_level": "high"
            },
            "blog": {
                "name": "Blog/Content Management",
                "description": "Simple blog or CMS infrastructure",
                "components": ["web_server", "database", "backup"],
                "estimated_cost": "$20-50/month",
                "scalability": "medium",
                "security_level": "medium"
            },
            "api_service": {
                "name": "API Service",
                "description": "RESTful API service infrastructure",
                "components": ["api_servers", "database", "cache", "monitoring"],
                "estimated_cost": "$100-500/month",
                "scalability": "high",
                "security_level": "high"
            },
            "development": {
                "name": "Development Environment",
                "description": "Development and testing infrastructure",
                "components": ["dev_server", "database", "monitoring"],
                "estimated_cost": "$10-30/month",
                "scalability": "low",
                "security_level": "low"
            }
        }
    
    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and determine the best response with enhanced keyword analysis.
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Dictionary with analysis results, recommendations, and actions
        """
        user_input_lower = user_input.lower()
        
        # Check for error cases first
        error_response = self._handle_error_cases(user_input)
        if error_response:
            return error_response
        
        # Enhanced keyword analysis
        keywords = self._extract_keywords(user_input_lower)
        print(f"🔍 Keywords detected: {keywords}")  # Debug output
        
        # Find matching patterns with enhanced matching
        matched_patterns = []
        for pattern in self.infrastructure_patterns:
            if re.search(pattern.regex, user_input_lower, re.IGNORECASE):
                matched_patterns.append(pattern)
        
        # Enhanced pattern matching based on keywords
        keyword_matches = self._match_by_keywords(keywords)
        matched_patterns.extend(keyword_matches)
        
        # Remove duplicates and sort by confidence
        unique_patterns = {}
        for pattern in matched_patterns:
            if pattern.pattern not in unique_patterns or pattern.confidence > unique_patterns[pattern.pattern].confidence:
                unique_patterns[pattern.pattern] = pattern
        
        matched_patterns = list(unique_patterns.values())
        
        # Enhanced pattern matching with semantic similarity
        def enhanced_pattern_priority(pattern):
            # Count how many keywords match in the pattern name
            pattern_keywords = pattern.pattern.lower().split()
            user_keywords = user_input.lower().split()
            keyword_matches = sum(1 for kw in pattern_keywords if any(ukw in kw or kw in ukw for ukw in user_keywords))
            
            # Add semantic similarity scoring
            semantic_score = self._calculate_semantic_similarity(user_input, pattern.pattern)
            
            # Combine keyword matching and semantic similarity
            return (keyword_matches + semantic_score, pattern.confidence)
        
        matched_patterns.sort(key=enhanced_pattern_priority, reverse=True)
        
        print(f"🎯 Patterns matched: {[p.pattern for p in matched_patterns]}")  # Debug output
        
        if not matched_patterns:
            return self._handle_general_query(user_input)
        
        best_match = matched_patterns[0]
        
        # Enhanced reasoning based on keywords
        reasoning = self._generate_reasoning(keywords, best_match, user_input)
        
        # Get relevant knowledge entries
        relevant_knowledge = self._get_relevant_knowledge(best_match.agent_type, user_input)
        
        # Get best practices
        best_practices = self._get_best_practices(best_match.agent_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(best_match, user_input)
        
        return {
            "intent": best_match.action,
            "agent_type": best_match.agent_type,
            "confidence": best_match.confidence,
            "parameters": best_match.parameters,
            "keywords": keywords,
            "reasoning": reasoning,
            "knowledge": relevant_knowledge,
            "best_practices": best_practices,
            "recommendations": recommendations,
            "templates": self._get_relevant_templates(best_match.agent_type),
            "scenarios": self._get_relevant_scenarios(user_input)
        }
    
    def _calculate_semantic_similarity(self, query: str, pattern: str) -> float:
        """Calculate semantic similarity between query and pattern."""
        # Simple semantic similarity based on word overlap and synonyms
        query_words = set(query.lower().split())
        pattern_words = set(pattern.lower().split())
        
        # Direct word overlap
        direct_overlap = len(query_words.intersection(pattern_words))
        
        # Synonym mapping for common infrastructure terms
        synonyms = {
            'aws': ['amazon', 'amazon web services'],
            'azure': ['microsoft', 'microsoft azure'],
            'gcp': ['google', 'google cloud', 'google cloud platform'],
            'terraform': ['iac', 'infrastructure as code'],
            'ansible': ['automation', 'configuration management'],
            'kubernetes': ['k8s', 'container orchestration'],
            'docker': ['containers', 'containerization'],
            'monitoring': ['observability', 'metrics', 'logging'],
            'security': ['cybersecurity', 'protection', 'hardening'],
            'cicd': ['ci/cd', 'continuous integration', 'continuous deployment'],
            'explain': ['tell', 'describe', 'what is', 'how does'],
            'about': ['regarding', 'concerning', 'on the subject of']
        }
        
        # Check for synonym matches
        synonym_score = 0
        for word in query_words:
            for key, values in synonyms.items():
                if word in values and key in pattern_words:
                    synonym_score += 0.5
                elif word == key and any(v in pattern_words for v in values):
                    synonym_score += 0.5
        
        # Calculate total similarity score
        total_words = max(len(query_words), len(pattern_words))
        if total_words == 0:
            return 0.0
        
        similarity = (direct_overlap + synonym_score) / total_words
        return min(similarity, 1.0)  # Cap at 1.0


    def _handle_error_cases(self, user_input: str) -> Dict[str, Any]:
        """Handle error cases and edge cases gracefully."""
        user_input_lower = user_input.lower().strip()
        
        # Empty or very short queries
        if not user_input_lower or len(user_input_lower) < 2:
            return {
                "intent": "clarification_needed",
                "agent_type": "general",
                "confidence": 0.8,
                "reasoning": ["Query too short or empty, requesting clarification"],
                "knowledge": [],
                "best_practices": ["Please provide more specific details about your infrastructure needs"],
                "recommendations": ["Try asking about specific technologies like 'explain terraform' or 'how to set up monitoring'"]
            }
        
        # Nonsensical queries
        if len(user_input_lower) < 5 and not any(word in user_input_lower for word in ["hi", "hello", "help"]):
            return {
                "intent": "clarification_needed",
                "agent_type": "general",
                "confidence": 0.7,
                "reasoning": ["Query appears unclear, requesting clarification"],
                "knowledge": [],
                "best_practices": ["Please provide more context about your infrastructure question"],
                "recommendations": ["I can help with: Terraform, Ansible, Kubernetes, AWS, Azure, GCP, Docker, Monitoring, Security, CI/CD"]
            }
        
        # Out-of-scope queries (non-infrastructure topics)
        out_of_scope_keywords = ["quantum", "mars", "time travel", "cooking", "cook", "pasta", "recipe", "food", "weather", "sports", "politics", "music", "movie", "book", "travel", "vacation"]
        if any(keyword in user_input_lower for keyword in out_of_scope_keywords):
            return {
                "intent": "out_of_scope",
                "agent_type": "general",
                "confidence": 0.9,
                "reasoning": ["Query is outside infrastructure and DevOps scope"],
                "knowledge": [],
                "best_practices": ["I specialize in infrastructure, DevOps, and cloud technologies"],
                "recommendations": ["I can help with: Infrastructure as Code, Container Orchestration, Cloud Platforms, Monitoring, Security, CI/CD"]
            }
        
        # If no specific error case matches, return None to continue normal processing
        return None

    def _handle_general_query(self, user_input: str) -> Dict[str, Any]:
        """Handle general queries that don't match specific patterns."""
        
        user_input_lower = user_input.lower()
        
        # Check for greetings first
        if any(greeting in user_input_lower for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            return {
                "intent": "greeting",
                "agent_type": "terraform",
                "confidence": 0.9,
                "parameters": {},
                "knowledge": [self.knowledge_entries.get("web_server_basics", list(self.knowledge_entries.values())[0])],
                "best_practices": self.best_practices.get("reliability", []),
                "recommendations": [
                    "Hello! I'm your AI infrastructure assistant. How can I help you today?",
                    "I can help you with infrastructure setup, security, monitoring, and optimization.",
                    "What would you like to work on today?"
                ],
                "templates": list(self.templates.values())[:2],
                "scenarios": list(self.scenarios.values())[:2]
            }
        
        # Check for specific technology requests first
        elif any(tech in user_input_lower for tech in ["terraform", "ansible", "kubernetes", "docker"]):
            tech_name = next(tech for tech in ["terraform", "ansible", "kubernetes", "docker"] if tech in user_input_lower)
            return {
                "intent": f"list_{tech_name}",
                "agent_type": tech_name,
                "confidence": 0.9,
                "parameters": {"technology": tech_name},
                "knowledge": [self.knowledge_entries.get("web_server_basics", list(self.knowledge_entries.values())[0])],
                "best_practices": self.best_practices.get("reliability", []),
                "recommendations": [
                    f"I'll provide you with {tech_name} capabilities and examples.",
                    f"Here's what I can help you with using {tech_name}:"
                ],
                "templates": [template for template in self.templates.values() if tech_name in template.get("tags", [])][:3],
                "scenarios": [scenario for scenario in self.scenarios.values() if tech_name in scenario.get("tags", [])][:3]
            }
        
        # Check for follow-up questions and variations
        elif any(phrase in user_input_lower for phrase in ["what else", "anything else", "more", "other", "different", "variations"]):
            return {
                "intent": "show_more_options",
                "agent_type": "terraform",
                "confidence": 0.8,
                "parameters": {},
                "knowledge": [self.knowledge_entries.get("web_server_basics", list(self.knowledge_entries.values())[0])],
                "best_practices": self.best_practices.get("reliability", []),
                "recommendations": [
                    "Here are additional capabilities and options I can help you with:",
                    "• **Advanced Infrastructure**: Microservices, serverless, edge computing",
                    "• **DevOps Automation**: CI/CD pipelines, deployment strategies, testing",
                    "• **Cloud Migration**: Lift-and-shift, refactoring, hybrid cloud",
                    "• **Disaster Recovery**: Backup strategies, failover, business continuity",
                    "• **Performance Tuning**: Optimization, scaling, load testing",
                    "• **Security Hardening**: Vulnerability assessment, compliance, encryption"
                ],
                "templates": list(self.templates.values())[3:6],
                "scenarios": list(self.scenarios.values())[3:6]
            }
        elif any(phrase in user_input_lower for phrase in ["why", "same response", "repetitive", "boring", "different answer"]):
            return {
                "intent": "explain_behavior",
                "agent_type": "terraform",
                "confidence": 0.8,
                "parameters": {},
                "knowledge": [],
                "best_practices": [],
                "recommendations": [
                    "I understand your concern about repetitive responses. Let me explain:",
                    "• I provide consistent, professional infrastructure guidance",
                    "• Each response is tailored to your specific query and context",
                    "• I can provide more detailed, specific information if you ask targeted questions",
                    "• Try asking about specific technologies, use cases, or implementation details",
                    "",
                    "**For more specific responses, try asking:**",
                    "• 'Show me terraform examples for AWS'",
                    "• 'How do I set up monitoring with Prometheus?'",
                    "• 'What's the best way to secure my Kubernetes cluster?'",
                    "• 'Compare different database options for my application'"
                ],
                "templates": [],
                "scenarios": []
            }
        # Check for agent functionality questions
        elif any(phrase in user_input_lower for phrase in ["how you work", "how you function", "how do you work", "how do you function", "explain how you work", "how does this work", "how does the agent work"]):
            return {
                "intent": "explain_agent_functionality",
                "agent_type": "terraform",
                "confidence": 0.9,
                "parameters": {},
                "knowledge": [],
                "best_practices": [],
                "recommendations": [
                    "## 🤖 How I Work - AI Infrastructure Assistant",
                    "",
                    "**My Intelligence System:**",
                    "• **Natural Language Processing**: I analyze your queries using keyword extraction and pattern matching",
                    "• **Local Knowledge Base**: I have a comprehensive database of infrastructure patterns, best practices, and scenarios",
                    "• **Context-Aware Responses**: I remember our conversation and provide contextual, non-repetitive responses",
                    "• **Multi-Agent Architecture**: I can route requests to specialized agents (Terraform, Ansible, Kubernetes, Security, Monitoring)",
                    "",
                    "**My Capabilities:**",
                    "• **Infrastructure Analysis**: I understand complex infrastructure requirements and provide detailed recommendations",
                    "• **Technology Expertise**: Deep knowledge of cloud platforms, DevOps tools, and infrastructure patterns",
                    "• **Cost Optimization**: I can analyze costs and suggest optimization strategies",
                    "• **Security & Compliance**: I provide security hardening and compliance guidance",
                    "",
                    "**How to Get the Best Results:**",
                    "• Ask specific questions about technologies or use cases",
                    "• Provide context about your infrastructure needs",
                    "• Ask follow-up questions for deeper insights",
                    "• Use clear, descriptive language about your requirements"
                ],
                "templates": [],
                "scenarios": []
            }
        # Check for capability questions
        elif any(phrase in user_input_lower for phrase in ["what can you do", "what do you do", "capabilities", "help"]):
            return {
                "intent": "show_capabilities",
                "agent_type": "terraform",
                "confidence": 0.8,  # High confidence for capability questions
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "## 🚀 **AI Infrastructure Assistant Capabilities**",
                    "",
                    "### **Infrastructure Management:**",
                    "• **Terraform**: Provision and manage cloud infrastructure",
                    "• **Ansible**: Configuration management and automation", 
                    "• **Kubernetes**: Container orchestration and deployment",
                    "",
                    "### **Security & Compliance:**",
                    "• Security hardening and vulnerability scanning",
                    "• Compliance framework implementation",
                    "• Access control and firewall configuration",
                    "",
                    "### **Monitoring & Optimization:**",
                    "• Infrastructure monitoring and alerting",
                    "• Performance analysis and optimization",
                    "• Cost optimization and resource management",
                    "",
                    "### **What I Can Help You With:**",
                    "• Create web servers, databases, and complete applications",
                    "• Set up monitoring and security systems",
                    "• Optimize costs and performance",
                    "• Provide best practices and templates",
                    "",
                    "**Just ask me what you need!** For example:",
                    "• 'Create a web server with database'",
                    "• 'Set up monitoring for my infrastructure'",
                    "• 'Help me optimize costs'"
                ],
                "templates": list(self.templates.values())[:3],
                "scenarios": list(self.scenarios.values())[:3]
            }
        
        # Handle follow-up questions and clarifications
        if any(phrase in user_input_lower for phrase in ["how", "what about", "tell me more", "explain", "details", "more info"]):
            return {
                "intent": "follow_up_question",
                "agent_type": "terraform",
                "confidence": 0.7,
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I'd be happy to provide more details! Could you please specify:",
                    "• What specific aspect would you like me to explain further?",
                    "• Are you looking for implementation details, best practices, or cost estimates?",
                    "• What type of infrastructure or technology are you most interested in?",
                    "",
                    "For example, you could ask:",
                    "• 'How do I implement microservices architecture?'",
                    "• 'What are the best practices for Kubernetes deployment?'",
                    "• 'Tell me more about security hardening'"
                ],
                "templates": [],
                "scenarios": []
            }
        
        # Handle comparison questions
        if any(phrase in user_input_lower for phrase in ["vs", "versus", "compare", "difference", "better", "which is"]):
            return {
                "intent": "comparison_question",
                "agent_type": "terraform",
                "confidence": 0.7,
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I can help you compare different infrastructure options! Please specify:",
                    "• What technologies or approaches are you comparing?",
                    "• What are your specific requirements (performance, cost, complexity)?",
                    "• What's your use case or application type?",
                    "",
                    "For example, you could ask:",
                    "• 'Kubernetes vs Docker Swarm for container orchestration'",
                    "• 'AWS vs Azure vs GCP for cloud hosting'",
                    "• 'Microservices vs monolithic architecture'"
                ],
                "templates": [],
                "scenarios": []
            }
        
        # Handle troubleshooting questions
        if any(phrase in user_input_lower for phrase in ["problem", "issue", "error", "troubleshoot", "fix", "debug", "not working"]):
            return {
                "intent": "troubleshooting",
                "agent_type": "terraform",
                "confidence": 0.7,
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I can help you troubleshoot infrastructure issues! Please provide:",
                    "• What specific problem are you experiencing?",
                    "• What error messages or symptoms are you seeing?",
                    "• What infrastructure components are involved?",
                    "• When did the issue start occurring?",
                    "",
                    "Common troubleshooting areas I can help with:",
                    "• Performance issues and bottlenecks",
                    "• Security vulnerabilities and hardening",
                    "• Deployment and configuration problems",
                    "• Monitoring and alerting setup"
                ],
                "templates": [],
                "scenarios": []
            }
        
        # Handle cost and budget questions
        if any(phrase in user_input_lower for phrase in ["cost", "price", "budget", "expensive", "cheap", "affordable", "money"]):
            return {
                "intent": "cost_inquiry",
                "agent_type": "terraform",
                "confidence": 0.7,
                "parameters": {},
                "knowledge": [self.knowledge_entries["cost_optimization"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I can help you with cost optimization and budget planning! Please specify:",
                    "• What type of infrastructure are you planning?",
                    "• What's your budget range or cost constraints?",
                    "• Are you looking for cost estimates or optimization strategies?",
                    "",
                    "I can help with:",
                    "• Cost estimates for different infrastructure options",
                    "• Cost optimization strategies and best practices",
                    "• Budget planning and resource allocation",
                    "• Cloud cost management and FinOps practices"
                ],
                "templates": [],
                "scenarios": []
            }
        
        # Check for general infrastructure terms
        if any(term in user_input_lower for term in ["infrastructure", "server", "cloud", "deployment"]):
            return {
                "intent": "general_infrastructure",
                "agent_type": "terraform",
                "confidence": 0.7,  # Increased confidence
                "parameters": {},
                "knowledge": [self.knowledge_entries["web_server_basics"]],
                "best_practices": self.best_practices["reliability"],
                "recommendations": [
                    "I can help you with infrastructure setup, security, monitoring, and optimization.",
                    "Please specify what type of infrastructure you need (web server, database, etc.).",
                    "I can provide templates and best practices for your use case."
                ],
                "templates": list(self.templates.values())[:2],
                "scenarios": list(self.scenarios.values())[:2]
            }
        
        return {
            "intent": "general_help",
            "agent_type": "general",
            "confidence": 0.6,  # Increased confidence
            "parameters": {},
            "knowledge": [],
            "best_practices": [],
            "recommendations": [
                "I'm an AI infrastructure assistant. I can help you with:",
                "• Infrastructure setup and management",
                "• Security hardening and compliance",
                "• Monitoring and observability",
                "• Cost optimization",
                "• Best practices and recommendations",
                "Please ask me about specific infrastructure needs!",
                "",
                "**Need help getting started?** Try asking:",
                "• 'What can you help me with?'",
                "• 'Create a web server with database'",
                "• 'Set up monitoring for my infrastructure'",
                "• 'Help me optimize costs'",
                "• 'How do I implement microservices?'",
                "• 'Compare AWS vs Azure for my use case'"
            ],
            "templates": [],
            "scenarios": []
        }
    
    def _extract_keywords(self, user_input: str) -> Dict[str, List[str]]:
        """Extract and categorize keywords from user input with comprehensive infrastructure knowledge."""
        keywords = {
            "infrastructure": [],
            "security": [],
            "performance": [],
            "cost": [],
            "scalability": [],
            "monitoring": [],
            "database": [],
            "application": [],
            "cloud_providers": [],
            "technologies": [],
            "deployment": [],
            "networking": [],
            "storage": [],
            "compliance": [],
            "disaster_recovery": []
        }
        
        # Comprehensive Infrastructure keywords
        infra_keywords = [
            "server", "web server", "infrastructure", "cloud", "aws", "azure", "gcp", "deployment", "provision",
            "compute", "instance", "vm", "virtual machine", "container", "docker", "kubernetes", "k8s",
            "orchestration", "cluster", "node", "pod", "service", "ingress", "namespace", "helm",
            "terraform", "ansible", "puppet", "chef", "infrastructure as code", "iac", "provisioning",
            "configuration management", "automation", "ci/cd", "continuous integration", "continuous deployment",
            "devops", "sre", "site reliability", "platform engineering", "gitops"
        ]
        for keyword in infra_keywords:
            if keyword in user_input:
                keywords["infrastructure"].append(keyword)
        
        # Comprehensive Security keywords
        security_keywords = [
            "secure", "security", "ssl", "https", "firewall", "authentication", "authorization", "encryption", 
            "vulnerability", "backup", "compliance", "gdpr", "hipaa", "sox", "pci", "iso", "nist",
            "zero trust", "identity", "iam", "rbac", "mfa", "2fa", "sso", "ldap", "active directory",
            "vpn", "private network", "vpc", "subnet", "security group", "nacl", "waf", "ddos protection",
            "penetration testing", "security audit", "vulnerability scan", "threat detection", "siem",
            "certificate", "tls", "pki", "key management", "secrets", "vault", "hashiCorp", "cyber security"
        ]
        for keyword in security_keywords:
            if keyword in user_input:
                keywords["security"].append(keyword)
        
        # Comprehensive Database keywords
        db_keywords = [
            "database", "db", "mysql", "postgres", "postgresql", "mongodb", "redis", "data", "storage",
            "sql", "nosql", "relational", "document", "key-value", "graph", "time-series", "in-memory",
            "elasticsearch", "cassandra", "dynamodb", "aurora", "rds", "cosmos", "firestore", "bigquery",
            "data warehouse", "data lake", "etl", "elt", "data pipeline", "streaming", "kafka", "kinesis",
            "backup", "replication", "sharding", "partitioning", "indexing", "query optimization",
            "acid", "consistency", "availability", "partition tolerance", "cap theorem"
        ]
        for keyword in db_keywords:
            if keyword in user_input:
                keywords["database"].append(keyword)
        
        # Comprehensive Application keywords
        app_keywords = [
            "e-commerce", "ecommerce", "website", "web app", "application", "api", "rest", "graphql", "grpc",
            "microservices", "blog", "cms", "lms", "erp", "crm", "saas", "paas", "iaas", "serverless",
            "lambda", "functions", "faas", "edge computing", "cdn", "static site", "spa", "pwa",
            "mobile app", "ios", "android", "react", "angular", "vue", "nodejs", "python", "java", "go",
            "ruby", "php", "dotnet", "spring", "django", "flask", "express", "fastapi", "rails",
            "frontend", "backend", "fullstack", "bff", "gateway", "proxy", "reverse proxy", "load balancer"
        ]
        for keyword in app_keywords:
            if keyword in user_input:
                keywords["application"].append(keyword)
        
        # Comprehensive Performance keywords
        perf_keywords = [
            "performance", "fast", "speed", "optimization", "caching", "cdn", "load balancer", "latency",
            "throughput", "bandwidth", "response time", "tps", "qps", "rps", "concurrent users", "scalability",
            "auto-scaling", "horizontal scaling", "vertical scaling", "elastic", "burst", "spike", "traffic",
            "memory", "cpu", "disk", "io", "iops", "network", "compression", "minification", "lazy loading",
            "preloading", "prefetching", "connection pooling", "database connection", "query optimization",
            "indexing", "partitioning", "sharding", "read replica", "write replica", "master-slave"
        ]
        for keyword in perf_keywords:
            if keyword in user_input:
                keywords["performance"].append(keyword)
        
        # Comprehensive Cost keywords
        cost_keywords = [
            "cost", "budget", "cheap", "expensive", "optimize", "save", "reduce", "pricing", "billing",
            "reserved instance", "spot instance", "on-demand", "pay-as-you-go", "subscription", "license",
            "tco", "total cost of ownership", "roi", "return on investment", "finops", "cloud economics",
            "right-sizing", "downsizing", "upsizing", "idle resources", "unused resources", "waste",
            "cost allocation", "tagging", "cost center", "chargeback", "showback", "cost visibility"
        ]
        for keyword in cost_keywords:
            if keyword in user_input:
                keywords["cost"].append(keyword)
        
        # Comprehensive Scalability keywords
        scale_keywords = [
            "scalable", "scaling", "high availability", "redundant", "auto-scaling", "elastic", "fault tolerance",
            "disaster recovery", "backup", "replication", "multi-region", "multi-az", "availability zone",
            "region", "geo-distributed", "edge", "global", "local", "proximity", "latency", "resilience",
            "circuit breaker", "bulkhead", "timeout", "retry", "exponential backoff", "graceful degradation",
            "blue-green", "canary", "rolling", "deployment", "strategy", "feature flag", "toggle"
        ]
        for keyword in scale_keywords:
            if keyword in user_input:
                keywords["scalability"].append(keyword)
        
        # Comprehensive Monitoring keywords
        monitor_keywords = [
            "monitoring", "alerting", "metrics", "logs", "dashboard", "observability", "telemetry", "tracing",
            "apm", "application performance monitoring", "infrastructure monitoring", "synthetic monitoring",
            "real user monitoring", "rum", "sla", "slo", "sli", "error rate", "availability", "uptime",
            "downtime", "incident", "on-call", "pagerduty", "opsgenie", "slack", "teams", "notification",
            "grafana", "prometheus", "datadog", "newrelic", "splunk", "elastic", "kibana", "jaeger",
            "zipkin", "opentelemetry", "cloudwatch", "azure monitor", "stackdriver", "sentry", "rollbar"
        ]
        for keyword in monitor_keywords:
            if keyword in user_input:
                keywords["monitoring"].append(keyword)
        
        # Cloud Providers keywords
        cloud_keywords = [
            "aws", "amazon web services", "ec2", "s3", "lambda", "rds", "dynamodb", "cloudfront", "route53",
            "vpc", "iam", "cloudformation", "cloudwatch", "sns", "sqs", "api gateway", "elastic beanstalk",
            "azure", "microsoft azure", "vm", "blob storage", "cosmos db", "app service", "functions",
            "gcp", "google cloud", "compute engine", "cloud storage", "bigquery", "cloud functions",
            "kubernetes engine", "gke", "eks", "aks", "fargate", "container instances", "serverless"
        ]
        for keyword in cloud_keywords:
            if keyword in user_input:
                keywords["cloud_providers"].append(keyword)
        
        # Technologies keywords
        tech_keywords = [
            "docker", "kubernetes", "helm", "terraform", "ansible", "jenkins", "gitlab", "github actions",
            "circleci", "travis", "bamboo", "octopus", "spinnaker", "argo", "flux", "tekton",
            "nginx", "apache", "haproxy", "traefik", "istio", "linkerd", "consul", "etcd", "zookeeper",
            "redis", "memcached", "varnish", "cloudflare", "fastly", "akamai", "maxcdn", "keycdn",
            "postgresql", "mysql", "mariadb", "mongodb", "cassandra", "elasticsearch", "kafka", "rabbitmq"
        ]
        for keyword in tech_keywords:
            if keyword in user_input:
                keywords["technologies"].append(keyword)
        
        # Deployment keywords
        deploy_keywords = [
            "deployment", "deploy", "release", "rollout", "rollback", "blue-green", "canary", "rolling",
            "strategy", "pipeline", "workflow", "automation", "ci/cd", "continuous integration",
            "continuous deployment", "continuous delivery", "devops", "gitops", "infrastructure as code",
            "configuration management", "provisioning", "bootstrap", "setup", "installation", "migration"
        ]
        for keyword in deploy_keywords:
            if keyword in user_input:
                keywords["deployment"].append(keyword)
        
        # Networking keywords
        network_keywords = [
            "network", "networking", "vpc", "subnet", "gateway", "router", "switch", "load balancer",
            "dns", "domain", "ssl", "tls", "certificate", "firewall", "security group", "nacl",
            "vpn", "private network", "public network", "internet", "bandwidth", "latency", "throughput",
            "cdn", "edge", "global", "regional", "availability zone", "multi-region", "geo-distributed"
        ]
        for keyword in network_keywords:
            if keyword in user_input:
                keywords["networking"].append(keyword)
        
        # Storage keywords
        storage_keywords = [
            "storage", "disk", "volume", "filesystem", "nfs", "cifs", "s3", "blob", "object storage",
            "block storage", "file storage", "backup", "snapshot", "replication", "mirroring", "raid",
            "ssd", "hdd", "nvme", "persistent", "ephemeral", "temporary", "cache", "memory", "ram"
        ]
        for keyword in storage_keywords:
            if keyword in user_input:
                keywords["storage"].append(keyword)
        
        # Compliance keywords
        compliance_keywords = [
            "compliance", "gdpr", "hipaa", "sox", "pci", "iso", "nist", "cis", "owasp", "security",
            "audit", "governance", "risk", "control", "policy", "procedure", "standard", "framework",
            "certification", "accreditation", "assessment", "evaluation", "review", "inspection"
        ]
        for keyword in compliance_keywords:
            if keyword in user_input:
                keywords["compliance"].append(keyword)
        
        # Disaster Recovery keywords
        dr_keywords = [
            "disaster recovery", "backup", "restore", "recovery", "rto", "rpo", "business continuity",
            "failover", "failback", "redundancy", "replication", "mirroring", "snapshot", "archive",
            "cold storage", "warm storage", "hot storage", "tape", "offsite", "geographic", "multi-region"
        ]
        for keyword in dr_keywords:
            if keyword in user_input:
                keywords["disaster_recovery"].append(keyword)
        
        return keywords
    
    def _match_by_keywords(self, keywords: Dict[str, List[str]]) -> List[InfrastructurePattern]:
        """Match patterns based on comprehensive keyword analysis."""
        matches = []
        
        # Complex E-commerce pattern with multiple components
        if keywords["application"] and any(word in ["e-commerce", "ecommerce"] for word in keywords["application"]):
            confidence = 0.95
            components = ["web_server", "database", "cache", "cdn", "load_balancer"]
            if keywords["security"]:
                components.append("security")
            if keywords["monitoring"]:
                components.append("monitoring")
            if keywords["performance"]:
                components.append("performance_optimization")
            
            matches.append(InfrastructurePattern(
                pattern="e-commerce infrastructure",
                regex=r"e.?commerce|ecommerce",
                agent_type="terraform",
                action="create_ecommerce_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "e-commerce", 
                    "high_availability": True, 
                    "security": True,
                    "components": components,
                    "scalability": "high"
                }
            ))
        
        # Microservices architecture pattern
        if keywords["application"] and any(word in ["microservices", "api"] for word in keywords["application"]):
            confidence = 0.9
            components = ["api_gateway", "service_mesh", "container_orchestration"]
            if keywords["database"]:
                components.append("database")
            if keywords["monitoring"]:
                components.append("observability")
            if keywords["security"]:
                components.append("security")
            
            matches.append(InfrastructurePattern(
                pattern="microservices infrastructure",
                regex=r"microservices|api.*architecture|service.*mesh",
                agent_type="kubernetes",
                action="create_microservices_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "microservices",
                    "components": components,
                    "orchestration": "kubernetes",
                    "scalability": "high"
                }
            ))
        
        # Container-based infrastructure pattern
        if keywords["technologies"] and any(word in ["docker", "kubernetes", "k8s", "container"] for word in keywords["technologies"]):
            confidence = 0.9
            components = ["container_registry", "orchestration", "service_mesh"]
            if keywords["monitoring"]:
                components.append("monitoring")
            if keywords["security"]:
                components.append("security")
            
            matches.append(InfrastructurePattern(
                pattern="container infrastructure",
                regex=r"docker|kubernetes|k8s|container",
                agent_type="kubernetes",
                action="create_container_infrastructure",
                confidence=confidence,
                parameters={
                    "container_platform": "kubernetes",
                    "components": components,
                    "scalability": "high"
                }
            ))
        
        # High-performance API pattern
        if keywords["application"] and any(word in ["api", "rest", "graphql"] for word in keywords["application"]):
            if keywords["performance"] or keywords["monitoring"]:
                confidence = 0.9
                components = ["api_gateway", "load_balancer", "cache"]
                if keywords["monitoring"]:
                    components.append("monitoring")
                if keywords["security"]:
                    components.append("security")
                
                matches.append(InfrastructurePattern(
                    pattern="high-performance api",
                    regex=r"api|rest|graphql|performance",
                    agent_type="terraform",
                    action="create_high_performance_api",
                    confidence=confidence,
                    parameters={
                        "app_type": "api",
                        "performance": True,
                        "components": components,
                        "monitoring": True
                    }
                ))
        
        # Data pipeline and analytics pattern
        if keywords["database"] and any(word in ["data", "analytics", "pipeline", "etl"] for word in keywords["database"]):
            confidence = 0.9
            components = ["data_lake", "data_warehouse", "etl_pipeline"]
            if keywords["monitoring"]:
                components.append("monitoring")
            if keywords["performance"]:
                components.append("performance_optimization")
            
            matches.append(InfrastructurePattern(
                pattern="data analytics infrastructure",
                regex=r"data.*pipeline|analytics|etl|data.*warehouse",
                agent_type="terraform",
                action="create_data_analytics_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "data_analytics",
                    "components": components,
                    "scalability": "high"
                }
            ))
        
        # Multi-tier web application pattern
        if keywords["infrastructure"] and keywords["database"] and keywords["application"]:
            confidence = 0.9
            components = ["web_tier", "app_tier", "database_tier", "load_balancer"]
            if keywords["security"]:
                components.append("security")
            if keywords["monitoring"]:
                components.append("monitoring")
            if keywords["performance"]:
                components.append("cache")
            
            matches.append(InfrastructurePattern(
                pattern="multi-tier web application",
                regex=r"web.*app|multi.*tier|three.*tier",
                agent_type="terraform",
                action="create_multi_tier_web_app",
                confidence=confidence,
                parameters={
                    "app_type": "web_application",
                    "architecture": "multi_tier",
                    "components": components,
                    "scalability": "medium"
                }
            ))
        
        # Serverless architecture pattern
        if keywords["technologies"] and any(word in ["serverless", "lambda", "functions", "faas"] for word in keywords["technologies"]):
            confidence = 0.9
            components = ["function_runtime", "api_gateway", "event_source"]
            if keywords["database"]:
                components.append("database")
            if keywords["monitoring"]:
                components.append("monitoring")
            
            matches.append(InfrastructurePattern(
                pattern="serverless architecture",
                regex=r"serverless|lambda|functions|faas",
                agent_type="terraform",
                action="create_serverless_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "serverless",
                    "components": components,
                    "scalability": "auto"
                }
            ))
        
        # Disaster recovery and backup pattern
        if keywords["disaster_recovery"] or (keywords["security"] and any(word in ["backup", "recovery"] for word in keywords["security"])):
            confidence = 0.9
            components = ["backup_system", "replication", "failover"]
            if keywords["storage"]:
                components.append("storage")
            
            matches.append(InfrastructurePattern(
                pattern="disaster recovery infrastructure",
                regex=r"disaster.*recovery|backup|failover|business.*continuity",
                agent_type="terraform",
                action="create_disaster_recovery_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "disaster_recovery",
                    "components": components,
                    "rto": "low",
                    "rpo": "low"
                }
            ))
        
        # Compliance and governance pattern
        if keywords["compliance"] or keywords["security"]:
            if any(word in ["gdpr", "hipaa", "sox", "pci", "compliance"] for word in keywords["compliance"] + keywords["security"]):
                confidence = 0.9
                components = ["audit_logging", "access_control", "encryption"]
                if keywords["monitoring"]:
                    components.append("compliance_monitoring")
                
                matches.append(InfrastructurePattern(
                    pattern="compliance infrastructure",
                    regex=r"compliance|gdpr|hipaa|sox|pci|governance",
                    agent_type="security",
                    action="create_compliance_infrastructure",
                    confidence=confidence,
                    parameters={
                        "app_type": "compliance",
                        "components": components,
                        "security_level": "high"
                    }
                ))
        
        # Cost optimization pattern
        if keywords["cost"] and any(word in ["optimize", "save", "reduce", "budget"] for word in keywords["cost"]):
            confidence = 0.9
            components = ["cost_monitoring", "resource_optimization", "automation"]
            
            matches.append(InfrastructurePattern(
                pattern="cost optimization infrastructure",
                regex=r"cost.*optimization|budget|save.*money|reduce.*cost",
                agent_type="terraform",
                action="create_cost_optimized_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "cost_optimization",
                    "components": components,
                    "optimization_level": "high"
                }
            ))
        
        # Monitoring and observability pattern
        if keywords["monitoring"] and len(keywords["monitoring"]) >= 2:
            confidence = 0.9
            components = ["metrics_collection", "log_aggregation", "alerting", "dashboard"]
            if keywords["performance"]:
                components.append("performance_monitoring")
            
            matches.append(InfrastructurePattern(
                pattern="monitoring and observability",
                regex=r"monitoring|observability|metrics|logs|alerting",
                agent_type="monitoring",
                action="create_monitoring_infrastructure",
                confidence=confidence,
                parameters={
                    "app_type": "monitoring",
                    "components": components,
                    "observability_level": "high"
                }
            ))
        
        # Cloud migration pattern
        if keywords["cloud_providers"] and keywords["deployment"]:
            confidence = 0.9
            components = ["migration_strategy", "cloud_resources", "monitoring"]
            if keywords["security"]:
                components.append("security")
            
            matches.append(InfrastructurePattern(
                pattern="cloud migration",
                regex=r"migration|cloud.*migration|lift.*shift|refactor",
                agent_type="terraform",
                action="create_cloud_migration_plan",
                confidence=confidence,
                parameters={
                    "app_type": "cloud_migration",
                    "components": components,
                    "migration_strategy": "assessed"
                }
            ))
        
        return matches
    
    def _generate_reasoning(self, keywords: Dict[str, List[str]], best_match: InfrastructurePattern, user_input: str) -> List[str]:
        """Generate advanced reasoning based on comprehensive keyword analysis and context."""
        reasoning = []
        
        # Context-aware application analysis
        if keywords["application"]:
            app_types = keywords["application"]
            if any("e-commerce" in app or "ecommerce" in app for app in app_types):
                reasoning.append("E-commerce applications require high availability, security, and scalability")
                reasoning.append("Need load balancing, database clustering, SSL certificates, and payment security")
                if keywords["compliance"]:
                    reasoning.append("PCI DSS compliance required for payment processing")
            elif any("api" in app or "rest" in app for app in app_types):
                reasoning.append("API services need high performance, monitoring, and security")
                reasoning.append("Consider rate limiting, caching, API gateway, and authentication")
                if keywords["performance"]:
                    reasoning.append("High-performance APIs require connection pooling and response optimization")
            elif any("microservices" in app for app in app_types):
                reasoning.append("Microservices architecture requires service mesh and container orchestration")
                reasoning.append("Need distributed tracing, service discovery, and circuit breakers")
            elif any("serverless" in app or "lambda" in app for app in app_types):
                reasoning.append("Serverless architecture requires event-driven design and cold start optimization")
                reasoning.append("Consider function composition, state management, and cost optimization")
        
        # Advanced security analysis
        if keywords["security"]:
            security_level = "high" if len(keywords["security"]) > 3 else "medium"
            reasoning.append(f"Security is a {security_level} priority - implementing comprehensive security measures")
            
            if any(comp in keywords["security"] for comp in ["gdpr", "hipaa", "sox", "pci"]):
                reasoning.append("Compliance requirements detected - implementing audit logging and data protection")
            
            if "zero-trust" in keywords["security"] or "zero trust" in user_input.lower():
                reasoning.append("Zero Trust security model - implementing identity-based access control")
            
            reasoning.append("Will include SSL/TLS, firewall configuration, and access controls")
        
        # Database and data architecture analysis
        if keywords["database"]:
            db_types = keywords["database"]
            if any("nosql" in db or "mongodb" in db for db in db_types):
                reasoning.append("NoSQL database architecture - considering document storage and horizontal scaling")
            elif any("sql" in db or "postgres" in db or "mysql" in db for db in db_types):
                reasoning.append("Relational database architecture - implementing ACID compliance and normalization")
            
            if any("data" in db for db in db_types):
                reasoning.append("Data architecture needed - considering data lake, warehouse, and ETL pipelines")
            
            reasoning.append("Will implement database clustering, replication, and automated backups")
        
        # Performance and scalability analysis
        if keywords["performance"] or keywords["scalability"]:
            if keywords["performance"] and keywords["scalability"]:
                reasoning.append("High-performance and scalable architecture required")
                reasoning.append("Implementing auto-scaling, load balancing, caching, and CDN")
            elif keywords["performance"]:
                reasoning.append("Performance optimization required - implementing caching, CDN, and query optimization")
            elif keywords["scalability"]:
                reasoning.append("Scalability is key - implementing horizontal scaling and auto-scaling policies")
        
        # Cloud provider and technology analysis
        if keywords["cloud_providers"]:
            cloud_providers = keywords["cloud_providers"]
            if "aws" in cloud_providers:
                reasoning.append("AWS cloud architecture - leveraging managed services and native integrations")
            elif "azure" in cloud_providers:
                reasoning.append("Azure cloud architecture - utilizing Microsoft ecosystem and hybrid capabilities")
            elif "gcp" in cloud_providers:
                reasoning.append("Google Cloud architecture - leveraging AI/ML services and global network")
        
        # Container and orchestration analysis
        if keywords["technologies"]:
            if any("kubernetes" in tech or "k8s" in tech for tech in keywords["technologies"]):
                reasoning.append("Kubernetes orchestration - implementing container management and service mesh")
            if any("docker" in tech for tech in keywords["technologies"]):
                reasoning.append("Container-based architecture - implementing containerization and registry management")
        
        # Monitoring and observability analysis
        if keywords["monitoring"]:
            monitoring_count = len(keywords["monitoring"])
            if monitoring_count >= 3:
                reasoning.append("Comprehensive observability required - implementing full-stack monitoring")
                reasoning.append("Will include metrics, logs, tracing, and APM tools")
            else:
                reasoning.append("Basic monitoring needed - implementing system and application metrics")
        
        # Cost optimization analysis
        if keywords["cost"]:
            cost_keywords = keywords["cost"]
            if any("optimize" in cost or "save" in cost for cost in cost_keywords):
                reasoning.append("Cost optimization is a priority - implementing FinOps practices")
                reasoning.append("Will recommend reserved instances, spot instances, and auto-scaling")
            elif "budget" in cost_keywords:
                reasoning.append("Budget constraints identified - focusing on cost-effective solutions")
        
        # Disaster recovery and compliance analysis
        if keywords["disaster_recovery"]:
            reasoning.append("Disaster recovery planning required - implementing backup and failover strategies")
            reasoning.append("Will define RTO and RPO objectives with multi-region deployment")
        
        if keywords["compliance"]:
            compliance_frameworks = [comp for comp in keywords["compliance"] if comp in ["gdpr", "hipaa", "sox", "pci", "iso"]]
            if compliance_frameworks:
                reasoning.append(f"Compliance requirements: {', '.join(compliance_frameworks).upper()}")
                reasoning.append("Implementing audit logging, data protection, and governance controls")
        
        # Query-specific reasoning
        user_input_lower = user_input.lower()
        if "why" in user_input_lower or "should" in user_input_lower:
            reasoning.append("Comparative analysis helps evaluate technology choices")
            if "terraform" in user_input_lower and "manual" in user_input_lower:
                reasoning.append("Infrastructure as Code provides consistency, versioning, and automation over manual processes")
                reasoning.append("Terraform enables reproducible deployments and reduces human error")
        if "what happens" in user_input_lower or "if" in user_input_lower:
            reasoning.append("Causal analysis identifies potential consequences and dependencies")
            if "monitoring" in user_input_lower:
                reasoning.append("Without monitoring: blind to performance issues, reactive problem solving, increased downtime")
                reasoning.append("Monitoring enables proactive issue detection and performance optimization")
        if "how to choose" in user_input_lower or "between" in user_input_lower:
            reasoning.append("Decision-making framework considers requirements, costs, and trade-offs")
            if "aws" in user_input_lower and "azure" in user_input_lower:
                reasoning.append("AWS vs Azure: consider existing ecosystem, team expertise, compliance requirements")
                reasoning.append("Evaluate costs, features, support, and integration with existing tools")
        
        # Architecture complexity analysis
        total_components = sum(len(category) for category in keywords.values())
        if total_components > 10:
            reasoning.append("Complex multi-component architecture detected - implementing comprehensive design")
            reasoning.append("Will require careful integration planning and testing strategies")
        elif total_components > 5:
            reasoning.append("Moderate complexity architecture - implementing balanced design approach")
        else:
            reasoning.append("Simple architecture requirements - implementing streamlined solution")
        
        return reasoning
    
    def _get_relevant_knowledge(self, agent_type: str, user_input: str) -> List[KnowledgeEntry]:
        """Get knowledge entries relevant to the agent type and user input."""
        relevant = []
        
        for entry in self.knowledge_entries.values():
            # Check if entry is relevant to agent type
            if agent_type in entry.tags or any(tag in user_input.lower() for tag in entry.tags):
                relevant.append(entry)
        
        return relevant[:3]  # Return top 3 most relevant
    
    def _get_best_practices(self, agent_type: str) -> List[str]:
        """Get best practices relevant to the agent type."""
        practices = []
        
        # Map agent types to practice categories
        category_mapping = {
            "terraform": ["reliability", "cost_optimization"],
            "security": ["security"],
            "monitoring": ["performance", "reliability"],
            "ansible": ["reliability", "performance"],
            "kubernetes": ["performance", "reliability"]
        }
        
        categories = category_mapping.get(agent_type, ["reliability"])
        for category in categories:
            practices.extend(self.best_practices.get(category, []))
        
        return practices[:5]  # Return top 5 practices
    
    def _generate_recommendations(self, pattern: InfrastructurePattern, user_input: str) -> List[str]:
        """Generate specific recommendations based on the matched pattern."""
        recommendations = []
        
        if pattern.action == "create_web_server":
            recommendations = [
                "I'll help you create a web server infrastructure.",
                "Recommended: Start with a basic web server template and scale as needed.",
                "Consider implementing load balancing for high availability.",
                "Don't forget to configure security groups and SSL certificates."
            ]
        elif pattern.action == "create_database":
            recommendations = [
                "I'll help you set up a database infrastructure.",
                "Recommended: Use managed database services for better reliability.",
                "Implement proper backup and monitoring for your database.",
                "Consider read replicas for better performance."
            ]
        elif pattern.action == "security_scan":
            recommendations = [
                "I'll perform a comprehensive security assessment.",
                "This will include vulnerability scanning and configuration review.",
                "I'll provide recommendations for security improvements.",
                "Consider implementing automated security monitoring."
            ]
        elif pattern.action == "setup_monitoring":
            recommendations = [
                "I'll set up comprehensive monitoring for your infrastructure.",
                "This includes system metrics, application metrics, and alerting.",
                "I'll configure dashboards for better visibility.",
                "Set up automated alerts for critical issues."
            ]
        elif pattern.action == "cost_optimization":
            recommendations = [
                "I'll analyze your infrastructure costs and provide optimization recommendations.",
                "This includes right-sizing instances, reserved instances, and unused resource cleanup.",
                "I'll provide cost estimates and savings projections.",
                "Consider implementing auto-scaling and spot instances for flexible workloads."
            ]
        elif pattern.action == "create_api_infrastructure":
            recommendations = [
                "I'll set up a high-performance API infrastructure for you.",
                "This includes load balancing, caching, and monitoring for optimal performance.",
                "I'll implement rate limiting and API gateway for security and scalability.",
                "Consider implementing auto-scaling and health checks for reliability."
            ]
        elif pattern.action == "create_scalable_infrastructure":
            recommendations = [
                "I'll design a scalable infrastructure architecture for your needs.",
                "This includes load balancing, auto-scaling, and microservices architecture.",
                "I'll implement monitoring and performance optimization strategies.",
                "Consider container orchestration and distributed systems for maximum scalability."
            ]
        elif pattern.action == "create_blog_infrastructure":
            recommendations = [
                "I'll set up a secure blog infrastructure with SSL and backup.",
                "This includes web server, database, and content delivery network.",
                "I'll implement security measures and automated backup strategies.",
                "Consider implementing caching and CDN for better performance."
            ]
        elif pattern.action == "create_microservices_infrastructure":
            recommendations = [
                "I'll design a comprehensive microservices architecture for you.",
                "This includes API gateway, service mesh, and container orchestration.",
                "I'll implement service discovery, load balancing, and circuit breakers.",
                "Consider implementing distributed tracing and centralized logging."
            ]
        elif pattern.action == "create_container_infrastructure":
            recommendations = [
                "I'll set up a robust container infrastructure with Kubernetes.",
                "This includes container registry, orchestration, and service mesh.",
                "I'll implement auto-scaling, health checks, and rolling deployments.",
                "Consider implementing GitOps for continuous deployment."
            ]
        elif pattern.action == "create_high_performance_api":
            recommendations = [
                "I'll design a high-performance API infrastructure for optimal speed.",
                "This includes API gateway, load balancing, and intelligent caching.",
                "I'll implement rate limiting, request throttling, and response optimization.",
                "Consider implementing CDN and edge computing for global performance."
            ]
        elif pattern.action == "create_data_analytics_infrastructure":
            recommendations = [
                "I'll set up a comprehensive data analytics infrastructure.",
                "This includes data lake, data warehouse, and ETL pipelines.",
                "I'll implement real-time streaming and batch processing capabilities.",
                "Consider implementing data governance and quality monitoring."
            ]
        elif pattern.action == "create_multi_tier_web_app":
            recommendations = [
                "I'll design a scalable multi-tier web application architecture.",
                "This includes web tier, application tier, and database tier separation.",
                "I'll implement load balancing, caching, and database optimization.",
                "Consider implementing horizontal scaling and auto-scaling policies."
            ]
        elif pattern.action == "create_serverless_infrastructure":
            recommendations = [
                "I'll design a serverless architecture for cost-effective scaling.",
                "This includes function runtime, API gateway, and event-driven architecture.",
                "I'll implement auto-scaling, pay-per-use billing, and event sourcing.",
                "Consider implementing function composition and state management."
            ]
        elif pattern.action == "create_disaster_recovery_infrastructure":
            recommendations = [
                "I'll set up a comprehensive disaster recovery infrastructure.",
                "This includes backup systems, replication, and automated failover.",
                "I'll implement RTO and RPO optimization with geographic distribution.",
                "Consider implementing regular disaster recovery testing and validation."
            ]
        elif pattern.action == "create_compliance_infrastructure":
            recommendations = [
                "I'll design a compliance-ready infrastructure with security controls.",
                "This includes audit logging, access control, and data encryption.",
                "I'll implement compliance monitoring and automated reporting.",
                "Consider implementing data classification and retention policies."
            ]
        elif pattern.action == "create_cost_optimized_infrastructure":
            recommendations = [
                "I'll design a cost-optimized infrastructure with intelligent resource management.",
                "This includes cost monitoring, resource optimization, and automation.",
                "I'll implement reserved instances, spot instances, and auto-scaling.",
                "Consider implementing FinOps practices and cost allocation strategies."
            ]
        elif pattern.action == "create_monitoring_infrastructure":
            recommendations = [
                "I'll set up comprehensive monitoring and observability infrastructure.",
                "This includes metrics collection, log aggregation, and alerting systems.",
                "I'll implement distributed tracing and performance monitoring.",
                "Consider implementing AI-powered anomaly detection and predictive alerting."
            ]
        elif pattern.action == "create_cloud_migration_plan":
            recommendations = [
                "I'll create a comprehensive cloud migration strategy and plan.",
                "This includes assessment, migration strategy, and execution roadmap.",
                "I'll implement lift-and-shift, refactor, or re-architect approaches as needed.",
                "Consider implementing hybrid cloud and multi-cloud strategies."
            ]
        else:
            recommendations = [
                f"I'll help you with {pattern.action.replace('_', ' ')}.",
                "Let me analyze your requirements and provide the best solution.",
                "I'll include best practices and security considerations."
            ]
        
        return recommendations
    
    def _get_relevant_templates(self, agent_type: str) -> List[Dict[str, Any]]:
        """Get templates relevant to the agent type."""
        relevant = []
        
        for template in self.templates.values():
            if template["agent_type"] == agent_type:
                relevant.append(template)
        
        return relevant[:2]  # Return top 2 templates
    
    def _get_relevant_scenarios(self, user_input: str) -> List[Dict[str, Any]]:
        """Get scenarios relevant to the user input."""
        relevant = []
        
        for scenario in self.scenarios.values():
            if any(term in user_input.lower() for term in scenario["name"].lower().split()):
                relevant.append(scenario)
        
        return relevant[:2]  # Return top 2 scenarios
    
    def get_knowledge_by_category(self, category: str) -> List[KnowledgeEntry]:
        """Get all knowledge entries for a specific category."""
        return [entry for entry in self.knowledge_entries.values() if entry.category == category]
    
    def add_knowledge_entry(self, entry: KnowledgeEntry):
        """Add a new knowledge entry to the knowledge base."""
        self.knowledge_entries[entry.id] = entry
        logger.info(f"Added knowledge entry: {entry.id}")
    
    def update_knowledge_entry(self, entry_id: str, updates: Dict[str, Any]):
        """Update an existing knowledge entry."""
        if entry_id in self.knowledge_entries:
            entry = self.knowledge_entries[entry_id]
            for key, value in updates.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            entry.updated_at = datetime.now()
            logger.info(f"Updated knowledge entry: {entry_id}")
    
    def search_knowledge(self, query: str) -> List[KnowledgeEntry]:
        """Search knowledge entries by query."""
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge_entries.values():
            # Search in title, content, and tags
            if (query_lower in entry.title.lower() or 
                query_lower in entry.content.lower() or 
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
        
        # Sort by relevance (simple scoring)
        results.sort(key=lambda x: (
            query_lower in x.title.lower(),
            query_lower in x.content.lower(),
            x.confidence
        ), reverse=True)
        
        return results
    
    async def enhanced_search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Enhanced search using vector search and NLP."""
        results = []
        
        # Traditional search
        traditional_results = self.search_knowledge(query)
        for entry in traditional_results:
            results.append({
                "type": "traditional",
                "entry": entry,
                "score": 1.0,
                "source": "keyword_match"
            })
        
        # Vector search if available
        if self.vector_search_engine:
            try:
                vector_results = await self.vector_search_engine.search("infrastructure", query, k=5, score_threshold=0.3)
                for result in vector_results:
                    # Find corresponding knowledge entry
                    entry = self.knowledge_entries.get(result.id)
                    if entry:
                        results.append({
                            "type": "vector",
                            "entry": entry,
                            "score": result.score,
                            "source": "semantic_search"
                        })
            except Exception as e:
                logger.warning(f"Vector search failed: {str(e)}")
        
        # Remove duplicates and sort by score
        unique_results = {}
        for result in results:
            entry_id = result["entry"].id
            if entry_id not in unique_results or result["score"] > unique_results[entry_id]["score"]:
                unique_results[entry_id] = result
        
        final_results = list(unique_results.values())
        final_results.sort(key=lambda x: x["score"], reverse=True)
        
        return final_results
    
    def match_pattern(self, query: str) -> Optional[InfrastructurePattern]:
        """Match query against infrastructure patterns."""
        query_lower = query.lower()
        
        for pattern in self.infrastructure_patterns:
            if re.search(pattern.regex, query_lower, re.IGNORECASE):
                return pattern
        
        return None
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a query with enhanced capabilities."""
        context = context or {}
        
        # Enhanced NLP processing if available
        nlp_result = None
        if self.nlp_processor:
            try:
                nlp_result = self.nlp_processor.process_text(query)
                logger.info(f"NLP processing: intent={nlp_result.intent}, confidence={nlp_result.confidence}")
            except Exception as e:
                logger.warning(f"NLP processing failed: {str(e)}")
        
        # Enhanced knowledge search
        search_results = await self.enhanced_search_knowledge(query)
        
        # Find matching pattern
        pattern = self.match_pattern(query)
        
        if pattern:
            # Generate enhanced response
            response = self._generate_enhanced_response(pattern, context, nlp_result, search_results)
            return {
                "response": response,
                "confidence": pattern.confidence,
                "pattern": pattern.pattern,
                "agent_type": pattern.agent_type,
                "action": pattern.action,
                "nlp_analysis": nlp_result.__dict__ if nlp_result else None,
                "search_results": search_results[:3],  # Top 3 results
                "metadata": {
                    "query": query,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
            }
        else:
            # Enhanced fallback response
            response = self._generate_enhanced_fallback_response(query, context, nlp_result, search_results)
            return {
                "response": response,
                "confidence": 0.3,
                "pattern": "fallback",
                "agent_type": "general",
                "action": "general_response",
                "nlp_analysis": nlp_result.__dict__ if nlp_result else None,
                "search_results": search_results[:3],  # Top 3 results
                "metadata": {
                    "query": query,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
            }

