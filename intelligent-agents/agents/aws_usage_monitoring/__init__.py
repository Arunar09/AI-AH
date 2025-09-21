"""
AWS Usage Monitoring Agent
Log^2 approach: Logic-driven functionality with log monitoring and self-improvement
"""

from .aws_usage_monitoring_agent import IntelligentAWSUsageMonitoringAgent
from .aws_usage_logic_engine import AWSUsageLogicEngine, MonitoringDomain, MonitoringRule, LogicWorkflow
from .aws_usage_log_engine import AWSUsageLogEngine, LogEntry, LogPattern, LogInsight
from .aws_usage_intelligence_engine import AWSUsageIntelligenceEngine, Improvement, Adaptation, LearningModel

__all__ = [
    'IntelligentAWSUsageMonitoringAgent',
    'AWSUsageLogicEngine',
    'MonitoringDomain',
    'MonitoringRule',
    'LogicWorkflow',
    'AWSUsageLogEngine',
    'LogEntry',
    'LogPattern',
    'LogInsight',
    'AWSUsageIntelligenceEngine',
    'Improvement',
    'Adaptation',
    'LearningModel'
]

__version__ = "1.0.0"
__author__ = "Intelligent Agents Team"
__description__ = "AWS Usage Monitoring Agent with Log^2 approach"
