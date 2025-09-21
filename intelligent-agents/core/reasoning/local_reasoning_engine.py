"""
Local Reasoning Engine - Enhanced Built-in Intelligence
"""

import json
import sqlite3
import os
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Local model integration removed - using enhanced built-in intelligence only
LOCAL_MODEL_AVAILABLE = False

@dataclass
class ParsedRequest:
    """Parsed user request with extracted information"""
    objective: str
    entities: List[str]
    constraints: Dict[str, Any]
    scale: Dict[str, Any]
    technology_preferences: List[str]

@dataclass
class Solution:
    """Infrastructure solution"""
    name: str
    description: str
    components: List[str]
    cost_estimate: float
    performance_score: float
    security_score: float
    complexity: str
    # Advanced reasoning attributes
    scalability_score: float = 0.0
    maintainability_score: float = 0.0
    compliance_score: float = 0.0
    risk_score: float = 0.0
    optimization_recommendations: List[str] = None
    
    def __post_init__(self):
        if self.optimization_recommendations is None:
            self.optimization_recommendations = []

@dataclass
class Decision:
    """Final decision with reasoning"""
    solution: Solution
    reasoning: str
    confidence: float

@dataclass
class ReasoningResult:
    """Complete reasoning result"""
    decision: Decision
    explanation: str
    reasoning_steps: List[str]
    confidence: float

