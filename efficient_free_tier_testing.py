"""
Efficient Free Tier Testing Script
Start/Stop testing to maximize Free Tier efficiency
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

def efficient_free_tier_test():
    """Run efficient Free Tier testing with start/stop capabilities"""
    
    print("🧪 EFFICIENT FREE TIER TESTING")
    print("=" * 50)
    
    # Initialize agent
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Check current usage BEFORE testing
    print("1. Checking current Free Tier usage...")
    before_usage = agent.check_free_tier_usage()
    
    print(f"   💰 Current Cost: ${before_usage['usage_summary']['total_cost']:.4f}")
    print(f"   📊 Budget Remaining: ${before_usage['usage_summary']['budget_remaining']:.4f}")
    print(f"   🚨 Alerts: {len(before_usage['alerts'])}")
    
    if before_usage['usage_summary']['total_cost'] > 0.8:
        print("   ⚠️  WARNING: Already at 80% of Free Tier budget!")
        print("   💡 Consider stopping other AWS resources before testing")
        return
    
    # Simulate efficient testing (no actual resource creation)
    print("2. Simulating efficient Free Tier testing...")
    print("   🚀 Starting test resources...")
    print("   ⏱️  Running test for 5 minutes...")
    print("   🧹 Cleaning up resources immediately...")
    
    # Simulate test duration
    time.sleep(2)  # 2 seconds for demo
    
    # Check usage AFTER testing
    print("3. Checking usage after testing...")
    after_usage = agent.check_free_tier_usage()
    
    print(f"   💰 Cost After: ${after_usage['usage_summary']['total_cost']:.4f}")
    print(f"   📊 Budget Remaining: ${after_usage['usage_summary']['budget_remaining']:.4f}")
    print(f"   🚨 Alerts: {len(after_usage['alerts'])}")
    
    # Calculate efficiency
    cost_increase = after_usage['usage_summary']['total_cost'] - before_usage['usage_summary']['total_cost']
    print(f"   📈 Cost Increase: ${cost_increase:.4f}")
    
    if cost_increase < 0.01:  # Less than 1 cent
        print("   ✅ EFFICIENT: Minimal cost increase!")
    else:
        print("   ⚠️  WARNING: Significant cost increase!")
    
    print("\n💡 EFFICIENT TESTING STRATEGY:")
    print("   1. Start test resources only when needed")
    print("   2. Run tests for minimal time")
    print("   3. Stop/cleanup resources immediately")
    print("   4. Monitor usage continuously")
    print("   5. Stay within Free Tier limits")

def show_free_tier_limits():
    """Show Free Tier limits and current usage"""
    
    print("\n📊 FREE TIER LIMITS & USAGE")
    print("=" * 50)
    
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Get Free Tier limits
    limits = agent.logic_engine.get_free_tier_limits()
    thresholds = agent.logic_engine.get_free_tier_thresholds()
    
    print("📋 Free Tier Limits:")
    print(f"   💰 Monthly Budget: ${limits['monthly_budget']}")
    print(f"   🖥️  EC2 Hours: {limits['ec2_hours']}/month")
    print(f"   🗄️  S3 Storage: {limits['s3_storage']} GB")
    print(f"   ⚡ Lambda Requests: {limits['lambda_requests']:,}/month")
    
    print("\n🚨 Alert Thresholds:")
    print(f"   ⚠️  50% Budget: ${thresholds['cost']['high']}")
    print(f"   🚨 80% Budget: ${thresholds['cost']['critical']}")
    print(f"   💥 Exceeded: ${thresholds['cost']['exceeded']}")
    
    # Get current usage
    usage = agent.check_free_tier_usage()
    
    print("\n📊 Current Usage:")
    print(f"   💰 Cost: ${usage['usage_summary']['total_cost']:.4f}")
    print(f"   📊 Budget %: {(usage['usage_summary']['total_cost'] / 1.0) * 100:.1f}%")
    print(f"   🖥️  EC2 %: {usage['usage_summary']['ec2_usage_percentage']:.1f}%")
    print(f"   🗄️  S3 %: {usage['usage_summary']['s3_usage_percentage']:.1f}%")
    
    # Show alerts
    if usage['alerts']:
        print("\n🚨 ACTIVE ALERTS:")
        for alert in usage['alerts']:
            print(f"   - {alert['description']}")
    else:
        print("\n✅ No active alerts")

if __name__ == "__main__":
    print("🚀 Starting Efficient Free Tier Testing...")
    
    try:
        show_free_tier_limits()
        efficient_free_tier_test()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This is expected if AWS credentials aren't configured")
        print("💡 The monitoring system will use demo data for testing")
