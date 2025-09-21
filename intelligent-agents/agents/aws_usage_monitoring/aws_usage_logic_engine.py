"""
AWS Usage Monitoring Agent - Logic Engine
Log^2 approach: Logic-driven functionality with log monitoring
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class MonitoringDomain(Enum):
    COST = "cost_monitoring"
    RESOURCE = "resource_monitoring"
    SECURITY = "security_monitoring"
    PERFORMANCE = "performance_monitoring"
    COMPLIANCE = "compliance_monitoring"

@dataclass
class MonitoringRule:
    """Individual monitoring rule definition"""
    name: str
    domain: MonitoringDomain
    threshold: float
    operator: str  # '>', '<', '>=', '<=', '==', '!='
    severity: str   # 'low', 'medium', 'high', 'critical'
    action: str    # 'alert', 'auto_fix', 'escalate', 'log'
    description: str

@dataclass
class LogicWorkflow:
    """Logic workflow definition"""
    name: str
    steps: List[str]
    conditions: Dict[str, Any]
    actions: List[str]
    dependencies: List[str]

class AWSUsageLogicEngine:
    """Core logic definition and execution for AWS monitoring"""
    
    def __init__(self):
        self.rules = {}
        self.workflows = {}
        self.constraints = {}
        self.patterns = {}
        self._initialize_default_logic()
    
    def _initialize_default_logic(self):
        """Initialize default AWS monitoring logic with Free Tier limits"""
        self._initialize_free_tier_limits()
        self._initialize_cost_conscious_rules()
        self._initialize_free_tier_thresholds()
        
        # Cost Monitoring Rules
        cost_rules = [
            MonitoringRule(
                name="daily_cost_threshold",
                domain=MonitoringDomain.COST,
                threshold=5.0,
                operator=">",
                severity="high",
                action="alert",
                description="Alert if daily cost exceeds $5"
            ),
            MonitoringRule(
                name="monthly_budget_alert",
                domain=MonitoringDomain.COST,
                threshold=120.0,  # 80% of $150 budget
                operator=">",
                severity="critical",
                action="escalate",
                description="Alert if monthly cost exceeds 80% of budget"
            ),
            MonitoringRule(
                name="cost_spike_detection",
                domain=MonitoringDomain.COST,
                threshold=2.0,  # 2x normal daily cost
                operator=">",
                severity="high",
                action="alert",
                description="Alert on cost spikes"
            ),
            MonitoringRule(
                name="unused_resource_cost",
                domain=MonitoringDomain.COST,
                threshold=1.0,  # $1/day for unused resources
                operator=">",
                severity="medium",
                action="auto_fix",
                description="Auto-optimize unused resources"
            )
        ]
        
        # Resource Monitoring Rules
        resource_rules = [
            MonitoringRule(
                name="ec2_utilization_high",
                domain=MonitoringDomain.RESOURCE,
                threshold=80.0,
                operator=">",
                severity="medium",
                action="alert",
                description="Alert if EC2 utilization > 80%"
            ),
            MonitoringRule(
                name="rds_connection_high",
                domain=MonitoringDomain.RESOURCE,
                threshold=90.0,
                operator=">",
                severity="high",
                action="alert",
                description="Alert if RDS connections > 90%"
            ),
            MonitoringRule(
                name="s3_storage_high",
                domain=MonitoringDomain.RESOURCE,
                threshold=4.5,  # 90% of 5GB free tier
                operator=">",
                severity="medium",
                action="alert",
                description="Alert if S3 storage > 4.5GB"
            ),
            MonitoringRule(
                name="lambda_invocations_high",
                domain=MonitoringDomain.RESOURCE,
                threshold=800000,  # 80% of 1M free tier
                operator=">",
                severity="medium",
                action="alert",
                description="Alert if Lambda invocations > 800K"
            )
        ]
        
        # Security Monitoring Rules
        security_rules = [
            MonitoringRule(
                name="unauthorized_access",
                domain=MonitoringDomain.SECURITY,
                threshold=0,  # Any unauthorized access
                operator=">",
                severity="critical",
                action="escalate",
                description="Alert on unauthorized access attempts"
            ),
            MonitoringRule(
                name="root_user_usage",
                domain=MonitoringDomain.SECURITY,
                threshold=0,  # Any root user usage
                operator=">",
                severity="high",
                action="alert",
                description="Alert on root user usage"
            ),
            MonitoringRule(
                name="public_s3_bucket",
                domain=MonitoringDomain.SECURITY,
                threshold=0,  # Any public S3 bucket
                operator=">",
                severity="high",
                action="alert",
                description="Alert on public S3 buckets"
            ),
            MonitoringRule(
                name="unencrypted_data",
                domain=MonitoringDomain.SECURITY,
                threshold=0,  # Any unencrypted data
                operator=">",
                severity="medium",
                action="alert",
                description="Alert on unencrypted data"
            )
        ]
        
        # Performance Monitoring Rules
        performance_rules = [
            MonitoringRule(
                name="api_latency_high",
                domain=MonitoringDomain.PERFORMANCE,
                threshold=1000,  # 1 second
                operator=">",
                severity="medium",
                action="alert",
                description="Alert if API latency > 1s"
            ),
            MonitoringRule(
                name="error_rate_high",
                domain=MonitoringDomain.PERFORMANCE,
                threshold=5.0,  # 5%
                operator=">",
                severity="high",
                action="alert",
                description="Alert if error rate > 5%"
            ),
            MonitoringRule(
                name="availability_low",
                domain=MonitoringDomain.PERFORMANCE,
                threshold=99.0,  # 99%
                operator="<",
                severity="critical",
                action="escalate",
                description="Alert if availability < 99%"
            ),
            MonitoringRule(
                name="response_time_high",
                domain=MonitoringDomain.PERFORMANCE,
                threshold=500,  # 500ms
                operator=">",
                severity="medium",
                action="alert",
                description="Alert if response time > 500ms"
            )
        ]
        
        # Store rules by domain
        self.rules[MonitoringDomain.COST] = cost_rules
        self.rules[MonitoringDomain.RESOURCE] = resource_rules
        self.rules[MonitoringDomain.SECURITY] = security_rules
        self.rules[MonitoringDomain.PERFORMANCE] = performance_rules
        
        # Define workflows
        self._define_workflows()
        
        # Define constraints
        self._define_constraints()
    
    def _define_workflows(self):
        """Define monitoring workflows"""
        
        # Cost Optimization Workflow
        cost_optimization_workflow = LogicWorkflow(
            name="cost_optimization",
            steps=[
                "collect_cost_data",
                "analyze_cost_patterns",
                "identify_optimization_opportunities",
                "generate_recommendations",
                "apply_optimizations"
            ],
            conditions={
                "daily_cost": "> 3.0",
                "unused_resources": "> 0"
            },
            actions=[
                "terminate_unused_resources",
                "right_size_instances",
                "optimize_storage_classes",
                "schedule_resources"
            ],
            dependencies=["cost_monitoring", "resource_monitoring"]
        )
        
        # Security Hardening Workflow
        security_hardening_workflow = LogicWorkflow(
            name="security_hardening",
            steps=[
                "scan_security_configurations",
                "identify_vulnerabilities",
                "assess_compliance",
                "generate_security_recommendations",
                "apply_security_fixes"
            ],
            conditions={
                "vulnerabilities": "> 0",
                "compliance_violations": "> 0"
            },
            actions=[
                "encrypt_unencrypted_data",
                "restrict_public_access",
                "update_security_groups",
                "enable_logging"
            ],
            dependencies=["security_monitoring", "compliance_monitoring"]
        )
        
        # Performance Optimization Workflow
        performance_optimization_workflow = LogicWorkflow(
            name="performance_optimization",
            steps=[
                "collect_performance_metrics",
                "analyze_performance_patterns",
                "identify_bottlenecks",
                "generate_optimization_recommendations",
                "apply_performance_improvements"
            ],
            conditions={
                "latency": "> 500",
                "error_rate": "> 2.0",
                "utilization": "> 80"
            },
            actions=[
                "scale_resources",
                "optimize_database_queries",
                "implement_caching",
                "load_balance_traffic"
            ],
            dependencies=["performance_monitoring", "resource_monitoring"]
        )
        
        self.workflows["cost_optimization"] = cost_optimization_workflow
        self.workflows["security_hardening"] = security_hardening_workflow
        self.workflows["performance_optimization"] = performance_optimization_workflow
    
    def _define_constraints(self):
        """Define operational constraints"""
        
        self.constraints = {
            "budget_limits": {
                "daily_limit": 5.0,
                "monthly_limit": 150.0,
                "quarterly_limit": 450.0
            },
            "resource_limits": {
                "max_ec2_instances": 10,
                "max_rds_instances": 5,
                "max_s3_buckets": 20,
                "max_lambda_functions": 50
            },
            "performance_limits": {
                "max_latency": 2000,  # 2 seconds
                "min_availability": 99.0,  # 99%
                "max_error_rate": 1.0  # 1%
            },
            "security_requirements": {
                "encryption_required": True,
                "public_access_forbidden": True,
                "root_user_forbidden": True,
                "mfa_required": True
            }
        }
    
    def define_logic(self, domain: MonitoringDomain, rules: List[MonitoringRule]):
        """Define logic for specific domain"""
        self.rules[domain] = rules
    
    def execute_logic(self, domain: MonitoringDomain, input_data: Dict[str, Any]) -> tuple:
        """Execute logic and generate logs"""
        
        # Get rules for domain
        domain_rules = self.rules.get(domain, [])
        
        # Execute rules
        results = []
        execution_logs = {
            'domain': domain.value,
            'timestamp': datetime.datetime.now().isoformat(),
            'input': input_data,
            'rules_evaluated': [],
            'results': [],
            'performance': {},
            'errors': [],
            'success': True
        }
        
        start_time = datetime.datetime.now()
        
        try:
            for rule in domain_rules:
                rule_result = self._evaluate_rule(rule, input_data)
                results.append(rule_result)
                execution_logs['rules_evaluated'].append(rule.name)
                execution_logs['results'].append(rule_result)
            
            execution_logs['success'] = True
            
        except Exception as e:
            execution_logs['errors'].append(str(e))
            execution_logs['success'] = False
        
        end_time = datetime.datetime.now()
        execution_logs['performance'] = {
            'execution_time_ms': (end_time - start_time).total_seconds() * 1000,
            'rules_evaluated': len(domain_rules),
            'success_rate': len([r for r in results if r['success']]) / len(results) if results else 0
        }
        
        return results, execution_logs
    
    def _evaluate_rule(self, rule: MonitoringRule, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single rule"""
        
        # Get the value to evaluate
        value = input_data.get(rule.name.split('_')[0], 0)  # Extract metric name
        
        # Evaluate the rule
        if rule.operator == '>':
            triggered = value > rule.threshold
        elif rule.operator == '<':
            triggered = value < rule.threshold
        elif rule.operator == '>=':
            triggered = value >= rule.threshold
        elif rule.operator == '<=':
            triggered = value <= rule.threshold
        elif rule.operator == '==':
            triggered = value == rule.threshold
        elif rule.operator == '!=':
            triggered = value != rule.threshold
        else:
            triggered = False
        
        return {
            'rule_name': rule.name,
            'domain': rule.domain.value,
            'threshold': rule.threshold,
            'actual_value': value,
            'operator': rule.operator,
            'triggered': triggered,
            'severity': rule.severity,
            'action': rule.action,
            'description': rule.description,
            'success': True,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def get_workflow(self, workflow_name: str) -> Optional[LogicWorkflow]:
        """Get workflow by name"""
        return self.workflows.get(workflow_name)
    
    def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow"""
        
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            return {'error': f'Workflow {workflow_name} not found'}
        
        # Check conditions
        conditions_met = self._check_workflow_conditions(workflow, input_data)
        if not conditions_met:
            return {'error': 'Workflow conditions not met'}
        
        # Execute workflow steps
        results = []
        for step in workflow.steps:
            step_result = self._execute_workflow_step(step, input_data)
            results.append(step_result)
        
        return {
            'workflow_name': workflow_name,
            'steps_executed': workflow.steps,
            'results': results,
            'success': all(r.get('success', False) for r in results),
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def _check_workflow_conditions(self, workflow: LogicWorkflow, input_data: Dict[str, Any]) -> bool:
        """Check if workflow conditions are met"""
        
        for condition_key, condition_value in workflow.conditions.items():
            actual_value = input_data.get(condition_key, 0)
            
            if isinstance(condition_value, str):
                # Parse condition (e.g., "> 3.0")
                operator, threshold = condition_value.split()
                threshold = float(threshold)
                
                if operator == '>' and actual_value <= threshold:
                    return False
                elif operator == '<' and actual_value >= threshold:
                    return False
                elif operator == '>=' and actual_value < threshold:
                    return False
                elif operator == '<=' and actual_value > threshold:
                    return False
                elif operator == '==' and actual_value != threshold:
                    return False
                elif operator == '!=' and actual_value == threshold:
                    return False
        
        return True
    
    def _execute_workflow_step(self, step: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        
        # This would be implemented based on specific step requirements
        # For now, return a placeholder
        return {
            'step': step,
            'success': True,
            'result': f'Executed {step}',
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def get_constraints(self) -> Dict[str, Any]:
        """Get operational constraints"""
        return self.constraints
    
    def update_constraints(self, new_constraints: Dict[str, Any]):
        """Update operational constraints"""
        self.constraints.update(new_constraints)
    
    def get_all_rules(self) -> Dict[MonitoringDomain, List[MonitoringRule]]:
        """Get all rules by domain"""
        return self.rules
    
    def add_rule(self, domain: MonitoringDomain, rule: MonitoringRule):
        """Add a new rule to a domain"""
        if domain not in self.rules:
            self.rules[domain] = []
        self.rules[domain].append(rule)
    
    def remove_rule(self, domain: MonitoringDomain, rule_name: str):
        """Remove a rule from a domain"""
        if domain in self.rules:
            self.rules[domain] = [r for r in self.rules[domain] if r.name != rule_name]
    
    def _initialize_free_tier_limits(self):
        """Initialize AWS Free Tier limits for cost-conscious monitoring"""
        self.free_tier_limits = {
            # EC2 Free Tier (12 months)
            'ec2_hours': 750,  # 750 hours per month
            'ec2_instances': 2,  # 2 instances max
            'ec2_storage': 30,  # 30 GB EBS storage
            
            # RDS Free Tier (12 months)
            'rds_hours': 750,  # 750 hours per month
            'rds_storage': 20,  # 20 GB storage
            'rds_instances': 1,  # 1 instance max
            
            # S3 Free Tier (12 months)
            's3_storage': 5,  # 5 GB storage
            's3_requests': 20000,  # 20,000 GET requests
            's3_put_requests': 2000,  # 2,000 PUT requests
            
            # Lambda Free Tier (12 months)
            'lambda_requests': 1000000,  # 1M requests
            'lambda_compute': 400000,  # 400,000 GB-seconds
            
            # CloudWatch Free Tier
            'cloudwatch_metrics': 10,  # 10 custom metrics
            'cloudwatch_logs': 5,  # 5 GB log ingestion
            
            # Data Transfer
            'data_transfer_out': 1,  # 1 GB data transfer out
            'data_transfer_in': 15,  # 15 GB data transfer in
            
            # Monthly Budget Limit
            'monthly_budget': 1.0,  # $1.00 maximum monthly spend
        }
    
    def _initialize_cost_conscious_rules(self):
        """Initialize cost-conscious monitoring rules"""
        cost_conscious_rules = [
            # Budget Rules
            MonitoringRule(
                name="monthly_budget_50_percent",
                domain=MonitoringDomain.COST,
                threshold=0.50,  # 50% of $1 budget = $0.50
                operator=">=",
                severity="high",
                action="alert",
                description="Monthly spend reached 50% of Free Tier budget ($0.50)"
            ),
            MonitoringRule(
                name="monthly_budget_80_percent",
                domain=MonitoringDomain.COST,
                threshold=0.80,  # 80% of $1 budget = $0.80
                operator=">=",
                severity="critical",
                action="escalate",
                description="Monthly spend reached 80% of Free Tier budget ($0.80)"
            ),
            MonitoringRule(
                name="monthly_budget_exceeded",
                domain=MonitoringDomain.COST,
                threshold=1.00,  # $1.00 budget exceeded
                operator=">",
                severity="critical",
                action="escalate",
                description="Monthly spend exceeded Free Tier budget ($1.00)"
            ),
            
            # EC2 Free Tier Rules
            MonitoringRule(
                name="ec2_hours_50_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=375,  # 50% of 750 hours
                operator=">=",
                severity="high",
                action="alert",
                description="EC2 usage reached 50% of Free Tier limit (375/750 hours)"
            ),
            MonitoringRule(
                name="ec2_hours_80_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=600,  # 80% of 750 hours
                operator=">=",
                severity="critical",
                action="escalate",
                description="EC2 usage reached 80% of Free Tier limit (600/750 hours)"
            ),
            MonitoringRule(
                name="ec2_hours_exceeded",
                domain=MonitoringDomain.RESOURCE,
                threshold=750,  # Free Tier limit exceeded
                operator=">",
                severity="critical",
                action="escalate",
                description="EC2 usage exceeded Free Tier limit (750 hours)"
            ),
            
            # S3 Free Tier Rules
            MonitoringRule(
                name="s3_storage_50_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=2.5,  # 50% of 5 GB
                operator=">=",
                severity="high",
                action="alert",
                description="S3 storage reached 50% of Free Tier limit (2.5/5 GB)"
            ),
            MonitoringRule(
                name="s3_storage_80_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=4.0,  # 80% of 5 GB
                operator=">=",
                severity="critical",
                action="escalate",
                description="S3 storage reached 80% of Free Tier limit (4/5 GB)"
            ),
            
            # Lambda Free Tier Rules
            MonitoringRule(
                name="lambda_requests_50_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=500000,  # 50% of 1M requests
                operator=">=",
                severity="high",
                action="alert",
                description="Lambda requests reached 50% of Free Tier limit (500K/1M)"
            ),
            MonitoringRule(
                name="lambda_requests_80_percent",
                domain=MonitoringDomain.RESOURCE,
                threshold=800000,  # 80% of 1M requests
                operator=">=",
                severity="critical",
                action="escalate",
                description="Lambda requests reached 80% of Free Tier limit (800K/1M)"
            ),
        ]
        
        # Add cost-conscious rules to the rules dictionary
        for rule in cost_conscious_rules:
            if rule.domain not in self.rules:
                self.rules[rule.domain] = []
            self.rules[rule.domain].append(rule)
    
    def _initialize_free_tier_thresholds(self):
        """Initialize Free Tier usage thresholds for monitoring"""
        self.free_tier_thresholds = {
            'cost': {
                'high': 0.50,      # 50% of $1 budget = $0.50
                'critical': 0.80,  # 80% of $1 budget = $0.80
                'exceeded': 1.00   # $1.00 budget exceeded
            },
            'ec2_hours': {
                'high': 375,       # 50% of 750 hours
                'critical': 600,   # 80% of 750 hours
                'exceeded': 750    # Free Tier limit
            },
            's3_storage': {
                'high': 2.5,       # 50% of 5 GB
                'critical': 4.0,   # 80% of 5 GB
                'exceeded': 5.0    # Free Tier limit
            },
            'lambda_requests': {
                'high': 500000,   # 50% of 1M requests
                'critical': 800000, # 80% of 1M requests
                'exceeded': 1000000 # Free Tier limit
            },
            'rds_hours': {
                'high': 375,       # 50% of 750 hours
                'critical': 600,   # 80% of 750 hours
                'exceeded': 750    # Free Tier limit
            }
        }
    
    def get_free_tier_limits(self) -> Dict[str, Any]:
        """Get AWS Free Tier limits"""
        return self.free_tier_limits
    
    def get_free_tier_thresholds(self) -> Dict[str, Any]:
        """Get Free Tier usage thresholds"""
        return self.free_tier_thresholds
    
    def check_free_tier_usage(self, current_usage: Dict[str, float]) -> Dict[str, Any]:
        """Check current usage against Free Tier limits and thresholds"""
        alerts = []
        warnings = []
        
        for resource, usage in current_usage.items():
            if resource in self.free_tier_limits:
                limit = self.free_tier_limits[resource]
                percentage = (usage / limit) * 100
                
                if resource in self.free_tier_thresholds:
                    thresholds = self.free_tier_thresholds[resource]
                    
                    if usage >= thresholds['exceeded']:
                        alerts.append({
                            'resource': resource,
                            'severity': 'critical',
                            'message': f"{resource} usage exceeded Free Tier limit ({usage}/{limit})",
                            'percentage': percentage
                        })
                    elif usage >= thresholds['critical']:
                        alerts.append({
                            'resource': resource,
                            'severity': 'critical',
                            'message': f"{resource} usage reached 80% of Free Tier limit ({usage}/{limit})",
                            'percentage': percentage
                        })
                    elif usage >= thresholds['high']:
                        warnings.append({
                            'resource': resource,
                            'severity': 'high',
                            'message': f"{resource} usage reached 50% of Free Tier limit ({usage}/{limit})",
                            'percentage': percentage
                        })
        
        return {
            'alerts': alerts,
            'warnings': warnings,
            'total_usage': current_usage,
            'free_tier_limits': self.free_tier_limits
        }
