"""
Enhanced Data Processing Module for AI-AH Platform.

This module provides comprehensive data processing capabilities using pandas,
NumPy, and SciPy for local dataset analysis and manipulation.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import sqlite3
from pathlib import Path
import logging

from ..base_platform import BasePlatformComponent, PlatformConfig, Task, ComponentStatus


@dataclass
class DataSource:
    """Represents a data source for processing."""
    name: str
    path: str
    format: str  # csv, json, excel, sqlite
    description: str
    metadata: Dict[str, Any]


@dataclass
class DataAnalysis:
    """Results of data analysis."""
    source_name: str
    analysis_type: str
    results: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime


class DataProcessor(BasePlatformComponent):
    """
    Enhanced data processor with pandas, NumPy, and SciPy capabilities.
    
    Provides comprehensive data processing for:
    - CSV/Excel file processing
    - Statistical analysis
    - Data visualization insights
    - Infrastructure metrics analysis
    """
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.data_sources: Dict[str, DataSource] = {}
        self.analysis_cache: Dict[str, DataAnalysis] = {}
        
    async def initialize(self) -> bool:
        """Initialize the data processor."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info("Initializing Data Processor")
            
            # Initialize pandas options
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', 50)
            
            self.status = ComponentStatus.READY
            self.logger.info("Data Processor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Data Processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the data processor."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info("Data Processor started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Data Processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the data processor."""
        try:
            self.status = ComponentStatus.STOPPED
            self.logger.info("Data Processor stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop Data Processor: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return {
            "status": self.status.value,
            "data_sources": len(self.data_sources),
            "analysis_cache": len(self.analysis_cache),
            "healthy": self.status == ComponentStatus.RUNNING
        }
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.task_type == "analyze_data":
            source_name = task.parameters.get("source_name")
            if source_name and source_name in self.data_sources:
                df = self.load_data(source_name)
                if df is not None:
                    return self.analyze_infrastructure_metrics(df)
        return {"status": "completed", "task_id": task.id}
    
    def register_data_source(self, source: DataSource) -> bool:
        """Register a new data source."""
        try:
            self.data_sources[source.name] = source
            self.logger.info(f"Registered data source: {source.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register data source {source.name}: {str(e)}")
            return False
    
    def load_data(self, source_name: str) -> Optional[pd.DataFrame]:
        """Load data from a registered source."""
        if source_name not in self.data_sources:
            self.logger.error(f"Data source {source_name} not found")
            return None
        
        source = self.data_sources[source_name]
        
        try:
            if source.format.lower() == 'csv':
                df = pd.read_csv(source.path)
            elif source.format.lower() == 'excel':
                df = pd.read_excel(source.path)
            elif source.format.lower() == 'json':
                df = pd.read_json(source.path)
            elif source.format.lower() == 'sqlite':
                df = pd.read_sql_query("SELECT * FROM data", f"sqlite:///{source.path}")
            else:
                self.logger.error(f"Unsupported format: {source.format}")
                return None
            
            self.logger.info(f"Loaded {len(df)} rows from {source_name}")
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load data from {source_name}: {str(e)}")
            return None
    
    def analyze_infrastructure_metrics(self, df: pd.DataFrame) -> DataAnalysis:
        """Analyze infrastructure metrics data."""
        insights = []
        recommendations = []
        results = {}
        
        try:
            # Basic statistics
            results['basic_stats'] = df.describe().to_dict()
            
            # Performance metrics analysis
            if 'response_time' in df.columns:
                response_times = df['response_time'].dropna()
                results['performance'] = {
                    'mean_response_time': response_times.mean(),
                    'median_response_time': response_times.median(),
                    'p95_response_time': response_times.quantile(0.95),
                    'p99_response_time': response_times.quantile(0.99)
                }
                
                # Performance insights
                if results['performance']['p95_response_time'] > 2.0:
                    insights.append("95th percentile response time exceeds 2 seconds")
                    recommendations.append("Consider optimizing slow endpoints")
            
            # Resource utilization analysis
            if 'cpu_usage' in df.columns and 'memory_usage' in df.columns:
                cpu_usage = df['cpu_usage'].dropna()
                memory_usage = df['memory_usage'].dropna()
                
                results['resource_utilization'] = {
                    'avg_cpu_usage': cpu_usage.mean(),
                    'avg_memory_usage': memory_usage.mean(),
                    'cpu_utilization_std': cpu_usage.std(),
                    'memory_utilization_std': memory_usage.std()
                }
                
                # Resource insights
                if results['resource_utilization']['avg_cpu_usage'] > 80:
                    insights.append("High CPU utilization detected")
                    recommendations.append("Consider horizontal scaling or resource optimization")
                
                if results['resource_utilization']['avg_memory_usage'] > 85:
                    insights.append("High memory utilization detected")
                    recommendations.append("Review memory usage patterns and optimize")
            
            # Error rate analysis
            if 'status_code' in df.columns:
                error_codes = df[df['status_code'] >= 400]
                error_rate = len(error_codes) / len(df) * 100
                
                results['error_analysis'] = {
                    'total_requests': len(df),
                    'error_requests': len(error_codes),
                    'error_rate': error_rate,
                    'error_distribution': error_codes['status_code'].value_counts().to_dict()
                }
                
                if error_rate > 5:
                    insights.append(f"High error rate detected: {error_rate:.2f}%")
                    recommendations.append("Investigate and fix error sources")
            
            # Trend analysis
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df_sorted = df.sort_values('timestamp')
                
                # Calculate trends
                if len(df_sorted) > 1:
                    time_diff = (df_sorted['timestamp'].iloc[-1] - df_sorted['timestamp'].iloc[0]).total_seconds()
                    if time_diff > 0:
                        results['trend_analysis'] = {
                            'time_span_hours': time_diff / 3600,
                            'data_points': len(df_sorted),
                            'sampling_rate': len(df_sorted) / (time_diff / 3600)
                        }
            
            # Correlation analysis
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) > 1:
                correlation_matrix = df[numeric_columns].corr()
                results['correlations'] = correlation_matrix.to_dict()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr_value = correlation_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:
                            strong_correlations.append({
                                'variable1': correlation_matrix.columns[i],
                                'variable2': correlation_matrix.columns[j],
                                'correlation': corr_value
                            })
                
                if strong_correlations:
                    results['strong_correlations'] = strong_correlations
                    insights.append(f"Found {len(strong_correlations)} strong correlations between variables")
            
            # Statistical significance tests
            if 'response_time' in df.columns and 'status_code' in df.columns:
                success_times = df[df['status_code'] < 400]['response_time'].dropna()
                error_times = df[df['status_code'] >= 400]['response_time'].dropna()
                
                if len(success_times) > 10 and len(error_times) > 10:
                    # T-test for response time differences
                    t_stat, p_value = stats.ttest_ind(success_times, error_times)
                    results['statistical_tests'] = {
                        'response_time_ttest': {
                            't_statistic': t_stat,
                            'p_value': p_value,
                            'significant': p_value < 0.05
                        }
                    }
                    
                    if p_value < 0.05:
                        insights.append("Statistically significant difference in response times between success and error cases")
            
            return DataAnalysis(
                source_name="infrastructure_metrics",
                analysis_type="comprehensive",
                results=results,
                insights=insights,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze infrastructure metrics: {str(e)}")
            return DataAnalysis(
                source_name="infrastructure_metrics",
                analysis_type="error",
                results={"error": str(e)},
                insights=[],
                recommendations=[],
                timestamp=datetime.now()
            )
    
    def analyze_cost_data(self, df: pd.DataFrame) -> DataAnalysis:
        """Analyze cloud cost data."""
        insights = []
        recommendations = []
        results = {}
        
        try:
            # Cost analysis
            if 'cost' in df.columns:
                costs = df['cost'].dropna()
                results['cost_analysis'] = {
                    'total_cost': costs.sum(),
                    'average_cost': costs.mean(),
                    'median_cost': costs.median(),
                    'cost_std': costs.std(),
                    'min_cost': costs.min(),
                    'max_cost': costs.max()
                }
                
                # Cost insights
                if results['cost_analysis']['cost_std'] > results['cost_analysis']['average_cost'] * 0.5:
                    insights.append("High cost variability detected")
                    recommendations.append("Review cost allocation and optimization opportunities")
            
            # Service-wise cost breakdown
            if 'service' in df.columns and 'cost' in df.columns:
                service_costs = df.groupby('service')['cost'].agg(['sum', 'mean', 'count']).to_dict()
                results['service_breakdown'] = service_costs
                
                # Find expensive services
                total_cost = df['cost'].sum()
                expensive_services = []
                for service, cost_sum in service_costs['sum'].items():
                    if cost_sum > total_cost * 0.2:  # More than 20% of total cost
                        expensive_services.append({
                            'service': service,
                            'cost': cost_sum,
                            'percentage': (cost_sum / total_cost) * 100
                        })
                
                if expensive_services:
                    results['expensive_services'] = expensive_services
                    insights.append(f"Found {len(expensive_services)} services consuming >20% of total cost")
                    recommendations.append("Review expensive services for optimization opportunities")
            
            # Time-based cost trends
            if 'date' in df.columns and 'cost' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                daily_costs = df.groupby(df['date'].dt.date)['cost'].sum()
                
                results['daily_trends'] = {
                    'daily_average': daily_costs.mean(),
                    'daily_std': daily_costs.std(),
                    'trend_slope': np.polyfit(range(len(daily_costs)), daily_costs.values, 1)[0]
                }
                
                if results['daily_trends']['trend_slope'] > 0:
                    insights.append("Increasing daily cost trend detected")
                    recommendations.append("Implement cost monitoring and alerting")
            
            return DataAnalysis(
                source_name="cost_data",
                analysis_type="cost_optimization",
                results=results,
                insights=insights,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze cost data: {str(e)}")
            return DataAnalysis(
                source_name="cost_data",
                analysis_type="error",
                results={"error": str(e)},
                insights=[],
                recommendations=[],
                timestamp=datetime.now()
            )
    
    def generate_data_report(self, analysis: DataAnalysis) -> str:
        """Generate a human-readable data analysis report."""
        report_parts = [
            f"# Data Analysis Report: {analysis.source_name}",
            f"**Analysis Type**: {analysis.analysis_type}",
            f"**Generated**: {analysis.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Key Findings",
        ]
        
        # Add insights
        if analysis.insights:
            report_parts.append("### Insights")
            for insight in analysis.insights:
                report_parts.append(f"- {insight}")
            report_parts.append("")
        
        # Add recommendations
        if analysis.recommendations:
            report_parts.append("### Recommendations")
            for rec in analysis.recommendations:
                report_parts.append(f"- {rec}")
            report_parts.append("")
        
        # Add detailed results
        report_parts.append("## Detailed Analysis")
        for key, value in analysis.results.items():
            if isinstance(value, dict):
                report_parts.append(f"### {key.replace('_', ' ').title()}")
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        report_parts.append(f"- **{sub_key}**: {sub_value:.2f}")
                    else:
                        report_parts.append(f"- **{sub_key}**: {sub_value}")
                report_parts.append("")
        
        return "\n".join(report_parts)
    
    def export_analysis(self, analysis: DataAnalysis, format: str = 'json') -> str:
        """Export analysis results to various formats."""
        if format.lower() == 'json':
            return json.dumps({
                'source_name': analysis.source_name,
                'analysis_type': analysis.analysis_type,
                'results': analysis.results,
                'insights': analysis.insights,
                'recommendations': analysis.recommendations,
                'timestamp': analysis.timestamp.isoformat()
            }, indent=2)
        elif format.lower() == 'csv':
            # Convert results to CSV format
            df = pd.json_normalize(analysis.results)
            return df.to_csv(index=False)
        else:
            return self.generate_data_report(analysis)
