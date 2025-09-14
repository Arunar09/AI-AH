"""
Local Reasoning Engine - The Heart of Intelligent Decision Making
No external APIs, no costs, fully offline reasoning
"""

import json
import sqlite3
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import networkx as nx
import spacy

@dataclass
class ParsedRequest:
    """Parsed user request with extracted information"""
    objective: str
    entities: List[str]
    constraints: Dict[str, Any]
    scale: Dict[str, Any]
    technology_preferences: List[str]
    urgency: str = "medium"
    budget: Optional[float] = None

@dataclass
class SubProblem:
    """Individual sub-problem to solve"""
    component: str
    requirements: List[str]
    constraints: Dict[str, Any]
    priority: int = 1

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
    pattern_id: str

@dataclass
class EvaluatedSolution:
    """Solution with evaluation scores"""
    solution: Solution
    overall_score: float
    constraint_scores: Dict[str, float]
    tradeoffs: List[str]
    reasoning: str

@dataclass
class Decision:
    """Final decision with reasoning"""
    solution: EvaluatedSolution
    reasoning: str
    alternatives: List[EvaluatedSolution]
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
    Local reasoning engine that thinks through problems step by step
    No external APIs, no costs, fully offline
    """
    
    def __init__(self):
        """Initialize the reasoning engine with local models"""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = spacy.load("en_core_web_sm")
        self.knowledge_graph = nx.DiGraph()
        self.db = sqlite3.connect('local_knowledge.db', check_same_thread=False)
        self.reasoning_steps = []
        
        # Initialize database
        self._init_database()
        
        # Load knowledge base
        self._load_knowledge_base()
    
    def _init_database(self):
        """Initialize SQLite database for local knowledge"""
        cursor = self.db.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS infrastructure_patterns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                components TEXT,
                cost_model TEXT,
                performance_model TEXT,
                security_model TEXT,
                complexity TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reasoning_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request TEXT,
                reasoning_steps TEXT,
                decision TEXT,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.db.commit()
    
    def _load_knowledge_base(self):
        """Load infrastructure knowledge from local data"""
        # This will be populated by dataset scraping
        # For now, add some basic patterns
        basic_patterns = [
            {
                "id": "web_app_basic",
                "name": "Basic Web Application",
                "description": "Simple web application with load balancer, web servers, and database",
                "category": "web_application",
                "components": ["load_balancer", "web_server", "database"],
                "cost_model": '{"base_cost": 100, "scaling": "linear"}',
                "performance_model": '{"throughput": "1000 req/sec", "latency": "50ms"}',
                "security_model": '{"level": "basic", "features": ["ssl", "firewall"]}',
                "complexity": "low"
            },
            {
                "id": "web_app_scalable",
                "name": "Scalable Web Application",
                "description": "High-availability web application with auto-scaling and CDN",
                "category": "web_application",
                "components": ["load_balancer", "auto_scaling", "web_servers", "database", "cdn"],
                "cost_model": '{"base_cost": 300, "scaling": "exponential"}',
                "performance_model": '{"throughput": "10000 req/sec", "latency": "20ms"}',
                "security_model": '{"level": "high", "features": ["ssl", "waf", "ddos_protection"]}',
                "complexity": "medium"
            }
        ]
        
        cursor = self.db.cursor()
        for pattern in basic_patterns:
            cursor.execute('''
                INSERT OR REPLACE INTO infrastructure_patterns 
                (id, name, description, category, components, cost_model, performance_model, security_model, complexity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern["id"], pattern["name"], pattern["description"], 
                pattern["category"], json.dumps(pattern["components"]),
                pattern["cost_model"], pattern["performance_model"], 
                pattern["security_model"], pattern["complexity"]
            ))
        
        self.db.commit()
    
    def reason_through_problem(self, request: str, context: Dict) -> ReasoningResult:
        """
        Main reasoning method - thinks through problems step by step
        """
        self.reasoning_steps = []
        
        # Step 1: Parse and understand the request
        self.reasoning_steps.append("Parsing and understanding the request")
        parsed_request = self._parse_request_locally(request)
        
        # Step 2: Decompose into sub-problems
        self.reasoning_steps.append("Decomposing problem into manageable sub-problems")
        sub_problems = self._decompose_problem_locally(parsed_request)
        
        # Step 3: Analyze constraints
        self.reasoning_steps.append("Analyzing constraints and requirements")
        constraints = self._analyze_constraints_locally(parsed_request, context)
        
        # Step 4: Find solutions using knowledge base
        self.reasoning_steps.append("Finding solutions using knowledge base")
        solutions = self._find_solutions_locally(sub_problems, constraints)
        
        # Step 5: Evaluate solutions
        self.reasoning_steps.append("Evaluating solutions against constraints")
        evaluated_solutions = self._evaluate_solutions_locally(solutions, constraints)
        
        # Step 6: Make decision
        self.reasoning_steps.append("Making informed decision")
        decision = self._make_decision_locally(evaluated_solutions)
        
        # Step 7: Generate explanation
        self.reasoning_steps.append("Generating comprehensive explanation")
        explanation = self._generate_explanation_locally(decision, constraints)
        
        # Store reasoning history
        self._store_reasoning_history(request, decision, explanation)
        
        return ReasoningResult(
            decision=decision,
            explanation=explanation,
            reasoning_steps=self.reasoning_steps,
            confidence=decision.confidence
        )
    
    def _parse_request_locally(self, request: str) -> ParsedRequest:
        """Parse request using local NLP and rule-based extraction"""
        doc = self.nlp(request)
        
        # Extract entities
        entities = [ent.text for ent in doc.ents]
        
        # Extract constraints using pattern matching
        constraints = self._extract_constraints_locally(request)
        
        # Extract scale requirements
        scale = self._extract_scale_locally(request)
        
        # Extract technology preferences
        tech_preferences = self._extract_tech_preferences_locally(request)
        
        # Extract objective
        objective = self._extract_objective_locally(request)
        
        return ParsedRequest(
            objective=objective,
            entities=entities,
            constraints=constraints,
            scale=scale,
            technology_preferences=tech_preferences
        )
    
    def _extract_constraints_locally(self, request: str) -> Dict[str, Any]:
        """Extract constraints using local pattern matching"""
        constraints = {}
        
        # Budget constraints
        if "budget" in request.lower() or "$" in request:
            # Simple regex to extract budget
            import re
            budget_match = re.search(r'\$(\d+)', request)
            if budget_match:
                constraints["budget"] = float(budget_match.group(1))
        
        # Performance constraints
        if "performance" in request.lower() or "fast" in request.lower():
            constraints["performance"] = "high"
        elif "slow" in request.lower():
            constraints["performance"] = "low"
        else:
            constraints["performance"] = "medium"
        
        # Security constraints
        if "security" in request.lower() or "secure" in request.lower():
            constraints["security"] = "high"
        elif "basic" in request.lower():
            constraints["security"] = "low"
        else:
            constraints["security"] = "medium"
        
        # Availability constraints
        if "99.9" in request or "high availability" in request.lower():
            constraints["availability"] = "high"
        elif "99" in request:
            constraints["availability"] = "medium"
        else:
            constraints["availability"] = "low"
        
        return constraints
    
    def _extract_scale_locally(self, request: str) -> Dict[str, Any]:
        """Extract scale requirements"""
        scale = {}
        
        # User count
        import re
        user_match = re.search(r'(\d+)\s*users?', request.lower())
        if user_match:
            scale["users"] = int(user_match.group(1))
        
        # Traffic
        if "high traffic" in request.lower():
            scale["traffic"] = "high"
        elif "low traffic" in request.lower():
            scale["traffic"] = "low"
        else:
            scale["traffic"] = "medium"
        
        return scale
    
    def _extract_tech_preferences_locally(self, request: str) -> List[str]:
        """Extract technology preferences"""
        preferences = []
        
        if "aws" in request.lower():
            preferences.append("aws")
        if "azure" in request.lower():
            preferences.append("azure")
        if "gcp" in request.lower() or "google" in request.lower():
            preferences.append("gcp")
        if "kubernetes" in request.lower() or "k8s" in request.lower():
            preferences.append("kubernetes")
        if "docker" in request.lower():
            preferences.append("docker")
        
        return preferences
    
    def _extract_objective_locally(self, request: str) -> str:
        """Extract the main objective"""
        # Simple keyword-based extraction
        if "web app" in request.lower():
            return "web_application"
        elif "api" in request.lower():
            return "api_service"
        elif "database" in request.lower():
            return "database_service"
        elif "monitoring" in request.lower():
            return "monitoring_system"
        else:
            return "general_infrastructure"
    
    def _decompose_problem_locally(self, parsed_request: ParsedRequest) -> List[SubProblem]:
        """Break down problems using local knowledge and rules"""
        sub_problems = []
        
        # Map objectives to components
        objective_components = {
            "web_application": ["load_balancer", "web_server", "database", "monitoring"],
            "api_service": ["api_gateway", "compute", "database", "monitoring"],
            "database_service": ["database", "backup", "monitoring", "security"],
            "monitoring_system": ["metrics_collection", "storage", "visualization", "alerting"]
        }
        
        components = objective_components.get(parsed_request.objective, ["compute", "storage", "networking"])
        
        for i, component in enumerate(components):
            sub_problem = SubProblem(
                component=component,
                requirements=self._get_component_requirements(component),
                constraints=self._filter_constraints(parsed_request.constraints, component),
                priority=i + 1
            )
            sub_problems.append(sub_problem)
        
        return sub_problems
    
    def _get_component_requirements(self, component: str) -> List[str]:
        """Get requirements for a specific component"""
        requirements_map = {
            "load_balancer": ["high_availability", "ssl_termination", "health_checks"],
            "web_server": ["auto_scaling", "load_balancing", "monitoring"],
            "database": ["backup", "replication", "monitoring", "security"],
            "monitoring": ["metrics_collection", "alerting", "visualization"]
        }
        return requirements_map.get(component, ["basic_functionality"])
    
    def _filter_constraints(self, constraints: Dict[str, Any], component: str) -> Dict[str, Any]:
        """Filter constraints relevant to a specific component"""
        # For now, return all constraints
        # In a more sophisticated implementation, this would filter based on component relevance
        return constraints
    
    def _find_solutions_locally(self, sub_problems: List[SubProblem], constraints: Dict[str, Any]) -> List[Solution]:
        """Find solutions using local knowledge base"""
        solutions = []
        
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM infrastructure_patterns")
        patterns = cursor.fetchall()
        
        for pattern in patterns:
            # Convert pattern to Solution object
            solution = Solution(
                name=pattern[1],
                description=pattern[2],
                components=json.loads(pattern[4]),
                cost_estimate=self._calculate_cost_estimate(pattern[5], constraints),
                performance_score=self._calculate_performance_score(pattern[6]),
                security_score=self._calculate_security_score(pattern[7]),
                complexity=pattern[8],
                pattern_id=pattern[0]
            )
            
            # Check if solution matches constraints
            if self._solution_matches_constraints(solution, constraints):
                solutions.append(solution)
        
        return solutions
    
    def _calculate_cost_estimate(self, cost_model: str, constraints: Dict[str, Any]) -> float:
        """Calculate cost estimate based on constraints"""
        cost_data = json.loads(cost_model)
        base_cost = cost_data.get("base_cost", 100)
        
        # Scale based on constraints
        scale_factor = 1.0
        if "users" in constraints:
            if constraints["users"] > 10000:
                scale_factor = 3.0
            elif constraints["users"] > 1000:
                scale_factor = 2.0
        
        return base_cost * scale_factor
    
    def _calculate_performance_score(self, performance_model: str) -> float:
        """Calculate performance score"""
        perf_data = json.loads(performance_model)
        
        # Simple scoring based on throughput
        throughput = perf_data.get("throughput", "100 req/sec")
        if "10000" in throughput:
            return 0.9
        elif "1000" in throughput:
            return 0.7
        else:
            return 0.5
    
    def _calculate_security_score(self, security_model: str) -> float:
        """Calculate security score"""
        sec_data = json.loads(security_model)
        
        level = sec_data.get("level", "basic")
        if level == "high":
            return 0.9
        elif level == "medium":
            return 0.7
        else:
            return 0.5
    
    def _solution_matches_constraints(self, solution: Solution, constraints: Dict[str, Any]) -> bool:
        """Check if solution matches constraints"""
        # Check budget constraint
        if "budget" in constraints:
            if solution.cost_estimate > constraints["budget"]:
                return False
        
        # Check performance constraint
        if "performance" in constraints:
            if constraints["performance"] == "high" and solution.performance_score < 0.8:
                return False
        
        # Check security constraint
        if "security" in constraints:
            if constraints["security"] == "high" and solution.security_score < 0.8:
                return False
        
        return True
    
    def _evaluate_solutions_locally(self, solutions: List[Solution], constraints: Dict[str, Any]) -> List[EvaluatedSolution]:
        """Evaluate solutions against constraints"""
        evaluated_solutions = []
        
        for solution in solutions:
            # Calculate constraint scores
            constraint_scores = {
                "cost": self._score_cost(solution, constraints),
                "performance": self._score_performance(solution, constraints),
                "security": self._score_security(solution, constraints),
                "complexity": self._score_complexity(solution, constraints)
            }
            
            # Calculate overall score
            overall_score = sum(constraint_scores.values()) / len(constraint_scores)
            
            # Generate tradeoffs
            tradeoffs = self._generate_tradeoffs(solution, constraints)
            
            # Generate reasoning
            reasoning = self._generate_solution_reasoning(solution, constraint_scores)
            
            evaluated_solution = EvaluatedSolution(
                solution=solution,
                overall_score=overall_score,
                constraint_scores=constraint_scores,
                tradeoffs=tradeoffs,
                reasoning=reasoning
            )
            
            evaluated_solutions.append(evaluated_solution)
        
        return evaluated_solutions
    
    def _score_cost(self, solution: Solution, constraints: Dict[str, Any]) -> float:
        """Score solution based on cost"""
        if "budget" not in constraints:
            return 0.5  # Neutral score if no budget constraint
        
        budget = constraints["budget"]
        cost_ratio = solution.cost_estimate / budget
        
        if cost_ratio <= 0.5:
            return 1.0  # Excellent
        elif cost_ratio <= 0.8:
            return 0.8  # Good
        elif cost_ratio <= 1.0:
            return 0.6  # Acceptable
        else:
            return 0.2  # Poor
    
    def _score_performance(self, solution: Solution, constraints: Dict[str, Any]) -> float:
        """Score solution based on performance"""
        if "performance" not in constraints:
            return solution.performance_score
        
        required_performance = constraints["performance"]
        if required_performance == "high" and solution.performance_score >= 0.8:
            return 1.0
        elif required_performance == "medium" and solution.performance_score >= 0.6:
            return 0.8
        else:
            return solution.performance_score
    
    def _score_security(self, solution: Solution, constraints: Dict[str, Any]) -> float:
        """Score solution based on security"""
        if "security" not in constraints:
            return solution.security_score
        
        required_security = constraints["security"]
        if required_security == "high" and solution.security_score >= 0.8:
            return 1.0
        elif required_security == "medium" and solution.security_score >= 0.6:
            return 0.8
        else:
            return solution.security_score
    
    def _score_complexity(self, solution: Solution, constraints: Dict[str, Any]) -> float:
        """Score solution based on complexity"""
        complexity_scores = {"low": 1.0, "medium": 0.7, "high": 0.4}
        return complexity_scores.get(solution.complexity, 0.5)
    
    def _generate_tradeoffs(self, solution: Solution, constraints: Dict[str, Any]) -> List[str]:
        """Generate tradeoffs for the solution"""
        tradeoffs = []
        
        if solution.cost_estimate > 200:
            tradeoffs.append("Higher cost for better performance and security")
        
        if solution.complexity == "high":
            tradeoffs.append("More complex setup for advanced features")
        
        if solution.performance_score > 0.8 and solution.cost_estimate > 150:
            tradeoffs.append("Performance vs cost tradeoff")
        
        return tradeoffs
    
    def _generate_solution_reasoning(self, solution: Solution, constraint_scores: Dict[str, float]) -> str:
        """Generate reasoning for why this solution was chosen"""
        reasoning_parts = []
        
        if constraint_scores["cost"] > 0.8:
            reasoning_parts.append("Cost-effective solution")
        
        if constraint_scores["performance"] > 0.8:
            reasoning_parts.append("High performance capabilities")
        
        if constraint_scores["security"] > 0.8:
            reasoning_parts.append("Strong security features")
        
        if constraint_scores["complexity"] > 0.8:
            reasoning_parts.append("Simple to implement and maintain")
        
        return "; ".join(reasoning_parts) if reasoning_parts else "Balanced solution"
    
    def _make_decision_locally(self, evaluated_solutions: List[EvaluatedSolution]) -> Decision:
        """Make decision using local rule-based reasoning"""
        if not evaluated_solutions:
            raise ValueError("No solutions to evaluate")
        
        # Sort by overall score
        sorted_solutions = sorted(evaluated_solutions, key=lambda x: x.overall_score, reverse=True)
        
        best_solution = sorted_solutions[0]
        alternatives = sorted_solutions[1:3]  # Top 2 alternatives
        
        # Generate decision reasoning
        reasoning = self._generate_decision_reasoning(best_solution, alternatives)
        
        # Calculate confidence based on score difference
        confidence = best_solution.overall_score
        if len(sorted_solutions) > 1:
            score_diff = best_solution.overall_score - sorted_solutions[1].overall_score
            confidence = min(confidence + score_diff * 0.5, 1.0)
        
        return Decision(
            solution=best_solution,
            reasoning=reasoning,
            alternatives=alternatives,
            confidence=confidence
        )
    
    def _generate_decision_reasoning(self, best_solution: EvaluatedSolution, alternatives: List[EvaluatedSolution]) -> str:
        """Generate reasoning for the decision"""
        reasoning_parts = [f"I chose {best_solution.solution.name} because:"]
        
        # Add reasoning from solution
        reasoning_parts.append(best_solution.reasoning)
        
        # Add comparison with alternatives
        if alternatives:
            alt_names = [alt.solution.name for alt in alternatives]
            reasoning_parts.append(f"Alternatives considered: {', '.join(alt_names)}")
        
        return " ".join(reasoning_parts)
    
    def _generate_explanation_locally(self, decision: Decision, constraints: Dict[str, Any]) -> str:
        """Generate comprehensive explanation"""
        explanation_parts = []
        
        # Why this solution was chosen
        explanation_parts.append(f"## Solution: {decision.solution.solution.name}")
        explanation_parts.append(f"**Why chosen:** {decision.reasoning}")
        
        # How it addresses requirements
        explanation_parts.append("**How it addresses your requirements:**")
        for requirement in decision.solution.solution.requirements:
            explanation_parts.append(f"- {requirement}")
        
        # Trade-offs made
        if decision.solution.tradeoffs:
            explanation_parts.append("**Trade-offs considered:**")
            for tradeoff in decision.solution.tradeoffs:
                explanation_parts.append(f"- {tradeoff}")
        
        # Implementation considerations
        explanation_parts.append("**Implementation considerations:**")
        explanation_parts.append(f"- Estimated cost: ${decision.solution.solution.cost_estimate:.0f}/month")
        explanation_parts.append(f"- Performance score: {decision.solution.solution.performance_score:.1f}/1.0")
        explanation_parts.append(f"- Security score: {decision.solution.solution.security_score:.1f}/1.0")
        explanation_parts.append(f"- Complexity: {decision.solution.solution.complexity}")
        
        # Confidence level
        explanation_parts.append(f"**Confidence level:** {decision.confidence:.1%}")
        
        return "\n".join(explanation_parts)
    
    def _store_reasoning_history(self, request: str, decision: Decision, explanation: str):
        """Store reasoning history for learning"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO reasoning_history (request, reasoning_steps, decision, confidence)
            VALUES (?, ?, ?, ?)
        ''', (
            request,
            json.dumps(self.reasoning_steps),
            json.dumps({
                "solution": decision.solution.solution.name,
                "reasoning": decision.reasoning
            }),
            decision.confidence
        ))
        self.db.commit()

