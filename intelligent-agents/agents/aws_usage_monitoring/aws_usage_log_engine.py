"""
AWS Usage Monitoring Agent - Log Engine
Log^2 approach: Log collection, analysis, and intelligence
"""

import json
import datetime
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics
import re

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    domain: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    performance: Dict[str, Any]
    errors: List[str]
    success: bool
    rule_results: List[Dict[str, Any]]
    execution_id: str

@dataclass
class LogPattern:
    """Identified log pattern"""
    pattern_type: str
    frequency: int
    confidence: float
    description: str
    examples: List[str]
    recommendations: List[str]

@dataclass
class LogInsight:
    """Derived insight from log analysis"""
    insight_type: str
    severity: str
    description: str
    metrics: Dict[str, Any]
    recommendations: List[str]
    confidence: float

class AWSUsageLogEngine:
    """Log collection, analysis, and intelligence"""
    
    def __init__(self, db_path: str = "aws_monitoring_logs.db"):
        self.db_path = db_path
        self.log_storage = {}
        self.analytics_cache = {}
        self.pattern_cache = {}
        self.insights_cache = {}
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for log storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                domain TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                performance TEXT,
                errors TEXT,
                success BOOLEAN,
                rule_results TEXT,
                execution_id TEXT
            )
        ''')
        
        # Create patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                frequency INTEGER,
                confidence REAL,
                description TEXT,
                examples TEXT,
                recommendations TEXT,
                created_at TEXT
            )
        ''')
        
        # Create insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                severity TEXT,
                description TEXT,
                metrics TEXT,
                recommendations TEXT,
                confidence REAL,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_logs(self, execution_logs: Dict[str, Any]) -> str:
        """Collect and store logs"""
        
        # Create log entry
        log_entry = LogEntry(
            timestamp=execution_logs['timestamp'],
            domain=execution_logs['domain'],
            input_data=execution_logs['input'],
            output_data=execution_logs.get('output', {}),
            performance=execution_logs.get('performance', {}),
            errors=execution_logs.get('errors', []),
            success=execution_logs.get('success', False),
            rule_results=execution_logs.get('results', []),
            execution_id=execution_logs.get('execution_id', f"exec_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        )
        
        # Store in memory
        self.log_storage[log_entry.execution_id] = asdict(log_entry)
        
        # Store in database
        self._store_log_in_db(log_entry)
        
        return log_entry.execution_id
    
    def _store_log_in_db(self, log_entry: LogEntry):
        """Store log entry in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO logs (timestamp, domain, input_data, output_data, performance, errors, success, rule_results, execution_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_entry.timestamp,
            log_entry.domain,
            json.dumps(log_entry.input_data),
            json.dumps(log_entry.output_data),
            json.dumps(log_entry.performance),
            json.dumps(log_entry.errors),
            log_entry.success,
            json.dumps(log_entry.rule_results),
            log_entry.execution_id
        ))
        
        conn.commit()
        conn.close()
    
    def analyze_logs(self, domain: Optional[str] = None, time_range: Optional[Tuple[str, str]] = None) -> Dict[str, Any]:
        """Analyze logs for patterns and insights"""
        
        # Get logs for analysis
        logs = self._get_logs_for_analysis(domain, time_range)
        
        if not logs:
            return {'error': 'No logs found for analysis'}
        
        # Perform analysis
        analysis = {
            'log_count': len(logs),
            'time_range': time_range,
            'domain': domain,
            'patterns': self._identify_patterns(logs),
            'performance_analysis': self._analyze_performance(logs),
            'error_analysis': self._analyze_errors(logs),
            'success_analysis': self._analyze_success(logs),
            'trend_analysis': self._analyze_trends(logs),
            'insights': self._generate_insights(logs)
        }
        
        # Cache analysis results
        cache_key = f"{domain}_{time_range}"
        self.analytics_cache[cache_key] = analysis
        
        return analysis
    
    def _get_logs_for_analysis(self, domain: Optional[str] = None, time_range: Optional[Tuple[str, str]] = None) -> List[Dict[str, Any]]:
        """Get logs for analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        
        if time_range:
            query += " AND timestamp BETWEEN ? AND ?"
            params.extend(time_range)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert to dictionaries
        logs = []
        for row in rows:
            log = {
                'id': row[0],
                'timestamp': row[1],
                'domain': row[2],
                'input_data': json.loads(row[3]) if row[3] else {},
                'output_data': json.loads(row[4]) if row[4] else {},
                'performance': json.loads(row[5]) if row[5] else {},
                'errors': json.loads(row[6]) if row[6] else [],
                'success': bool(row[7]),
                'rule_results': json.loads(row[8]) if row[8] else [],
                'execution_id': row[9]
            }
            logs.append(log)
        
        conn.close()
        return logs
    
    def _identify_patterns(self, logs: List[Dict[str, Any]]) -> List[LogPattern]:
        """Identify patterns in logs"""
        patterns = []
        
        # Performance patterns
        performance_patterns = self._identify_performance_patterns(logs)
        patterns.extend(performance_patterns)
        
        # Error patterns
        error_patterns = self._identify_error_patterns(logs)
        patterns.extend(error_patterns)
        
        # Success patterns
        success_patterns = self._identify_success_patterns(logs)
        patterns.extend(success_patterns)
        
        # Cost patterns
        cost_patterns = self._identify_cost_patterns(logs)
        patterns.extend(cost_patterns)
        
        return patterns
    
    def _identify_performance_patterns(self, logs: List[Dict[str, Any]]) -> List[LogPattern]:
        """Identify performance patterns"""
        patterns = []
        
        # Execution time patterns
        execution_times = [log['performance'].get('execution_time_ms', 0) for log in logs if log['performance']]
        if execution_times:
            avg_time = statistics.mean(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)
            
            if max_time > avg_time * 2:
                patterns.append(LogPattern(
                    pattern_type="performance_degradation",
                    frequency=len([t for t in execution_times if t > avg_time * 1.5]),
                    confidence=0.8,
                    description=f"Performance degradation detected. Max time: {max_time}ms, Avg: {avg_time:.2f}ms",
                    examples=[f"Execution time: {max_time}ms"],
                    recommendations=[
                        "Investigate performance bottlenecks",
                        "Consider resource scaling",
                        "Optimize database queries"
                    ]
                ))
        
        return patterns
    
    def _identify_error_patterns(self, logs: List[Dict[str, Any]]) -> List[LogPattern]:
        """Identify error patterns"""
        patterns = []
        
        # Error frequency
        error_logs = [log for log in logs if not log['success'] or log['errors']]
        if error_logs:
            error_count = len(error_logs)
            total_count = len(logs)
            error_rate = error_count / total_count
            
            if error_rate > 0.1:  # 10% error rate
                patterns.append(LogPattern(
                    pattern_type="high_error_rate",
                    frequency=error_count,
                    confidence=0.9,
                    description=f"High error rate detected: {error_rate:.2%}",
                    examples=[f"Error rate: {error_rate:.2%}"],
                    recommendations=[
                        "Investigate root cause of errors",
                        "Implement better error handling",
                        "Add monitoring and alerting"
                    ]
                ))
        
        # Common error types
        all_errors = []
        for log in error_logs:
            all_errors.extend(log['errors'])
        
        if all_errors:
            error_counter = Counter(all_errors)
            most_common_errors = error_counter.most_common(3)
            
            for error, count in most_common_errors:
                if count > 1:  # Error appears multiple times
                    patterns.append(LogPattern(
                        pattern_type="recurring_error",
                        frequency=count,
                        confidence=0.7,
                        description=f"Recurring error: {error}",
                        examples=[error],
                        recommendations=[
                            f"Fix recurring error: {error}",
                            "Implement retry logic",
                            "Add error monitoring"
                        ]
                    ))
        
        return patterns
    
    def _identify_success_patterns(self, logs: List[Dict[str, Any]]) -> List[LogPattern]:
        """Identify success patterns"""
        patterns = []
        
        # Success rate analysis
        success_logs = [log for log in logs if log['success']]
        success_count = len(success_logs)
        total_count = len(logs)
        success_rate = success_count / total_count if total_count > 0 else 0
        
        if success_rate > 0.9:  # 90% success rate
            patterns.append(LogPattern(
                pattern_type="high_success_rate",
                frequency=success_count,
                confidence=0.8,
                description=f"High success rate: {success_rate:.2%}",
                examples=[f"Success rate: {success_rate:.2%}"],
                recommendations=[
                    "Maintain current performance",
                    "Document successful patterns",
                    "Share best practices"
                ]
            ))
        
        return patterns
    
    def _identify_cost_patterns(self, logs: List[Dict[str, Any]]) -> List[LogPattern]:
        """Identify cost patterns"""
        patterns = []
        
        # Cost trend analysis
        cost_data = []
        for log in logs:
            if 'input_data' in log and 'cost' in log['input_data']:
                cost_data.append(log['input_data']['cost'])
        
        if len(cost_data) > 1:
            # Calculate cost trend
            cost_trend = self._calculate_trend(cost_data)
            
            if cost_trend > 0.1:  # 10% increase
                patterns.append(LogPattern(
                    pattern_type="cost_increase",
                    frequency=len(cost_data),
                    confidence=0.7,
                    description=f"Cost increasing trend: {cost_trend:.2%}",
                    examples=[f"Cost trend: {cost_trend:.2%}"],
                    recommendations=[
                        "Investigate cost drivers",
                        "Implement cost optimization",
                        "Set up cost alerts"
                    ]
                ))
            elif cost_trend < -0.1:  # 10% decrease
                patterns.append(LogPattern(
                    pattern_type="cost_optimization",
                    frequency=len(cost_data),
                    confidence=0.8,
                    description=f"Cost optimization trend: {cost_trend:.2%}",
                    examples=[f"Cost trend: {cost_trend:.2%}"],
                    recommendations=[
                        "Continue optimization efforts",
                        "Document successful strategies",
                        "Scale optimization to other areas"
                    ]
                ))
        
        return patterns
    
    def _analyze_performance(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        performance_data = {
            'execution_times': [],
            'success_rates': [],
            'error_rates': [],
            'throughput': []
        }
        
        for log in logs:
            if 'performance' in log:
                perf = log['performance']
                if 'execution_time_ms' in perf:
                    performance_data['execution_times'].append(perf['execution_time_ms'])
                if 'success_rate' in perf:
                    performance_data['success_rates'].append(perf['success_rate'])
        
        # Calculate statistics
        analysis = {}
        for metric, values in performance_data.items():
            if values:
                analysis[metric] = {
                    'count': len(values),
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0
                }
        
        return analysis
    
    def _analyze_errors(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze error patterns"""
        error_analysis = {
            'total_errors': 0,
            'error_rate': 0,
            'common_errors': [],
            'error_trends': []
        }
        
        total_logs = len(logs)
        error_logs = [log for log in logs if not log['success'] or log['errors']]
        
        error_analysis['total_errors'] = len(error_logs)
        error_analysis['error_rate'] = len(error_logs) / total_logs if total_logs > 0 else 0
        
        # Common errors
        all_errors = []
        for log in error_logs:
            all_errors.extend(log['errors'])
        
        if all_errors:
            error_counter = Counter(all_errors)
            error_analysis['common_errors'] = error_counter.most_common(5)
        
        return error_analysis
    
    def _analyze_success(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze success patterns"""
        success_analysis = {
            'total_success': 0,
            'success_rate': 0,
            'success_trends': []
        }
        
        total_logs = len(logs)
        success_logs = [log for log in logs if log['success']]
        
        success_analysis['total_success'] = len(success_logs)
        success_analysis['success_rate'] = len(success_logs) / total_logs if total_logs > 0 else 0
        
        return success_analysis
    
    def _analyze_trends(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends over time"""
        trends = {
            'performance_trend': 0,
            'error_trend': 0,
            'success_trend': 0,
            'cost_trend': 0
        }
        
        # Sort logs by timestamp
        sorted_logs = sorted(logs, key=lambda x: x['timestamp'])
        
        if len(sorted_logs) > 1:
            # Performance trend
            early_perf = [log['performance'].get('execution_time_ms', 0) for log in sorted_logs[:len(sorted_logs)//2]]
            late_perf = [log['performance'].get('execution_time_ms', 0) for log in sorted_logs[len(sorted_logs)//2:]]
            
            if early_perf and late_perf:
                early_avg = statistics.mean(early_perf)
                late_avg = statistics.mean(late_perf)
                trends['performance_trend'] = (late_avg - early_avg) / early_avg if early_avg > 0 else 0
            
            # Error trend
            early_errors = len([log for log in sorted_logs[:len(sorted_logs)//2] if not log['success']])
            late_errors = len([log for log in sorted_logs[len(sorted_logs)//2:] if not log['success']])
            trends['error_trend'] = (late_errors - early_errors) / len(sorted_logs) if len(sorted_logs) > 0 else 0
        
        return trends
    
    def _generate_insights(self, logs: List[Dict[str, Any]]) -> List[LogInsight]:
        """Generate insights from log analysis"""
        insights = []
        
        # Performance insights
        perf_insights = self._generate_performance_insights(logs)
        insights.extend(perf_insights)
        
        # Cost insights
        cost_insights = self._generate_cost_insights(logs)
        insights.extend(cost_insights)
        
        # Security insights
        security_insights = self._generate_security_insights(logs)
        insights.extend(security_insights)
        
        return insights
    
    def _generate_performance_insights(self, logs: List[Dict[str, Any]]) -> List[LogInsight]:
        """Generate performance insights"""
        insights = []
        
        # Execution time analysis
        execution_times = [log['performance'].get('execution_time_ms', 0) for log in logs if log['performance']]
        if execution_times:
            avg_time = statistics.mean(execution_times)
            max_time = max(execution_times)
            
            if max_time > avg_time * 3:
                insights.append(LogInsight(
                    insight_type="performance_anomaly",
                    severity="high",
                    description=f"Performance anomaly detected: {max_time}ms vs avg {avg_time:.2f}ms",
                    metrics={'max_time': max_time, 'avg_time': avg_time},
                    recommendations=[
                        "Investigate performance bottleneck",
                        "Consider resource scaling",
                        "Optimize slow operations"
                    ],
                    confidence=0.8
                ))
        
        return insights
    
    def _generate_cost_insights(self, logs: List[Dict[str, Any]]) -> List[LogInsight]:
        """Generate cost insights"""
        insights = []
        
        # Cost analysis
        cost_data = []
        for log in logs:
            if 'input_data' in log and 'cost' in log['input_data']:
                cost_data.append(log['input_data']['cost'])
        
        if len(cost_data) > 1:
            cost_trend = self._calculate_trend(cost_data)
            if cost_trend > 0.2:  # 20% increase
                insights.append(LogInsight(
                    insight_type="cost_spike",
                    severity="high",
                    description=f"Significant cost increase: {cost_trend:.2%}",
                    metrics={'cost_trend': cost_trend, 'recent_cost': cost_data[-1]},
                    recommendations=[
                        "Investigate cost drivers",
                        "Implement cost controls",
                        "Set up cost alerts"
                    ],
                    confidence=0.9
                ))
        
        return insights
    
    def _generate_security_insights(self, logs: List[Dict[str, Any]]) -> List[LogInsight]:
        """Generate security insights"""
        insights = []
        
        # Security analysis
        security_issues = []
        for log in logs:
            if 'rule_results' in log:
                for rule in log['rule_results']:
                    if rule.get('domain') == 'security_monitoring' and rule.get('triggered'):
                        security_issues.append(rule)
        
        if security_issues:
            insights.append(LogInsight(
                insight_type="security_issues",
                severity="high",
                description=f"Security issues detected: {len(security_issues)}",
                metrics={'security_issues': len(security_issues)},
                recommendations=[
                    "Review security configurations",
                    "Implement security fixes",
                    "Enhance monitoring"
                ],
                confidence=0.9
            ))
        
        return insights
    
    def _calculate_trend(self, data: List[float]) -> float:
        """Calculate trend percentage"""
        if len(data) < 2:
            return 0
        
        first_half = data[:len(data)//2]
        second_half = data[len(data)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        return (second_avg - first_avg) / first_avg if first_avg > 0 else 0
    
    def get_logs_by_domain(self, domain: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get logs by domain"""
        return self._get_logs_for_analysis(domain=domain)[:limit]
    
    def get_recent_logs(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent logs"""
        end_time = datetime.datetime.now().isoformat()
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).isoformat()
        return self._get_logs_for_analysis(time_range=(start_time, end_time))
    
    def export_logs(self, domain: Optional[str] = None, format: str = 'json') -> str:
        """Export logs in specified format"""
        logs = self._get_logs_for_analysis(domain=domain)
        
        if format == 'json':
            return json.dumps(logs, indent=2)
        elif format == 'csv':
            # Convert to CSV format
            import csv
            import io
            output = io.StringIO()
            if logs:
                writer = csv.DictWriter(output, fieldnames=logs[0].keys())
                writer.writeheader()
                writer.writerows(logs)
            return output.getvalue()
        else:
            return str(logs)
