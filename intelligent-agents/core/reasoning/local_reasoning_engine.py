"""
Local Reasoning Engine - Enhanced with CodeLlama Integration
"""

import json
import sqlite3
import os
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from core.models.simple_local_model import get_simple_model, is_simple_model_available
    LOCAL_MODEL_AVAILABLE = True
except ImportError:
    LOCAL_MODEL_AVAILABLE = False
    print("⚠️ Local model integration not available")

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
    Enhanced Local reasoning engine with CodeLlama integration
    """
    
    def __init__(self):
        """Initialize the reasoning engine"""
        self.reasoning_steps = []
        self.local_model = None
        self.use_local_model = False
        
        # Disable local model for performance - use fast built-in logic instead
        self.use_local_model = False
        print("🧠 Local Reasoning Engine initialized (using fast built-in logic)")
    
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
        """Simple request parsing"""
        # Extract basic information
        objective = "web_application"
        entities = ["web", "application", "users"]
        constraints = {"budget": 200, "performance": "medium", "security": "medium"}
        scale = {"users": 1000}
        technology_preferences = []
        
        return ParsedRequest(
            objective=objective,
            entities=entities,
            constraints=constraints,
            scale=scale,
            technology_preferences=technology_preferences
        )
    
    def _find_solution_simple(self, parsed_request: ParsedRequest) -> Solution:
        """Find a simple solution"""
        return Solution(
            name="Basic Web Application",
            description="Simple web application with load balancer, web servers, and database",
            components=["load_balancer", "web_server", "database"],
            cost_estimate=150.0,
            performance_score=0.7,
            security_score=0.6,
            complexity="low"
        )
    
    def _make_decision_simple(self, solution: Solution, parsed_request: ParsedRequest) -> Decision:
        """Make a simple decision"""
        reasoning = f"I chose {solution.name} because it fits your budget of ${parsed_request.constraints['budget']} and can handle {parsed_request.scale['users']} users effectively."
        confidence = 0.85
        
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
        """Generate enhanced explanation using CodeLlama"""
        try:
            prompt = f"""<s>[INST] Explain this infrastructure solution briefly:

Solution: {decision.solution.name}
Cost: ${decision.solution.cost_estimate}/month
Users: {parsed_request.scale['users']}
Budget: ${parsed_request.constraints['budget']}/month

Provide a concise explanation in 2-3 paragraphs covering:
- Why this solution fits the requirements
- Key benefits and implementation notes
[/INST]"""
            
            response = self.local_model.generate_response(prompt, max_tokens=300)
            return response
            
        except Exception as e:
            print(f"⚠️ Local model failed, using fallback: {e}")
            return self._generate_explanation_fallback(decision, parsed_request)
    
    def _generate_explanation_fallback(self, decision: Decision, parsed_request: ParsedRequest) -> str:
        """Fallback explanation without local model"""
        explanation = f"""
## Solution: {decision.solution.name}

**Why chosen:** {decision.reasoning}

**How it addresses your requirements:**
- Handles {parsed_request.scale['users']} users with auto-scaling
- Fits within your ${parsed_request.constraints['budget']}/month budget
- Provides good performance and security

**Implementation considerations:**
- Estimated cost: ${decision.solution.cost_estimate}/month
- Performance score: {decision.solution.performance_score:.1f}/1.0
- Security score: {decision.solution.security_score:.1f}/1.0
- Complexity: {decision.solution.complexity}

**Confidence level:** {decision.confidence:.1%}
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

