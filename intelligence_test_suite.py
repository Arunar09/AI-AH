#!/usr/bin/env python3
"""
AI-AH Platform Intelligence Test Suite

This comprehensive test suite evaluates the platform's intelligence capabilities,
reasoning quality, and knowledge curation effectiveness.
"""

import asyncio
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
import time

class IntelligenceTestSuite:
    """Comprehensive intelligence testing framework."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
        self.start_time = datetime.now()
    
    async def run_comprehensive_tests(self):
        """Run all intelligence tests and generate report."""
        print("🧠 AI-AH Platform Intelligence Test Suite")
        print("=" * 60)
        
        # Test Categories
        test_categories = [
            ("Knowledge Curation", self.test_knowledge_curation),
            ("Pattern Matching", self.test_pattern_matching),
            ("Response Quality", self.test_response_quality),
            ("Reasoning Capabilities", self.test_reasoning_capabilities),
            ("Context Awareness", self.test_context_awareness),
            ("Learning Potential", self.test_learning_potential),
            ("Creativity Assessment", self.test_creativity),
            ("Error Handling", self.test_error_handling)
        ]
        
        for category_name, test_function in test_categories:
            print(f"\n🔍 Testing {category_name}...")
            try:
                results = await test_function()
                self.test_results[category_name] = results
                self.print_category_results(category_name, results)
            except Exception as e:
                print(f"❌ Error in {category_name}: {str(e)}")
                self.test_results[category_name] = {"error": str(e)}
        
        # Generate comprehensive report
        self.generate_intelligence_report()
    
    async def test_knowledge_curation(self) -> Dict[str, Any]:
        """Test knowledge base quality and coverage."""
        test_queries = [
            "explain about ansible",
            "what is terraform",
            "how does kubernetes work",
            "tell me about aws services",
            "explain docker containers",
            "what is monitoring",
            "security best practices",
            "ci/cd pipeline setup"
        ]
        
        results = {
            "total_queries": len(test_queries),
            "successful_responses": 0,
            "comprehensive_responses": 0,
            "generic_responses": 0,
            "response_quality_scores": [],
            "knowledge_coverage": {},
            "average_confidence": 0
        }
        
        confidence_scores = []
        
        for query in test_queries:
            try:
                response = await self.make_request(query)
                if response:
                    results["successful_responses"] += 1
                    
                    # Analyze response quality
                    quality_score = self.analyze_response_quality(response)
                    results["response_quality_scores"].append(quality_score)
                    
                    # Check for comprehensive vs generic responses
                    if self.is_comprehensive_response(response):
                        results["comprehensive_responses"] += 1
                    else:
                        results["generic_responses"] += 1
                    
                    # Track confidence
                    confidence = response.get("confidence", 0)
                    confidence_scores.append(confidence)
                    
                    # Analyze knowledge coverage
                    technology = self.extract_technology(query)
                    if technology:
                        results["knowledge_coverage"][technology] = quality_score
                
            except Exception as e:
                print(f"  ⚠️ Error testing query '{query}': {str(e)}")
        
        results["average_confidence"] = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        results["average_quality"] = sum(results["response_quality_scores"]) / len(results["response_quality_scores"]) if results["response_quality_scores"] else 0
        
        return results
    
    async def test_pattern_matching(self) -> Dict[str, Any]:
        """Test pattern matching accuracy and specificity."""
        test_cases = [
            ("explain ansible", "ansible"),
            ("what is terraform", "terraform"),
            ("kubernetes deployment", "kubernetes"),
            ("aws services", "aws"),
            ("docker containers", "docker"),
            ("monitoring setup", "monitoring"),
            ("security hardening", "security"),
            ("ci/cd pipeline", "cicd")
        ]
        
        results = {
            "total_tests": len(test_cases),
            "correct_matches": 0,
            "incorrect_matches": 0,
            "ambiguous_matches": 0,
            "match_accuracy": 0,
            "specificity_scores": []
        }
        
        for query, expected_technology in test_cases:
            try:
                response = await self.make_request(query)
                if response:
                    # Analyze pattern matching
                    matched_technology = self.extract_technology_from_response(response)
                    specificity = self.measure_specificity(response)
                    results["specificity_scores"].append(specificity)
                    
                    if matched_technology == expected_technology:
                        results["correct_matches"] += 1
                    elif matched_technology is None:
                        results["ambiguous_matches"] += 1
                    else:
                        results["incorrect_matches"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing pattern '{query}': {str(e)}")
        
        results["match_accuracy"] = results["correct_matches"] / results["total_tests"] if results["total_tests"] > 0 else 0
        results["average_specificity"] = sum(results["specificity_scores"]) / len(results["specificity_scores"]) if results["specificity_scores"] else 0
        
        return results
    
    async def test_response_quality(self) -> Dict[str, Any]:
        """Test response quality, clarity, and completeness."""
        quality_tests = [
            {
                "query": "explain ansible playbooks",
                "expected_elements": ["yaml", "tasks", "handlers", "roles", "variables"],
                "complexity": "detailed"
            },
            {
                "query": "terraform best practices",
                "expected_elements": ["state", "modules", "variables", "security"],
                "complexity": "comprehensive"
            },
            {
                "query": "kubernetes security",
                "expected_elements": ["rbac", "network", "policies", "secrets"],
                "complexity": "specific"
            }
        ]
        
        results = {
            "total_tests": len(quality_tests),
            "high_quality_responses": 0,
            "medium_quality_responses": 0,
            "low_quality_responses": 0,
            "completeness_scores": [],
            "clarity_scores": [],
            "technical_accuracy": []
        }
        
        for test in quality_tests:
            try:
                response = await self.make_request(test["query"])
                if response:
                    # Analyze completeness
                    completeness = self.measure_completeness(response, test["expected_elements"])
                    results["completeness_scores"].append(completeness)
                    
                    # Analyze clarity
                    clarity = self.measure_clarity(response)
                    results["clarity_scores"].append(clarity)
                    
                    # Analyze technical accuracy
                    accuracy = self.measure_technical_accuracy(response, test["query"])
                    results["technical_accuracy"].append(accuracy)
                    
                    # Overall quality assessment
                    overall_quality = (completeness + clarity + accuracy) / 3
                    if overall_quality >= 0.8:
                        results["high_quality_responses"] += 1
                    elif overall_quality >= 0.6:
                        results["medium_quality_responses"] += 1
                    else:
                        results["low_quality_responses"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing quality for '{test['query']}': {str(e)}")
        
        return results
    
    async def test_reasoning_capabilities(self) -> Dict[str, Any]:
        """Test reasoning depth and logical consistency."""
        reasoning_tests = [
            {
                "query": "why should I use terraform over manual infrastructure setup",
                "expected_reasoning": ["consistency", "versioning", "automation", "scalability"],
                "reasoning_type": "comparative"
            },
            {
                "query": "what happens if I don't implement monitoring",
                "expected_reasoning": ["blindness", "reactive", "downtime", "performance"],
                "reasoning_type": "causal"
            },
            {
                "query": "how do I choose between aws and azure",
                "expected_reasoning": ["requirements", "cost", "features", "ecosystem"],
                "reasoning_type": "decision_making"
            }
        ]
        
        results = {
            "total_tests": len(reasoning_tests),
            "deep_reasoning": 0,
            "shallow_reasoning": 0,
            "no_reasoning": 0,
            "reasoning_depth_scores": [],
            "logical_consistency": []
        }
        
        for test in reasoning_tests:
            try:
                response = await self.make_request(test["query"])
                if response:
                    # Analyze reasoning depth
                    depth = self.measure_reasoning_depth(response, test["expected_reasoning"])
                    results["reasoning_depth_scores"].append(depth)
                    
                    # Analyze logical consistency
                    consistency = self.measure_logical_consistency(response)
                    results["logical_consistency"].append(consistency)
                    
                    if depth >= 0.7:
                        results["deep_reasoning"] += 1
                    elif depth >= 0.4:
                        results["shallow_reasoning"] += 1
                    else:
                        results["no_reasoning"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing reasoning for '{test['query']}': {str(e)}")
        
        return results
    
    async def test_context_awareness(self) -> Dict[str, Any]:
        """Test context retention and awareness."""
        context_tests = [
            {
                "conversation": [
                    "I'm working on a web application",
                    "What database should I use?",
                    "What about caching?"
                ],
                "expected_context": ["web application", "database", "caching"]
            },
            {
                "conversation": [
                    "I need to deploy to production",
                    "What about security?",
                    "How do I monitor it?"
                ],
                "expected_context": ["production", "security", "monitoring"]
            }
        ]
        
        results = {
            "total_conversations": len(context_tests),
            "context_retention": 0,
            "context_awareness": 0,
            "context_scores": []
        }
        
        for test in context_tests:
            try:
                context_score = 0
                for i, message in enumerate(test["conversation"]):
                    response = await self.make_request(message)
                    if response:
                        # Check if response shows awareness of previous context
                        awareness = self.measure_context_awareness(response, test["expected_context"][:i+1])
                        context_score += awareness
                
                results["context_scores"].append(context_score / len(test["conversation"]))
                
                if context_score / len(test["conversation"]) >= 0.7:
                    results["context_retention"] += 1
                if context_score / len(test["conversation"]) >= 0.5:
                    results["context_awareness"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing context: {str(e)}")
        
        return results
    
    async def test_learning_potential(self) -> Dict[str, Any]:
        """Test potential for learning and adaptation."""
        # This tests the system's ability to handle new information
        learning_tests = [
            "I have a custom deployment tool called 'DeployBot'",
            "My company uses a proprietary monitoring system",
            "We have specific compliance requirements for healthcare"
        ]
        
        results = {
            "total_tests": len(learning_tests),
            "adaptation_capability": 0,
            "knowledge_integration": 0,
            "learning_scores": []
        }
        
        for test in learning_tests:
            try:
                response = await self.make_request(test)
                if response:
                    # Measure how well the system adapts to new information
                    adaptation = self.measure_adaptation(response, test)
                    results["learning_scores"].append(adaptation)
                    
                    if adaptation >= 0.6:
                        results["adaptation_capability"] += 1
                    if adaptation >= 0.4:
                        results["knowledge_integration"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing learning: {str(e)}")
        
        return results
    
    async def test_creativity(self) -> Dict[str, Any]:
        """Test creative problem-solving capabilities."""
        creativity_tests = [
            "design a cost-effective multi-region architecture",
            "create a disaster recovery plan for a startup",
            "innovative approach to zero-downtime deployments"
        ]
        
        results = {
            "total_tests": len(creativity_tests),
            "creative_responses": 0,
            "standard_responses": 0,
            "creative_scores": []
        }
        
        for test in creativity_tests:
            try:
                response = await self.make_request(test)
                if response:
                    creativity = self.measure_creativity(response)
                    results["creative_scores"].append(creativity)
                    
                    if creativity >= 0.7:
                        results["creative_responses"] += 1
                    else:
                        results["standard_responses"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing creativity: {str(e)}")
        
        return results
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and edge cases."""
        error_tests = [
            "explain quantum computing infrastructure",
            "how to deploy to mars",
            "best practices for time travel in devops",
            "",  # Empty query
            "asdfghjkl",  # Nonsensical query
        ]
        
        results = {
            "total_tests": len(error_tests),
            "graceful_handling": 0,
            "error_responses": 0,
            "fallback_quality": []
        }
        
        for test in error_tests:
            try:
                response = await self.make_request(test)
                if response:
                    # Check if response handles the error gracefully
                    graceful = self.measure_graceful_handling(response, test)
                    results["fallback_quality"].append(graceful)
                    
                    if graceful >= 0.6:
                        results["graceful_handling"] += 1
                    else:
                        results["error_responses"] += 1
                
            except Exception as e:
                print(f"  ⚠️ Error testing error handling: {str(e)}")
        
        return results
    
    # Helper methods for analysis
    async def make_request(self, query: str) -> Dict[str, Any]:
        """Make a request to the AI-AH platform."""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/agents/conversation",
                json={
                    "message": query,
                    "user_id": "test_user",
                    "context": {}
                },
                timeout=15
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"    Request failed: {str(e)}")
            return None
    
    def analyze_response_quality(self, response: Dict[str, Any]) -> float:
        """Analyze the quality of a response."""
        content = response.get("response", "")
        confidence = response.get("confidence", 0)
        
        # Quality factors
        length_score = min(len(content) / 500, 1.0)  # Prefer longer responses
        confidence_score = confidence
        structure_score = 1.0 if "##" in content else 0.5  # Prefer structured responses
        
        return (length_score + confidence_score + structure_score) / 3
    
    def is_comprehensive_response(self, response: Dict[str, Any]) -> bool:
        """Check if response is comprehensive vs generic."""
        content = response.get("response", "")
        
        # Comprehensive indicators
        comprehensive_indicators = [
            "Core Components", "Best Practices", "Recommendations",
            "1)", "2)", "3)", "•", "##"
        ]
        
        # Generic indicators
        generic_indicators = [
            "I'm still here", "What would you like to work on",
            "I can help you with", "Quick Actions"
        ]
        
        comprehensive_count = sum(1 for indicator in comprehensive_indicators if indicator in content)
        generic_count = sum(1 for indicator in generic_indicators if indicator in content)
        
        return comprehensive_count > generic_count
    
    def extract_technology(self, query: str) -> str:
        """Extract technology from query."""
        technologies = ["ansible", "terraform", "kubernetes", "aws", "azure", "gcp", "docker", "monitoring", "security", "cicd"]
        query_lower = query.lower()
        for tech in technologies:
            if tech in query_lower:
                return tech
        return None
    
    def extract_technology_from_response(self, response: Dict[str, Any]) -> str:
        """Extract technology from response metadata."""
        metadata = response.get("metadata", {})
        return metadata.get("technology", None)
    
    def measure_specificity(self, response: Dict[str, Any]) -> float:
        """Measure response specificity."""
        content = response.get("response", "")
        
        # Specificity indicators
        specific_terms = [
            "Core Components", "Modules", "Variables", "Handlers",
            "Providers", "Resources", "State Management", "Pods",
            "Services", "Deployments", "ConfigMaps", "Secrets"
        ]
        
        specific_count = sum(1 for term in specific_terms if term in content)
        return min(specific_count / 5, 1.0)  # Normalize to 0-1
    
    def measure_completeness(self, response: Dict[str, Any], expected_elements: List[str]) -> float:
        """Measure response completeness against expected elements."""
        content = response.get("response", "").lower()
        found_elements = sum(1 for element in expected_elements if element.lower() in content)
        return found_elements / len(expected_elements)
    
    def measure_clarity(self, response: Dict[str, Any]) -> float:
        """Measure response clarity."""
        content = response.get("response", "")
        
        # Clarity indicators
        clarity_indicators = [
            "##", "•", "1)", "2)", "3)", "Best Practices", "Recommendations"
        ]
        
        clarity_score = sum(1 for indicator in clarity_indicators if indicator in content)
        return min(clarity_score / 3, 1.0)
    
    def measure_technical_accuracy(self, response: Dict[str, Any], query: str) -> float:
        """Measure technical accuracy (simplified)."""
        content = response.get("response", "")
        
        # Technical accuracy indicators
        technical_terms = [
            "infrastructure", "deployment", "configuration", "automation",
            "scalability", "security", "monitoring", "best practices"
        ]
        
        technical_count = sum(1 for term in technical_terms if term in content)
        return min(technical_count / 4, 1.0)
    
    def measure_reasoning_depth(self, response: Dict[str, Any], expected_reasoning: List[str]) -> float:
        """Measure reasoning depth."""
        content = response.get("response", "").lower()
        found_reasoning = sum(1 for reason in expected_reasoning if reason.lower() in content)
        return found_reasoning / len(expected_reasoning)
    
    def measure_logical_consistency(self, response: Dict[str, Any]) -> float:
        """Measure logical consistency."""
        content = response.get("response", "")
        
        # Consistency indicators
        consistency_indicators = [
            "because", "therefore", "as a result", "consequently",
            "however", "alternatively", "in addition", "furthermore"
        ]
        
        consistency_count = sum(1 for indicator in consistency_indicators if indicator in content)
        return min(consistency_count / 2, 1.0)
    
    def measure_context_awareness(self, response: Dict[str, Any], context: List[str]) -> float:
        """Measure context awareness."""
        content = response.get("response", "").lower()
        context_mentions = sum(1 for ctx in context if ctx.lower() in content)
        return context_mentions / len(context) if context else 0
    
    def measure_adaptation(self, response: Dict[str, Any], new_info: str) -> float:
        """Measure adaptation to new information."""
        content = response.get("response", "")
        
        # Adaptation indicators
        adaptation_indicators = [
            "custom", "specific", "your", "tailored", "adapted",
            "considering", "based on", "according to"
        ]
        
        adaptation_count = sum(1 for indicator in adaptation_indicators if indicator in content)
        return min(adaptation_count / 3, 1.0)
    
    def measure_creativity(self, response: Dict[str, Any]) -> float:
        """Measure creative problem-solving."""
        content = response.get("response", "")
        
        # Creativity indicators
        creativity_indicators = [
            "innovative", "creative", "novel", "unique", "alternative",
            "different approach", "new way", "unconventional"
        ]
        
        creativity_count = sum(1 for indicator in creativity_indicators if indicator in content)
        return min(creativity_count / 2, 1.0)
    
    def measure_graceful_handling(self, response: Dict[str, Any], query: str) -> float:
        """Measure graceful error handling."""
        content = response.get("response", "")
        
        # Graceful handling indicators
        graceful_indicators = [
            "I understand", "Let me help", "I can assist", "I'd be happy to",
            "I'm not sure", "I don't have specific information", "I can provide general guidance"
        ]
        
        graceful_count = sum(1 for indicator in graceful_indicators if indicator in content)
        return min(graceful_count / 2, 1.0)
    
    def print_category_results(self, category: str, results: Dict[str, Any]):
        """Print results for a test category."""
        if "error" in results:
            print(f"  ❌ {category}: {results['error']}")
            return
        
        # Print key metrics
        for key, value in results.items():
            if isinstance(value, (int, float)) and not key.endswith("_scores"):
                print(f"  📊 {key}: {value}")
    
    def generate_intelligence_report(self):
        """Generate comprehensive intelligence report."""
        print("\n" + "=" * 60)
        print("🧠 COMPREHENSIVE INTELLIGENCE ASSESSMENT REPORT")
        print("=" * 60)
        
        total_tests = sum(len(results) for results in self.test_results.values() if isinstance(results, dict) and "error" not in results)
        successful_tests = sum(1 for results in self.test_results.values() if isinstance(results, dict) and "error" not in results)
        
        print(f"\n📈 Overall Performance:")
        print(f"  • Test Categories: {len(self.test_results)}")
        print(f"  • Successful Categories: {successful_tests}")
        print(f"  • Success Rate: {(successful_tests/len(self.test_results)*100):.1f}%")
        
        # Calculate overall intelligence score
        intelligence_scores = []
        for category, results in self.test_results.items():
            if isinstance(results, dict) and "error" not in results:
                # Calculate category score based on key metrics
                category_score = self.calculate_category_score(category, results)
                intelligence_scores.append(category_score)
                print(f"\n🎯 {category}: {category_score:.1f}/10")
        
        overall_score = sum(intelligence_scores) / len(intelligence_scores) if intelligence_scores else 0
        print(f"\n🏆 Overall Intelligence Score: {overall_score:.1f}/10")
        
        # Intelligence level assessment
        if overall_score >= 8.0:
            level = "Advanced Intelligence"
        elif overall_score >= 6.0:
            level = "Intermediate Intelligence"
        elif overall_score >= 4.0:
            level = "Basic Intelligence"
        else:
            level = "Limited Intelligence"
        
        print(f"🎖️ Intelligence Level: {level}")
        
        # Recommendations
        print(f"\n💡 Key Recommendations:")
        if overall_score < 6.0:
            print("  • Implement semantic similarity for better pattern matching")
            print("  • Add conversation context awareness")
            print("  • Enhance reasoning depth and logical consistency")
        if overall_score < 8.0:
            print("  • Add learning mechanisms for continuous improvement")
            print("  • Implement knowledge graphs for better relationships")
            print("  • Develop creative problem-solving capabilities")
        
        print(f"\n⏱️ Test Duration: {datetime.now() - self.start_time}")
        print("=" * 60)
    
    def calculate_category_score(self, category: str, results: Dict[str, Any]) -> float:
        """Calculate intelligence score for a category."""
        if category == "Knowledge Curation":
            return (results.get("average_quality", 0) * 5 + 
                   results.get("average_confidence", 0) * 5)
        elif category == "Pattern Matching":
            return (results.get("match_accuracy", 0) * 5 + 
                   results.get("average_specificity", 0) * 5)
        elif category == "Response Quality":
            avg_completeness = sum(results.get("completeness_scores", [0])) / max(len(results.get("completeness_scores", [1])), 1)
            avg_clarity = sum(results.get("clarity_scores", [0])) / max(len(results.get("clarity_scores", [1])), 1)
            avg_accuracy = sum(results.get("technical_accuracy", [0])) / max(len(results.get("technical_accuracy", [1])), 1)
            return (avg_completeness + avg_clarity + avg_accuracy) * 3.33
        elif category == "Reasoning Capabilities":
            avg_depth = sum(results.get("reasoning_depth_scores", [0])) / max(len(results.get("reasoning_depth_scores", [1])), 1)
            avg_consistency = sum(results.get("logical_consistency", [0])) / max(len(results.get("logical_consistency", [1])), 1)
            return (avg_depth + avg_consistency) * 5
        elif category == "Context Awareness":
            avg_context = sum(results.get("context_scores", [0])) / max(len(results.get("context_scores", [1])), 1)
            return avg_context * 10
        elif category == "Learning Potential":
            avg_learning = sum(results.get("learning_scores", [0])) / max(len(results.get("learning_scores", [1])), 1)
            return avg_learning * 10
        elif category == "Creativity Assessment":
            avg_creativity = sum(results.get("creative_scores", [0])) / max(len(results.get("creative_scores", [1])), 1)
            return avg_creativity * 10
        elif category == "Error Handling":
            avg_graceful = sum(results.get("fallback_quality", [0])) / max(len(results.get("fallback_quality", [1])), 1)
            return avg_graceful * 10
        
        return 5.0  # Default score


async def main():
    """Run the intelligence test suite."""
    test_suite = IntelligenceTestSuite()
    await test_suite.run_comprehensive_tests()


if __name__ == "__main__":
    asyncio.run(main())
