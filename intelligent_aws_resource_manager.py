"""
Intelligent AWS Resource Manager
Uses the enhanced monitoring agent to analyze and manage AWS resources with approval
"""

import sys
import os
from datetime import datetime

# Add intelligent-agents to path
current_dir = os.path.dirname(os.path.abspath(__file__))
intelligent_agents_dir = os.path.join(current_dir, 'intelligent-agents')
sys.path.insert(0, intelligent_agents_dir)

from agents.aws_usage_monitoring import IntelligentAWSUsageMonitoringAgent

def main():
    """Main resource management workflow"""
    
    print("🤖 INTELLIGENT AWS RESOURCE MANAGER")
    print("=" * 60)
    print("This agent will analyze your AWS resources and get your approval")
    print("before making any changes to help optimize your Free Tier usage.")
    print()
    
    # Initialize the monitoring agent
    print("1. Initializing AWS Usage Monitoring Agent...")
    agent = IntelligentAWSUsageMonitoringAgent()
    
    # Check current Free Tier usage
    print("2. Checking current Free Tier usage...")
    usage_check = agent.check_free_tier_usage()
    
    print(f"   💰 Current Cost: ${usage_check['usage_summary']['total_cost']:.4f}")
    print(f"   📊 Budget Remaining: ${usage_check['usage_summary']['budget_remaining']:.4f}")
    print(f"   📈 Budget Percentage: {(usage_check['usage_summary']['total_cost'] / 1.0) * 100:.1f}%")
    print(f"   🚨 Active Alerts: {len(usage_check['alerts'])}")
    
    if usage_check['alerts']:
        print("   🚨 ALERTS:")
        for alert in usage_check['alerts']:
            print(f"      - {alert['description']}")
    
    # Analyze active resources
    print("\n3. Analyzing active AWS resources...")
    active_resources = agent.analyze_active_resources()
    
    # Display resource summary
    print(f"\n📊 ACTIVE RESOURCES SUMMARY:")
    print(f"   🖥️  EC2 Instances: {len(active_resources['ec2_instances'])}")
    print(f"   🗄️  S3 Buckets: {len(active_resources['s3_buckets'])}")
    print(f"   ⚡ Lambda Functions: {len(active_resources['lambda_functions'])}")
    print(f"   🗃️  RDS Instances: {len(active_resources['rds_instances'])}")
    
    # Show detailed resource information
    if active_resources['ec2_instances']:
        print(f"\n🖥️  EC2 INSTANCES:")
        for instance in active_resources['ec2_instances']:
            print(f"   - {instance['id']} ({instance['type']}) - {instance['state']}")
            print(f"     Cost: ${instance['estimated_cost_per_hour']:.4f}/hour")
            print(f"     Launch: {instance['launch_time']}")
    
    if active_resources['s3_buckets']:
        print(f"\n🗄️  S3 BUCKETS:")
        for bucket in active_resources['s3_buckets']:
            print(f"   - {bucket['name']}")
            print(f"     Objects: {bucket['object_count']}")
            print(f"     Cost: ${bucket['estimated_cost_per_month']:.4f}/month")
    
    if active_resources['lambda_functions']:
        print(f"\n⚡ LAMBDA FUNCTIONS:")
        for function in active_resources['lambda_functions']:
            print(f"   - {function['name']} ({function['runtime']})")
            print(f"     Size: {function['code_size']} bytes")
    
    if active_resources['rds_instances']:
        print(f"\n🗃️  RDS INSTANCES:")
        for db in active_resources['rds_instances']:
            print(f"   - {db['id']} ({db['engine']}) - {db['status']}")
            print(f"     Cost: ${db['estimated_cost_per_hour']:.4f}/hour")
    
    # Get intelligent recommendations
    print("\n4. Generating intelligent recommendations...")
    recommendations = agent.get_resource_management_recommendations(active_resources)
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print(f"   🔴 High Priority: {len(recommendations['high_priority'])}")
    print(f"   🟡 Medium Priority: {len(recommendations['medium_priority'])}")
    print(f"   🟢 Low Priority: {len(recommendations['low_priority'])}")
    print(f"   💰 Total Potential Savings: ${recommendations['total_potential_savings']:.2f}/month")
    
    # Show recommendations
    if recommendations['high_priority']:
        print(f"\n🔴 HIGH PRIORITY RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations['high_priority'], 1):
            print(f"   {i}. {rec['resource_type']} - {rec['resource_id']}")
            print(f"      Action: {rec['action']}")
            print(f"      Reason: {rec['reason']}")
            print(f"      Savings: ${rec['potential_savings']:.2f}/month")
            print(f"      Risk: {rec['risk']}")
    
    if recommendations['medium_priority']:
        print(f"\n🟡 MEDIUM PRIORITY RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations['medium_priority'], 1):
            print(f"   {i}. {rec['resource_type']} - {rec['resource_id']}")
            print(f"      Action: {rec['action']}")
            print(f"      Reason: {rec['reason']}")
    
    if recommendations['low_priority']:
        print(f"\n🟢 LOW PRIORITY RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations['low_priority'], 1):
            print(f"   {i}. {rec['resource_type']} - {rec['resource_id']}")
            print(f"      Action: {rec['action']}")
            print(f"      Reason: {rec['reason']}")
    
    # Ask user if they want to proceed with recommendations
    if any([recommendations['high_priority'], recommendations['medium_priority'], recommendations['low_priority']]):
        print(f"\n❓ Do you want to proceed with these recommendations?")
        print("   The agent will ask for your approval before each action.")
        
        while True:
            response = input("   Continue? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                # Execute approved actions
                print(f"\n5. Executing approved resource management actions...")
                results = agent.execute_approved_resource_actions(recommendations)
                
                print(f"\n📊 EXECUTION RESULTS:")
                print(f"   ✅ Successful: {len(results['successful'])}")
                print(f"   ❌ Failed: {len(results['failed'])}")
                print(f"   💰 Total Savings: ${results['total_savings']:.2f}/month")
                
                if results['successful']:
                    print(f"\n✅ SUCCESSFUL ACTIONS:")
                    for action in results['successful']:
                        print(f"   - {action['resource_type']} {action['resource_id']}: {action['action']}")
                
                if results['failed']:
                    print(f"\n❌ FAILED ACTIONS:")
                    for action in results['failed']:
                        print(f"   - {action['resource_type']} {action['resource_id']}: {action['action']}")
                
                break
            elif response in ['n', 'no']:
                print("   Resource management cancelled.")
                break
            else:
                print("   Please enter 'y' for yes or 'n' for no.")
    else:
        print("\n✅ No recommendations found. Your AWS resources are already optimized!")
    
    # Final usage check
    print(f"\n6. Final Free Tier usage check...")
    final_usage = agent.check_free_tier_usage()
    
    print(f"   💰 Final Cost: ${final_usage['usage_summary']['total_cost']:.4f}")
    print(f"   📊 Budget Remaining: ${final_usage['usage_summary']['budget_remaining']:.4f}")
    print(f"   📈 Budget Percentage: {(final_usage['usage_summary']['total_cost'] / 1.0) * 100:.1f}%")
    
    if final_usage['usage_summary']['total_cost'] < usage_check['usage_summary']['total_cost']:
        savings = usage_check['usage_summary']['total_cost'] - final_usage['usage_summary']['total_cost']
        print(f"   💰 Cost Reduction: ${savings:.4f}")
        print(f"   ✅ Successfully optimized your AWS usage!")
    else:
        print(f"   ℹ️  No cost reduction achieved.")
    
    print(f"\n🎉 Resource management completed!")
    print(f"💡 Monitor your usage regularly to stay within Free Tier limits.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Resource management interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"💡 Make sure AWS credentials are configured properly.")
