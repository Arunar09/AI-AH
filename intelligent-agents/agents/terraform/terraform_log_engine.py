"""
Terraform Log Engine - Log^2 Architecture
Log collection, storage, and analysis for Terraform operations
"""

import os
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import re

@dataclass
class TerraformOperationLog:
    """Log entry for a Terraform operation"""
    log_id: str
    timestamp: datetime
    operation_type: str
    operation_id: str
    user_id: Optional[str]
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    success: bool
    error_message: Optional[str]
    execution_time: float
    resource_changes: List[Dict[str, Any]]
    cost_impact: float
    security_impact: str
    performance_metrics: Dict[str, Any]

@dataclass
class InfrastructureStateLog:
    """Log entry for infrastructure state changes"""
    state_id: str
    timestamp: datetime
    resource_type: str
    resource_id: str
    action: str  # create, update, delete
    previous_state: Dict[str, Any]
    current_state: Dict[str, Any]
    change_reason: str
    impact_assessment: Dict[str, Any]

@dataclass
class PerformanceLog:
    """Log entry for performance metrics"""
    metric_id: str
    timestamp: datetime
    metric_type: str
    metric_name: str
    value: float
    unit: str
    resource_id: str
    threshold: Optional[float]
    alert_level: str

@dataclass
class SecurityLog:
    """Log entry for security events"""
    security_id: str
    timestamp: datetime
    event_type: str
    severity: str
    source_ip: Optional[str]
    user_agent: Optional[str]
    action: str
    resource_affected: str
    details: Dict[str, Any]

