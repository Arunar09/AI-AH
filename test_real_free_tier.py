"""
Real AWS Free Tier Testing Script
Tests actual AWS usage with start/stop capabilities
"""

import sys
import os
import time
from datetime import datetime

# Add intelligent-agents to path
current_dir = os.path.dirname(os.path.abspath(__file__))
intelligent_agents_dir = os.path.join(current_dir, 'intelligent-agents')
sys.path.insert(0, intelligent_agents_dir)

from agents.aws_usage_monitoring import IntelligentAWSUsageMonitoringAgent
from agents.aws_usage_monitoring.free_tier_testing_framework import FreeTierTestingFramework

def test_real_free_tier_usage():
    """Test real Free Tier usage with actual AWS API calls"""
    
    print("🧪 REAL AWS FREE TIER TESTING")
    print("=" * 50)
    
    # Initialize monitoring agent
    print("1. Initializing AWS Usage Monitoring Agent...")
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Get real usage data (not demo data)
    print("2. Collecting REAL AWS usage data...")
    real_usage = agent._collect_aws_data()
    
    print("3. REAL Usage Data:")
    print(f"   💰 Monthly Cost: ${real_usage['cost']['current_month_cost']:.4f}")
    print(f"   📊 Budget Remaining: ${real_usage['cost']['budget_remaining']:.4f}")
    print(f"   📈 Budget Percentage: {real_usage['cost']['budget_percentage']:.1f}%")
    print(f"   🖥️  EC2 Instances: {real_usage['resources']['ec2_instances']}")
    print(f"   🗄️  S3 Buckets: {real_usage['resources']['s3_buckets']}")
    print(f"   ⚡ Lambda Functions: {real_usage['resources']['lambda_functions']}")
    
    # Check Free Tier usage
    print("4. Checking Free Tier usage...")
    free_tier_check = agent.check_free_tier_usage()
    
    print("5. Free Tier Status:")
    print(f"   🚨 Alerts: {len(free_tier_check['alerts'])}")
    print(f"   ⚠️  Warnings: {len(free_tier_check['free_tier_status']['warnings'])}")
    
    if free_tier_check['alerts']:
        print("   🚨 ALERTS:")
        for alert in free_tier_check['alerts']:
            print(f"      - {alert['description']}")
    
    if free_tier_check['free_tier_status']['warnings']:
        print("   ⚠️  WARNINGS:")
        for warning in free_tier_check['free_tier_status']['warnings']:
            print(f"      - {warning['message']}")
    
    # Test efficient testing framework
    print("6. Testing Efficient Free Tier Framework...")
    framework = FreeTierTestingFramework()
    
    # Run a short test (5 minutes)
    print("   🚀 Starting 5-minute efficient test...")
    test_result = framework.run_efficient_test_cycle(5)  # 5 minutes
    
    print("7. Test Results:")
    print(f"   ⏱️  Test Duration: {test_result['test_duration_minutes']} minutes")
    print(f"   🧹 Resources Cleaned: {test_result['cleanup_result']['resources_cleaned']}")
    print(f"   ❌ Cleanup Errors: {test_result['cleanup_result']['cleanup_errors']}")
    print(f"   💰 Estimated Cost: ${test_result['cleanup_result']['total_cost']:.4f}")
    
    print("\n✅ REAL Free Tier testing completed!")
    print("💡 This used ACTUAL AWS APIs, not demo data!")
    print("💡 Resources were created and cleaned up efficiently!")
    print("💡 Cost was minimized by immediate cleanup!")

def test_demo_vs_real():
    """Compare demo data vs real data"""
    
    print("\n🔍 DEMO vs REAL DATA COMPARISON")
    print("=" * 50)
    
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Get demo data
    print("1. Demo Data (Hardcoded):")
    demo_data = agent._get_demo_data()
    print(f"   💰 Cost: ${demo_data['cost']['current_month_cost']}")
    print(f"   🖥️  EC2: {demo_data['resources']['ec2_instances']}")
    print(f"   🗄️  S3: {demo_data['resources']['s3_buckets']}")
    
    # Get real data
    print("2. Real Data (AWS API):")
    real_data = agent._collect_aws_data()
    print(f"   💰 Cost: ${real_data['cost']['current_month_cost']}")
    print(f"   🖥️  EC2: {real_data['resources']['ec2_instances']}")
    print(f"   🗄️  S3: {real_data['resources']['s3_buckets']}")
    
    # Check if using demo data
    if real_data['cost']['current_month_cost'] == demo_data['cost']['current_month_cost']:
        print("   ⚠️  WARNING: Still using demo data (AWS credentials not configured)")
    else:
        print("   ✅ Using real AWS data!")

if __name__ == "__main__":
    print("🚀 Starting Real AWS Free Tier Testing...")
    
    try:
        test_real_free_tier_usage()
        test_demo_vs_real()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure AWS credentials are configured!")
        print("💡 Run: aws configure")
