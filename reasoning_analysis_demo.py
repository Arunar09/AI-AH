#!/usr/bin/env python3
"""
AI-AH Platform Reasoning Analysis Demo

This script demonstrates the current reasoning capabilities and limitations
of the AI-AH platform through detailed analysis of specific queries.
"""

import requests
import json
from typing import Dict, List, Any
import time

class ReasoningAnalyzer:
    """Analyzes reasoning capabilities of the AI-AH platform."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def analyze_reasoning_quality(self):
        """Analyze reasoning quality through specific test cases."""
        print("🧠 AI-AH Platform Reasoning Analysis")
        print("=" * 60)
        
        # Test cases designed to reveal reasoning capabilities
        test_cases = [
            {
                "name": "Comparative Reasoning",
                "query": "why should I use terraform over manual infrastructure setup",
                "expected_reasoning": [
                    "consistency", "versioning", "automation", "scalability",
                    "reproducibility", "collaboration", "error reduction"
                ],
                "reasoning_type": "comparative"
            },
            {
                "name": "Causal Reasoning",
                "query": "what happens if I don't implement monitoring in production",
                "expected_reasoning": [
                    "blindness", "reactive", "downtime", "performance issues",
                    "security risks", "cost overruns", "customer impact"
                ],
                "reasoning_type": "causal"
            },
            {
                "name": "Decision Making",
                "query": "how do I choose between aws and azure for my startup",
                "expected_reasoning": [
                    "requirements", "cost", "features", "ecosystem",
                    "support", "compliance", "team expertise"
                ],
                "reasoning_type": "decision_making"
            },
            {
                "name": "Problem Solving",
                "query": "my application is slow, what could be causing this",
                "expected_reasoning": [
                    "database", "network", "code", "infrastructure",
                    "caching", "load", "configuration"
                ],
                "reasoning_type": "problem_solving"
            },
            {
                "name": "Strategic Planning",
                "query": "how should I plan my infrastructure for a growing startup",
                "expected_reasoning": [
                    "scalability", "cost optimization", "reliability",
                    "security", "monitoring", "disaster recovery"
                ],
                "reasoning_type": "strategic"
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            print(f"\n🔍 Testing {test_case['name']} ({test_case['reasoning_type']})")
            print(f"Query: '{test_case['query']}'")
            
            try:
                response = self.make_request(test_case['query'])
                if response:
                    analysis = self.analyze_response_reasoning(
                        response, 
                        test_case['expected_reasoning'],
                        test_case['reasoning_type']
                    )
                    results.append({
                        'test_case': test_case,
                        'analysis': analysis
                    })
                    self.print_reasoning_analysis(analysis)
                else:
                    print("  ❌ No response received")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
        
        # Generate reasoning summary
        self.generate_reasoning_summary(results)
    
    def make_request(self, query: str) -> Dict[str, Any]:
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
    
    def analyze_response_reasoning(self, response: Dict[str, Any], expected_reasoning: List[str], reasoning_type: str) -> Dict[str, Any]:
        """Analyze the reasoning quality of a response."""
        content = response.get("response", "")
        confidence = response.get("confidence", 0)
        
        analysis = {
            "reasoning_type": reasoning_type,
            "confidence": confidence,
            "content_length": len(content),
            "reasoning_depth": 0,
            "logical_structure": 0,
            "expected_coverage": 0,
            "reasoning_indicators": [],
            "missing_reasoning": [],
            "reasoning_quality": "poor"
        }
        
        # Analyze reasoning depth
        analysis["reasoning_depth"] = self.measure_reasoning_depth(content, expected_reasoning)
        
        # Analyze logical structure
        analysis["logical_structure"] = self.measure_logical_structure(content)
        
        # Analyze expected reasoning coverage
        analysis["expected_coverage"] = self.measure_expected_coverage(content, expected_reasoning)
        
        # Find reasoning indicators
        analysis["reasoning_indicators"] = self.find_reasoning_indicators(content)
        
        # Find missing reasoning elements
        analysis["missing_reasoning"] = self.find_missing_reasoning(content, expected_reasoning)
        
        # Determine overall reasoning quality
        analysis["reasoning_quality"] = self.determine_reasoning_quality(analysis)
        
        return analysis
    
    def measure_reasoning_depth(self, content: str, expected_reasoning: List[str]) -> float:
        """Measure the depth of reasoning in the response."""
        content_lower = content.lower()
        
        # Count how many expected reasoning elements are present
        found_elements = sum(1 for element in expected_reasoning if element.lower() in content_lower)
        coverage = found_elements / len(expected_reasoning)
        
        # Look for reasoning depth indicators
        depth_indicators = [
            "because", "therefore", "as a result", "consequently",
            "however", "alternatively", "in addition", "furthermore",
            "specifically", "for example", "in particular", "moreover"
        ]
        
        depth_count = sum(1 for indicator in depth_indicators if indicator in content_lower)
        depth_score = min(depth_count / 3, 1.0)  # Normalize to 0-1
        
        return (coverage + depth_score) / 2
    
    def measure_logical_structure(self, content: str) -> float:
        """Measure the logical structure of the response."""
        structure_indicators = [
            "##", "•", "1)", "2)", "3)", "first", "second", "third",
            "step", "phase", "stage", "process", "workflow"
        ]
        
        structure_count = sum(1 for indicator in structure_indicators if indicator in content)
        return min(structure_count / 5, 1.0)
    
    def measure_expected_coverage(self, content: str, expected_reasoning: List[str]) -> float:
        """Measure how well the response covers expected reasoning elements."""
        content_lower = content.lower()
        found_elements = sum(1 for element in expected_reasoning if element.lower() in content_lower)
        return found_elements / len(expected_reasoning)
    
    def find_reasoning_indicators(self, content: str) -> List[str]:
        """Find reasoning indicators in the response."""
        reasoning_indicators = [
            "because", "therefore", "as a result", "consequently",
            "however", "alternatively", "in addition", "furthermore",
            "specifically", "for example", "in particular", "moreover",
            "due to", "caused by", "leads to", "results in"
        ]
        
        found_indicators = []
        content_lower = content.lower()
        for indicator in reasoning_indicators:
            if indicator in content_lower:
                found_indicators.append(indicator)
        
        return found_indicators
    
    def find_missing_reasoning(self, content: str, expected_reasoning: List[str]) -> List[str]:
        """Find missing reasoning elements."""
        content_lower = content.lower()
        missing = []
        for element in expected_reasoning:
            if element.lower() not in content_lower:
                missing.append(element)
        return missing
    
    def determine_reasoning_quality(self, analysis: Dict[str, Any]) -> str:
        """Determine overall reasoning quality."""
        depth = analysis["reasoning_depth"]
        structure = analysis["logical_structure"]
        coverage = analysis["expected_coverage"]
        
        overall_score = (depth + structure + coverage) / 3
        
        if overall_score >= 0.8:
            return "excellent"
        elif overall_score >= 0.6:
            return "good"
        elif overall_score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def print_reasoning_analysis(self, analysis: Dict[str, Any]):
        """Print detailed reasoning analysis."""
        print(f"  📊 Confidence: {analysis['confidence']:.2f}")
        print(f"  📊 Content Length: {analysis['content_length']} characters")
        print(f"  📊 Reasoning Depth: {analysis['reasoning_depth']:.2f}")
        print(f"  📊 Logical Structure: {analysis['logical_structure']:.2f}")
        print(f"  📊 Expected Coverage: {analysis['expected_coverage']:.2f}")
        print(f"  📊 Reasoning Quality: {analysis['reasoning_quality'].upper()}")
        
        if analysis['reasoning_indicators']:
            print(f"  🔍 Reasoning Indicators: {', '.join(analysis['reasoning_indicators'])}")
        else:
            print(f"  🔍 Reasoning Indicators: None found")
        
        if analysis['missing_reasoning']:
            print(f"  ❌ Missing Reasoning: {', '.join(analysis['missing_reasoning'])}")
        else:
            print(f"  ✅ All Expected Reasoning Present")
    
    def generate_reasoning_summary(self, results: List[Dict[str, Any]]):
        """Generate a summary of reasoning capabilities."""
        print("\n" + "=" * 60)
        print("🧠 REASONING CAPABILITIES SUMMARY")
        print("=" * 60)
        
        if not results:
            print("❌ No test results available")
            return
        
        # Calculate overall metrics
        total_tests = len(results)
        excellent_reasoning = sum(1 for r in results if r['analysis']['reasoning_quality'] == 'excellent')
        good_reasoning = sum(1 for r in results if r['analysis']['reasoning_quality'] == 'good')
        fair_reasoning = sum(1 for r in results if r['analysis']['reasoning_quality'] == 'fair')
        poor_reasoning = sum(1 for r in results if r['analysis']['reasoning_quality'] == 'poor')
        
        avg_depth = sum(r['analysis']['reasoning_depth'] for r in results) / total_tests
        avg_structure = sum(r['analysis']['logical_structure'] for r in results) / total_tests
        avg_coverage = sum(r['analysis']['expected_coverage'] for r in results) / total_tests
        
        print(f"\n📈 Overall Reasoning Performance:")
        print(f"  • Total Tests: {total_tests}")
        print(f"  • Excellent Reasoning: {excellent_reasoning} ({excellent_reasoning/total_tests*100:.1f}%)")
        print(f"  • Good Reasoning: {good_reasoning} ({good_reasoning/total_tests*100:.1f}%)")
        print(f"  • Fair Reasoning: {fair_reasoning} ({fair_reasoning/total_tests*100:.1f}%)")
        print(f"  • Poor Reasoning: {poor_reasoning} ({poor_reasoning/total_tests*100:.1f}%)")
        
        print(f"\n📊 Average Scores:")
        print(f"  • Reasoning Depth: {avg_depth:.2f}/1.0")
        print(f"  • Logical Structure: {avg_structure:.2f}/1.0")
        print(f"  • Expected Coverage: {avg_coverage:.2f}/1.0")
        
        overall_score = (avg_depth + avg_structure + avg_coverage) / 3
        print(f"  • Overall Reasoning Score: {overall_score:.2f}/1.0")
        
        # Reasoning level assessment
        if overall_score >= 0.8:
            level = "Advanced Reasoning"
        elif overall_score >= 0.6:
            level = "Intermediate Reasoning"
        elif overall_score >= 0.4:
            level = "Basic Reasoning"
        else:
            level = "Limited Reasoning"
        
        print(f"\n🎖️ Reasoning Level: {level}")
        
        # Detailed analysis by reasoning type
        print(f"\n🔍 Analysis by Reasoning Type:")
        reasoning_types = {}
        for result in results:
            reasoning_type = result['analysis']['reasoning_type']
            if reasoning_type not in reasoning_types:
                reasoning_types[reasoning_type] = []
            reasoning_types[reasoning_type].append(result['analysis'])
        
        for reasoning_type, analyses in reasoning_types.items():
            avg_score = sum(a['reasoning_depth'] for a in analyses) / len(analyses)
            print(f"  • {reasoning_type.replace('_', ' ').title()}: {avg_score:.2f}/1.0")
        
        # Key findings
        print(f"\n💡 Key Findings:")
        if overall_score < 0.4:
            print("  ❌ Limited reasoning capabilities - responses lack logical structure")
            print("  ❌ Missing causal relationships and comparative analysis")
            print("  ❌ No evidence of deep thinking or problem-solving")
        elif overall_score < 0.6:
            print("  ⚠️ Basic reasoning present but limited depth")
            print("  ⚠️ Some logical structure but missing key reasoning elements")
            print("  ⚠️ Limited ability to draw conclusions or make comparisons")
        else:
            print("  ✅ Good reasoning capabilities demonstrated")
            print("  ✅ Logical structure and reasoning indicators present")
            print("  ✅ Ability to cover expected reasoning elements")
        
        # Recommendations
        print(f"\n🚀 Recommendations for Improvement:")
        if overall_score < 0.4:
            print("  • Implement causal reasoning mechanisms")
            print("  • Add comparative analysis capabilities")
            print("  • Develop logical structure templates")
            print("  • Create reasoning chains for complex queries")
        elif overall_score < 0.6:
            print("  • Enhance reasoning depth with more detailed analysis")
            print("  • Add missing reasoning elements to knowledge base")
            print("  • Improve logical flow and structure")
            print("  • Implement reasoning validation mechanisms")
        else:
            print("  • Continue to refine reasoning quality")
            print("  • Add more sophisticated reasoning patterns")
            print("  • Implement reasoning learning from user feedback")
            print("  • Develop advanced reasoning capabilities")
        
        print("=" * 60)


def main():
    """Run the reasoning analysis."""
    analyzer = ReasoningAnalyzer()
    analyzer.analyze_reasoning_quality()


if __name__ == "__main__":
    main()
