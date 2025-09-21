"""
Terraform Intelligence Engine - Log^2 Architecture
Learning, adaptation, and intelligence for Terraform operations
"""

import os
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

@dataclass
class LearningPattern:
    """Pattern learned from operations"""
    pattern_id: str
    pattern_type: str
    conditions: Dict[str, Any]
    outcomes: Dict[str, Any]
    confidence: float
    frequency: int
    last_seen: datetime
    success_rate: float

@dataclass
class OptimizationSuggestion:
    """Suggestion for infrastructure optimization"""
    suggestion_id: str
    category: str  # cost, performance, security, scalability
    description: str
    current_value: float
    suggested_value: float
    potential_improvement: float
    confidence: float
    risk_level: str
    implementation_steps: List[str]

@dataclass
class PredictiveInsight:
    """Predictive insight based on historical data"""
    insight_id: str
    insight_type: str
    prediction: Dict[str, Any]
    confidence: float
    time_horizon: str
    factors: List[str]
    recommendations: List[str]

@dataclass
class AdaptationRule:
    """Rule for adapting behavior based on learning"""
    rule_id: str
    trigger_conditions: Dict[str, Any]
    adaptation_actions: List[str]
    success_criteria: Dict[str, Any]
    learning_rate: float
    effectiveness_score: float

