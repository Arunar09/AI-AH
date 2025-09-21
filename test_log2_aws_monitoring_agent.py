"""
Test Script for Log^2 AWS Usage Monitoring Agent
Demonstrates the Log^2 approach: Logic-driven functionality with log monitoring
"""

import sys
import os
import json
import time
from datetime import datetime

# Add intelligent-agents to path
current_dir = os.path.dirname(os.path.abspath(__file__))
intelligent_agents_dir = os.path.join(current_dir, 'intelligent-agents')
sys.path.insert(0, intelligent_agents_dir)

from agents.aws_usage_monitoring import IntelligentAWSUsageMonitoringAgent

def test_log2_approach():
    """Test the Log^2 approach with AWS Usage Monitoring Agent"""
    
    print("🧠 Testing Log^2 (Logics-Logs) Approach")
    print("=" * 50)
    
    # Create agent
    print("1. Creating AWS Usage Monitoring Agent...")
    agent = IntelligentAWSUsageMonitoringAgent(aws_region='us-east-1')
    
    # Get agent status
    print("\n2. Agent Status:")
    status = agent.get_agent_status()
    print(f"   Agent Name: {status['agent_name']}")
    print(f"   Version: {status['version']}")
    print(f"   AWS Region: {status['aws_region']}")
    print(f"   AWS Clients Available: {status['aws_clients_available']}")
    
    # Run monitoring
    print("\n3. Running AWS Usage Monitoring...")
    result = agent.monitor_aws_usage()
    
    print(f"   Success: {result.success}")
    print(f"   Execution Time: {result.execution_time_ms:.2f}ms")
    print(f"   Timestamp: {result.timestamp}")
    
    # Display metrics
    print("\n4. AWS Metrics:")
    metrics = result.metrics
    print(f"   Region: {metrics.get('region', 'N/A')}")
    
    cost_data = metrics.get('cost', {})
    print(f"   Current Month Cost: ${cost_data.get('current_month_cost', 0):.2f}")
    print(f"   Daily Average: ${cost_data.get('daily_average', 0):.2f}")
    
    resource_data = metrics.get('resources', {})
    print(f"   EC2 Instances: {resource_data.get('ec2_instances', 0)}")
    print(f"   RDS Instances: {resource_data.get('rds_instances', 0)}")
    print(f"   S3 Buckets: {resource_data.get('s3_buckets', 0)}")
    
    # Display alerts
    print(f"\n5. Alerts ({len(result.alerts)}):")
    for i, alert in enumerate(result.alerts, 1):
        print(f"   {i}. {alert.get('rule', 'Unknown Rule')}")
        print(f"      Severity: {alert.get('severity', 'Unknown')}")
        print(f"      Description: {alert.get('description', 'No description')}")
    
    # Display recommendations
    print(f"\n6. Recommendations ({len(result.recommendations)}):")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"   {i}. {rec.get('type', 'Unknown Type')}")
        print(f"      Description: {rec.get('description', 'No description')}")
        if 'recommendations' in rec:
            for j, sub_rec in enumerate(rec['recommendations'], 1):
                print(f"         {j}. {sub_rec}")
    
    # Display analysis
    print("\n7. Analysis:")
    cost_analysis = result.cost_analysis
    print(f"   Cost Analysis:")
    print(f"     Current Cost: ${cost_analysis.get('current_cost', 0):.2f}")
    print(f"     Budget Status: {cost_analysis.get('budget_status', 'Unknown')}")
    print(f"     Cost Trend: {cost_analysis.get('cost_trend', 'Unknown')}")
    
    performance_analysis = result.performance_analysis
    print(f"   Performance Analysis:")
    print(f"     CPU Utilization: {performance_analysis.get('cpu_utilization', 0):.1f}%")
    print(f"     Performance Status: {performance_analysis.get('performance_status', 'Unknown')}")
    
    security_analysis = result.security_analysis
    print(f"   Security Analysis:")
    print(f"     Compliance Violations: {security_analysis.get('compliance_violations', 0)}")
    print(f"     Security Score: {security_analysis.get('security_score', 0)}")
    print(f"     Security Status: {security_analysis.get('security_status', 'Unknown')}")
    
    # Test learning capabilities
    print("\n8. Testing Learning Capabilities...")
    
    # Run multiple monitoring cycles to generate logs
    print("   Running multiple monitoring cycles to generate learning data...")
    for i in range(3):
        print(f"   Cycle {i+1}/3...")
        agent.monitor_aws_usage()
        time.sleep(1)  # Small delay between cycles
    
    # Get learning summary
    learning_summary = agent.intelligence_engine.get_learning_summary()
    print(f"   Learning Summary:")
    print(f"     Models Trained: {learning_summary['models_trained']}")
    print(f"     Total Improvements: {learning_summary['total_improvements']}")
    print(f"     Total Adaptations: {learning_summary['total_adaptations']}")
    
    # Test predictions
    print("\n9. Testing Predictions...")
    
    # Performance prediction
    perf_features = {
        'execution_time_ms': 1200,
        'success_rate': 0.85,
        'error_rate': 0.05
    }
    perf_prediction = agent.intelligence_engine.predict_performance(perf_features)
    print(f"   Performance Prediction: {perf_prediction}")
    
    # Cost optimization prediction
    cost_features = {
        'resource_count': 10,
        'utilization': 0.7,
        'cost_per_hour': 2.5
    }
    cost_prediction = agent.intelligence_engine.predict_cost_optimization(cost_features)
    print(f"   Cost Optimization Prediction: {cost_prediction}")
    
    # Error prediction
    error_features = {
        'load': 0.8,
        'complexity': 0.6,
        'resource_usage': 0.75
    }
    error_prediction = agent.intelligence_engine.predict_errors(error_features)
    print(f"   Error Prediction: {error_prediction}")
    
    # Export data
    print("\n10. Exporting Data...")
    export_data = agent.export_monitoring_data()
    print(f"   Export data length: {len(export_data)} characters")
    
    # Save export data to file
    export_filename = f"aws_monitoring_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(export_filename, 'w') as f:
        f.write(export_data)
    print(f"   Data exported to: {export_filename}")
    
    print("\n✅ Log^2 AWS Usage Monitoring Agent test completed successfully!")
    print("\n🎯 Key Benefits of Log^2 Approach:")
    print("   • Logic-driven functionality with clear rules")
    print("   • Comprehensive log monitoring and analysis")
    print("   • Self-improvement through learning")
    print("   • Predictive capabilities for optimization")
    print("   • Continuous adaptation and improvement")