class TerraformLogEngine:
    """Log collection, storage, and analysis for Terraform operations"""
    
    def __init__(self, log_directory: str = "logs"):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(exist_ok=True)
        
        # Initialize logging
        self.logger = self._setup_logger()
        
        # Initialize database
        self.db_path = self.log_directory / "terraform_operations.db"
        self._initialize_database()
        
        # Log storage paths
        self.operation_logs_path = self.log_directory / "operations"
        self.state_logs_path = self.log_directory / "state_changes"
        self.performance_logs_path = self.log_directory / "performance"
        self.security_logs_path = self.log_directory / "security"
        
        # Create subdirectories
        for path in [self.operation_logs_path, self.state_logs_path, 
                    self.performance_logs_path, self.security_logs_path]:
            path.mkdir(exist_ok=True)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('terraform_log_engine')
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create file handler
        log_file = self.log_directory / f"terraform_log_engine_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_database(self):
        """Initialize SQLite database for log storage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create operations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operations (
                    log_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    operation_type TEXT,
                    operation_id TEXT,
                    user_id TEXT,
                    input_data TEXT,
                    output_data TEXT,
                    success BOOLEAN,
                    error_message TEXT,
                    execution_time REAL,
                    resource_changes TEXT,
                    cost_impact REAL,
                    security_impact TEXT,
                    performance_metrics TEXT
                )
            ''')
            
            # Create state changes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS state_changes (
                    state_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    resource_type TEXT,
                    resource_id TEXT,
                    action TEXT,
                    previous_state TEXT,
                    current_state TEXT,
                    change_reason TEXT,
                    impact_assessment TEXT
                )
            ''')
            
            # Create performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    metric_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    metric_type TEXT,
                    metric_name TEXT,
                    value REAL,
                    unit TEXT,
                    resource_id TEXT,
                    threshold REAL,
                    alert_level TEXT
                )
            ''')
            
            # Create security events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_events (
                    security_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    event_type TEXT,
                    severity TEXT,
                    source_ip TEXT,
                    user_agent TEXT,
                    action TEXT,
                    resource_affected TEXT,
                    details TEXT
                )
            ''')
            
            conn.commit()
    
    def log_operation(self, operation_log: TerraformOperationLog):
        """Log a Terraform operation"""
        try:
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO operations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    operation_log.log_id,
                    operation_log.timestamp.isoformat(),
                    operation_log.operation_type,
                    operation_log.operation_id,
                    operation_log.user_id,
                    json.dumps(operation_log.input_data),
                    json.dumps(operation_log.output_data),
                    operation_log.success,
                    operation_log.error_message,
                    operation_log.execution_time,
                    json.dumps(operation_log.resource_changes),
                    operation_log.cost_impact,
                    operation_log.security_impact,
                    json.dumps(operation_log.performance_metrics)
                ))
                conn.commit()
            
            # Store in JSON file for backup
            log_file = self.operation_logs_path / f"operation_{operation_log.operation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(asdict(operation_log), f, indent=2, default=str)
            
            self.logger.info(f"Logged operation: {operation_log.operation_type} - {operation_log.operation_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to log operation: {e}")
    
    def log_state_change(self, state_log: InfrastructureStateLog):
        """Log infrastructure state change"""
        try:
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO state_changes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    state_log.state_id,
                    state_log.timestamp.isoformat(),
                    state_log.resource_type,
                    state_log.resource_id,
                    state_log.action,
                    json.dumps(state_log.previous_state),
                    json.dumps(state_log.current_state),
                    state_log.change_reason,
                    json.dumps(state_log.impact_assessment)
                ))
                conn.commit()
            
            # Store in JSON file
            log_file = self.state_logs_path / f"state_{state_log.resource_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(asdict(state_log), f, indent=2, default=str)
            
            self.logger.info(f"Logged state change: {state_log.resource_type} - {state_log.resource_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to log state change: {e}")
    
    def log_performance_metric(self, performance_log: PerformanceLog):
        """Log performance metric"""
        try:
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO performance_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    performance_log.metric_id,
                    performance_log.timestamp.isoformat(),
                    performance_log.metric_type,
                    performance_log.metric_name,
                    performance_log.value,
                    performance_log.unit,
                    performance_log.resource_id,
                    performance_log.threshold,
                    performance_log.alert_level
                ))
                conn.commit()
            
            # Store in JSON file
            log_file = self.performance_logs_path / f"metric_{performance_log.metric_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(asdict(performance_log), f, indent=2, default=str)
            
            self.logger.info(f"Logged performance metric: {performance_log.metric_name} - {performance_log.value}")
            
        except Exception as e:
            self.logger.error(f"Failed to log performance metric: {e}")
    
    def log_security_event(self, security_log: SecurityLog):
        """Log security event"""
        try:
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO security_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    security_log.security_id,
                    security_log.timestamp.isoformat(),
                    security_log.event_type,
                    security_log.severity,
                    security_log.source_ip,
                    security_log.user_agent,
                    security_log.action,
                    security_log.resource_affected,
                    json.dumps(security_log.details)
                ))
                conn.commit()
            
            # Store in JSON file
            log_file = self.security_logs_path / f"security_{security_log.event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w') as f:
                json.dump(asdict(security_log), f, indent=2, default=str)
            
            self.logger.info(f"Logged security event: {security_log.event_type} - {security_log.severity}")
            
        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
    
    def get_operation_logs(self, 
                          operation_type: Optional[str] = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          limit: int = 100) -> List[TerraformOperationLog]:
        """Retrieve operation logs with filters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM operations WHERE 1=1"
                params = []
                
                if operation_type:
                    query += " AND operation_type = ?"
                    params.append(operation_type)
                
                if start_date:
                    query += " AND timestamp >= ?"
                    params.append(start_date.isoformat())
                
                if end_date:
                    query += " AND timestamp <= ?"
                    params.append(end_date.isoformat())
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                logs = []
                for row in rows:
                    log = TerraformOperationLog(
                        log_id=row[0],
                        timestamp=datetime.fromisoformat(row[1]),
                        operation_type=row[2],
                        operation_id=row[3],
                        user_id=row[4],
                        input_data=json.loads(row[5]),
                        output_data=json.loads(row[6]),
                        success=bool(row[7]),
                        error_message=row[8],
                        execution_time=row[9],
                        resource_changes=json.loads(row[10]),
                        cost_impact=row[11],
                        security_impact=row[12],
                        performance_metrics=json.loads(row[13])
                    )
                    logs.append(log)
                
                return logs
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve operation logs: {e}")
            return []
    
    def get_performance_metrics(self, 
                               metric_name: Optional[str] = None,
                               resource_id: Optional[str] = None,
                               start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> List[PerformanceLog]:
        """Retrieve performance metrics with filters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM performance_metrics WHERE 1=1"
                params = []
                
                if metric_name:
                    query += " AND metric_name = ?"
                    params.append(metric_name)
                
                if resource_id:
                    query += " AND resource_id = ?"
                    params.append(resource_id)
                
                if start_date:
                    query += " AND timestamp >= ?"
                    params.append(start_date.isoformat())
                
                if end_date:
                    query += " AND timestamp <= ?"
                    params.append(end_date.isoformat())
                
                query += " ORDER BY timestamp DESC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                metrics = []
                for row in rows:
                    metric = PerformanceLog(
                        metric_id=row[0],
                        timestamp=datetime.fromisoformat(row[1]),
                        metric_type=row[2],
                        metric_name=row[3],
                        value=row[4],
                        unit=row[5],
                        resource_id=row[6],
                        threshold=row[7],
                        alert_level=row[8]
                    )
                    metrics.append(metric)
                
                return metrics
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve performance metrics: {e}")
            return []
    
    def analyze_operation_patterns(self, days: int = 30) -> Dict[str, Any]:
        """Analyze operation patterns from logs"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get operation logs
            logs = self.get_operation_logs(start_date=start_date, end_date=end_date, limit=1000)
            
            if not logs:
                return {"error": "No logs found for analysis"}
            
            # Analyze patterns
            analysis = {
                'total_operations': len(logs),
                'success_rate': sum(1 for log in logs if log.success) / len(logs),
                'average_execution_time': sum(log.execution_time for log in logs) / len(logs),
                'operation_types': {},
                'error_patterns': {},
                'cost_impact': sum(log.cost_impact for log in logs),
                'security_issues': sum(1 for log in logs if log.security_impact == 'high'),
                'performance_trends': {}
            }
            
            # Count operation types
            for log in logs:
                op_type = log.operation_type
                if op_type not in analysis['operation_types']:
                    analysis['operation_types'][op_type] = 0
                analysis['operation_types'][op_type] += 1
            
            # Analyze error patterns
            error_logs = [log for log in logs if not log.success]
            for log in error_logs:
                error_type = log.error_message.split(':')[0] if log.error_message else 'unknown'
                if error_type not in analysis['error_patterns']:
                    analysis['error_patterns'][error_type] = 0
                analysis['error_patterns'][error_type] += 1
            
            # Analyze performance trends
            performance_logs = self.get_performance_metrics(start_date=start_date, end_date=end_date)
            if performance_logs:
                analysis['performance_trends'] = {
                    'avg_cpu_usage': self._calculate_average_metric(performance_logs, 'cpu_usage'),
                    'avg_memory_usage': self._calculate_average_metric(performance_logs, 'memory_usage'),
                    'avg_response_time': self._calculate_average_metric(performance_logs, 'response_time')
                }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze operation patterns: {e}")
            return {"error": str(e)}
    
    def _calculate_average_metric(self, metrics: List[PerformanceLog], metric_name: str) -> float:
        """Calculate average value for a specific metric"""
        relevant_metrics = [m for m in metrics if m.metric_name == metric_name]
        if not relevant_metrics:
            return 0.0
        return sum(m.value for m in relevant_metrics) / len(relevant_metrics)
    
    def generate_operation_report(self, operation_id: str) -> Dict[str, Any]:
        """Generate detailed report for a specific operation"""
        try:
            logs = self.get_operation_logs()
            operation_logs = [log for log in logs if log.operation_id == operation_id]
            
            if not operation_logs:
                return {"error": f"No logs found for operation {operation_id}"}
            
            report = {
                'operation_id': operation_id,
                'total_operations': len(operation_logs),
                'success_count': sum(1 for log in operation_logs if log.success),
                'failure_count': sum(1 for log in operation_logs if not log.success),
                'total_execution_time': sum(log.execution_time for log in operation_logs),
                'total_cost_impact': sum(log.cost_impact for log in operation_logs),
                'resource_changes': [],
                'performance_summary': {},
                'security_summary': {}
            }
            
            # Collect resource changes
            for log in operation_logs:
                report['resource_changes'].extend(log.resource_changes)
            
            # Performance summary
            if operation_logs:
                report['performance_summary'] = {
                    'avg_execution_time': report['total_execution_time'] / len(operation_logs),
                    'max_execution_time': max(log.execution_time for log in operation_logs),
                    'min_execution_time': min(log.execution_time for log in operation_logs)
                }
            
            # Security summary
            security_impacts = [log.security_impact for log in operation_logs]
            report['security_summary'] = {
                'high_impact_count': security_impacts.count('high'),
                'medium_impact_count': security_impacts.count('medium'),
                'low_impact_count': security_impacts.count('low')
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate operation report: {e}")
            return {"error": str(e)}
    
    def cleanup_old_logs(self, days_to_keep: int = 90):
        """Clean up old log files and database entries"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean up database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM operations WHERE timestamp < ?", (cutoff_date.isoformat(),))
                cursor.execute("DELETE FROM state_changes WHERE timestamp < ?", (cutoff_date.isoformat(),))
                cursor.execute("DELETE FROM performance_metrics WHERE timestamp < ?", (cutoff_date.isoformat(),))
                cursor.execute("DELETE FROM security_events WHERE timestamp < ?", (cutoff_date.isoformat(),))
                conn.commit()
            
            # Clean up old JSON files
            for log_dir in [self.operation_logs_path, self.state_logs_path, 
                           self.performance_logs_path, self.security_logs_path]:
                for file_path in log_dir.glob("*.json"):
                    if file_path.stat().st_mtime < cutoff_date.timestamp():
                        file_path.unlink()
            
            self.logger.info(f"Cleaned up logs older than {days_to_keep} days")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old logs: {e}")
    
    def export_logs(self, export_format: str = "json", output_path: Optional[str] = None) -> str:
        """Export logs in specified format"""
        try:
            if not output_path:
                output_path = self.log_directory / f"terraform_logs_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}"
            
            if export_format == "json":
                # Export as JSON
                export_data = {
                    'operations': [asdict(log) for log in self.get_operation_logs(limit=1000)],
                    'performance_metrics': [asdict(metric) for metric in self.get_performance_metrics()],
                    'export_timestamp': datetime.now().isoformat()
                }
                
                with open(output_path, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)
            
            elif export_format == "csv":
                # Export as CSV (simplified)
                import csv
                with open(output_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['log_id', 'timestamp', 'operation_type', 'success', 'execution_time'])
                    
                    for log in self.get_operation_logs(limit=1000):
                        writer.writerow([
                            log.log_id,
                            log.timestamp.isoformat(),
                            log.operation_type,
                            log.success,
                            log.execution_time
                        ])
            
            self.logger.info(f"Exported logs to {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to export logs: {e}")
            return ""
