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

from logic_engine import AWSUsageLogicEngine, MonitoringDomain
from log_engine import AWSUsageLogEngine
from intelligence_engine import AWSUsageIntelligenceEngine

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
        """Collect cost data"""
        
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
            
            return {
                'current_month_cost': current_cost,
                'daily_average': current_cost / datetime.datetime.now().day,
                'projected_monthly': current_cost * 30 / datetime.datetime.now().day,
                'cost_trend': 'increasing' if current_cost > 100 else 'stable'
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
        """Demo cost data"""
        return {
            'current_month_cost': 45.67,
            'daily_average': 1.52,
            'projected_monthly': 45.67,
            'cost_trend': 'stable'
        }
    
    def _get_demo_resource_data(self) -> Dict[str, Any]:
        """Demo resource data"""
        return {
            'ec2_instances': 2,
            'rds_instances': 1,
            's3_buckets': 3,
            'total_resources': 6
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
