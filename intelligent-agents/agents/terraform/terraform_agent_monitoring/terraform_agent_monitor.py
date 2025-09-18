"""
Terraform Agent Monitoring System
Comprehensive monitoring and validation for Terraform Agent actions
"""

import json
import time
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import re

@dataclass
class TerraformActionMetrics:
    """Metrics for a single Terraform agent action"""
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

@dataclass
class TerraformPerformanceMetrics:
    """Overall performance metrics for Terraform agent"""
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

class TerraformAgentMonitor:
    """Comprehensive monitoring system for Terraform agent"""
    
    def __init__(self, monitoring_dir: str = None):
        # Set up monitoring directory structure
        if monitoring_dir is None:
            self.monitoring_dir = Path(__file__).parent
        else:
            self.monitoring_dir = Path(monitoring_dir)
        
        # Create subdirectories
        self.logs_dir = self.monitoring_dir / "logs"
        self.metrics_dir = self.monitoring_dir / "metrics"
        self.reports_dir = self.monitoring_dir / "reports"
        
        # Ensure directories exist
        self.logs_dir.mkdir(exist_ok=True)
        self.metrics_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Setup logging with organized structure
        self._setup_logging()
        
        # Initialize metrics
        self.actions: List[TerraformActionMetrics] = []
        self.performance_metrics = TerraformPerformanceMetrics()
        
        # Validation rules for Terraform
        self.validation_rules = self._load_terraform_validation_rules()
        
        self.logger.info("Terraform Agent Monitor initialized")
    
    def _setup_logging(self):
        """Setup comprehensive logging with organized structure"""
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = self.logs_dir / f"terraform_agent_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('terraform_agent_monitor')
    
    def _load_terraform_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules specifically for Terraform code"""
        return {
            "terraform_syntax": {
                "required_blocks": ["provider", "resource"],
                "forbidden_patterns": [
                    r"password\s*=\s*[\"'][^\"']*[\"']",
                    r"secret\s*=\s*[\"'][^\"']*[\"']",
                    r"api_key\s*=\s*[\"'][^\"']*[\"']"
                ],
                "required_variables": ["region", "environment"],
                "required_providers": ["aws", "azurerm", "google"]
            },
            "terraform_security": {
                "required_security_groups": True,
                "forbidden_public_access": ["rds", "elasticache", "redshift", "database"],
                "required_encryption": ["s3", "rds", "dynamodb", "storage"],
                "forbidden_hardcoded_credentials": True,
                "required_iam_roles": True
            },
            "terraform_cost_optimization": {
                "max_cost_per_month": 10000,
                "cost_warning_threshold": 5000,
                "suspicious_patterns": ["m5.24xlarge", "r5.24xlarge", "c5.24xlarge", "p3.16xlarge"],
                "required_autoscaling": True,
                "required_spot_instances": False
            },
            "terraform_architecture": {
                "required_components": ["networking", "compute", "storage"],
                "scalability_indicators": ["autoscaling", "load_balancer", "cloudfront", "cdn"],
                "monitoring_required": True,
                "backup_required": True,
                "disaster_recovery_required": False
            },
            "terraform_domain_specific": {
                "ml_patterns": ["sagemaker", "emr", "lambda", "s3"],
                "iot_patterns": ["iot_core", "kinesis", "dynamodb", "lambda"],
                "analytics_patterns": ["emr", "redshift", "athena", "glue"],
                "enterprise_patterns": ["eks", "istio", "prometheus", "grafana"]
            }
        }
    
    def start_terraform_action_monitoring(self, action_id: str, action_type: str, input_request: str) -> Dict[str, Any]:
        """Start monitoring a new Terraform agent action"""
        start_time = time.time()
        
        self.logger.info(f"Starting Terraform action monitoring: {action_id} - {action_type}")
        
        return {
            "action_id": action_id,
            "start_time": start_time,
            "action_type": action_type,
            "input_request": input_request
        }
    
    def validate_terraform_code(self, terraform_code: str, domain: str) -> Dict[str, Any]:
        """Validate generated Terraform code for correctness and best practices"""
        validation_results = {
            "syntax_valid": True,
            "security_compliant": True,
            "cost_optimized": True,
            "architecture_sound": True,
            "domain_appropriate": True,
            "issues": [],
            "warnings": [],
            "recommendations": [],
            "validation_score": 0.0
        }
        
        # Terraform syntax validation
        syntax_issues = self._validate_terraform_syntax(terraform_code)
        if syntax_issues:
            validation_results["syntax_valid"] = False
            validation_results["issues"].extend(syntax_issues)
        
        # Security validation
        security_issues = self._validate_terraform_security(terraform_code)
        if security_issues:
            validation_results["security_compliant"] = False
            validation_results["issues"].extend(security_issues)
        
        # Cost optimization validation
        cost_issues = self._validate_terraform_cost_optimization(terraform_code)
        if cost_issues:
            validation_results["cost_optimized"] = False
            validation_results["warnings"].extend(cost_issues)
        
        # Architecture validation
        architecture_issues = self._validate_terraform_architecture(terraform_code, domain)
        if architecture_issues:
            validation_results["architecture_sound"] = False
            validation_results["issues"].extend(architecture_issues)
        
        # Domain-specific validation
        domain_issues = self._validate_terraform_domain_specific(terraform_code, domain)
        if domain_issues:
            validation_results["domain_appropriate"] = False
            validation_results["issues"].extend(domain_issues)
        
        # Generate recommendations
        recommendations = self._generate_terraform_recommendations(terraform_code, domain)
        validation_results["recommendations"].extend(recommendations)
        
        # Calculate validation score
        validation_results["validation_score"] = self._calculate_validation_score(validation_results)
        
        return validation_results
    
    def _validate_terraform_syntax(self, terraform_code: str) -> List[str]:
        """Validate Terraform syntax and structure"""
        issues = []
        
        # Check for required blocks
        if "provider" not in terraform_code:
            issues.append("Missing provider block")
        if "resource" not in terraform_code:
            issues.append("Missing resource blocks")
        
        # Check for forbidden patterns
        forbidden_patterns = self.validation_rules["terraform_syntax"]["forbidden_patterns"]
        for pattern in forbidden_patterns:
            if re.search(pattern, terraform_code, re.IGNORECASE):
                issues.append(f"Security issue: Found hardcoded credentials pattern: {pattern}")
        
        # Check for required variables
        required_vars = self.validation_rules["terraform_syntax"]["required_variables"]
        for var in required_vars:
            if f"var.{var}" not in terraform_code and f'"{var}"' not in terraform_code:
                issues.append(f"Missing required variable: {var}")
        
        return issues
    
    def _validate_terraform_security(self, terraform_code: str) -> List[str]:
        """Validate Terraform security compliance"""
        issues = []
        
        # Check for public access to sensitive services
        forbidden_public = self.validation_rules["terraform_security"]["forbidden_public_access"]
        for service in forbidden_public:
            if f"aws_{service}" in terraform_code:
                if "publicly_accessible = true" in terraform_code:
                    issues.append(f"Security risk: {service} is publicly accessible")
        
        # Check for encryption
        required_encryption = self.validation_rules["terraform_security"]["required_encryption"]
        for service in required_encryption:
            if f"aws_{service}" in terraform_code:
                if "encryption" not in terraform_code.lower():
                    issues.append(f"Security issue: {service} should have encryption enabled")
        
        # Check for security groups
        if "aws_security_group" not in terraform_code:
            issues.append("Security issue: No security groups defined")
        
        # Check for IAM roles
        if "aws_iam_role" not in terraform_code and "aws_instance" in terraform_code:
            issues.append("Security issue: EC2 instances should have IAM roles")
        
        return issues
    
    def _validate_terraform_cost_optimization(self, terraform_code: str) -> List[str]:
        """Validate Terraform cost optimization"""
        warnings = []
        
        # Check for expensive instance types
        suspicious_patterns = self.validation_rules["terraform_cost_optimization"]["suspicious_patterns"]
        for pattern in suspicious_patterns:
            if pattern in terraform_code:
                warnings.append(f"Cost warning: Using expensive instance type {pattern}")
        
        # Check for missing cost optimization features
        if "aws_autoscaling_group" not in terraform_code and "t3" in terraform_code:
            warnings.append("Cost optimization: Consider using autoscaling for better cost efficiency")
        
        # Check for spot instances
        if "aws_instance" in terraform_code and "spot_instance_request" not in terraform_code:
            warnings.append("Cost optimization: Consider using spot instances for non-critical workloads")
        
        return warnings
    
    def _validate_terraform_architecture(self, terraform_code: str, domain: str) -> List[str]:
        """Validate Terraform architecture soundness"""
        issues = []
        
        # Check for required components
        required_components = self.validation_rules["terraform_architecture"]["required_components"]
        for component in required_components:
            if component == "networking" and "aws_vpc" not in terraform_code:
                issues.append("Architecture issue: Missing VPC for networking")
            elif component == "compute" and "aws_instance" not in terraform_code and "aws_ecs" not in terraform_code:
                issues.append("Architecture issue: Missing compute resources")
            elif component == "storage" and "aws_s3" not in terraform_code and "aws_rds" not in terraform_code:
                issues.append("Architecture issue: Missing storage resources")
        
        # Check for monitoring
        if "aws_cloudwatch" not in terraform_code:
            issues.append("Architecture issue: Missing CloudWatch monitoring")
        
        # Check for backup
        if "aws_rds" in terraform_code and "backup_retention_period" not in terraform_code:
            issues.append("Architecture issue: RDS should have backup retention configured")
        
        return issues
    
    def _validate_terraform_domain_specific(self, terraform_code: str, domain: str) -> List[str]:
        """Validate domain-specific Terraform patterns"""
        issues = []
        
        domain_patterns = self.validation_rules["terraform_domain_specific"]
        
        if domain == "ml":
            required_patterns = domain_patterns["ml_patterns"]
            for pattern in required_patterns:
                if pattern not in terraform_code:
                    issues.append(f"ML domain issue: Missing {pattern} for ML workloads")
        
        elif domain == "iot":
            required_patterns = domain_patterns["iot_patterns"]
            for pattern in required_patterns:
                if pattern not in terraform_code:
                    issues.append(f"IoT domain issue: Missing {pattern} for IoT workloads")
        
        elif domain == "analytics":
            required_patterns = domain_patterns["analytics_patterns"]
            for pattern in required_patterns:
                if pattern not in terraform_code:
                    issues.append(f"Analytics domain issue: Missing {pattern} for analytics workloads")
        
        elif domain == "enterprise":
            required_patterns = domain_patterns["enterprise_patterns"]
            for pattern in required_patterns:
                if pattern not in terraform_code:
                    issues.append(f"Enterprise domain issue: Missing {pattern} for enterprise workloads")
        
        return issues
    
    def _generate_terraform_recommendations(self, terraform_code: str, domain: str) -> List[str]:
        """Generate improvement recommendations for Terraform code"""
        recommendations = []
        
        # Monitoring recommendations
        if "aws_cloudwatch" not in terraform_code:
            recommendations.append("Add CloudWatch monitoring for better observability")
        
        # Backup recommendations
        if "aws_rds" in terraform_code and "backup_retention_period" not in terraform_code:
            recommendations.append("Configure RDS backup retention for data protection")
        
        # Security recommendations
        if "aws_s3" in terraform_code and "versioning" not in terraform_code:
            recommendations.append("Enable S3 versioning for data protection")
        
        # Performance recommendations
        if "aws_cloudfront" not in terraform_code and "aws_lb" in terraform_code:
            recommendations.append("Consider adding CloudFront for global content delivery")
        
        # Cost optimization recommendations
        if "aws_instance" in terraform_code and "aws_autoscaling_group" not in terraform_code:
            recommendations.append("Consider using autoscaling groups for better cost efficiency")
        
        return recommendations
    
    def _calculate_validation_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall validation score"""
        score = 100.0
        
        # Deduct points for issues
        score -= len(validation_results.get("issues", [])) * 10
        
        # Deduct points for warnings
        score -= len(validation_results.get("warnings", [])) * 5
        
        # Bonus for recommendations
        score += len(validation_results.get("recommendations", [])) * 2
        
        return max(0.0, min(100.0, score))
    
    def complete_terraform_action_monitoring(self, action_id: str, success: bool, 
                                           confidence_score: float, cost_estimate: float,
                                           complexity_score: int, validation_results: Dict[str, Any],
                                           domain: str, terraform_files_generated: int,
                                           implementation_steps: int,
                                           error_message: Optional[str] = None) -> TerraformActionMetrics:
        """Complete Terraform action monitoring and record metrics"""
        
        # Find the action start time
        start_time = None
        for action in self.actions:
            if action.action_id == action_id:
                start_time = action.timestamp
                break
        
        if start_time is None:
            start_time = datetime.now()
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create action metrics
        action_metrics = TerraformActionMetrics(
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
            implementation_steps=implementation_steps
        )
        
        # Record the action
        self.actions.append(action_metrics)
        
        # Update performance metrics
        self._update_terraform_performance_metrics()
        
        # Log the completion
        if success:
            self.logger.info(f"Terraform action completed successfully: {action_id} (confidence: {confidence_score:.2f}, domain: {domain})")
        else:
            self.logger.error(f"Terraform action failed: {action_id} - {error_message}")
        
        # Save metrics to file
        self._save_terraform_metrics()
        
        return action_metrics
    
    def _update_terraform_performance_metrics(self):
        """Update overall Terraform performance metrics"""
        if not self.actions:
            return
        
        total_actions = len(self.actions)
        successful_actions = sum(1 for action in self.actions if action.success)
        failed_actions = total_actions - successful_actions
        
        avg_processing_time = sum(action.processing_time for action in self.actions) / total_actions
        avg_confidence = sum(action.confidence_score for action in self.actions) / total_actions
        success_rate = successful_actions / total_actions if total_actions > 0 else 0
        
        # Calculate validation success rate
        validation_successes = sum(1 for action in self.actions 
                                 if action.validation_results and 
                                 action.validation_results.get("validation_score", 0) > 70)
        validation_success_rate = validation_successes / total_actions if total_actions > 0 else 0
        
        # Calculate Terraform generation rate
        terraform_generations = sum(1 for action in self.actions if action.terraform_files_generated > 0)
        terraform_generation_rate = terraform_generations / total_actions if total_actions > 0 else 0
        
        self.performance_metrics = TerraformPerformanceMetrics(
            total_actions=total_actions,
            successful_actions=successful_actions,
            failed_actions=failed_actions,
            average_processing_time=avg_processing_time,
            average_confidence=avg_confidence,
            success_rate=success_rate,
            validation_success_rate=validation_success_rate,
            terraform_generation_rate=terraform_generation_rate
        )
    
    def _save_terraform_metrics(self):
        """Save Terraform metrics to organized files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save action metrics
        actions_file = self.metrics_dir / f"terraform_actions_{timestamp}.json"
        with open(actions_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(action) for action in self.actions[-50:]], f, indent=2, default=str)
        
        # Save performance metrics
        performance_file = self.metrics_dir / f"terraform_performance_{timestamp}.json"
        with open(performance_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.performance_metrics), f, indent=2, default=str)
    
    def get_terraform_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive Terraform performance report"""
        recent_actions = [action for action in self.actions 
                         if action.timestamp > datetime.now() - timedelta(hours=24)]
        
        # Domain accuracy analysis
        domain_accuracy = {}
        for action in recent_actions:
            domain = action.domain
            if domain not in domain_accuracy:
                domain_accuracy[domain] = {"total": 0, "correct": 0}
            domain_accuracy[domain]["total"] += 1
            if action.success:
                domain_accuracy[domain]["correct"] += 1
        
        # Calculate accuracy percentages
        for domain in domain_accuracy:
            total = domain_accuracy[domain]["total"]
            correct = domain_accuracy[domain]["correct"]
            domain_accuracy[domain]["accuracy"] = correct / total if total > 0 else 0
        
        return {
            "overall_metrics": asdict(self.performance_metrics),
            "recent_actions": len(recent_actions),
            "domain_accuracy": domain_accuracy,
            "top_issues": self._get_terraform_top_issues(),
            "recommendations": self._get_terraform_system_recommendations()
        }
    
    def _get_terraform_top_issues(self) -> List[Dict[str, Any]]:
        """Get top issues from recent Terraform actions"""
        issues = []
        for action in self.actions[-20:]:  # Last 20 actions
            if action.validation_results and action.validation_results.get("issues"):
                issues.extend(action.validation_results["issues"])
        
        # Count issue frequency
        issue_counts = {}
        for issue in issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Return top 5 issues
        return [{"issue": issue, "count": count} for issue, count in 
                sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _get_terraform_system_recommendations(self) -> List[str]:
        """Get system-level recommendations for Terraform agent"""
        recommendations = []
        
        if self.performance_metrics.success_rate < 0.8:
            recommendations.append("Success rate is below 80%. Review error patterns and improve validation logic.")
        
        if self.performance_metrics.average_processing_time > 5.0:
            recommendations.append("Average processing time is high. Consider optimizing agent logic.")
        
        if self.performance_metrics.average_confidence < 0.7:
            recommendations.append("Average confidence is low. Consider improving reasoning logic.")
        
        if self.performance_metrics.validation_success_rate < 0.7:
            recommendations.append("Validation success rate is low. Review validation rules and improve code generation.")
        
        return recommendations
    
    def export_terraform_metrics(self, filename: str = None) -> str:
        """Export Terraform metrics to organized report"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"terraform_agent_report_{timestamp}.json"
        
        report_file = self.reports_dir / filename
        
        metrics_data = {
            "export_timestamp": datetime.now().isoformat(),
            "performance_metrics": asdict(self.performance_metrics),
            "recent_actions": [asdict(action) for action in self.actions[-100:]],  # Last 100 actions
            "performance_report": self.get_terraform_performance_report()
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, default=str)
        
        self.logger.info(f"Terraform metrics exported to {report_file}")
        return str(report_file)