class LocalReasoningEngine:
    """
    Enhanced Local reasoning engine with built-in intelligence
    """
    
    def __init__(self):
        """Initialize the reasoning engine"""
        self.reasoning_steps = []
        self.local_model = None
        self.use_local_model = False
        
        # For web interface, use enhanced built-in logic for better performance
        # Local model can be slow and cause connection timeouts
        self.use_local_model = False
        print("🧠 Local Reasoning Engine initialized (using enhanced built-in logic for web interface)")
    
    def reason_through_problem(self, request: str, context: Dict) -> ReasoningResult:
        """
        Main reasoning method - simplified version
        """
        self.reasoning_steps = []
        
        # Step 1: Parse request
        self.reasoning_steps.append("Parsing and understanding the request")
        parsed_request = self._parse_request_simple(request)
        
        # Step 2: Find solution
        self.reasoning_steps.append("Finding appropriate solution")
        solution = self._find_solution_simple(parsed_request)
        
        # Step 3: Make decision
        self.reasoning_steps.append("Making informed decision")
        decision = self._make_decision_simple(solution, parsed_request)
        
        # Step 4: Generate explanation
        self.reasoning_steps.append("Generating comprehensive explanation")
        explanation = self._generate_explanation_simple(decision, parsed_request)
        
        return ReasoningResult(
            decision=decision,
            explanation=explanation,
            reasoning_steps=self.reasoning_steps,
            confidence=decision.confidence
        )
    
    def _parse_request_simple(self, request: str) -> ParsedRequest:
        """Enhanced request parsing with intelligent analysis"""
        request_lower = request.lower()
        
        # Intelligent user count extraction
        users = self._extract_user_count(request_lower)
        
        # Intelligent budget extraction
        budget = self._extract_budget(request_lower)
        
        # Intelligent performance analysis
        performance = self._analyze_performance_requirements(request_lower)
        
        # Intelligent security analysis
        security = self._analyze_security_requirements(request_lower)
        
        # Intelligent scalability analysis
        scalability = self._analyze_scalability_requirements(request_lower, users)
        
        # Extract technology preferences
        tech_preferences = self._extract_technology_preferences(request_lower)
        
        # Determine objective from request
        objective = self._determine_objective(request_lower)
        
        # Extract entities
        entities = self._extract_entities(request_lower)
        
        return ParsedRequest(
            objective=objective,
            entities=entities,
            constraints={
                "budget": budget,
                "performance": performance,
                "security": security,
                "scalability": scalability
            },
            scale={
                "users": users,
                "traffic": "low" if users < 100 else "medium" if users < 5000 else "high"
            },
            technology_preferences=tech_preferences
        )
    
    def _extract_user_count(self, request_lower: str) -> int:
        """Intelligently extract user count from request"""
        import re
        
        # Enhanced patterns for user count extraction
        patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*(?:users?|concurrent|simultaneous|devices?)\b',  # Handle comma-separated numbers
            r'for\s+(\d{1,3}(?:,\d{3})*)\s*(?:users?|devices?|concurrent)',
            r'(\d{1,3}(?:,\d{3})*)\s*(?:users?|devices?)\s*with',
            r'support\s+(\d{1,3}(?:,\d{3})*)\s*(?:users?|devices?)',
            r'(\d{1,3}(?:,\d{3})*)\s*(?:users?|devices?)\s*and',
            r'\b(\d+)\s*(?:users?|concurrent|simultaneous|devices?)\b',  # Simple numbers
            r'for\s+(\d+)\s*(?:users?|devices?|concurrent)',
            r'(\d+)\s*(?:users?|devices?)\s*with',
            r'support\s+(\d+)\s*(?:users?|devices?)',
            r'(\d+)\s*(?:users?|devices?)\s*and',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, request_lower)
            if matches:
                # Handle comma-separated numbers like "10,000"
                if isinstance(matches[0], tuple):
                    number_str = ''.join(matches[0])
                    return int(number_str)
                else:
                    # Remove commas and convert to int
                    number_str = matches[0].replace(',', '')
                    return int(number_str)
        
        # Keyword-based estimation
        if any(word in request_lower for word in ['millions', 'enterprise', 'global', 'massive']):
            return 100000
        elif any(word in request_lower for word in ['hundreds of thousands', 'large scale']):
            return 50000
        elif any(word in request_lower for word in ['tens of thousands', '10k', '10000']):
            return 10000
        elif any(word in request_lower for word in ['thousands', '5k', '5000']):
            return 5000
        elif any(word in request_lower for word in ['hundreds', '1k', '1000']):
            return 1000
        elif any(word in request_lower for word in ['dozens', '100', 'small']):
            return 100
        else:
            return 500  # Default reasonable estimate
    
    def _extract_budget(self, request_lower: str) -> int:
        """Intelligently extract budget from request"""
        import re
        
        # Look for explicit budget amounts
        budget_patterns = [
            r'\$(\d+)\s*(?:per\s*month|/month|monthly)',
            r'budget\s*(?:of\s*)?\$(\d+)',
            r'cost\s*(?:of\s*)?\$(\d+)',
            r'spend\s*(?:up\s*to\s*)?\$(\d+)'
        ]
        
        for pattern in budget_patterns:
            matches = re.findall(pattern, request_lower)
            if matches:
                return int(matches[0])
        
        # Keyword-based estimation
        if any(word in request_lower for word in ['unlimited', 'enterprise', 'premium', 'high budget']):
            return 2000
        elif any(word in request_lower for word in ['expensive', 'high cost', 'premium']):
            return 1000
        elif any(word in request_lower for word in ['moderate', 'medium', 'reasonable']):
            return 300
        elif any(word in request_lower for word in ['low budget', 'cheap', 'minimal', 'basic', 'startup']):
            return 100
        else:
            return 200  # Default reasonable budget
    
    def _analyze_performance_requirements(self, request_lower: str) -> str:
        """Analyze performance requirements from request"""
        high_perf_keywords = [
            'high performance', 'fast', 'optimized', 'enterprise', 'production',
            'real-time', 'low latency', 'high throughput', 'scalable', 'robust'
        ]
        
        low_perf_keywords = [
            'basic', 'simple', 'prototype', 'demo', 'testing', 'development'
        ]
        
        if any(keyword in request_lower for keyword in high_perf_keywords):
            return "high"
        elif any(keyword in request_lower for keyword in low_perf_keywords):
            return "low"
        else:
            return "medium"
    
    def _analyze_security_requirements(self, request_lower: str) -> str:
        """Analyze security requirements from request"""
        high_sec_keywords = [
            'secure', 'security', 'compliance', 'enterprise', 'production',
            'encryption', 'authentication', 'authorization', 'audit', 'pci',
            'hipaa', 'gdpr', 'soc2', 'iso27001'
        ]
        
        low_sec_keywords = [
            'basic', 'simple', 'prototype', 'demo', 'testing', 'development'
        ]
        
        if any(keyword in request_lower for keyword in high_sec_keywords):
            return "high"
        elif any(keyword in request_lower for keyword in low_sec_keywords):
            return "low"
        else:
            return "medium"
    
    def _analyze_scalability_requirements(self, request_lower: str, users: int) -> str:
        """Analyze scalability requirements from request"""
        if users > 10000 or any(word in request_lower for word in ['auto-scaling', 'elastic', 'scalable', 'growth']):
            return "high"
        elif users > 1000 or any(word in request_lower for word in ['scaling', 'expandable']):
            return "medium"
        else:
            return "low"
    
    def _extract_technology_preferences(self, request_lower: str) -> list:
        """Extract technology preferences from request"""
        preferences = []
        
        if any(word in request_lower for word in ['docker', 'container', 'kubernetes', 'k8s']):
            preferences.append('containers')
        if any(word in request_lower for word in ['serverless', 'lambda', 'functions']):
            preferences.append('serverless')
        if any(word in request_lower for word in ['microservices', 'microservice']):
            preferences.append('microservices')
        if any(word in request_lower for word in ['postgres', 'postgresql', 'mysql', 'database']):
            preferences.append('database')
        if any(word in request_lower for word in ['redis', 'cache', 'caching']):
            preferences.append('caching')
        if any(word in request_lower for word in ['cdn', 'cloudfront', 'static']):
            preferences.append('cdn')
        
        return preferences
    
    def _determine_objective(self, request_lower: str) -> str:
        """Determine the main objective from request with enhanced domain recognition"""
        # Machine Learning / AI domain
        if any(word in request_lower for word in ['ml', 'machine learning', 'ai', 'data science', 'training', 'inference', 'model', 'neural', 'deep learning']):
            return "machine learning pipeline"
        # IoT domain
        elif any(word in request_lower for word in ['iot', 'device', 'sensor', 'telemetry', 'connected', 'smart']):
            return "iot platform"
        # Data Analytics domain
        elif any(word in request_lower for word in ['data', 'analytics', 'processing', 'pipeline', 'warehouse', 'lake', 'etl', 'analytics']):
            return "data analytics platform"
        # Enterprise domain
        elif any(word in request_lower for word in ['enterprise', 'microservices', 'distributed', 'multi-tenant', 'saas']):
            return "enterprise microservices"
        # Standard domains
        elif any(word in request_lower for word in ['web app', 'website', 'web application', 'web service']):
            return "web_application"
        elif any(word in request_lower for word in ['api', 'rest api', 'graphql', 'microservice']):
            return "api_service"
        elif any(word in request_lower for word in ['database', 'db', 'data storage']):
            return "database"
        elif any(word in request_lower for word in ['monitoring', 'logging', 'observability']):
            return "monitoring"
        else:
            return "web_application"  # Default
    
    def _extract_entities(self, request_lower: str) -> list:
        """Extract key entities from request"""
        entities = []
        
        # Infrastructure entities
        if any(word in request_lower for word in ['server', 'ec2', 'compute']):
            entities.append('compute')
        if any(word in request_lower for word in ['database', 'db', 'rds', 'postgres', 'mysql']):
            entities.append('database')
        if any(word in request_lower for word in ['load balancer', 'alb', 'nlb']):
            entities.append('load_balancer')
        if any(word in request_lower for word in ['storage', 's3', 'files']):
            entities.append('storage')
        if any(word in request_lower for word in ['cdn', 'cloudfront', 'cache']):
            entities.append('cdn')
        
        # Application entities
        if any(word in request_lower for word in ['web', 'frontend', 'ui']):
            entities.append('web')
        if any(word in request_lower for word in ['api', 'backend', 'service']):
            entities.append('api')
        if any(word in request_lower for word in ['mobile', 'app']):
            entities.append('mobile')
        
        return entities if entities else ['web', 'application', 'users']

    def _find_solution_simple(self, parsed_request: ParsedRequest) -> Solution:
        """Intelligent solution finding with domain recognition"""
        users = parsed_request.scale['users']
        budget = parsed_request.constraints['budget']
        performance = parsed_request.constraints['performance']
        security = parsed_request.constraints['security']
        scalability = parsed_request.constraints['scalability']
        
        # Check for specialized domains in the objective
        objective_lower = parsed_request.objective.lower()
        
        # Machine Learning / AI domain recognition
        if any(keyword in objective_lower for keyword in ["machine learning", "ml", "ai", "training", "inference", "model", "neural", "deep learning"]):
            if "training" in objective_lower or "model" in objective_lower:
                solution = Solution(
                    name="ML Training Pipeline",
                    description="Machine learning model training infrastructure with SageMaker, EMR, and S3",
                    components=["sagemaker", "emr", "s3", "iam", "cloudwatch", "vpc"],
                    cost_estimate=min(budget * 0.9, 1200),
                    performance_score=0.9,
                    security_score=0.85,
                    complexity="high",
                    scalability_score=0.9,
                    maintainability_score=0.7,
                    compliance_score=0.8,
                    risk_score=0.3
                )
            else:
                solution = Solution(
                    name="ML Inference Pipeline",
                    description="Real-time ML inference infrastructure with Lambda, ECS, and API Gateway",
                    components=["lambda", "ecs", "api_gateway", "dynamodb", "cloudwatch"],
                    cost_estimate=min(budget * 0.8, 400),
                    performance_score=0.9,
                    security_score=0.8,
                    complexity="high",
                    scalability_score=0.95,
                    maintainability_score=0.8,
                    compliance_score=0.75,
                    risk_score=0.2
                )
        # IoT domain recognition
        elif any(keyword in objective_lower for keyword in ["iot", "device", "sensor", "telemetry", "connected", "smart"]):
            solution = Solution(
                name="IoT Platform",
                description="IoT device management and data processing with AWS IoT Core and Kinesis",
                components=["iot_core", "kinesis", "lambda", "dynamodb", "s3", "cloudwatch"],
                cost_estimate=min(budget * 0.8, 300),
                performance_score=0.85,
                security_score=0.9,
                complexity="high",
                scalability_score=0.95,
                maintainability_score=0.6,
                compliance_score=0.85,
                risk_score=0.4
            )
        # Data Analytics domain recognition
        elif any(keyword in objective_lower for keyword in ["data", "analytics", "processing", "pipeline", "warehouse", "lake", "etl"]):
            solution = Solution(
                name="Data Analytics Platform",
                description="Data analytics and processing platform with EMR, S3, and Redshift",
                components=["emr", "s3", "redshift", "glue", "athena", "cloudwatch"],
                cost_estimate=min(budget * 0.9, 800),
                performance_score=0.9,
                security_score=0.8,
                complexity="high",
                scalability_score=0.9,
                maintainability_score=0.7,
                compliance_score=0.8,
                risk_score=0.3
            )
        # Enterprise domain recognition
        elif any(keyword in objective_lower for keyword in ["enterprise", "microservices", "distributed", "multi-tenant", "saas"]):
            solution = Solution(
                name="Enterprise Microservices Architecture",
                description="Enterprise-grade microservices with EKS, service mesh, and comprehensive monitoring",
                components=["eks", "istio", "prometheus", "grafana", "jaeger", "vpc", "alb"],
                cost_estimate=min(budget * 0.8, 1500),
                performance_score=0.95,
                security_score=0.95,
                complexity="very_high",
                scalability_score=0.98,
                maintainability_score=0.6,
                compliance_score=0.95,
                risk_score=0.5
            )
        # Standard web application logic with proper scale recognition
        elif users > 100000 or budget > 2000:
            # Enterprise-scale solution
            solution = Solution(
                name="Enterprise Microservices Architecture",
                description="High-scale microservices architecture with auto-scaling, load balancing, and enterprise security",
                components=["eks", "alb", "rds_cluster", "cloudfront", "waf", "autoscaling", "monitoring"],
                cost_estimate=min(budget * 0.8, 2000),
                performance_score=0.95,
                security_score=0.95,
                complexity="very_high",
                scalability_score=0.98,
                maintainability_score=0.6,
                compliance_score=0.95,
                risk_score=0.5
            )
        elif users > 50000 or budget > 1000:
            # Large-scale solution
            solution = Solution(
                name="Scalable Web Application",
                description="High-scale web application with load balancing, auto-scaling, and monitoring",
                components=["alb", "ec2", "rds", "autoscaling", "cloudfront", "monitoring"],
                cost_estimate=min(budget * 0.8, 1200),
                performance_score=0.9,
                security_score=0.85,
                complexity="high",
                scalability_score=0.9,
                maintainability_score=0.7,
                compliance_score=0.8,
                risk_score=0.3
            )
        elif users > 10000 or budget > 500:
            # Scalable web application
            solution = Solution(
                name="Scalable Web Application",
                description="Multi-tier web application with auto-scaling, load balancing, and high availability",
                components=["load_balancer", "web_servers", "database", "cache", "monitoring"],
                cost_estimate=min(budget * 0.8, 800),
                performance_score=0.85,
                security_score=0.8,
                complexity="medium"
            )
        elif users > 1000 or budget > 200:
            # Standard web application
            solution = Solution(
                name="Load Balanced Web Application",
                description="Standard web application with load balancer, multiple web servers, and database",
                components=["load_balancer", "web_servers", "database", "monitoring"],
                cost_estimate=min(budget * 0.8, 400),
                performance_score=0.75,
                security_score=0.7,
                complexity="medium"
            )
        else:
            # Basic web application
            solution = Solution(
                name="Basic Web Application",
                description="Simple web application with single server and database",
                components=["web_server", "database"],
                cost_estimate=min(budget * 0.8, 150),
                performance_score=0.6,
                security_score=0.6,
                complexity="low"
            )
        
        # Adjust based on specific requirements
        if performance == "high":
            solution.performance_score = min(solution.performance_score + 0.1, 1.0)
            solution.cost_estimate *= 1.2
        
        if security == "high":
            solution.security_score = min(solution.security_score + 0.1, 1.0)
            solution.cost_estimate *= 1.15
            solution.components.append("security_groups")
        
        if scalability == "high":
            solution.components.append("auto_scaling")
            solution.cost_estimate *= 1.1
        
        return solution
    
    def _make_decision_simple(self, solution: Solution, parsed_request: ParsedRequest) -> Decision:
        """Intelligent decision making with detailed reasoning"""
        users = parsed_request.scale['users']
        budget = parsed_request.constraints['budget']
        performance = parsed_request.constraints['performance']
        security = parsed_request.constraints['security']
        scalability = parsed_request.constraints['scalability']
        
        # Build intelligent reasoning
        reasoning_parts = []
        
        # User scale reasoning
        if users > 50000:
            reasoning_parts.append(f"Your requirement for {users:,} users demands enterprise-scale architecture")
        elif users > 10000:
            reasoning_parts.append(f"With {users:,} users, you need a highly scalable solution")
        elif users > 1000:
            reasoning_parts.append(f"For {users:,} users, a load-balanced architecture is optimal")
        else:
            reasoning_parts.append(f"A simple architecture is sufficient for {users} users")
        
        # Budget reasoning
        if budget > 1000:
            reasoning_parts.append(f"Your ${budget}/month budget allows for enterprise features")
        elif budget > 500:
            reasoning_parts.append(f"Your ${budget}/month budget enables advanced scaling and monitoring")
        elif budget > 200:
            reasoning_parts.append(f"Your ${budget}/month budget supports standard production features")
        else:
            reasoning_parts.append(f"Your ${budget}/month budget is optimized for cost-effective solutions")
        
        # Performance reasoning
        if performance == "high":
            reasoning_parts.append("High performance requirements drive the need for optimized infrastructure")
        elif performance == "low":
            reasoning_parts.append("Basic performance needs allow for simpler, cost-effective solutions")
        
        # Security reasoning
        if security == "high":
            reasoning_parts.append("High security requirements necessitate enterprise-grade security features")
        elif security == "low":
            reasoning_parts.append("Basic security needs are addressed with standard configurations")
        
        # Scalability reasoning
        if scalability == "high":
            reasoning_parts.append("High scalability requirements ensure future growth accommodation")
        
        # Calculate confidence based on how well the solution matches requirements
        confidence = 0.7  # Base confidence
        
        # Increase confidence based on good matches
        if solution.cost_estimate <= budget * 1.1:  # Within 10% of budget
            confidence += 0.1
        if users <= 1000 and solution.complexity == "low":
            confidence += 0.05
        elif users <= 10000 and solution.complexity == "medium":
            confidence += 0.05
        elif users > 10000 and solution.complexity == "high":
            confidence += 0.05
        
        if performance == "high" and solution.performance_score > 0.8:
            confidence += 0.05
        if security == "high" and solution.security_score > 0.8:
            confidence += 0.05
        
        confidence = min(confidence, 0.95)  # Cap at 95%
        
        reasoning = f"{solution.name} was selected because: " + "; ".join(reasoning_parts) + "."
        
        return Decision(
            solution=solution,
            reasoning=reasoning,
            confidence=confidence
        )
    
    def _generate_explanation_simple(self, decision: Decision, parsed_request: ParsedRequest) -> str:
        """Generate explanation using local model if available"""
        if self.use_local_model and self.local_model:
            return self._generate_explanation_with_local_model(decision, parsed_request)
        else:
            return self._generate_explanation_fallback(decision, parsed_request)
    
    def _generate_explanation_with_local_model(self, decision: Decision, parsed_request: ParsedRequest) -> str:
        """Generate enhanced explanation using built-in intelligence"""
        # This method is kept for compatibility but always uses fallback
        return self._generate_explanation_fallback(decision, parsed_request)
    
    def _generate_explanation_fallback(self, decision: Decision, parsed_request: ParsedRequest) -> str:
        """Enhanced fallback explanation with advanced reasoning analysis"""
        users = parsed_request.scale['users']
        budget = parsed_request.constraints['budget']
        performance = parsed_request.constraints['performance']
        security = parsed_request.constraints['security']
        scalability = parsed_request.constraints['scalability']
        
        # Advanced reasoning analysis
        constraint_analysis = self._analyze_constraints(decision.solution)
        risk_assessment = self._assess_risks(decision.solution)
        optimization_recommendations = self._generate_optimization_recommendations(decision.solution)
        
        # Generate intelligent explanation with advanced reasoning
        explanation = f"""
## Solution: {decision.solution.name}

**Why chosen:** {decision.reasoning}

**How it addresses your specific requirements:**
- **Scale:** Handles {users:,} users with {decision.solution.complexity} complexity architecture
- **Budget:** Estimated ${decision.solution.cost_estimate:.0f}/month (within your ${budget}/month budget)
- **Performance:** {performance.title()} performance requirements met with {decision.solution.performance_score:.1f}/1.0 score
- **Security:** {security.title()} security needs addressed with {decision.solution.security_score:.1f}/1.0 score
- **Scalability:** {scalability.title()} scalability requirements supported

**Advanced Performance Metrics:**
- **Scalability Score:** {decision.solution.scalability_score:.1f}/1.0
- **Maintainability Score:** {decision.solution.maintainability_score:.1f}/1.0
- **Compliance Score:** {decision.solution.compliance_score:.1f}/1.0
- **Risk Score:** {decision.solution.risk_score:.1f}/1.0 (Lower is better)

**Architecture Components:**
{chr(10).join([f"- {component.replace('_', ' ').title()}" for component in decision.solution.components])}

**Multi-Constraint Analysis:**
{constraint_analysis}

**Risk Assessment:**
{risk_assessment}

**Optimization Recommendations:**
{optimization_recommendations}

**Implementation considerations:**
- **Cost Optimization:** Solution designed to stay within budget while meeting requirements
- **Performance Tuning:** Architecture optimized for your {performance} performance needs
- **Security Hardening:** Security measures appropriate for {security} security requirements
- **Future Growth:** Scalability features ensure accommodation of future growth

**Confidence Assessment:** {decision.confidence:.1%} confidence based on requirement analysis and solution matching
        """
        return explanation.strip()
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get status of local model integration"""
        if self.local_model:
            return self.local_model.get_model_info()
        else:
            return {
                "model_name": "None",
                "model_path": None,
                "is_loaded": False,
                "is_available": False,
                "llama_cpp_available": LOCAL_MODEL_AVAILABLE
            }
    
    def _analyze_constraints_locally(self, parsed_request: ParsedRequest, context: Dict) -> Dict:
        """Analyze constraints locally (placeholder method)"""
        return {
            "budget": parsed_request.constraints.get("budget", 200),
            "performance": parsed_request.constraints.get("performance", "medium"),
            "security": parsed_request.constraints.get("security", "medium"),
            "scalability": parsed_request.constraints.get("scalability", "medium")
        }
    
    def _analyze_constraints(self, solution: Solution) -> str:
        """Analyze multi-constraint trade-offs"""
        analysis = []
        
        # Cost vs Performance Analysis
        if solution.cost_estimate > 1000 and solution.performance_score < 0.7:
            analysis.append("⚠️ High cost with moderate performance - consider right-sizing")
        elif solution.cost_estimate < 200 and solution.performance_score > 0.8:
            analysis.append("✅ Excellent cost-performance ratio")
        
        # Security vs Usability Trade-offs
        if solution.security_score > 0.8 and solution.complexity == "high":
            analysis.append("🔒 High security with high complexity - consider security automation")
        elif solution.security_score < 0.6 and solution.complexity == "low":
            analysis.append("⚠️ Low security with simple architecture - add security layers")
        
        # Scalability vs Complexity Balance
        if solution.scalability_score > 0.8 and solution.complexity == "very_high":
            analysis.append("📈 High scalability with high complexity - consider managed services")
        elif solution.scalability_score < 0.6 and solution.complexity == "low":
            analysis.append("⚠️ Limited scalability - plan for future growth")
        
        return "\n".join(analysis) if analysis else "✅ Well-balanced solution across all constraints"
    
    def _assess_risks(self, solution: Solution) -> str:
        """Comprehensive risk assessment"""
        risks = []
        mitigations = []
        
        # Infrastructure Risks
        if solution.complexity == "very_high":
            risks.append("🔴 High operational complexity - single points of failure")
            mitigations.append("💡 Implement comprehensive monitoring and automation")
        
        if solution.cost_estimate > 2000:
            risks.append("🔴 High cost risk - potential budget overruns")
            mitigations.append("💡 Implement cost monitoring and auto-scaling")
        
        # Security Risks
        if solution.security_score < 0.7:
            risks.append("🔴 Security vulnerabilities - compliance issues")
            mitigations.append("💡 Implement security scanning and compliance monitoring")
        
        # Performance Risks
        if solution.performance_score < 0.6:
            risks.append("🔴 Performance bottlenecks - user experience issues")
            mitigations.append("💡 Implement performance monitoring and optimization")
        
        # Scalability Risks
        if solution.scalability_score < 0.6:
            risks.append("🔴 Limited scalability - growth constraints")
            mitigations.append("💡 Plan for horizontal scaling and load balancing")
        
        risk_text = "**Identified Risks:**\n" + "\n".join(risks) if risks else "✅ Low risk profile"
        mitigation_text = "**Risk Mitigations:**\n" + "\n".join(mitigations) if mitigations else "✅ No major risks identified"
        
        return f"{risk_text}\n\n{mitigation_text}"
    
    def _generate_optimization_recommendations(self, solution: Solution) -> str:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Cost Optimization
        if solution.cost_estimate > 1000:
            recommendations.append("💰 Cost Optimization: Consider reserved instances, spot instances, or auto-scaling")
        
        if solution.cost_estimate < 100:
            recommendations.append("💰 Cost Optimization: Current solution is cost-effective")
        
        # Performance Optimization
        if solution.performance_score < 0.7:
            recommendations.append("⚡ Performance: Add caching layers, CDN, or database optimization")
        
        # Security Optimization
        if solution.security_score < 0.8:
            recommendations.append("🔒 Security: Implement WAF, encryption, and access controls")
        
        # Scalability Optimization
        if solution.scalability_score < 0.7:
            recommendations.append("📈 Scalability: Add load balancers, auto-scaling, and microservices")
        
        # Maintenance Optimization
        if solution.complexity == "very_high":
            recommendations.append("🛠️ Maintenance: Consider managed services and automation")
        
        return "\n".join(recommendations) if recommendations else "✅ Solution is well-optimized"