class TerraformIntelligenceEngine:
    """Learning, adaptation, and intelligence for Terraform operations"""
    
    def __init__(self, model_directory: str = "models"):
        self.model_directory = Path(model_directory)
        self.model_directory.mkdir(exist_ok=True)
        
        # Initialize logging
        self.logger = logging.getLogger('terraform_intelligence_engine')
        self.logger.setLevel(logging.INFO)
        
        # Learning components
        self.learning_patterns: Dict[str, LearningPattern] = {}
        self.adaptation_rules: List[AdaptationRule] = []
        self.optimization_suggestions: List[OptimizationSuggestion] = []
        self.predictive_insights: List[PredictiveInsight] = []
        
        # ML models
        self.cost_prediction_model = None
        self.performance_prediction_model = None
        self.anomaly_detection_model = None
        self.scaler = StandardScaler()
        
        # Learning parameters
        self.learning_rate = 0.1
        self.min_pattern_frequency = 5
        self.confidence_threshold = 0.7
        
        # Initialize models
        self._initialize_models()
        self._load_existing_patterns()
    
    def _initialize_models(self):
        """Initialize machine learning models"""
        try:
            # Cost prediction model
            cost_model_path = self.model_directory / "cost_prediction_model.pkl"
            if cost_model_path.exists():
                self.cost_prediction_model = joblib.load(cost_model_path)
            else:
                self.cost_prediction_model = RandomForestRegressor(n_estimators=10, random_state=42)
                # Initialize with dummy data to avoid sklearn warnings
                dummy_X = [[0, 0, 99.0, 0, 0, 0, 12, 0]]
                dummy_y = [100.0]
                self.cost_prediction_model.fit(dummy_X, dummy_y)
            
            # Performance prediction model
            perf_model_path = self.model_directory / "performance_prediction_model.pkl"
            if perf_model_path.exists():
                self.performance_prediction_model = joblib.load(perf_model_path)
            else:
                self.performance_prediction_model = RandomForestRegressor(n_estimators=10, random_state=42)
                # Initialize with dummy data
                dummy_X = [[0, 0, 99.0, 0, 0, 0, 12, 0]]
                dummy_y = [5.0]
                self.performance_prediction_model.fit(dummy_X, dummy_y)
            
            # Anomaly detection model - use simpler approach
            anomaly_model_path = self.model_directory / "anomaly_detection_model.pkl"
            if anomaly_model_path.exists():
                self.anomaly_detection_model = joblib.load(anomaly_model_path)
            else:
                # Use a simple threshold-based approach instead of KMeans
                self.anomaly_detection_model = None  # Will use simple threshold logic
            
            self.logger.info("ML models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize models: {e}")
            # Fallback to simple models
            self.cost_prediction_model = None
            self.performance_prediction_model = None
            self.anomaly_detection_model = None
    
    def _load_existing_patterns(self):
        """Load existing learning patterns from storage"""
        try:
            patterns_file = self.model_directory / "learning_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                    for pattern_id, pattern_data in patterns_data.items():
                        pattern_data['last_seen'] = datetime.fromisoformat(pattern_data['last_seen'])
                        self.learning_patterns[pattern_id] = LearningPattern(**pattern_data)
            
            self.logger.info(f"Loaded {len(self.learning_patterns)} existing patterns")
            
        except Exception as e:
            self.logger.error(f"Failed to load existing patterns: {e}")
    
    def learn_from_operation(self, operation_data: Dict[str, Any]) -> bool:
        """Learn from a Terraform operation"""
        try:
            # Extract features from operation
            features = self._extract_features(operation_data)
            
            # Update learning patterns
            self._update_learning_patterns(features, operation_data)
            
            # Update ML models
            self._update_ml_models(features, operation_data)
            
            # Generate new insights
            self._generate_insights()
            
            # Save updated patterns
            self._save_patterns()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to learn from operation: {e}")
            return False
    
    def _extract_features(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from operation data"""
        features = {
            'operation_type': operation_data.get('operation_type', 'unknown'),
            'user_count': operation_data.get('user_count', 0),
            'data_volume': operation_data.get('data_volume', 0),
            'availability_requirement': operation_data.get('availability_requirement', 99.0),
            'security_requirements': operation_data.get('security_requirements', False),
            'compliance_required': operation_data.get('compliance_required', False),
            'execution_time': operation_data.get('execution_time', 0.0),
            'success': operation_data.get('success', False),
            'cost_impact': operation_data.get('cost_impact', 0.0),
            'resource_count': len(operation_data.get('resource_changes', [])),
            'timestamp_hour': datetime.now().hour,
            'timestamp_day': datetime.now().weekday()
        }
        
        return features
    
    def _update_learning_patterns(self, features: Dict[str, Any], operation_data: Dict[str, Any]):
        """Update learning patterns based on operation"""
        # Create pattern key
        pattern_key = f"{features['operation_type']}_{features['user_count']}_{features['data_volume']}"
        
        if pattern_key in self.learning_patterns:
            # Update existing pattern
            pattern = self.learning_patterns[pattern_key]
            pattern.frequency += 1
            pattern.last_seen = datetime.now()
            
            # Update success rate
            if operation_data.get('success', False):
                pattern.success_rate = (pattern.success_rate * (pattern.frequency - 1) + 1.0) / pattern.frequency
            else:
                pattern.success_rate = (pattern.success_rate * (pattern.frequency - 1)) / pattern.frequency
            
            # Update confidence based on frequency and success rate
            pattern.confidence = min(1.0, pattern.frequency / 10.0) * pattern.success_rate
            
        else:
            # Create new pattern
            pattern = LearningPattern(
                pattern_id=pattern_key,
                pattern_type=features['operation_type'],
                conditions=features,
                outcomes=operation_data,
                confidence=0.1,
                frequency=1,
                last_seen=datetime.now(),
                success_rate=1.0 if operation_data.get('success', False) else 0.0
            )
            self.learning_patterns[pattern_key] = pattern
    
    def _update_ml_models(self, features: Dict[str, Any], operation_data: Dict[str, Any]):
        """Update machine learning models with new data"""
        try:
            # Prepare feature vector
            feature_vector = self._prepare_feature_vector(features)
            
            # Update cost prediction model
            if 'cost_impact' in operation_data:
                cost_target = operation_data['cost_impact']
                if hasattr(self.cost_prediction_model, 'partial_fit'):
                    self.cost_prediction_model.partial_fit([feature_vector], [cost_target])
                else:
                    # For models that don't support partial_fit, retrain periodically
                    self._retrain_cost_model()
            
            # Update performance prediction model
            if 'execution_time' in operation_data:
                perf_target = operation_data['execution_time']
                if hasattr(self.performance_prediction_model, 'partial_fit'):
                    self.performance_prediction_model.partial_fit([feature_vector], [perf_target])
                else:
                    self._retrain_performance_model()
            
            # Update anomaly detection model
            self._update_anomaly_detection(feature_vector)
            
        except Exception as e:
            self.logger.error(f"Failed to update ML models: {e}")
    
    def _prepare_feature_vector(self, features: Dict[str, Any]) -> List[float]:
        """Prepare feature vector for ML models"""
        # Convert features to numerical vector
        vector = [
            features.get('user_count', 0),
            features.get('data_volume', 0),
            features.get('availability_requirement', 99.0),
            float(features.get('security_requirements', False)),
            float(features.get('compliance_required', False)),
            features.get('resource_count', 0),
            features.get('timestamp_hour', 0),
            features.get('timestamp_day', 0)
        ]
        
        return vector
    
    def _retrain_cost_model(self):
        """Retrain cost prediction model with historical data"""
        # This would typically load historical data and retrain
        # For now, we'll keep the existing model
        pass
    
    def _retrain_performance_model(self):
        """Retrain performance prediction model with historical data"""
        # This would typically load historical data and retrain
        # For now, we'll keep the existing model
        pass
    
    def _update_anomaly_detection(self, feature_vector: List[float]):
        """Update anomaly detection model"""
        try:
            # Simple threshold-based anomaly detection doesn't need model updates
            # Just log the feature vector for pattern analysis
            self.logger.debug(f"Anomaly detection feature vector: {feature_vector}")
        except Exception as e:
            self.logger.error(f"Failed to update anomaly detection: {e}")
    
    def _generate_insights(self):
        """Generate new insights based on learning patterns"""
        try:
            # Analyze patterns for insights
            high_confidence_patterns = [
                p for p in self.learning_patterns.values() 
                if p.confidence > self.confidence_threshold
            ]
            
            # Generate optimization suggestions
            self._generate_optimization_suggestions(high_confidence_patterns)
            
            # Generate predictive insights
            self._generate_predictive_insights(high_confidence_patterns)
            
            # Update adaptation rules
            self._update_adaptation_rules(high_confidence_patterns)
            
        except Exception as e:
            self.logger.error(f"Failed to generate insights: {e}")
    
    def _generate_optimization_suggestions(self, patterns: List[LearningPattern]):
        """Generate optimization suggestions based on patterns"""
        suggestions = []
        
        for pattern in patterns:
            if pattern.success_rate < 0.8:  # Low success rate
                suggestion = OptimizationSuggestion(
                    suggestion_id=f"opt_{pattern.pattern_id}",
                    category="performance",
                    description=f"Improve {pattern.pattern_type} operations",
                    current_value=pattern.success_rate,
                    suggested_value=0.9,
                    potential_improvement=0.9 - pattern.success_rate,
                    confidence=pattern.confidence,
                    risk_level="low",
                    implementation_steps=[
                        "Review operation parameters",
                        "Optimize resource allocation",
                        "Improve error handling"
                    ]
                )
                suggestions.append(suggestion)
            
            # Cost optimization suggestions
            if pattern.outcomes.get('cost_impact', 0) > 100:  # High cost
                suggestion = OptimizationSuggestion(
                    suggestion_id=f"cost_{pattern.pattern_id}",
                    category="cost",
                    description=f"Optimize costs for {pattern.pattern_type}",
                    current_value=pattern.outcomes.get('cost_impact', 0),
                    suggested_value=pattern.outcomes.get('cost_impact', 0) * 0.8,
                    potential_improvement=pattern.outcomes.get('cost_impact', 0) * 0.2,
                    confidence=pattern.confidence,
                    risk_level="medium",
                    implementation_steps=[
                        "Review resource sizing",
                        "Implement cost optimization rules",
                        "Consider reserved instances"
                    ]
                )
                suggestions.append(suggestion)
        
        self.optimization_suggestions = suggestions
    
    def _generate_predictive_insights(self, patterns: List[LearningPattern]):
        """Generate predictive insights based on patterns"""
        insights = []
        
        # Predict future costs
        if self.cost_prediction_model:
            try:
                # Use recent patterns to predict future costs
                recent_patterns = [p for p in patterns if p.frequency > 5]
                if recent_patterns:
                    avg_cost = sum(p.outcomes.get('cost_impact', 0) for p in recent_patterns) / len(recent_patterns)
                    
                    insight = PredictiveInsight(
                        insight_id="cost_prediction",
                        insight_type="cost_forecast",
                        prediction={
                            "predicted_monthly_cost": avg_cost * 30,
                            "confidence_interval": [avg_cost * 0.8, avg_cost * 1.2]
                        },
                        confidence=0.7,
                        time_horizon="30_days",
                        factors=["historical_patterns", "resource_usage"],
                        recommendations=[
                            "Monitor cost trends",
                            "Implement cost alerts",
                            "Consider budget optimization"
                        ]
                    )
                    insights.append(insight)
            except Exception as e:
                self.logger.error(f"Failed to generate cost prediction: {e}")
        
        # Predict performance issues
        low_performance_patterns = [p for p in patterns if p.success_rate < 0.7]
        if low_performance_patterns:
            insight = PredictiveInsight(
                insight_id="performance_risk",
                insight_type="performance_forecast",
                prediction={
                    "risk_level": "high",
                    "affected_operations": len(low_performance_patterns),
                    "predicted_failure_rate": sum(p.success_rate for p in low_performance_patterns) / len(low_performance_patterns)
                },
                confidence=0.8,
                time_horizon="7_days",
                factors=["historical_failures", "operation_complexity"],
                recommendations=[
                    "Review operation procedures",
                    "Implement additional monitoring",
                    "Prepare rollback procedures"
                ]
            )
            insights.append(insight)
        
        self.predictive_insights = insights
    
    def _update_adaptation_rules(self, patterns: List[LearningPattern]):
        """Update adaptation rules based on learning patterns"""
        rules = []
        
        for pattern in patterns:
            if pattern.confidence > 0.8 and pattern.frequency > 10:
                rule = AdaptationRule(
                    rule_id=f"adapt_{pattern.pattern_id}",
                    trigger_conditions=pattern.conditions,
                    adaptation_actions=[
                        f"Apply {pattern.pattern_type} optimization",
                        "Monitor performance metrics",
                        "Adjust resource allocation"
                    ],
                    success_criteria={
                        "success_rate": 0.9,
                        "execution_time": "< 300 seconds",
                        "cost_impact": "< 50"
                    },
                    learning_rate=self.learning_rate,
                    effectiveness_score=pattern.success_rate
                )
                rules.append(rule)
        
        self.adaptation_rules = rules
    
    def _save_patterns(self):
        """Save learning patterns to storage"""
        try:
            patterns_file = self.model_directory / "learning_patterns.json"
            patterns_data = {}
            
            for pattern_id, pattern in self.learning_patterns.items():
                pattern_dict = asdict(pattern)
                pattern_dict['last_seen'] = pattern.last_seen.isoformat()
                patterns_data[pattern_id] = pattern_dict
            
            with open(patterns_file, 'w') as f:
                json.dump(patterns_data, f, indent=2)
            
            # Save ML models
            joblib.dump(self.cost_prediction_model, self.model_directory / "cost_prediction_model.pkl")
            joblib.dump(self.performance_prediction_model, self.model_directory / "performance_prediction_model.pkl")
            joblib.dump(self.anomaly_detection_model, self.model_directory / "anomaly_detection_model.pkl")
            
            self.logger.info("Patterns and models saved successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to save patterns: {e}")
    
    def predict_cost(self, features: Dict[str, Any]) -> float:
        """Predict cost for given features"""
        try:
            if not self.cost_prediction_model:
                # Simple cost estimation based on features
                user_count = features.get('user_count', 0)
                data_volume = features.get('data_volume', 0)
                base_cost = 50.0
                user_cost = user_count * 0.1
                data_cost = data_volume * 0.5
                return base_cost + user_cost + data_cost
            
            feature_vector = self._prepare_feature_vector(features)
            prediction = self.cost_prediction_model.predict([feature_vector])[0]
            return max(0.0, prediction)
            
        except Exception as e:
            self.logger.error(f"Failed to predict cost: {e}")
            # Fallback to simple estimation
            user_count = features.get('user_count', 0)
            data_volume = features.get('data_volume', 0)
            return 50.0 + (user_count * 0.1) + (data_volume * 0.5)
    
    def predict_performance(self, features: Dict[str, Any]) -> float:
        """Predict performance for given features"""
        try:
            if not self.performance_prediction_model:
                # Simple performance estimation based on features
                user_count = features.get('user_count', 0)
                data_volume = features.get('data_volume', 0)
                base_time = 5.0
                user_time = user_count * 0.01
                data_time = data_volume * 0.1
                return base_time + user_time + data_time
            
            feature_vector = self._prepare_feature_vector(features)
            prediction = self.performance_prediction_model.predict([feature_vector])[0]
            return max(0.0, prediction)
            
        except Exception as e:
            self.logger.error(f"Failed to predict performance: {e}")
            # Fallback to simple estimation
            user_count = features.get('user_count', 0)
            data_volume = features.get('data_volume', 0)
            return 5.0 + (user_count * 0.01) + (data_volume * 0.1)
    
    def detect_anomaly(self, features: Dict[str, Any]) -> bool:
        """Detect if operation is anomalous using simple threshold logic"""
        try:
            # Simple anomaly detection based on feature thresholds
            user_count = features.get('user_count', 0)
            data_volume = features.get('data_volume', 0)
            availability_requirement = features.get('availability_requirement', 99.0)
            
            # Define anomaly thresholds
            max_users = 10000
            max_data_volume = 1000  # GB
            min_availability = 95.0
            
            # Check for anomalies
            if user_count > max_users:
                return True
            if data_volume > max_data_volume:
                return True
            if availability_requirement < min_availability:
                return True
            
            # Check for unusual combinations
            if user_count > 1000 and data_volume < 1:  # High users but low data
                return True
            if user_count < 10 and data_volume > 100:  # Low users but high data
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to detect anomaly: {e}")
            return False
    
    def get_optimization_suggestions(self) -> List[OptimizationSuggestion]:
        """Get current optimization suggestions"""
        return self.optimization_suggestions
    
    def get_predictive_insights(self) -> List[PredictiveInsight]:
        """Get current predictive insights"""
        return self.predictive_insights
    
    def get_adaptation_rules(self) -> List[AdaptationRule]:
        """Get current adaptation rules"""
        return self.adaptation_rules
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        return {
            'total_patterns': len(self.learning_patterns),
            'high_confidence_patterns': len([p for p in self.learning_patterns.values() if p.confidence > 0.8]),
            'optimization_suggestions': len(self.optimization_suggestions),
            'predictive_insights': len(self.predictive_insights),
            'adaptation_rules': len(self.adaptation_rules),
            'learning_rate': self.learning_rate,
            'model_status': {
                'cost_prediction': self.cost_prediction_model is not None,
                'performance_prediction': self.performance_prediction_model is not None,
                'anomaly_detection': self.anomaly_detection_model is not None
            }
        }
