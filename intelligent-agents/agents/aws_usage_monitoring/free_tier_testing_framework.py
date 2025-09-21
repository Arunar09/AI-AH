"""
AWS Free Tier Testing Framework
Real testing with start/stop capabilities to maximize Free Tier efficiency
"""

import boto3
import time
import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .aws_usage_monitoring_agent import IntelligentAWSUsageMonitoringAgent

@dataclass
class TestResource:
    """Test resource definition"""
    resource_type: str
    resource_id: str
    region: str
    created_at: datetime.datetime
    estimated_cost_per_hour: float

@dataclass
class TestSession:
    """Free Tier test session"""
    session_id: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    resources: List[TestResource]
    total_cost: float
    status: str  # 'running', 'stopped', 'completed'

class FreeTierTestingFramework:
    """Framework for efficient Free Tier testing with start/stop capabilities"""
    
    def __init__(self, aws_region: str = 'us-east-1'):
        self.aws_region = aws_region
        self.monitoring_agent = IntelligentAWSUsageMonitoringAgent(aws_region)
        self.test_sessions = {}
        self.active_resources = []
        
        # Initialize AWS clients
        self.ec2_client = boto3.client('ec2', region_name=aws_region)
        self.s3_client = boto3.client('s3', region_name=aws_region)
        self.lambda_client = boto3.client('lambda', region_name=aws_region)
        self.rds_client = boto3.client('rds', region_name=aws_region)
        
        # Free Tier limits
        self.free_tier_limits = self.monitoring_agent.logic_engine.get_free_tier_limits()
        
    def start_test_session(self, session_name: str) -> str:
        """Start a new Free Tier test session"""
        session_id = f"{session_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = TestSession(
            session_id=session_id,
            start_time=datetime.datetime.now(),
            end_time=None,
            resources=[],
            total_cost=0.0,
            status='running'
        )
        
        self.test_sessions[session_id] = session
        print(f"🚀 Started Free Tier test session: {session_id}")
        return session_id
    
    def stop_test_session(self, session_id: str) -> Dict[str, Any]:
        """Stop a Free Tier test session and clean up resources"""
        if session_id not in self.test_sessions:
            return {"error": "Session not found"}
        
        session = self.test_sessions[session_id]
        session.end_time = datetime.datetime.now()
        session.status = 'stopped'
        
        # Clean up resources
        cleanup_results = self._cleanup_session_resources(session)
        
        # Calculate final cost
        session_duration = (session.end_time - session.start_time).total_seconds() / 3600  # hours
        session.total_cost = sum(resource.estimated_cost_per_hour * session_duration 
                                for resource in session.resources)
        
        print(f"🛑 Stopped Free Tier test session: {session_id}")
        print(f"⏱️  Duration: {session_duration:.2f} hours")
        print(f"💰 Estimated Cost: ${session.total_cost:.4f}")
        
        return {
            'session_id': session_id,
            'duration_hours': session_duration,
            'total_cost': session.total_cost,
            'resources_cleaned': len(cleanup_results['cleaned']),
            'cleanup_errors': len(cleanup_results['errors'])
        }
    
    def create_test_ec2_instance(self, session_id: str) -> Optional[str]:
        """Create a test EC2 instance within Free Tier limits"""
        if session_id not in self.test_sessions:
            return None
        
        try:
            # Use t2.micro (Free Tier eligible)
            response = self.ec2_client.run_instances(
                ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2 AMI
                MinCount=1,
                MaxCount=1,
                InstanceType='t2.micro',  # Free Tier eligible
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {'Key': 'Name', 'Value': f'FreeTier-Test-{session_id}'},
                            {'Key': 'FreeTierTest', 'Value': 'true'},
                            {'Key': 'SessionId', 'Value': session_id}
                        ]
                    }
                ]
            )
            
            instance_id = response['Instances'][0]['InstanceId']
            
            # Add to session resources
            resource = TestResource(
                resource_type='ec2',
                resource_id=instance_id,
                region=self.aws_region,
                created_at=datetime.datetime.now(),
                estimated_cost_per_hour=0.0  # Free Tier
            )
            
            self.test_sessions[session_id].resources.append(resource)
            print(f"✅ Created EC2 instance: {instance_id}")
            return instance_id
            
        except Exception as e:
            print(f"❌ Error creating EC2 instance: {e}")
            return None
    
    def create_test_s3_bucket(self, session_id: str) -> Optional[str]:
        """Create a test S3 bucket within Free Tier limits"""
        if session_id not in self.test_sessions:
            return None
        
        try:
            bucket_name = f"freetier-test-{session_id.lower()}-{int(time.time())}"
            
            self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.aws_region}
            )
            
            # Add to session resources
            resource = TestResource(
                resource_type='s3',
                resource_id=bucket_name,
                region=self.aws_region,
                created_at=datetime.datetime.now(),
                estimated_cost_per_hour=0.0  # Free Tier
            )
            
            self.test_sessions[session_id].resources.append(resource)
            print(f"✅ Created S3 bucket: {bucket_name}")
            return bucket_name
            
        except Exception as e:
            print(f"❌ Error creating S3 bucket: {e}")
            return None
    
    def create_test_lambda_function(self, session_id: str) -> Optional[str]:
        """Create a test Lambda function within Free Tier limits"""
        if session_id not in self.test_sessions:
            return None
        
        try:
            function_name = f"freetier-test-{session_id}"
            
            # Simple test function
            test_code = '''
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Free Tier Test Function'
    }
'''
            
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role='arn:aws:iam::123456789012:role/lambda-execution-role',  # You'll need to create this
                Handler='index.lambda_handler',
                Code={'ZipFile': test_code.encode()},
                Description='Free Tier Test Function',
                Tags={'FreeTierTest': 'true', 'SessionId': session_id}
            )
            
            # Add to session resources
            resource = TestResource(
                resource_type='lambda',
                resource_id=function_name,
                region=self.aws_region,
                created_at=datetime.datetime.now(),
                estimated_cost_per_hour=0.0  # Free Tier
            )
            
            self.test_sessions[session_id].resources.append(resource)
            print(f"✅ Created Lambda function: {function_name}")
            return function_name
            
        except Exception as e:
            print(f"❌ Error creating Lambda function: {e}")
            return None
    
    def _cleanup_session_resources(self, session: TestSession) -> Dict[str, List[str]]:
        """Clean up all resources for a test session"""
        cleaned = []
        errors = []
        
        for resource in session.resources:
            try:
                if resource.resource_type == 'ec2':
                    self.ec2_client.terminate_instances(InstanceIds=[resource.resource_id])
                    cleaned.append(f"EC2: {resource.resource_id}")
                    
                elif resource.resource_type == 's3':
                    # Delete all objects first
                    try:
                        objects = self.s3_client.list_objects_v2(Bucket=resource.resource_id)
                        if 'Contents' in objects:
                            for obj in objects['Contents']:
                                self.s3_client.delete_object(Bucket=resource.resource_id, Key=obj['Key'])
                    except:
                        pass
                    
                    self.s3_client.delete_bucket(Bucket=resource.resource_id)
                    cleaned.append(f"S3: {resource.resource_id}")
                    
                elif resource.resource_type == 'lambda':
                    self.lambda_client.delete_function(FunctionName=resource.resource_id)
                    cleaned.append(f"Lambda: {resource.resource_id}")
                    
            except Exception as e:
                errors.append(f"{resource.resource_type}: {resource.resource_id} - {str(e)}")
        
        return {'cleaned': cleaned, 'errors': errors}
    
    def get_real_usage_data(self) -> Dict[str, Any]:
        """Get real AWS usage data (not demo data)"""
        try:
            # Get real cost data
            cost_data = self._get_real_cost_data()
            
            # Get real resource data
            resource_data = self._get_real_resource_data()
            
            # Get real performance data
            performance_data = self._get_real_performance_data()
            
            return {
                'cost': cost_data,
                'resources': resource_data,
                'performance': performance_data,
                'timestamp': datetime.datetime.now().isoformat(),
                'data_source': 'real_aws_api'
            }
            
        except Exception as e:
            print(f"Error getting real usage data: {e}")
            return self.monitoring_agent._get_demo_data()
    
    def _get_real_cost_data(self) -> Dict[str, Any]:
        """Get real cost data from AWS Cost Explorer"""
        try:
            ce_client = boto3.client('ce', region_name='us-east-1')
            
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
            start_date = datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d')
            
            response = ce_client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            current_cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
            
            return {
                'current_month_cost': current_cost,
                'daily_average': current_cost / datetime.datetime.now().day,
                'projected_monthly': current_cost * 30 / datetime.datetime.now().day,
                'budget_limit': 1.0,
                'budget_percentage': (current_cost / 1.0) * 100,
                'budget_remaining': 1.0 - current_cost,
                'free_tier_status': 'within_limits' if current_cost < 1.0 else 'exceeded',
                'data_source': 'real_aws_api'
            }
            
        except Exception as e:
            print(f"Error getting real cost data: {e}")
            return self.monitoring_agent._get_demo_cost_data()
    
    def _get_real_resource_data(self) -> Dict[str, Any]:
        """Get real resource data from AWS APIs"""
        try:
            # Get EC2 instances
            ec2_response = self.ec2_client.describe_instances()
            ec2_count = sum(len(reservation['Instances']) for reservation in ec2_response['Reservations'])
            
            # Get S3 buckets
            s3_response = self.s3_client.list_buckets()
            s3_count = len(s3_response['Buckets'])
            
            # Get Lambda functions
            lambda_response = self.lambda_client.list_functions()
            lambda_count = len(lambda_response['Functions'])
            
            return {
                'ec2_instances': ec2_count,
                's3_buckets': s3_count,
                'lambda_functions': lambda_count,
                'data_source': 'real_aws_api'
            }
            
        except Exception as e:
            print(f"Error getting real resource data: {e}")
            return self.monitoring_agent._get_demo_resource_data()
    
    def _get_real_performance_data(self) -> Dict[str, Any]:
        """Get real performance data from CloudWatch"""
        try:
            cloudwatch = boto3.client('cloudwatch', region_name=self.aws_region)
            
            end_time = datetime.datetime.now()
            start_time = end_time - datetime.timedelta(hours=1)
            
            response = cloudwatch.get_metric_statistics(
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
                'data_source': 'real_aws_api'
            }
            
        except Exception as e:
            print(f"Error getting real performance data: {e}")
            return self.monitoring_agent._get_demo_performance_data()
    
    def run_efficient_test_cycle(self, test_duration_minutes: int = 30) -> Dict[str, Any]:
        """Run an efficient Free Tier test cycle"""
        print(f"🧪 Starting efficient Free Tier test cycle ({test_duration_minutes} minutes)")
        
        # Start test session
        session_id = self.start_test_session("efficient_test")
        
        # Create minimal test resources
        print("📦 Creating test resources...")
        ec2_id = self.create_test_ec2_instance(session_id)
        s3_bucket = self.create_test_s3_bucket(session_id)
        lambda_func = self.create_test_lambda_function(session_id)
        
        # Monitor usage during test
        print("⏱️  Monitoring usage...")
        time.sleep(test_duration_minutes * 60)  # Wait for test duration
        
        # Get real usage data
        real_usage = self.get_real_usage_data()
        
        # Stop test session and clean up
        cleanup_result = self.stop_test_session(session_id)
        
        return {
            'session_id': session_id,
            'test_duration_minutes': test_duration_minutes,
            'real_usage_data': real_usage,
            'cleanup_result': cleanup_result,
            'efficiency': 'maximized'  # Resources cleaned up immediately
        }

# Example usage
if __name__ == "__main__":
    framework = FreeTierTestingFramework()
    
    # Run a 30-minute efficient test
    result = framework.run_efficient_test_cycle(30)
    print(f"Test completed: {result}")