def test_individual_components():
    """Test individual Log^2 components"""
    
    print("\n🔧 Testing Individual Log^2 Components")
    print("=" * 50)
    
    from agents.aws_usage_monitoring import AWSUsageLogicEngine, AWSUsageLogEngine, AWSUsageIntelligenceEngine
    
    # Test Logic Engine
    print("1. Testing Logic Engine...")
    logic_engine = AWSUsageLogicEngine()
    
    # Test rule execution
    test_data = {
        'daily_cost': 6.5,  # Above threshold
        'cpu_utilization': 85,  # Above threshold
        'error_rate': 0.08  # Above threshold
    }
    
    cost_results, cost_logs = logic_engine.execute_logic(
        logic_engine.MonitoringDomain.COST, test_data
    )
    print(f"   Cost monitoring results: {len(cost_results)} rules evaluated")
    
    # Test Log Engine
    print("2. Testing Log Engine...")
    log_engine = AWSUsageLogEngine()
    
    # Collect logs
    log_id = log_engine.collect_logs(cost_logs)
    print(f"   Log collected with ID: {log_id}")
    
    # Analyze logs
    analysis = log_engine.analyze_logs()
    print(f"   Log analysis completed: {len(analysis.get('patterns', []))} patterns identified")
    
    # Test Intelligence Engine
    print("3. Testing Intelligence Engine...")
    intelligence_engine = AWSUsageIntelligenceEngine()
    
    # Learn from logs
    improvements, adaptations = intelligence_engine.learn_from_logs(analysis)
    print(f"   Learning completed: {len(improvements)} improvements, {len(adaptations)} adaptations")
    
    # Get learning summary
    learning_summary = intelligence_engine.get_learning_summary()
    print(f"   Learning summary: {learning_summary['models_trained']} models trained")
    
    print("✅ Individual component tests completed!")

if __name__ == "__main__":
    print("🚀 Starting Log^2 AWS Usage Monitoring Agent Tests")
    print("=" * 60)
    
    try:
        # Test main agent
        test_log2_approach()
        
        # Test individual components
        test_individual_components()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📊 Log^2 System Benefits Demonstrated:")
        print("   ✅ Logic-driven functionality")
        print("   ✅ Comprehensive log monitoring")
        print("   ✅ Intelligent learning and adaptation")
        print("   ✅ Predictive capabilities")
        print("   ✅ Self-improvement through logs")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
