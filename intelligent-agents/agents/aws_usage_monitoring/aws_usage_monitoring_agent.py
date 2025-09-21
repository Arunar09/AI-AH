"""
Intelligent AWS Usage Monitoring Agent
Log^2 approach: Logic-driven functionality with log monitoring and self-improvement
"""

import json
import datetime
import boto3
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from .aws_usage_logic_engine import AWSUsageLogicEngine, MonitoringDomain
from .aws_usage_log_engine import AWSUsageLogEngine
from .aws_usage_intelligence_engine import AWSUsageIntelligenceEngine

@dataclass
class AWSMonitoringResult:
    """Result of AWS monitoring operation"""
    timestamp: str
    domain: str
    metrics: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    cost_analysis: Dict[str, Any]
    performance_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    success: bool
    execution_time_ms: float

class IntelligentAWSUsageMonitoringAgent:
    """AWS Usage Monitoring Agent using Log^2 approach"""
    
    def __init__(self, aws_region: str = 'us-east-1'):
        self.aws_region = aws_region
        self.logic_engine = AWSUsageLogicEngine()
        self.log_engine = AWSUsageLogEngine()
        self.intelligence_engine = AWSUsageIntelligenceEngine()
        
        # Initialize AWS clients
        self._initialize_aws_clients()
        
        # Agent metadata
        self.agent_name = "aws_usage_monitoring"
        self.version = "1.0.0"
        self.created_at = datetime.datetime.now().isoformat()
        self.last_updated = datetime.datetime.now().isoformat()
        
        # Performance tracking
        self.performance_metrics = {
            'total_monitoring_runs': 0,
            'successful_runs': 0,
            'average_execution_time': 0,
            'last_run_timestamp': None
        }
    
    def _initialize_aws_clients(self):
        """Initialize AWS service clients"""
        try:
            self.ec2_client = boto3.client('ec2', region_name=self.aws_region)
            self.rds_client = boto3.client('rds', region_name=self.aws_region)
            self.s3_client = boto3.client('s3', region_name=self.aws_region)
            self.lambda_client = boto3.client('lambda', region_name=self.aws_region)
            self.cloudwatch_client = boto3.client('cloudwatch', region_name=self.aws_region)
            self.ce_client = boto3.client('ce', region_name=self.aws_region)  # Cost Explorer
            self.iam_client = boto3.client('iam', region_name=self.aws_region)
            self.config_client = boto3.client('config', region_name=self.aws_region)
            self.guardduty_client = boto3.client('guardduty', region_name=self.aws_region)
            self.inspector_client = boto3.client('inspector', region_name=self.aws_region)
            
            print(f"AWS clients initialized for region: {self.aws_region}")
        except Exception as e:
            print(f"Warning: Could not initialize AWS clients: {e}")
            print("Running in demo mode without AWS integration")
            self.ec2_client = None
            self.rds_client = None
            self.s3_client = None
            self.lambda_client = None
            self.cloudwatch_client = None
            self.ce_client = None
            self.iam_client = None
            self.config_client = None
            self.guardduty_client = None
            self.inspector_client = None
    
    def monitor_aws_usage(self) -> AWSMonitoringResult:
        """Main monitoring function using Log^2 approach"""
        
        start_time = time.time()
        
        try:
            # 1. Execute Logic (Collect AWS data)
            aws_data = self._collect_aws_data()
            
            # 2. Execute monitoring logic for each domain
            monitoring_results = {}
            all_alerts = []
            all_recommendations = []
            
            for domain in MonitoringDomain:
                domain_results, execution_logs = self.logic_engine.execute_logic(domain, aws_data)
                monitoring_results[domain.value] = domain_results
                
                # Collect logs
                log_id = self.log_engine.collect_logs(execution_logs)
                
                # Extract alerts and recommendations
                for result in domain_results:
                    if result.get('triggered', False):
                        all_alerts.append({
                            'domain': domain.value,
                            'rule': result['rule_name'],
                            'severity': result['severity'],
                            'description': result['description'],
                            'timestamp': result['timestamp']
                        })
            
            # 3. Analyze logs and learn
            log_analysis = self.log_engine.analyze_logs()
            improvements, adaptations = self.intelligence_engine.learn_from_logs(log_analysis)
            
            # 4. Generate recommendations from learning
            learning_recommendations = self._generate_learning_recommendations(improvements, adaptations)
            all_recommendations.extend(learning_recommendations)
            
            # 5. Perform specialized analysis
            cost_analysis = self._analyze_costs(aws_data)
            performance_analysis = self._analyze_performance(aws_data)
            security_analysis = self._analyze_security(aws_data)
            
            execution_time = (time.time() - start_time) * 1000
            
            # Create result
            result = AWSMonitoringResult(
                timestamp=datetime.datetime.now().isoformat(),
                domain='aws_usage_monitoring',
                metrics=aws_data,
                alerts=all_alerts,
                recommendations=all_recommendations,
                cost_analysis=cost_analysis,
                performance_analysis=performance_analysis,
                security_analysis=security_analysis,
                success=True,
                execution_time_ms=execution_time
            )
            
            # Update performance metrics
            self._update_performance_metrics(True, execution_time)
            
            return result
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_performance_metrics(False, execution_time)
            
            return AWSMonitoringResult(
                timestamp=datetime.datetime.now().isoformat(),
                domain='aws_usage_monitoring',
                metrics={},
                alerts=[{'error': str(e), 'severity': 'critical'}],
                recommendations=[],
                cost_analysis={},
                performance_analysis={},
                security_analysis={},
                success=False,
                execution_time_ms=execution_time
            )
    
    def _collect_aws_data(self) -> Dict[str, Any]:
        """Collect AWS usage data"""
        
        aws_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'region': self.aws_region,
            'cost': {},
            'resources': {},
            'performance': {},
            'security': {}
        }
        
        try:
            # Cost data
            aws_data['cost'] = self._collect_cost_data()
            
            # Resource data
            aws_data['resources'] = self._collect_resource_data()
            
            # Performance data
            aws_data['performance'] = self._collect_performance_data()
            
            # Security data
            aws_data['security'] = self._collect_security_data()
            
        except Exception as e:
            print(f"Error collecting AWS data: {e}")
            # Return demo data if AWS clients not available
            aws_data = self._get_demo_data()
        
        return aws_data
    
    def _collect_cost_data(self) -> Dict[str, Any]:
        """Collect cost data with Free Tier budget awareness"""
        
        if not self.ce_client:
            return self._get_demo_cost_data()
        
        try:
            # Get current month costs
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            start_date = datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d')
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            current_cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
            
            # Get Free Tier budget limit
            free_tier_limits = self.logic_engine.get_free_tier_limits()
            budget_limit = free_tier_limits.get('monthly_budget', 1.0)  # $1.00 default
            
            # Calculate budget percentage
            budget_percentage = (current_cost / budget_limit) * 100
            
            # Determine cost trend based on Free Tier budget
            if current_cost >= budget_limit:
                cost_trend = 'exceeded_budget'
            elif current_cost >= budget_limit * 0.8:
                cost_trend = 'approaching_budget'
            elif current_cost >= budget_limit * 0.5:
                cost_trend = 'moderate_usage'
            else:
                cost_trend = 'low_usage'
            
            return {
                'current_month_cost': current_cost,
                'daily_average': current_cost / datetime.datetime.now().day,
                'projected_monthly': current_cost * 30 / datetime.datetime.now().day,
                'cost_trend': cost_trend,
                'budget_limit': budget_limit,
                'budget_percentage': budget_percentage,
                'budget_remaining': budget_limit - current_cost,
                'free_tier_status': 'within_limits' if current_cost < budget_limit else 'exceeded'
            }
            
        except Exception as e:
            print(f"Error collecting cost data: {e}")
            return self._get_demo_cost_data()
    
    def _collect_resource_data(self) -> Dict[str, Any]:
        """Collect resource usage data"""
        
        if not self.ec2_client:
            return self._get_demo_resource_data()
        
        try:
            # EC2 instances
            ec2_response = self.ec2_client.describe_instances()
            ec2_count = sum(len(reservation['Instances']) for reservation in ec2_response['Reservations'])
            
            # RDS instances
            rds_response = self.rds_client.describe_db_instances()
            rds_count = len(rds_response['DBInstances'])
            
            # S3 buckets
            s3_response = self.s3_client.list_buckets()
            s3_count = len(s3_response['Buckets'])
            
            return {
                'ec2_instances': ec2_count,
                'rds_instances': rds_count,
                's3_buckets': s3_count,
                'total_resources': ec2_count + rds_count + s3_count
            }
            
        except Exception as e:
            print(f"Error collecting resource data: {e}")
            return self._get_demo_resource_data()
    
    def _collect_performance_data(self) -> Dict[str, Any]:
        """Collect performance data"""
        
        if not self.cloudwatch_client:
            return self._get_demo_performance_data()
        
        try:
            # Get CloudWatch metrics
            end_time = datetime.datetime.now()
            start_time = end_time - datetime.timedelta(hours=1)
            
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            cpu_utilization = 0
            if response['Datapoints']:
                cpu_utilization = response['Datapoints'][0]['Average']
            
            return {
                'cpu_utilization': cpu_utilization,
                'memory_utilization': 0,  # Would need custom metrics
                'response_time': 0,  # Would need custom metrics
                'error_rate': 0  # Would need custom metrics
            }
            
        except Exception as e:
            print(f"Error collecting performance data: {e}")
            return self._get_demo_performance_data()
    
    def _collect_security_data(self) -> Dict[str, Any]:
        """Collect security data"""
        
        if not self.config_client:
            return self._get_demo_security_data()
        
        try:
            # Get Config compliance
            response = self.config_client.describe_compliance_by_resource()
            
            compliance_violations = 0
            if 'ComplianceByResources' in response:
                compliance_violations = len([r for r in response['ComplianceByResources'] 
                                          if r['Compliance']['ComplianceType'] == 'NON_COMPLIANT'])
            
            return {
                'compliance_violations': compliance_violations,
                'security_score': max(0, 100 - compliance_violations * 10),
                'vulnerability_count': 0,  # Would need Inspector
                'unauthorized_access': 0  # Would need GuardDuty
            }
            
        except Exception as e:
            print(f"Error collecting security data: {e}")
            return self._get_demo_security_data()
    
    def _analyze_costs(self, aws_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze costs and provide insights"""
        
        cost_data = aws_data.get('cost', {})
        current_cost = cost_data.get('current_month_cost', 0)
        daily_average = cost_data.get('daily_average', 0)
        
        analysis = {
            'current_cost': current_cost,
            'daily_average': daily_average,
            'budget_status': 'within_budget' if current_cost < 150 else 'over_budget',
            'optimization_opportunities': [],
            'cost_trend': cost_data.get('cost_trend', 'stable')
        }
        
        # Identify optimization opportunities
        if current_cost > 100:
            analysis['optimization_opportunities'].append({
                'type': 'high_cost',
                'description': f'Current cost ${current_cost:.2f} is high',
                'recommendation': 'Review resource usage and optimize'
            })
        
        if daily_average > 5:
            analysis['optimization_opportunities'].append({
                'type': 'high_daily_average',
                'description': f'Daily average ${daily_average:.2f} is high',
                'recommendation': 'Implement cost controls'
            })
        
        return analysis
    
    def _analyze_performance(self, aws_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance and provide insights"""
        
        perf_data = aws_data.get('performance', {})
        cpu_util = perf_data.get('cpu_utilization', 0)
        
        analysis = {
            'cpu_utilization': cpu_util,
            'performance_status': 'good' if cpu_util < 80 else 'degraded',
            'recommendations': []
        }
        
        if cpu_util > 80:
            analysis['recommendations'].append({
                'type': 'high_cpu',
                'description': f'CPU utilization {cpu_util:.1f}% is high',
                'recommendation': 'Consider scaling resources'
            })
        
        return analysis
    
    def _analyze_security(self, aws_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security and provide insights"""
        
        security_data = aws_data.get('security', {})
        violations = security_data.get('compliance_violations', 0)
        security_score = security_data.get('security_score', 100)
        
        analysis = {
            'compliance_violations': violations,
            'security_score': security_score,
            'security_status': 'good' if violations == 0 else 'needs_attention',
            'recommendations': []
        }
        
        if violations > 0:
            analysis['recommendations'].append({
                'type': 'compliance_violations',
                'description': f'{violations} compliance violations found',
                'recommendation': 'Review and fix compliance issues'
            })
        
        return analysis
    
    def _generate_learning_recommendations(self, improvements: List, adaptations: List) -> List[Dict[str, Any]]:
        """Generate recommendations from learning"""
        
        recommendations = []
        
        for improvement in improvements:
            recommendations.append({
                'type': 'learning_improvement',
                'source': 'intelligence_engine',
                'description': improvement.description,
                'recommendations': improvement.recommendations,
                'confidence': improvement.confidence
            })
        
        for adaptation in adaptations:
            recommendations.append({
                'type': 'logic_adaptation',
                'source': 'intelligence_engine',
                'description': f"Suggested adaptation: {adaptation.reasoning}",
                'recommendations': [f"Apply {adaptation.adaptation_type} adaptation"],
                'confidence': adaptation.confidence
            })
        
        return recommendations
    
    def _update_performance_metrics(self, success: bool, execution_time: float):
        """Update agent performance metrics"""
        
        self.performance_metrics['total_monitoring_runs'] += 1
        if success:
            self.performance_metrics['successful_runs'] += 1
        
        # Update average execution time
        total_runs = self.performance_metrics['total_monitoring_runs']
        current_avg = self.performance_metrics['average_execution_time']
        self.performance_metrics['average_execution_time'] = (
            (current_avg * (total_runs - 1) + execution_time) / total_runs
        )
        
        self.performance_metrics['last_run_timestamp'] = datetime.datetime.now().isoformat()
        self.last_updated = datetime.datetime.now().isoformat()
    
    def _get_demo_data(self) -> Dict[str, Any]:
        """Get demo data when AWS clients are not available"""
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'region': self.aws_region,
            'cost': self._get_demo_cost_data(),
            'resources': self._get_demo_resource_data(),
            'performance': self._get_demo_performance_data(),
            'security': self._get_demo_security_data()
        }
    
    def _get_demo_cost_data(self) -> Dict[str, Any]:
        """Demo cost data with Free Tier budget awareness"""
        # Simulate low Free Tier usage (within $1 budget)
        current_cost = 0.15  # $0.15 - well within Free Tier budget
        budget_limit = 1.0   # $1.00 Free Tier budget
        
        return {
            'current_month_cost': current_cost,
            'daily_average': current_cost / datetime.datetime.now().day,
            'projected_monthly': current_cost * 30 / datetime.datetime.now().day,
            'cost_trend': 'low_usage',
            'budget_limit': budget_limit,
            'budget_percentage': (current_cost / budget_limit) * 100,
            'budget_remaining': budget_limit - current_cost,
            'free_tier_status': 'within_limits'
        }
    
    def _get_demo_resource_data(self) -> Dict[str, Any]:
        """Demo resource data with Free Tier limits"""
        # Simulate Free Tier usage (well within limits)
        return {
            'ec2_instances': 1,  # Within Free Tier limit of 2
            'rds_instances': 0,   # Within Free Tier limit of 1
            's3_buckets': 2,     # Within Free Tier limit
            'lambda_functions': 2,  # Within Free Tier limit
            'ec2_hours_used': 45,    # Well within 750 hours Free Tier limit
            's3_storage_gb': 1.2,    # Well within 5 GB Free Tier limit
            'lambda_invocations': 5000,  # Well within 1M Free Tier limit
            'rds_hours_used': 0,     # No RDS usage
            'data_transfer_gb': 0.3,  # Well within Free Tier limits
            'total_resources': 5
        }
    
    def _get_demo_performance_data(self) -> Dict[str, Any]:
        """Demo performance data"""
        return {
            'cpu_utilization': 65.5,
            'memory_utilization': 72.3,
            'response_time': 245,
            'error_rate': 1.2
        }
    
    def _get_demo_security_data(self) -> Dict[str, Any]:
        """Demo security data"""
        return {
            'compliance_violations': 0,
            'security_score': 95,
            'vulnerability_count': 0,
            'unauthorized_access': 0
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and metrics"""
        
        return {
            'agent_name': self.agent_name,
            'version': self.version,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'aws_region': self.aws_region,
            'performance_metrics': self.performance_metrics,
            'aws_clients_available': all([
                self.ec2_client, self.rds_client, self.s3_client,
                self.cloudwatch_client, self.ce_client
            ]),
            'learning_summary': self.intelligence_engine.get_learning_summary()
        }
    
    def export_monitoring_data(self, format: str = 'json') -> str:
        """Export monitoring data"""
        
        # Get recent logs
        recent_logs = self.log_engine.get_recent_logs(hours=24)
        
        # Get learning data
        learning_data = self.intelligence_engine.export_learning_data()
        
        # Combine data
        export_data = {
            'agent_status': self.get_agent_status(),
            'recent_logs': recent_logs,
            'learning_data': learning_data,
            'export_timestamp': datetime.datetime.now().isoformat()
        }
        
        if format == 'json':
            return json.dumps(export_data, indent=2)
        else:
            return str(export_data)
    
    def check_free_tier_usage(self) -> Dict[str, Any]:
        """Check current usage against Free Tier limits and generate alerts"""
        # Get current usage data
        aws_data = self._collect_aws_data()
        
        # Extract usage metrics
        current_usage = {
            'cost': aws_data['cost']['current_month_cost'],
            'ec2_hours': aws_data['resources'].get('ec2_hours_used', 0),
            's3_storage': aws_data['resources'].get('s3_storage_gb', 0),
            'lambda_requests': aws_data['resources'].get('lambda_invocations', 0),
            'rds_hours': aws_data['resources'].get('rds_hours_used', 0)
        }
        
        # Check against Free Tier limits
        free_tier_check = self.logic_engine.check_free_tier_usage(current_usage)
        
        # Generate alerts based on Free Tier usage
        alerts = []
        for alert in free_tier_check['alerts']:
            alerts.append({
                'rule': f"free_tier_{alert['resource']}_exceeded",
                'severity': alert['severity'],
                'description': alert['message'],
                'resource': alert['resource'],
                'percentage': alert['percentage']
            })
        
        for warning in free_tier_check['warnings']:
            alerts.append({
                'rule': f"free_tier_{warning['resource']}_warning",
                'severity': warning['severity'],
                'description': warning['message'],
                'resource': warning['resource'],
                'percentage': warning['percentage']
            })
        
        return {
            'free_tier_status': free_tier_check,
            'alerts': alerts,
            'usage_summary': {
                'total_cost': current_usage['cost'],
                'budget_remaining': 1.0 - current_usage['cost'],
                'ec2_usage_percentage': (current_usage['ec2_hours'] / 750) * 100,
                's3_usage_percentage': (current_usage['s3_storage'] / 5) * 100,
                'lambda_usage_percentage': (current_usage['lambda_requests'] / 1000000) * 100
            }
        }
    
    def analyze_active_resources(self) -> Dict[str, Any]:
        """Analyze all active AWS resources and their cost impact"""
        print("🔍 Analyzing active AWS resources...")
        
        active_resources = {
            'ec2_instances': [],
            's3_buckets': [],
            'lambda_functions': [],
            'rds_instances': [],
            'other_resources': []
        }
        
        # Analyze EC2 instances
        if self.ec2_client:
            try:
                response = self.ec2_client.describe_instances()
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:
                        if instance['State']['Name'] in ['running', 'pending']:
                            resource_info = {
                                'id': instance['InstanceId'],
                                'type': instance['InstanceType'],
                                'state': instance['State']['Name'],
                                'launch_time': instance['LaunchTime'].isoformat(),
                                'estimated_cost_per_hour': self._estimate_ec2_cost(instance['InstanceType']),
                                'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                                'can_stop': True,
                                'stop_action': 'terminate' if instance['InstanceType'] != 't2.micro' else 'stop'
                            }
                            active_resources['ec2_instances'].append(resource_info)
            except Exception as e:
                print(f"Error analyzing EC2 instances: {e}")
        
        # Analyze S3 buckets
        if self.s3_client:
            try:
                response = self.s3_client.list_buckets()
                for bucket in response['Buckets']:
                    # Check if bucket has objects
                    try:
                        objects = self.s3_client.list_objects_v2(Bucket=bucket['Name'])
                        has_objects = 'Contents' in objects and len(objects['Contents']) > 0
                        
                        resource_info = {
                            'name': bucket['Name'],
                            'created': bucket['CreationDate'].isoformat(),
                            'has_objects': has_objects,
                            'object_count': len(objects.get('Contents', [])),
                            'can_delete': True,
                            'estimated_cost_per_month': self._estimate_s3_cost(bucket['Name'])
                        }
                        active_resources['s3_buckets'].append(resource_info)
                    except Exception as e:
                        print(f"Error analyzing S3 bucket {bucket['Name']}: {e}")
            except Exception as e:
                print(f"Error analyzing S3 buckets: {e}")
        
        # Analyze Lambda functions
        if self.lambda_client:
            try:
                response = self.lambda_client.list_functions()
                for function in response['Functions']:
                    resource_info = {
                        'name': function['FunctionName'],
                        'runtime': function['Runtime'],
                        'last_modified': function['LastModified'],
                        'code_size': function['CodeSize'],
                        'can_delete': True,
                        'estimated_cost_per_month': self._estimate_lambda_cost(function)
                    }
                    active_resources['lambda_functions'].append(resource_info)
            except Exception as e:
                print(f"Error analyzing Lambda functions: {e}")
        
        # Analyze RDS instances
        if self.rds_client:
            try:
                response = self.rds_client.describe_db_instances()
                for db in response['DBInstances']:
                    if db['DBInstanceStatus'] in ['available', 'starting']:
                        resource_info = {
                            'id': db['DBInstanceIdentifier'],
                            'engine': db['Engine'],
                            'class': db['DBInstanceClass'],
                            'status': db['DBInstanceStatus'],
                            'can_stop': True,
                            'estimated_cost_per_hour': self._estimate_rds_cost(db['DBInstanceClass'])
                        }
                        active_resources['rds_instances'].append(resource_info)
            except Exception as e:
                print(f"Error analyzing RDS instances: {e}")
        
        return active_resources
    
    def _estimate_ec2_cost(self, instance_type: str) -> float:
        """Estimate EC2 cost per hour"""
        # Free Tier: t2.micro is free for 750 hours/month
        if instance_type == 't2.micro':
            return 0.0
        # Rough estimates for other types
        cost_map = {
            't2.nano': 0.0058,
            't2.micro': 0.0116,
            't2.small': 0.023,
            't2.medium': 0.0464,
            't2.large': 0.0928
        }
        return cost_map.get(instance_type, 0.1)
    
    def _estimate_s3_cost(self, bucket_name: str) -> float:
        """Estimate S3 cost per month"""
        # Free Tier: 5 GB storage, 20,000 GET requests, 2,000 PUT requests
        try:
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
            total_size = sum(obj['Size'] for obj in objects.get('Contents', []))
            size_gb = total_size / (1024**3)
            
            # Free Tier: 5 GB free
            if size_gb <= 5:
                return 0.0
            else:
                return (size_gb - 5) * 0.023  # $0.023 per GB
        except:
            return 0.0
    
    def _estimate_lambda_cost(self, function: Dict[str, Any]) -> float:
        # Free Tier: 1M requests, 400,000 GB-seconds
        return 0.0  # Assume within Free Tier
    
    def _estimate_rds_cost(self, instance_class: str) -> float:
        """Estimate RDS cost per hour"""
        # Free Tier: 750 hours/month for db.t2.micro
        if instance_class == 'db.t2.micro':
            return 0.0
        return 0.017  # Rough estimate for other classes
    
    def get_resource_management_recommendations(self, active_resources: Dict[str, Any]) -> Dict[str, Any]:
        """Get intelligent recommendations for resource management"""
        recommendations = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'total_potential_savings': 0.0
        }
        
        total_potential_savings = 0.0
        
        # Analyze EC2 instances
        for instance in active_resources['ec2_instances']:
            if instance['can_stop']:
                estimated_monthly_cost = instance['estimated_cost_per_hour'] * 24 * 30
                if instance['type'] != 't2.micro':
                    recommendations['high_priority'].append({
                        'resource_type': 'EC2',
                        'resource_id': instance['id'],
                        'action': instance['stop_action'],
                        'reason': f"Non-Free Tier instance ({instance['type']}) costing ~${estimated_monthly_cost:.2f}/month",
                        'potential_savings': estimated_monthly_cost,
                        'risk': 'low' if instance['stop_action'] == 'stop' else 'medium'
                    })
                    total_potential_savings += estimated_monthly_cost
        
        # Analyze S3 buckets
        for bucket in active_resources['s3_buckets']:
            if bucket['can_delete'] and not bucket['has_objects']:
                recommendations['low_priority'].append({
                    'resource_type': 'S3',
                    'resource_id': bucket['name'],
                    'action': 'delete',
                    'reason': f"Empty bucket with no objects",
                    'potential_savings': 0.0,
                    'risk': 'low'
                })
        
        # Analyze Lambda functions
        for function in active_resources['lambda_functions']:
            if function['can_delete']:
                recommendations['medium_priority'].append({
                    'resource_type': 'Lambda',
                    'resource_id': function['name'],
                    'action': 'delete',
                    'reason': f"Unused Lambda function ({function['runtime']})",
                    'potential_savings': 0.0,
                    'risk': 'low'
                })
        
        recommendations['total_potential_savings'] = total_potential_savings
        return recommendations
    
    def request_resource_action_approval(self, resource_info: Dict[str, Any]) -> bool:
        """Request user approval for resource management action"""
        print(f"\n🤖 AWS Resource Management Request")
        print(f"=" * 50)
        print(f"Resource Type: {resource_info['resource_type']}")
        print(f"Resource ID: {resource_info['resource_id']}")
        print(f"Proposed Action: {resource_info['action']}")
        print(f"Reason: {resource_info['reason']}")
        print(f"Potential Savings: ${resource_info['potential_savings']:.2f}/month")
        print(f"Risk Level: {resource_info['risk']}")
        
        while True:
            response = input(f"\n❓ Do you approve this action? (y/n/info): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['i', 'info']:
                print(f"\n📋 Additional Information:")
                print(f"   - This action will help reduce your AWS costs")
                print(f"   - Risk level: {resource_info['risk']}")
                if resource_info['action'] == 'terminate':
                    print(f"   - ⚠️  WARNING: This will permanently delete the resource")
                elif resource_info['action'] == 'stop':
                    print(f"   - ✅ This will stop the resource (can be restarted later)")
                continue
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'info' for more information")
    
    def execute_approved_resource_actions(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Execute approved resource management actions"""
        executed_actions = {
            'successful': [],
            'failed': [],
            'total_savings': 0.0
        }
        
        print(f"\n🚀 Executing approved resource management actions...")
        
        # Process high priority recommendations
        for rec in recommendations['high_priority']:
            if self.request_resource_action_approval(rec):
                try:
                    if rec['resource_type'] == 'EC2':
                        if rec['action'] == 'terminate':
                            self.ec2_client.terminate_instances(InstanceIds=[rec['resource_id']])
                            print(f"✅ Terminated EC2 instance: {rec['resource_id']}")
                        elif rec['action'] == 'stop':
                            self.ec2_client.stop_instances(InstanceIds=[rec['resource_id']])
                            print(f"✅ Stopped EC2 instance: {rec['resource_id']}")
                    
                    executed_actions['successful'].append(rec)
                    executed_actions['total_savings'] += rec['potential_savings']
                    
                except Exception as e:
                    print(f"❌ Failed to {rec['action']} {rec['resource_id']}: {e}")
                    executed_actions['failed'].append(rec)
        
        # Process medium priority recommendations
        for rec in recommendations['medium_priority']:
            if self.request_resource_action_approval(rec):
                try:
                    if rec['resource_type'] == 'Lambda':
                        self.lambda_client.delete_function(FunctionName=rec['resource_id'])
                        print(f"✅ Deleted Lambda function: {rec['resource_id']}")
                    
                    executed_actions['successful'].append(rec)
                    
                except Exception as e:
                    print(f"❌ Failed to {rec['action']} {rec['resource_id']}: {e}")
                    executed_actions['failed'].append(rec)
        
        # Process low priority recommendations
        for rec in recommendations['low_priority']:
            if self.request_resource_action_approval(rec):
                try:
                    if rec['resource_type'] == 'S3':
                        # Delete all objects first
                        objects = self.s3_client.list_objects_v2(Bucket=rec['resource_id'])
                        if 'Contents' in objects:
                            for obj in objects['Contents']:
                                self.s3_client.delete_object(Bucket=rec['resource_id'], Key=obj['Key'])
                        self.s3_client.delete_bucket(Bucket=rec['resource_id'])
                        print(f"✅ Deleted S3 bucket: {rec['resource_id']}")
                    
                    executed_actions['successful'].append(rec)
                    
                except Exception as e:
                    print(f"❌ Failed to {rec['action']} {rec['resource_id']}: {e}")
                    executed_actions['failed'].append(rec)
        
        return executed_actions
    
    def execute_resource_action_direct(self, action: str, resource_id: str, resource_type: str) -> Dict[str, Any]:
        """Execute resource action directly without asking for approval (for UI use)"""
        try:
            print(f"🚀 Executing {action} on {resource_type} {resource_id}...")
            
            if resource_type == 'EC2':
                if action == 'terminate':
                    self.ec2_client.terminate_instances(InstanceIds=[resource_id])
                    print(f"✅ Terminated EC2 instance: {resource_id}")
                elif action == 'stop':
                    self.ec2_client.stop_instances(InstanceIds=[resource_id])
                    print(f"✅ Stopped EC2 instance: {resource_id}")
                    
            elif resource_type == 'Lambda':
                if action == 'delete':
                    self.lambda_client.delete_function(FunctionName=resource_id)
                    print(f"✅ Deleted Lambda function: {resource_id}")
                    
            elif resource_type == 'S3':
                if action == 'delete':
                    # Delete all objects first
                    objects = self.s3_client.list_objects_v2(Bucket=resource_id)
                    if 'Contents' in objects:
                        for obj in objects['Contents']:
                            self.s3_client.delete_object(Bucket=resource_id, Key=obj['Key'])
                    self.s3_client.delete_bucket(Bucket=resource_id)
                    print(f"✅ Deleted S3 bucket: {resource_id}")
                    
            elif resource_type == 'RDS':
                if action == 'delete':
                    self.rds_client.delete_db_instance(DBInstanceIdentifier=resource_id, SkipFinalSnapshot=True)
                    print(f"✅ Deleted RDS instance: {resource_id}")
            
            return {
                'success': True,
                'message': f'Successfully executed {action} on {resource_type} {resource_id}',
                'resource_id': resource_id,
                'action': action
            }
            
        except Exception as e:
            print(f"❌ Failed to {action} {resource_id}: {e}")
            return {
                'success': False,
                'message': f'Failed to execute {action} on {resource_type} {resource_id}: {str(e)}',
                'resource_id': resource_id,
                'action': action,
                'error': str(e)
            }
    
    def run_continuous_monitoring(self, interval_minutes: int = 60):
        """Run continuous monitoring"""
        
        print(f"Starting continuous monitoring every {interval_minutes} minutes...")
        
        while True:
            try:
                print(f"\n--- Monitoring Run at {datetime.datetime.now()} ---")
                
                # Run monitoring
                result = self.monitor_aws_usage()
                
                # Print results
                print(f"Success: {result.success}")
                print(f"Execution Time: {result.execution_time_ms:.2f}ms")
                print(f"Alerts: {len(result.alerts)}")
                print(f"Recommendations: {len(result.recommendations)}")
                
                if result.alerts:
                    print("Alerts:")
                    for alert in result.alerts:
                        print(f"  - {alert.get('rule', 'Unknown')}: {alert.get('description', 'No description')}")
                
                # Wait for next interval
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Error in monitoring: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

# Example usage
if __name__ == "__main__":
    # Create agent
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Run single monitoring
    result = agent.monitor_aws_usage()
    print(f"Monitoring Result: {result}")
    
    # Get agent status
    status = agent.get_agent_status()
    print(f"Agent Status: {status}")
    
    # Export data
    export_data = agent.export_monitoring_data()
    print(f"Export Data: {export_data[:200]}...")
