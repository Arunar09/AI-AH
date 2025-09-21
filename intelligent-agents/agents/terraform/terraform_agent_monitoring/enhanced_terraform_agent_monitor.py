"""
Enhanced Terraform Agent Monitoring System with Phase 4 Operational Intelligence
Comprehensive monitoring, validation, and operational intelligence for Terraform Agent actions
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import re

@dataclass
class MonitoringMetrics:
    """Enhanced monitoring metrics for operational intelligence"""
    infrastructure_health: float = 0.0
    performance_score: float = 0.0
    cost_efficiency: float = 0.0
    security_compliance: float = 0.0
    scalability_readiness: float = 0.0
    operational_readiness: float = 0.0
    monitoring_coverage: float = 0.0
    alerting_effectiveness: float = 0.0

@dataclass
class OperationalIntelligence:
    """Operational intelligence insights"""
    monitoring_setup: Dict[str, Any]
    performance_optimization: List[str]
    cost_optimization: List[str]
    security_recommendations: List[str]
    scalability_improvements: List[str]
    operational_best_practices: List[str]

@dataclass
class TerraformActionMetrics:
    """Enhanced metrics for a single Terraform agent action"""
    action_id: str
    timestamp: datetime
    action_type: str
    input_request: str
    processing_time: float
    success: bool
    error_message: Optional[str] = None
    confidence_score: float = 0.0
    cost_estimate: float = 0.0
    complexity_score: int = 0
    validation_results: Dict[str, Any] = None
    domain: str = "unknown"
    terraform_files_generated: int = 0
    implementation_steps: int = 0
    operational_metrics: Dict[str, Any] = None
    operational_intelligence: Dict[str, Any] = None

@dataclass
class TerraformPerformanceMetrics:
    """Enhanced performance metrics for Terraform agent"""
    total_actions: int = 0
    successful_actions: int = 0
    failed_actions: int = 0
    average_processing_time: float = 0.0
    average_confidence: float = 0.0
    success_rate: float = 0.0
    domain_accuracy: Dict[str, float] = None
    cost_accuracy: Dict[str, float] = None
    validation_success_rate: float = 0.0
    terraform_generation_rate: float = 0.0
    # Phase 4 Operational Intelligence Metrics
    infrastructure_health_score: float = 0.0
    performance_score: float = 0.0
    cost_efficiency_score: float = 0.0
    security_compliance_score: float = 0.0
    scalability_score: float = 0.0
    operational_readiness_score: float = 0.0
    monitoring_coverage_score: float = 0.0
    alerting_effectiveness_score: float = 0.0

class EnhancedTerraformAgentMonitor:
    """
    Enhanced monitoring system for the Intelligent Terraform Agent with Phase 4 operational intelligence.
    Tracks agent actions, validates generated Terraform code, and provides comprehensive operational insights.
    """
    
    def __init__(self):
        self.actions: List[TerraformActionMetrics] = []
        self.performance_metrics: TerraformPerformanceMetrics = TerraformPerformanceMetrics()
        self.operational_intelligence: Dict[str, Any] = {}
        
        # Enhanced monitoring directories
        self.log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        self.metrics_dir = os.path.join(os.path.dirname(__file__), 'metrics')
        self.reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        self.monitoring_dir = os.path.join(os.path.dirname(__file__), 'monitoring')
        self.optimization_dir = os.path.join(os.path.dirname(__file__), 'optimization')
        
        # Create directories
        for directory in [self.log_dir, self.metrics_dir, self.reports_dir, self.monitoring_dir, self.optimization_dir]:
            os.makedirs(directory, exist_ok=True)
        
        self._setup_logging()
        self.logger.info("Enhanced Terraform Agent Monitor initialized with Phase 4 operational intelligence")

    def _setup_logging(self):
        """Setup enhanced logging with operational intelligence"""
        log_file = os.path.join(self.log_dir, f"terraform_agent_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('enhanced_terraform_agent_monitor')

    def start_terraform_action_monitoring(self, action_id: str, action_type: str, input_request: str) -> Dict[str, Any]:
        """Start monitoring a new Terraform agent action with operational intelligence"""
        start_time = time.time()
        
        self.logger.info(f"Starting enhanced Terraform action monitoring: {action_id} - {action_type}")
        
        # Initialize operational intelligence tracking
        operational_context = {
            "monitoring_requirements": self._analyze_monitoring_requirements(input_request),
            "performance_requirements": self._analyze_performance_requirements(input_request),
            "cost_requirements": self._analyze_cost_requirements(input_request),
            "security_requirements": self._analyze_security_requirements(input_request),
            "scalability_requirements": self._analyze_scalability_requirements(input_request)
        }
        
        return {
            "action_id": action_id,
            "start_time": start_time,
            "action_type": action_type,
            "input_request": input_request,
            "operational_context": operational_context
        }

    def complete_terraform_action_monitoring(self, action_id: str, success: bool, confidence_score: float,
                                           cost_estimate: float, complexity_score: int,
                                           validation_results: Dict[str, Any], domain: str,
                                           terraform_files_generated: int, implementation_steps: int,
                                           error_message: Optional[str] = None):
        """Complete monitoring with enhanced operational intelligence analysis"""
        end_time = time.time()
        processing_time = end_time - time.time()
        
        # Enhanced metrics calculation
        operational_metrics = self._calculate_operational_metrics(
            success, confidence_score, cost_estimate, complexity_score,
            validation_results, domain, terraform_files_generated
        )
        
        # Operational intelligence analysis
        operational_intelligence = self._generate_operational_intelligence(
            action_id, success, validation_results, domain, operational_metrics
        )
        
        # Update performance metrics
        self._update_performance_metrics(success, confidence_score, cost_estimate, 
                                       complexity_score, operational_metrics)
        
        # Log enhanced results
        if success:
            self.logger.info(f"Enhanced Terraform action completed: {action_id} (confidence: {confidence_score:.2f}, domain: {domain})")
            self.logger.info(f"Operational Intelligence: {operational_intelligence['summary']}")
        else:
            self.logger.error(f"Enhanced Terraform action failed: {action_id} - {error_message}")
        
        # Store enhanced action data
        action_data = TerraformActionMetrics(
            action_id=action_id,
            timestamp=datetime.now(),
            action_type="terraform_generation",
            input_request="",  # Will be filled from context
            processing_time=processing_time,
            success=success,
            error_message=error_message,
            confidence_score=confidence_score,
            cost_estimate=cost_estimate,
            complexity_score=complexity_score,
            validation_results=validation_results,
            domain=domain,
            terraform_files_generated=terraform_files_generated,
            implementation_steps=implementation_steps,
            operational_metrics=operational_metrics,
            operational_intelligence=operational_intelligence
        )
        
        self.actions.append(action_data)
        
        # Export enhanced metrics and reports
        self._export_enhanced_metrics()
        self._export_operational_report()

    def _analyze_monitoring_requirements(self, request: str) -> Dict[str, Any]:
        """Analyze monitoring requirements from the request"""
        request_lower = request.lower()
        
        monitoring_requirements = {
            "basic_monitoring": True,  # Always include basic monitoring
            "performance_monitoring": False,
            "cost_monitoring": False,
            "security_monitoring": False,
            "compliance_monitoring": False,
            "custom_dashboards": False
        }
        
        # Analyze request for monitoring needs
        if any(keyword in request_lower for keyword in ["monitor", "observability", "metrics", "dashboard"]):
            monitoring_requirements["performance_monitoring"] = True
            monitoring_requirements["custom_dashboards"] = True
        
        if any(keyword in request_lower for keyword in ["cost", "budget", "optimize", "efficient"]):
            monitoring_requirements["cost_monitoring"] = True
        
        if any(keyword in request_lower for keyword in ["security", "compliance", "audit", "governance"]):
            monitoring_requirements["security_monitoring"] = True
            monitoring_requirements["compliance_monitoring"] = True
        
        return monitoring_requirements

    def _analyze_performance_requirements(self, request: str) -> Dict[str, Any]:
        """Analyze performance requirements from the request"""
        request_lower = request.lower()
        
        performance_requirements = {
            "high_performance": False,
            "scalability": False,
            "load_balancing": False,
            "caching": False,
            "cdn": False,
            "auto_scaling": False
        }
        
        # Analyze performance keywords
        if any(keyword in request_lower for keyword in ["high performance", "fast", "responsive", "optimized"]):
            performance_requirements["high_performance"] = True
        
        if any(keyword in request_lower for keyword in ["scale", "scalable", "growth", "traffic"]):
            performance_requirements["scalability"] = True
            performance_requirements["auto_scaling"] = True
        
        if any(keyword in request_lower for keyword in ["load balancer", "distributed", "multi-tier"]):
            performance_requirements["load_balancing"] = True
        
        if any(keyword in request_lower for keyword in ["cache", "caching", "redis", "memcached"]):
            performance_requirements["caching"] = True
        
        if any(keyword in request_lower for keyword in ["cdn", "global", "edge", "cloudfront"]):
            performance_requirements["cdn"] = True
        
        return performance_requirements

    def _analyze_cost_requirements(self, request: str) -> Dict[str, Any]:
        """Analyze cost optimization requirements from the request"""
        request_lower = request.lower()
        
        cost_requirements = {
            "cost_optimization": False,
            "budget_constraints": False,
            "reserved_instances": False,
            "spot_instances": False,
            "auto_scaling": False,
            "cost_monitoring": False
        }
        
        # Analyze cost keywords
        if any(keyword in request_lower for keyword in ["cost", "budget", "cheap", "affordable", "optimize"]):
            cost_requirements["cost_optimization"] = True
            cost_requirements["cost_monitoring"] = True
        
        if any(keyword in request_lower for keyword in ["budget", "limit", "constraint"]):
            cost_requirements["budget_constraints"] = True
        
        if any(keyword in request_lower for keyword in ["reserved", "commitment", "savings"]):
            cost_requirements["reserved_instances"] = True
        
        if any(keyword in request_lower for keyword in ["spot", "interruptible", "flexible"]):
            cost_requirements["spot_instances"] = True
        
        return cost_requirements

    def _analyze_security_requirements(self, request: str) -> Dict[str, Any]:
        """Analyze security requirements from the request"""
        request_lower = request.lower()
        
        security_requirements = {
            "high_security": False,
            "compliance": False,
            "encryption": False,
            "access_control": False,
            "monitoring": False,
            "audit": False
        }
        
        # Analyze security keywords
        if any(keyword in request_lower for keyword in ["security", "secure", "protected", "safe"]):
            security_requirements["high_security"] = True
            security_requirements["monitoring"] = True
        
        if any(keyword in request_lower for keyword in ["compliance", "audit", "governance", "policy"]):
            security_requirements["compliance"] = True
            security_requirements["audit"] = True
        
        if any(keyword in request_lower for keyword in ["encrypt", "encryption", "ssl", "tls"]):
            security_requirements["encryption"] = True
        
        if any(keyword in request_lower for keyword in ["access", "permission", "role", "iam"]):
            security_requirements["access_control"] = True
        
        return security_requirements

    def _analyze_scalability_requirements(self, request: str) -> Dict[str, Any]:
        """Analyze scalability requirements from the request"""
        request_lower = request.lower()
        
        scalability_requirements = {
            "high_scalability": False,
            "auto_scaling": False,
            "load_balancing": False,
            "microservices": False,
            "containerization": False,
            "serverless": False
        }
        
        # Analyze scalability keywords
        if any(keyword in request_lower for keyword in ["scale", "scalable", "growth", "traffic", "users"]):
            scalability_requirements["high_scalability"] = True
            scalability_requirements["auto_scaling"] = True
        
        if any(keyword in request_lower for keyword in ["load balancer", "distributed", "multi-tier"]):
            scalability_requirements["load_balancing"] = True
        
        if any(keyword in request_lower for keyword in ["microservice", "microservices", "distributed"]):
            scalability_requirements["microservices"] = True
        
        if any(keyword in request_lower for keyword in ["container", "docker", "kubernetes", "eks"]):
            scalability_requirements["containerization"] = True
        
        if any(keyword in request_lower for keyword in ["serverless", "lambda", "function"]):
            scalability_requirements["serverless"] = True
        
        return scalability_requirements

    def _calculate_operational_metrics(self, success: bool, confidence_score: float, 
                                     cost_estimate: float, complexity_score: int,
                                     validation_results: Dict[str, Any], domain: str,
                                     terraform_files_generated: int) -> Dict[str, Any]:
        """Calculate enhanced operational metrics"""
        metrics = {
            "infrastructure_health": 0.0,
            "performance_score": 0.0,
            "cost_efficiency": 0.0,
            "security_compliance": 0.0,
            "scalability_readiness": 0.0,
            "operational_readiness": 0.0,
            "monitoring_coverage": 0.0,
            "alerting_effectiveness": 0.0
        }
        
        # Calculate infrastructure health based on validation results
        if success and validation_results:
            syntax_valid = validation_results.get("syntax_valid", False)
            security_compliant = validation_results.get("security_compliant", False)
            cost_optimized = validation_results.get("cost_optimized", False)
            
            metrics["infrastructure_health"] = (0.4 * syntax_valid + 0.3 * security_compliant + 0.3 * cost_optimized)
        
        # Calculate performance score based on complexity and domain
        if domain in ["ml", "analytics", "enterprise"]:
            metrics["performance_score"] = min(0.9, 0.7 + (complexity_score * 0.02))
        else:
            metrics["performance_score"] = min(0.8, 0.6 + (complexity_score * 0.02))
        
        # Calculate cost efficiency
        if cost_estimate > 0:
            if cost_estimate < 100:
                metrics["cost_efficiency"] = 0.9
            elif cost_estimate < 500:
                metrics["cost_efficiency"] = 0.7
            elif cost_estimate < 1000:
                metrics["cost_efficiency"] = 0.5
            else:
                metrics["cost_efficiency"] = 0.3
        
        # Calculate security compliance
        if validation_results.get("security_compliant", False):
            metrics["security_compliance"] = 0.8
        else:
            metrics["security_compliance"] = 0.4
        
        # Calculate scalability readiness
        if domain in ["ml", "analytics", "enterprise"]:
            metrics["scalability_readiness"] = 0.9
        elif domain == "web":
            metrics["scalability_readiness"] = 0.7
        else:
            metrics["scalability_readiness"] = 0.5
        
        # Calculate operational readiness
        metrics["operational_readiness"] = (
            metrics["infrastructure_health"] * 0.3 +
            metrics["performance_score"] * 0.2 +
            metrics["cost_efficiency"] * 0.2 +
            metrics["security_compliance"] * 0.2 +
            metrics["scalability_readiness"] * 0.1
        )
        
        # Calculate monitoring coverage
        if terraform_files_generated > 0:
            metrics["monitoring_coverage"] = min(0.9, 0.5 + (terraform_files_generated * 0.1))
        else:
            metrics["monitoring_coverage"] = 0.3
        
        # Calculate alerting effectiveness
        if success and validation_results.get("security_compliant", False):
            metrics["alerting_effectiveness"] = 0.8
        else:
            metrics["alerting_effectiveness"] = 0.4
        
        return metrics

    def _generate_operational_intelligence(self, action_id: str, success: bool,
                                         validation_results: Dict[str, Any], domain: str,
                                         operational_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate operational intelligence insights"""
        
        intelligence = {
            "monitoring_setup": self._generate_monitoring_setup(domain, operational_metrics),
            "performance_optimization": self._generate_performance_optimization(domain, operational_metrics),
            "cost_optimization": self._generate_cost_optimization(operational_metrics),
            "security_recommendations": self._generate_security_recommendations(domain, operational_metrics),
            "scalability_improvements": self._generate_scalability_improvements(domain, operational_metrics),
            "operational_best_practices": self._generate_operational_best_practices(domain, operational_metrics),
            "summary": self._generate_operational_summary(operational_metrics)
        }
        
        return intelligence

    def _generate_monitoring_setup(self, domain: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate monitoring setup recommendations"""
        monitoring_setup = {
            "cloudwatch_dashboards": [],
            "alarms": [],
            "logs": [],
            "metrics": [],
            "custom_monitoring": []
        }
        
        # Domain-specific monitoring
        if domain == "ml":
            monitoring_setup["cloudwatch_dashboards"].append("ML Training Pipeline Dashboard")
            monitoring_setup["alarms"].extend([
                "SageMaker Training Job Status",
                "EMR Cluster Health",
                "S3 Data Processing Metrics"
            ])
            monitoring_setup["metrics"].extend([
                "Training Accuracy",
                "Model Performance",
                "Data Processing Throughput"
            ])
        elif domain == "analytics":
            monitoring_setup["cloudwatch_dashboards"].append("Data Analytics Dashboard")
            monitoring_setup["alarms"].extend([
                "Data Processing Pipeline Status",
                "Storage Utilization",
                "Query Performance"
            ])
        elif domain == "enterprise":
            monitoring_setup["cloudwatch_dashboards"].append("Enterprise Microservices Dashboard")
            monitoring_setup["alarms"].extend([
                "Service Health Checks",
                "API Response Times",
                "Database Performance"
            ])
        else:
            monitoring_setup["cloudwatch_dashboards"].append("Web Application Dashboard")
            monitoring_setup["alarms"].extend([
                "Application Health",
                "Response Times",
                "Error Rates"
            ])
        
        # Performance-based monitoring
        if metrics["performance_score"] > 0.7:
            monitoring_setup["custom_monitoring"].append("Advanced Performance Monitoring")
            monitoring_setup["metrics"].append("Custom Performance Metrics")
        
        # Security-based monitoring
        if metrics["security_compliance"] > 0.7:
            monitoring_setup["alarms"].extend([
                "Security Events",
                "Access Violations",
                "Compliance Status"
            ])
        
        return monitoring_setup

    def _generate_performance_optimization(self, domain: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Domain-specific optimizations
        if domain == "ml":
            recommendations.extend([
                "Implement SageMaker Spot Instances for cost optimization",
                "Use EMR with appropriate instance types for data processing",
                "Implement S3 Intelligent Tiering for data storage",
                "Add CloudFront for model serving optimization"
            ])
        elif domain == "analytics":
            recommendations.extend([
                "Implement Redshift Spectrum for large-scale analytics",
                "Use Athena for ad-hoc queries",
                "Implement data partitioning for better performance",
                "Add caching layers for frequently accessed data"
            ])
        elif domain == "enterprise":
            recommendations.extend([
                "Implement API Gateway caching",
                "Use Application Load Balancer with health checks",
                "Implement database connection pooling",
                "Add CDN for static content delivery"
            ])
        else:
            recommendations.extend([
                "Implement auto-scaling for web applications",
                "Use CloudFront for global content delivery",
                "Implement database read replicas",
                "Add caching for improved performance"
            ])
        
        # Performance score-based optimizations
        if metrics["performance_score"] < 0.6:
            recommendations.extend([
                "Review and optimize resource allocation",
                "Implement performance monitoring and alerting",
                "Consider upgrading to higher-performance instances",
                "Implement caching strategies"
            ])
        
        return recommendations

    def _generate_cost_optimization(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        # Cost efficiency-based recommendations
        if metrics["cost_efficiency"] < 0.5:
            recommendations.extend([
                "Implement Reserved Instances for predictable workloads",
                "Use Spot Instances for flexible workloads",
                "Implement auto-scaling to match demand",
                "Review and optimize storage costs"
            ])
        
        if metrics["cost_efficiency"] < 0.7:
            recommendations.extend([
                "Implement cost monitoring and budgeting",
                "Use AWS Cost Explorer for cost analysis",
                "Consider serverless options for variable workloads",
                "Implement resource tagging for cost tracking"
            ])
        
        # General cost optimizations
        recommendations.extend([
            "Implement cost monitoring dashboards",
            "Set up budget alerts and notifications",
            "Regular cost reviews and optimization",
            "Implement resource lifecycle management"
        ])
        
        return recommendations

    def _generate_security_recommendations(self, domain: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Domain-specific security
        if domain == "ml":
            recommendations.extend([
                "Implement data encryption at rest and in transit",
                "Use IAM roles for SageMaker and EMR access",
                "Implement VPC endpoints for secure data access",
                "Add security scanning for ML models"
            ])
        elif domain == "analytics":
            recommendations.extend([
                "Implement data classification and tagging",
                "Use encryption for sensitive data",
                "Implement access controls for data lakes",
                "Add audit logging for data access"
            ])
        elif domain == "enterprise":
            recommendations.extend([
                "Implement microservices security patterns",
                "Use API Gateway with authentication",
                "Implement service mesh security",
                "Add comprehensive logging and monitoring"
            ])
        else:
            recommendations.extend([
                "Implement WAF for web application protection",
                "Use SSL/TLS for all communications",
                "Implement proper IAM policies",
                "Add security monitoring and alerting"
            ])
        
        # Security compliance-based recommendations
        if metrics["security_compliance"] < 0.7:
            recommendations.extend([
                "Implement comprehensive security scanning",
                "Add compliance monitoring and reporting",
                "Implement security best practices",
                "Regular security audits and reviews"
            ])
        
        return recommendations

    def _generate_scalability_improvements(self, domain: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate scalability improvement recommendations"""
        recommendations = []
        
        # Domain-specific scalability
        if domain == "ml":
            recommendations.extend([
                "Implement distributed training with multiple instances",
                "Use SageMaker multi-model endpoints",
                "Implement data pipeline auto-scaling",
                "Add model versioning and A/B testing"
            ])
        elif domain == "analytics":
            recommendations.extend([
                "Implement data partitioning strategies",
                "Use Redshift auto-scaling",
                "Implement query optimization",
                "Add data lifecycle management"
            ])
        elif domain == "enterprise":
            recommendations.extend([
                "Implement microservices auto-scaling",
                "Use container orchestration (ECS/EKS)",
                "Implement service discovery",
                "Add load balancing and health checks"
            ])
        else:
            recommendations.extend([
                "Implement horizontal scaling",
                "Use auto-scaling groups",
                "Implement database scaling",
                "Add CDN for global distribution"
            ])
        
        # Scalability readiness-based recommendations
        if metrics["scalability_readiness"] < 0.7:
            recommendations.extend([
                "Review and improve scalability architecture",
                "Implement comprehensive monitoring",
                "Add performance testing and optimization",
                "Plan for future growth and scaling"
            ])
        
        return recommendations

    def _generate_operational_best_practices(self, domain: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate operational best practices"""
        practices = []
        
        # General operational practices
        practices.extend([
            "Implement Infrastructure as Code (IaC) best practices",
            "Use version control for all infrastructure changes",
            "Implement automated testing and validation",
            "Add comprehensive documentation and runbooks"
        ])
        
        # Domain-specific practices
        if domain == "ml":
            practices.extend([
                "Implement MLOps practices for model lifecycle",
                "Use version control for ML models and data",
                "Implement automated model testing and validation",
                "Add model performance monitoring and alerting"
            ])
        elif domain == "analytics":
            practices.extend([
                "Implement data governance and quality checks",
                "Use automated data pipeline testing",
                "Implement data lineage tracking",
                "Add data quality monitoring and alerting"
            ])
        elif domain == "enterprise":
            practices.extend([
                "Implement microservices best practices",
                "Use service mesh for communication",
                "Implement distributed tracing",
                "Add comprehensive service monitoring"
            ])
        else:
            practices.extend([
                "Implement web application best practices",
                "Use CI/CD for deployment automation",
                "Implement comprehensive testing strategies",
                "Add performance and security monitoring"
            ])
        
        # Operational readiness-based practices
        if metrics["operational_readiness"] < 0.7:
            practices.extend([
                "Improve operational processes and procedures",
                "Implement comprehensive monitoring and alerting",
                "Add disaster recovery and backup strategies",
                "Regular operational reviews and improvements"
            ])
        
        return practices

    def _generate_operational_summary(self, metrics: Dict[str, Any]) -> str:
        """Generate operational intelligence summary"""
        summary_parts = []
        
        # Infrastructure health
        if metrics["infrastructure_health"] > 0.8:
            summary_parts.append("✅ Infrastructure is healthy and well-configured")
        elif metrics["infrastructure_health"] > 0.6:
            summary_parts.append("⚠️ Infrastructure needs some improvements")
        else:
            summary_parts.append("❌ Infrastructure requires significant improvements")
        
        # Performance
        if metrics["performance_score"] > 0.8:
            summary_parts.append("✅ Performance is optimized for the workload")
        elif metrics["performance_score"] > 0.6:
            summary_parts.append("⚠️ Performance can be improved with optimization")
        else:
            summary_parts.append("❌ Performance needs significant optimization")
        
        # Cost efficiency
        if metrics["cost_efficiency"] > 0.7:
            summary_parts.append("✅ Cost efficiency is good")
        elif metrics["cost_efficiency"] > 0.5:
            summary_parts.append("⚠️ Cost optimization opportunities available")
        else:
            summary_parts.append("❌ Cost optimization is needed")
        
        # Security
        if metrics["security_compliance"] > 0.8:
            summary_parts.append("✅ Security compliance is strong")
        elif metrics["security_compliance"] > 0.6:
            summary_parts.append("⚠️ Security can be improved")
        else:
            summary_parts.append("❌ Security improvements are needed")
        
        # Scalability
        if metrics["scalability_readiness"] > 0.8:
            summary_parts.append("✅ Scalability is well-prepared")
        elif metrics["scalability_readiness"] > 0.6:
            summary_parts.append("⚠️ Scalability can be improved")
        else:
            summary_parts.append("❌ Scalability improvements are needed")
        
        # Overall operational readiness
        if metrics["operational_readiness"] > 0.8:
            summary_parts.append("🚀 Overall operational readiness is excellent")
        elif metrics["operational_readiness"] > 0.6:
            summary_parts.append("📈 Operational readiness is good with room for improvement")
        else:
            summary_parts.append("🔧 Operational readiness needs significant improvement")
        
        return "\n".join(summary_parts)

    def _update_performance_metrics(self, success: bool, confidence_score: float, 
                                 cost_estimate: float, complexity_score: int,
                                 operational_metrics: Dict[str, Any]):
        """Update enhanced performance metrics"""
        self.performance_metrics.total_actions += 1
        
        if success:
            self.performance_metrics.successful_actions += 1
        else:
            self.performance_metrics.failed_actions += 1
        
        # Update averages
        total_actions = self.performance_metrics.total_actions
        if total_actions > 0:
            self.performance_metrics.average_confidence = (
                (self.performance_metrics.average_confidence * (total_actions - 1) + confidence_score) / total_actions
            )
        
        # Update operational metrics
        for key, value in operational_metrics.items():
            if hasattr(self.performance_metrics, key):
                setattr(self.performance_metrics, key, value)

    def _export_enhanced_metrics(self):
        """Export enhanced metrics to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.metrics_dir, f"terraform_operational_metrics_{timestamp}.json")
        
        metrics_data = {
            "export_timestamp": datetime.now().isoformat(),
            "performance_metrics": asdict(self.performance_metrics),
            "recent_actions": [asdict(action) for action in self.actions[-10:]] if self.actions else [],
            "operational_intelligence": self.operational_intelligence
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, default=str)
        
        self.logger.info(f"Enhanced metrics exported to {filename}")

    def _export_operational_report(self):
        """Export comprehensive operational report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"terraform_operational_report_{timestamp}.json")
        
        report_data = {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_actions": self.performance_metrics.total_actions,
                "success_rate": (
                    self.performance_metrics.successful_actions / 
                    max(1, self.performance_metrics.total_actions)
                ),
                "average_confidence": self.performance_metrics.average_confidence,
                "operational_readiness": self.performance_metrics.operational_readiness_score
            },
            "performance_metrics": asdict(self.performance_metrics),
            "recent_actions": [asdict(action) for action in self.actions[-5:]] if self.actions else [],
            "operational_intelligence": self.operational_intelligence
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        self.logger.info(f"Operational report exported to {filename}")

    def validate_terraform_code(self, terraform_content: str, domain: str) -> Dict[str, Any]:
        """Enhanced Terraform code validation with operational intelligence"""
        validation_results = {
            "syntax_valid": False,
            "security_compliant": False,
            "cost_optimized": False,
            "monitoring_included": False,
            "scalability_ready": False,
            "operational_ready": False,
            "recommendations": []
        }
        
        if not terraform_content:
            return validation_results
        
        # Basic syntax validation
        validation_results["syntax_valid"] = self._validate_syntax(terraform_content)
        
        # Security validation
        validation_results["security_compliant"] = self._validate_security(terraform_content)
        
        # Cost optimization validation
        validation_results["cost_optimized"] = self._validate_cost_optimization(terraform_content)
        
        # Monitoring validation
        validation_results["monitoring_included"] = self._validate_monitoring(terraform_content)
        
        # Scalability validation
        validation_results["scalability_ready"] = self._validate_scalability(terraform_content)
        
        # Operational readiness
        validation_results["operational_ready"] = self._validate_operational_readiness(terraform_content)
        
        # Generate recommendations
        validation_results["recommendations"] = self._generate_validation_recommendations(
            validation_results, domain
        )
        
        return validation_results

    def _validate_syntax(self, content: str) -> bool:
        """Validate Terraform syntax"""
        # Basic syntax checks
        required_elements = ['resource "', 'provider "', 'terraform {']
        return all(element in content for element in required_elements)

    def _validate_security(self, content: str) -> bool:
        """Validate security compliance"""
        security_indicators = [
            'encryption',
            'iam',
            'security_group',
            'vpc',
            'private_subnet'
        ]
        return any(indicator in content.lower() for indicator in security_indicators)

    def _validate_cost_optimization(self, content: str) -> bool:
        """Validate cost optimization"""
        cost_indicators = [
            'auto_scaling',
            'spot_instance',
            'reserved_instance',
            'cloudwatch',
            's3_lifecycle'
        ]
        return any(indicator in content.lower() for indicator in cost_indicators)

    def _validate_monitoring(self, content: str) -> bool:
        """Validate monitoring setup"""
        monitoring_indicators = [
            'cloudwatch',
            'monitoring',
            'alarm',
            'dashboard',
            'log_group'
        ]
        return any(indicator in content.lower() for indicator in monitoring_indicators)

    def _validate_scalability(self, content: str) -> bool:
        """Validate scalability readiness"""
        scalability_indicators = [
            'auto_scaling',
            'load_balancer',
            'target_group',
            'launch_template',
            'scaling_policy'
        ]
        return any(indicator in content.lower() for indicator in scalability_indicators)

    def _validate_operational_readiness(self, content: str) -> bool:
        """Validate operational readiness"""
        operational_indicators = [
            'cloudwatch',
            'monitoring',
            'alarm',
            'iam',
            'security_group',
            'vpc'
        ]
        return sum(1 for indicator in operational_indicators if indicator in content.lower()) >= 3

    def _generate_validation_recommendations(self, validation_results: Dict[str, Any], domain: str) -> List[str]:
        """Generate validation recommendations"""
        recommendations = []
        
        if not validation_results["syntax_valid"]:
            recommendations.append("Fix Terraform syntax errors")
        
        if not validation_results["security_compliant"]:
            recommendations.append("Add security groups, IAM roles, and encryption")
        
        if not validation_results["cost_optimized"]:
            recommendations.append("Implement cost optimization strategies")
        
        if not validation_results["monitoring_included"]:
            recommendations.append("Add CloudWatch monitoring and alerting")
        
        if not validation_results["scalability_ready"]:
            recommendations.append("Implement auto-scaling and load balancing")
        
        if not validation_results["operational_ready"]:
            recommendations.append("Improve operational readiness with monitoring and security")
        
        # Domain-specific recommendations
        if domain == "ml":
            recommendations.append("Add SageMaker monitoring and model performance tracking")
        elif domain == "analytics":
            recommendations.append("Add data pipeline monitoring and cost optimization")
        elif domain == "enterprise":
            recommendations.append("Add microservices monitoring and service mesh")
        else:
            recommendations.append("Add web application monitoring and performance optimization")
        
        return recommendations

    def export_metrics(self) -> str:
        """Export all collected metrics to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.metrics_dir, f"terraform_performance_{timestamp}.json")
        
        metrics_data = {
            "export_timestamp": datetime.now().isoformat(),
            "performance_metrics": asdict(self.performance_metrics),
            "recent_actions": [asdict(action) for action in self.actions]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, default=str)
        
        self.logger.info(f"Metrics exported to {filename}")
        return filename

    def export_report(self) -> str:
        """Export comprehensive report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"terraform_agent_report_{timestamp}.json")
        
        report_data = {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_actions": self.performance_metrics.total_actions,
                "success_rate": (
                    self.performance_metrics.successful_actions / 
                    max(1, self.performance_metrics.total_actions)
                ),
                "average_confidence": self.performance_metrics.average_confidence
            },
            "performance_metrics": asdict(self.performance_metrics),
            "recent_actions": [asdict(action) for action in self.actions]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        self.logger.info(f"Report exported to {filename}")
        return filename



