"""
AWS Usage Monitoring Agent - Intelligence Engine
Log^2 approach: Learn from logs and improve logic
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics
from collections import defaultdict, Counter
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Improvement:
    """Identified improvement opportunity"""
    improvement_type: str
    domain: str
    description: str
    potential_impact: str
    confidence: float
    recommendations: List[str]
    metrics: Dict[str, Any]

@dataclass
class Adaptation:
    """Logic adaptation suggestion"""
    adaptation_type: str
    domain: str
    current_logic: Dict[str, Any]
    suggested_logic: Dict[str, Any]
    reasoning: str
    confidence: float
    validation_required: bool

@dataclass
class LearningModel:
    """Machine learning model for pattern recognition"""
    model_type: str
    domain: str
    accuracy: float
    features: List[str]
    predictions: Dict[str, Any]
    last_updated: str

class AWSUsageIntelligenceEngine:
    """Learn from logs and improve logic"""
    
    def __init__(self):
        self.learning_models = {}
        self.improvements = {}
        self.adaptations = {}
        self.pattern_recognition = {}
        self.performance_history = defaultdict(list)
        self.cost_history = defaultdict(list)
        self.error_history = defaultdict(list)
        self.success_history = defaultdict(list)
        self._initialize_learning_models()
    
    def _initialize_learning_models(self):
        """Initialize machine learning models"""
        
        # Performance prediction model
        self.learning_models['performance_prediction'] = {
            'model': LinearRegression(),
            'features': ['execution_time_ms', 'success_rate', 'error_rate'],
            'target': 'performance_score',
            'accuracy': 0.0,
            'last_trained': None
        }
        
        # Cost optimization model
        self.learning_models['cost_optimization'] = {
            'model': LinearRegression(),
            'features': ['resource_count', 'utilization', 'cost_per_hour'],
            'target': 'optimization_potential',
            'accuracy': 0.0,
            'last_trained': None
        }
        
        # Error prediction model
        self.learning_models['error_prediction'] = {
            'model': LinearRegression(),
            'features': ['load', 'complexity', 'resource_usage'],
            'target': 'error_probability',
            'accuracy': 0.0,
            'last_trained': None
        }
        
        # Pattern clustering model
        self.learning_models['pattern_clustering'] = {
            'model': KMeans(n_clusters=5),
            'features': ['performance_metrics', 'cost_metrics', 'error_metrics'],
            'target': 'pattern_cluster',
            'accuracy': 0.0,
            'last_trained': None
        }
    
    def learn_from_logs(self, log_analysis: Dict[str, Any]) -> Tuple[List[Improvement], List[Adaptation]]:
        """Learn from log analysis and generate improvements"""
        
        improvements = []
        adaptations = []
        
        # Analyze patterns for improvements
        pattern_improvements = self._analyze_patterns_for_improvements(log_analysis)
        improvements.extend(pattern_improvements)
        
        # Analyze performance for improvements
        performance_improvements = self._analyze_performance_for_improvements(log_analysis)
        improvements.extend(performance_improvements)
        
        # Analyze costs for improvements
        cost_improvements = self._analyze_costs_for_improvements(log_analysis)
        improvements.extend(cost_improvements)
        
        # Analyze errors for improvements
        error_improvements = self._analyze_errors_for_improvements(log_analysis)
        improvements.extend(error_improvements)
        
        # Generate adaptations based on improvements
        for improvement in improvements:
            adaptation = self._generate_adaptation_from_improvement(improvement)
            if adaptation:
                adaptations.append(adaptation)
        
        # Update learning models
        self._update_learning_models(log_analysis)
        
        # Store improvements and adaptations
        self.improvements[datetime.datetime.now().isoformat()] = improvements
        self.adaptations[datetime.datetime.now().isoformat()] = adaptations
        
        return improvements, adaptations
    
    def _analyze_patterns_for_improvements(self, log_analysis: Dict[str, Any]) -> List[Improvement]:
        """Analyze patterns for improvement opportunities"""
        improvements = []
        
        patterns = log_analysis.get('patterns', [])
        
        for pattern in patterns:
            if pattern.pattern_type == "performance_degradation":
                improvements.append(Improvement(
                    improvement_type="performance_optimization",
                    domain="performance_monitoring",
                    description=f"Performance degradation detected: {pattern.description}",
                    potential_impact="high",
                    confidence=pattern.confidence,
                    recommendations=pattern.recommendations,
                    metrics={'frequency': pattern.frequency, 'confidence': pattern.confidence}
                ))
            
            elif pattern.pattern_type == "high_error_rate":
                improvements.append(Improvement(
                    improvement_type="error_reduction",
                    domain="error_monitoring",
                    description=f"High error rate detected: {pattern.description}",
                    potential_impact="critical",
                    confidence=pattern.confidence,
                    recommendations=pattern.recommendations,
                    metrics={'frequency': pattern.frequency, 'confidence': pattern.confidence}
                ))
            
            elif pattern.pattern_type == "cost_increase":
                improvements.append(Improvement(
                    improvement_type="cost_optimization",
                    domain="cost_monitoring",
                    description=f"Cost increase detected: {pattern.description}",
                    potential_impact="high",
                    confidence=pattern.confidence,
                    recommendations=pattern.recommendations,
                    metrics={'frequency': pattern.frequency, 'confidence': pattern.confidence}
                ))
        
        return improvements
    
    def _analyze_performance_for_improvements(self, log_analysis: Dict[str, Any]) -> List[Improvement]:
        """Analyze performance for improvement opportunities"""
        improvements = []
        
        performance_analysis = log_analysis.get('performance_analysis', {})
        
        # Execution time improvements
        if 'execution_times' in performance_analysis:
            exec_times = performance_analysis['execution_times']
            if exec_times['mean'] > 1000:  # 1 second
                improvements.append(Improvement(
                    improvement_type="execution_time_optimization",
                    domain="performance_monitoring",
                    description=f"Average execution time is high: {exec_times['mean']:.2f}ms",
                    potential_impact="medium",
                    confidence=0.8,
                    recommendations=[
                        "Optimize database queries",
                        "Implement caching",
                        "Scale resources",
                        "Parallelize operations"
                    ],
                    metrics={'mean_time': exec_times['mean'], 'max_time': exec_times['max']}
                ))
        
        # Success rate improvements
        if 'success_rates' in performance_analysis:
            success_rates = performance_analysis['success_rates']
            if success_rates['mean'] < 0.9:  # 90%
                improvements.append(Improvement(
                    improvement_type="success_rate_improvement",
                    domain="reliability_monitoring",
                    description=f"Success rate is low: {success_rates['mean']:.2%}",
                    potential_impact="high",
                    confidence=0.9,
                    recommendations=[
                        "Improve error handling",
                        "Add retry logic",
                        "Implement circuit breakers",
                        "Enhance monitoring"
                    ],
                    metrics={'mean_success_rate': success_rates['mean']}
                ))
        
        return improvements
    
    def _analyze_costs_for_improvements(self, log_analysis: Dict[str, Any]) -> List[Improvement]:
        """Analyze costs for improvement opportunities"""
        improvements = []
        
        # Cost trend analysis
        trends = log_analysis.get('trend_analysis', {})
        cost_trend = trends.get('cost_trend', 0)
        
        if cost_trend > 0.1:  # 10% increase
            improvements.append(Improvement(
                improvement_type="cost_optimization",
                domain="cost_monitoring",
                description=f"Cost trend is increasing: {cost_trend:.2%}",
                potential_impact="high",
                confidence=0.8,
                recommendations=[
                    "Review resource usage",
                    "Implement auto-scaling",
                    "Use spot instances",
                    "Optimize storage classes"
                ],
                metrics={'cost_trend': cost_trend}
            ))
        
        # Cost insights
        insights = log_analysis.get('insights', [])
        for insight in insights:
            if insight.insight_type == "cost_spike":
                improvements.append(Improvement(
                    improvement_type="cost_spike_mitigation",
                    domain="cost_monitoring",
                    description=f"Cost spike detected: {insight.description}",
                    potential_impact="critical",
                    confidence=insight.confidence,
                    recommendations=insight.recommendations,
                    metrics=insight.metrics
                ))
        
        return improvements
    
    def _analyze_errors_for_improvements(self, log_analysis: Dict[str, Any]) -> List[Improvement]:
        """Analyze errors for improvement opportunities"""
        improvements = []
        
        error_analysis = log_analysis.get('error_analysis', {})
        error_rate = error_analysis.get('error_rate', 0)
        
        if error_rate > 0.05:  # 5%
            improvements.append(Improvement(
                improvement_type="error_reduction",
                domain="error_monitoring",
                description=f"Error rate is high: {error_rate:.2%}",
                potential_impact="high",
                confidence=0.9,
                recommendations=[
                    "Investigate root causes",
                    "Improve error handling",
                    "Add input validation",
                    "Implement monitoring"
                ],
                metrics={'error_rate': error_rate}
            ))
        
        # Common errors
        common_errors = error_analysis.get('common_errors', [])
        if common_errors:
            for error, count in common_errors[:3]:  # Top 3 errors
                improvements.append(Improvement(
                    improvement_type="recurring_error_fix",
                    domain="error_monitoring",
                    description=f"Recurring error: {error} (count: {count})",
                    potential_impact="medium",
                    confidence=0.8,
                    recommendations=[
                        f"Fix recurring error: {error}",
                        "Add error monitoring",
                        "Implement retry logic"
                    ],
                    metrics={'error': error, 'count': count}
                ))
        
        return improvements
    
    def _generate_adaptation_from_improvement(self, improvement: Improvement) -> Optional[Adaptation]:
        """Generate adaptation from improvement"""
        
        if improvement.improvement_type == "performance_optimization":
            return Adaptation(
                adaptation_type="threshold_adjustment",
                domain=improvement.domain,
                current_logic={'performance_threshold': 1000},
                suggested_logic={'performance_threshold': 800},
                reasoning=f"Lower threshold to catch performance issues earlier: {improvement.description}",
                confidence=improvement.confidence,
                validation_required=True
            )
        
        elif improvement.improvement_type == "cost_optimization":
            return Adaptation(
                adaptation_type="cost_rule_addition",
                domain=improvement.domain,
                current_logic={'cost_rules': []},
                suggested_logic={'cost_rules': ['daily_cost_alert', 'monthly_budget_alert']},
                reasoning=f"Add cost monitoring rules: {improvement.description}",
                confidence=improvement.confidence,
                validation_required=True
            )
        
        elif improvement.improvement_type == "error_reduction":
            return Adaptation(
                adaptation_type="error_handling_improvement",
                domain=improvement.domain,
                current_logic={'error_handling': 'basic'},
                suggested_logic={'error_handling': 'enhanced', 'retry_logic': True},
                reasoning=f"Improve error handling: {improvement.description}",
                confidence=improvement.confidence,
                validation_required=True
            )
        
        return None
    
    def _update_learning_models(self, log_analysis: Dict[str, Any]):
        """Update machine learning models with new data"""
        
        # Extract features and targets
        features_data = self._extract_features(log_analysis)
        
        # Update performance prediction model
        if 'performance_metrics' in features_data:
            self._update_model('performance_prediction', features_data['performance_metrics'])
        
        # Update cost optimization model
        if 'cost_metrics' in features_data:
            self._update_model('cost_optimization', features_data['cost_metrics'])
        
        # Update error prediction model
        if 'error_metrics' in features_data:
            self._update_model('error_prediction', features_data['error_metrics'])
        
        # Update pattern clustering model
        if 'pattern_metrics' in features_data:
            self._update_model('pattern_clustering', features_data['pattern_metrics'])
    
    def _extract_features(self, log_analysis: Dict[str, Any]) -> Dict[str, List[float]]:
        """Extract features from log analysis"""
        features = {
            'performance_metrics': [],
            'cost_metrics': [],
            'error_metrics': [],
            'pattern_metrics': []
        }
        
        # Performance features
        perf_analysis = log_analysis.get('performance_analysis', {})
        if 'execution_times' in perf_analysis:
            exec_times = perf_analysis['execution_times']
            features['performance_metrics'].extend([
                exec_times.get('mean', 0),
                exec_times.get('max', 0),
                exec_times.get('std_dev', 0)
            ])
        
        # Cost features
        trends = log_analysis.get('trend_analysis', {})
        features['cost_metrics'].extend([
            trends.get('cost_trend', 0),
            trends.get('performance_trend', 0)
        ])
        
        # Error features
        error_analysis = log_analysis.get('error_analysis', {})
        features['error_metrics'].extend([
            error_analysis.get('error_rate', 0),
            error_analysis.get('total_errors', 0)
        ])
        
        # Pattern features
        patterns = log_analysis.get('patterns', [])
        features['pattern_metrics'].extend([
            len(patterns),
            sum(p.confidence for p in patterns) / len(patterns) if patterns else 0
        ])
        
        return features
    
    def _update_model(self, model_name: str, features: List[float]):
        """Update a specific learning model"""
        if not features:
            return
        
        model_info = self.learning_models[model_name]
        model = model_info['model']
        
        # Prepare training data
        X = np.array(features).reshape(1, -1)
        
        # For now, use simple heuristics for target values
        if model_name == 'performance_prediction':
            y = [1.0 if features[0] < 1000 else 0.0]  # Good performance if < 1000ms
        elif model_name == 'cost_optimization':
            y = [1.0 if features[0] < 0.1 else 0.0]  # Good if cost trend < 10%
        elif model_name == 'error_prediction':
            y = [1.0 if features[0] < 0.05 else 0.0]  # Good if error rate < 5%
        else:
            y = [0.5]  # Default
        
        # Update model
        try:
            model.fit(X, y)
            model_info['accuracy'] = 0.8  # Placeholder accuracy
            model_info['last_trained'] = datetime.datetime.now().isoformat()
        except Exception as e:
            print(f"Error updating model {model_name}: {e}")
    
    def predict_performance(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict performance based on current features"""
        model_info = self.learning_models['performance_prediction']
        model = model_info['model']
        
        # Extract features
        feature_vector = [
            features.get('execution_time_ms', 0),
            features.get('success_rate', 0),
            features.get('error_rate', 0)
        ]
        
        try:
            prediction = model.predict([feature_vector])[0]
            return {
                'predicted_performance': prediction,
                'confidence': model_info['accuracy'],
                'recommendations': self._get_performance_recommendations(prediction)
            }
        except Exception as e:
            return {'error': f"Prediction failed: {e}"}
    
    def predict_cost_optimization(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict cost optimization potential"""
        model_info = self.learning_models['cost_optimization']
        model = model_info['model']
        
        # Extract features
        feature_vector = [
            features.get('resource_count', 0),
            features.get('utilization', 0),
            features.get('cost_per_hour', 0)
        ]
        
        try:
            prediction = model.predict([feature_vector])[0]
            return {
                'optimization_potential': prediction,
                'confidence': model_info['accuracy'],
                'recommendations': self._get_cost_recommendations(prediction)
            }
        except Exception as e:
            return {'error': f"Prediction failed: {e}"}
    
    def predict_errors(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict error probability"""
        model_info = self.learning_models['error_prediction']
        model = model_info['model']
        
        # Extract features
        feature_vector = [
            features.get('load', 0),
            features.get('complexity', 0),
            features.get('resource_usage', 0)
        ]
        
        try:
            prediction = model.predict([feature_vector])[0]
            return {
                'error_probability': prediction,
                'confidence': model_info['accuracy'],
                'recommendations': self._get_error_prevention_recommendations(prediction)
            }
        except Exception as e:
            return {'error': f"Prediction failed: {e}"}
    
    def _get_performance_recommendations(self, prediction: float) -> List[str]:
        """Get performance recommendations based on prediction"""
        if prediction < 0.5:
            return [
                "Performance is predicted to be poor",
                "Consider scaling resources",
                "Optimize database queries",
                "Implement caching"
            ]
        else:
            return [
                "Performance is predicted to be good",
                "Continue current practices",
                "Monitor for changes"
            ]
    
    def _get_cost_recommendations(self, prediction: float) -> List[str]:
        """Get cost recommendations based on prediction"""
        if prediction > 0.7:
            return [
                "High cost optimization potential",
                "Review resource usage",
                "Consider spot instances",
                "Implement auto-scaling"
            ]
        else:
            return [
                "Cost optimization potential is low",
                "Current cost management is effective",
                "Continue monitoring"
            ]
    
    def _get_error_prevention_recommendations(self, prediction: float) -> List[str]:
        """Get error prevention recommendations based on prediction"""
        if prediction > 0.5:
            return [
                "High error probability predicted",
                "Implement additional error handling",
                "Add monitoring and alerting",
                "Consider circuit breakers"
            ]
        else:
            return [
                "Low error probability predicted",
                "Current error handling is adequate",
                "Continue monitoring"
            ]
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        return {
            'models_trained': len([m for m in self.learning_models.values() if m['last_trained']]),
            'total_improvements': sum(len(imps) for imps in self.improvements.values()),
            'total_adaptations': sum(len(adapts) for adapts in self.adaptations.values()),
            'learning_models': {
                name: {
                    'accuracy': model['accuracy'],
                    'last_trained': model['last_trained'],
                    'features': model['features']
                }
                for name, model in self.learning_models.items()
            },
            'recent_improvements': list(self.improvements.keys())[-5:],
            'recent_adaptations': list(self.adaptations.keys())[-5:]
        }
    
    def export_learning_data(self) -> Dict[str, Any]:
        """Export learning data for analysis"""
        return {
            'learning_models': self.learning_models,
            'improvements': self.improvements,
            'adaptations': self.adaptations,
            'pattern_recognition': self.pattern_recognition,
            'export_timestamp': datetime.datetime.now().isoformat()
        }
