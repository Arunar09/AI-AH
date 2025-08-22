#!/usr/bin/env python3
"""
Agent Capability Test Suite
===========================

This script thoroughly tests the base agent capabilities and saves factual results.
Each test run is versioned and documented with real performance data.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.example_docker_plugin import DockerPlugin


class AgentCapabilityTester:
    """Comprehensive agent capability testing with result versioning"""
    
    def __init__(self):
        self.version = "1.2.0"  # Updated for enhanced conversation patterns  # Increment version for enhanced testing
        self.test_date = datetime.now().isoformat()
        self.results = {
            "version": self.version,
            "test_date": self.test_date,
            "agent_info": {},
            "test_categories": {},
            "overall_performance": {},
            "detailed_results": [],
            "test_scaling": {
                "current_level": "20_tests",
                "next_target": "50_tests",
                "scaling_logic": "20→50→75→100 tests per category when 100% achieved"
            }
        }
    
    def run_complete_test_suite(self):
        """Run all capability tests and save results"""
        print(f"🧪 Agent Capability Test Suite v{self.version}")
        print(f"📅 Test Date: {self.test_date}")
        print("=" * 60)
        
        # Initialize agent
        print("\n1️⃣ Initializing Base Agent...")
        agent = BaseAgent("CapabilityTestAgent")
        
        # Add Docker plugin for testing
        docker_config = {
            'name': 'Docker Test Plugin',
            'version': '1.0.0',
            'description': 'Docker plugin for testing',
            'keywords': ['docker', 'container', 'dockerfile'],
            'confidence_threshold': 0.4  # Lowered for better plugin activation
        }
        docker_plugin = DockerPlugin(docker_config)
        agent.register_plugin(docker_plugin)
        
        # Get agent info
        self.results["agent_info"] = agent.get_agent_info()
        
        # Start test session
        session_id = agent.start_session("capability_test_user")
        
        # Run test categories
        print("\n2️⃣ Running Capability Tests...")
        
        test_categories = [
            ("Basic Conversation", self._test_basic_conversation),
            ("Intent Classification", self._test_intent_classification),
            ("Plugin Integration", self._test_plugin_integration),
            ("Memory & Context", self._test_memory_context),
            ("Response Quality", self._test_response_quality),
            ("Error Handling", self._test_error_handling),
            ("Performance", self._test_performance)
        ]
        
        for category_name, test_function in test_categories:
            print(f"\n🔍 Testing: {category_name}")
            category_results = test_function(agent, session_id)
            self.results["test_categories"][category_name] = category_results
            self._print_category_summary(category_name, category_results)
        
        # Calculate overall performance
        self._calculate_overall_performance()
        
        # Save results
        self._save_results()
        
        # Print final summary
        self._print_final_summary()
    
    def _test_basic_conversation(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test basic conversation capabilities - 20 comprehensive tests"""
        test_cases = [
            # Greeting variations (8 tests)
            {"query": "Hello!", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Basic greeting"},
            {"query": "Hi there", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Casual greeting"},
            {"query": "Hey", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Informal greeting"},
            {"query": "Good morning", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Time-specific greeting"},
            {"query": "Good afternoon", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Afternoon greeting"},
            {"query": "Greetings", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Formal greeting"},
            {"query": "Hi there, how are you?", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Extended greeting"},
            {"query": "Hello, nice to meet you", "expected_intent": "greeting", "min_confidence": 0.4, "description": "Polite greeting"},
            
            # Capability inquiries (8 tests)
            {"query": "What can you do?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Direct capability question"},
            {"query": "What can you help me with?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Help capability inquiry"},
            {"query": "What are your features?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Feature inquiry"},
            {"query": "What are your capabilities?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Capabilities question"},
            {"query": "Can you help me?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Help availability question"},
            {"query": "Are you able to assist?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Assistance capability"},
            {"query": "Do you support technical questions?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Technical support inquiry"},
            {"query": "What kind of support do you provide?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Support type inquiry"},
            
            # Mixed conversation tests (4 tests)
            {"query": "Hi, what can you do?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Combined greeting+capability"},
            {"query": "Hello, are you working?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Greeting+status check"},
            {"query": "Hey there, can you help?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Casual greeting+help"},
            {"query": "Good morning, what features do you have?", "expected_intent": "capability_inquiry", "min_confidence": 0.4, "description": "Formal greeting+features"}
        ]
        
        return self._run_test_cases(agent, session_id, test_cases, "Basic Conversation")
    
    def _test_intent_classification(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test intent classification accuracy - 20 comprehensive tests"""
        test_cases = [
            # Information requests (5 tests)
            {"query": "What is Docker?", "expected_intent": "information_request", "min_confidence": 0.3, "description": "What is question"},
            {"query": "Explain containerization", "expected_intent": "information_request", "min_confidence": 0.3, "description": "Explain request"},
            {"query": "Describe Kubernetes", "expected_intent": "information_request", "min_confidence": 0.3, "description": "Describe request"},
            {"query": "Tell me about cloud computing", "expected_intent": "information_request", "min_confidence": 0.3, "description": "Tell me request"},
            {"query": "Show me how this works", "expected_intent": "information_request", "min_confidence": 0.3, "description": "Show me request"},
            
            # Command requests (5 tests)
            {"query": "How do I install Docker?", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Installation command"},
            {"query": "Create a new container", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Create command"},
            {"query": "Build an image", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Build command"},
            {"query": "Run a deployment", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Run command"},
            {"query": "Configure the settings", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Configure command"},
            
            # Troubleshooting requests (5 tests)
            {"query": "I have an error with my setup", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Error report"},
            {"query": "My container is not working", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Not working issue"},
            {"query": "Fix this problem", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Fix request"},
            {"query": "Debug the deployment", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Debug request"},
            {"query": "Resolve connection issues", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Resolve request"},
            
            # Mixed intent tests (5 tests)
            {"query": "How does this work and why?", "expected_intent": "information_request", "min_confidence": 0.3, "description": "How+why question"},
            {"query": "Install and configure Docker", "expected_intent": "command_request", "min_confidence": 0.3, "description": "Multi-step command"},
            {"query": "What's wrong with my installation?", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "What's wrong question"},
            {"query": "Help me understand this error", "expected_intent": "troubleshooting", "min_confidence": 0.3, "description": "Understanding error"},
            {"query": "Explain and then show me how", "expected_intent": "information_request", "min_confidence": 0.3, "description": "Explain then show"}
        ]
        
        return self._run_test_cases(agent, session_id, test_cases, "Intent Classification")
    
    def _test_plugin_integration(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test plugin system integration - 20 comprehensive tests"""
        test_cases = [
            # Docker-specific queries that should activate plugin (10 tests)
            {"query": "What is Docker?", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Docker definition"},
            {"query": "How do I run a Docker container?", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Docker run command"},
            {"query": "Explain containerization", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.4, "description": "Containerization concept"},
            {"query": "Docker installation guide", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Docker installation"},
            {"query": "Create a Dockerfile", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Dockerfile creation"},
            {"query": "Docker build command", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Docker build"},
            {"query": "Container troubleshooting", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.4, "description": "Container issues"},
            {"query": "Docker image management", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Image management"},
            {"query": "Container networking", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.4, "description": "Docker networking"},
            {"query": "Docker volumes explained", "expected_plugins": ["Docker Test Plugin"], "min_confidence": 0.5, "description": "Docker volumes"},
            
            # Non-Docker queries that should NOT activate plugin (10 tests)
            {"query": "Hello world", "expected_plugins": [], "min_confidence": 0.3, "description": "Basic greeting"},
            {"query": "What can you do?", "expected_plugins": [], "min_confidence": 0.3, "description": "Capability inquiry"},
            {"query": "Explain machine learning", "expected_plugins": [], "min_confidence": 0.3, "description": "ML topic"},
            {"query": "How does networking work?", "expected_plugins": [], "min_confidence": 0.3, "description": "General networking"},
            {"query": "Python programming help", "expected_plugins": [], "min_confidence": 0.3, "description": "Python help"},
            {"query": "Database design principles", "expected_plugins": [], "min_confidence": 0.3, "description": "Database design"},
            {"query": "Cloud computing overview", "expected_plugins": [], "min_confidence": 0.3, "description": "Cloud overview"},
            {"query": "Software architecture", "expected_plugins": [], "min_confidence": 0.3, "description": "Architecture"},
            {"query": "Good morning", "expected_plugins": [], "min_confidence": 0.3, "description": "Morning greeting"},
            {"query": "Help me understand APIs", "expected_plugins": [], "min_confidence": 0.3, "description": "API help"}
        ]
        
        results = []
        passed = 0
        
        for test_case in test_cases:
            try:
                start_time = time.time()
                response = agent.process_query(test_case["query"], session_id)
                response_time = (time.time() - start_time) * 1000
                
                # Check plugin usage
                plugins_used = response.plugins_used
                expected_plugins = test_case.get("expected_plugins", [])
                
                plugin_check = (
                    (len(expected_plugins) == 0 and len(plugins_used) == 0) or
                    (len(expected_plugins) > 0 and any(plugin in plugins_used for plugin in expected_plugins))
                )
                
                confidence_check = response.confidence >= test_case["min_confidence"]
                success = response.success and plugin_check and confidence_check
                
                if success:
                    passed += 1
                
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": success,
                    "response": response.response[:100] + "..." if len(response.response) > 100 else response.response,
                    "confidence": response.confidence,
                    "plugins_used": plugins_used,
                    "expected_plugins": expected_plugins,
                    "plugin_check_passed": plugin_check,
                    "confidence_check_passed": confidence_check,
                    "response_time_ms": round(response_time, 2),
                    "intent": response.intent
                }
                
                results.append(result)
                
            except Exception as e:
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": False,
                    "error": str(e),
                    "response_time_ms": 0
                }
                results.append(result)
        
        return {
            "passed": passed,
            "total": len(test_cases),
            "success_rate": (passed / len(test_cases)) * 100,
            "results": results
        }
    
    def _test_memory_context(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test memory and context capabilities - 20 comprehensive tests"""
        # Establish varied context for testing
        context_setups = [
            ("I'm learning about containerization", "Specifically Docker containers"),
            ("I need help with cloud computing", "Particularly AWS services"),
            ("I'm working on a Python project", "Using Flask framework"),
            ("I'm setting up CI/CD", "With Jenkins and Docker"),
            ("I'm designing microservices", "For e-commerce platform")
        ]
        
        test_cases = []
        
        for i, (context1, context2) in enumerate(context_setups):
            # Set up context
            agent.process_query(context1, session_id)
            agent.process_query(context2, session_id)
            
            # Add context recall tests
            test_cases.extend([
                {
                    "query": "What were we discussing?",
                    "should_have_context": True,
                    "min_confidence": 0.3,
                    "description": f"Context recall test {i+1}"
                },
                {
                    "query": "Continue with that topic",
                    "should_have_context": True,
                    "min_confidence": 0.3,
                    "description": f"Context continuation test {i+1}"
                },
                {
                    "query": "Tell me more about that",
                    "should_have_context": True,
                    "min_confidence": 0.3,
                    "description": f"Context elaboration test {i+1}"
                },
                {
                    "query": "What did we talk about before?",
                    "should_have_context": True,
                    "min_confidence": 0.3,
                    "description": f"Previous context test {i+1}"
                }
            ])
        
        # Take only first 20 tests to maintain consistency
        test_cases = test_cases[:20]
        
        results = []
        passed = 0
        
        for test_case in test_cases:
            try:
                start_time = time.time()
                response = agent.process_query(test_case["query"], session_id)
                response_time = (time.time() - start_time) * 1000
                
                context_used = response.context_used
                confidence_check = response.confidence >= test_case["min_confidence"]
                context_check = context_used == test_case["should_have_context"]
                
                success = response.success and confidence_check and context_check
                
                if success:
                    passed += 1
                
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": success,
                    "response": response.response[:100] + "..." if len(response.response) > 100 else response.response,
                    "confidence": response.confidence,
                    "context_used": context_used,
                    "expected_context": test_case["should_have_context"],
                    "context_check_passed": context_check,
                    "confidence_check_passed": confidence_check,
                    "response_time_ms": round(response_time, 2)
                }
                
                results.append(result)
                
            except Exception as e:
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": False,
                    "error": str(e),
                    "response_time_ms": 0
                }
                results.append(result)
        
        return {
            "passed": passed,
            "total": len(test_cases),
            "success_rate": (passed / len(test_cases)) * 100,
            "results": results
        }
    
    def _test_response_quality(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test response quality metrics - 20 comprehensive tests"""
        test_cases = [
            # Basic response length tests (5 tests)
            {"query": "Hello", "min_length": 20, "max_length": 300, "description": "Greeting response length"},
            {"query": "Hi", "min_length": 15, "max_length": 300, "description": "Short greeting response"},
            {"query": "Good morning", "min_length": 20, "max_length": 300, "description": "Formal greeting response"},
            {"query": "Help", "min_length": 30, "max_length": 400, "description": "Help request response"},
            {"query": "Thanks", "min_length": 10, "max_length": 200, "description": "Acknowledgment response"},
            
            # Capability explanation tests (5 tests)
            {"query": "What can you do?", "min_length": 50, "max_length": 800, "description": "Capability explanation completeness"},
            {"query": "What are your features?", "min_length": 50, "max_length": 800, "description": "Feature explanation length"},
            {"query": "How can you help me?", "min_length": 40, "max_length": 600, "description": "Help explanation appropriateness"},
            {"query": "What services do you provide?", "min_length": 50, "max_length": 700, "description": "Service explanation detail"},
            {"query": "Tell me about your capabilities", "min_length": 60, "max_length": 900, "description": "Detailed capability response"},
            
            # Technical explanation tests (5 tests)
            {"query": "What is Docker?", "min_length": 100, "max_length": 1500, "description": "Technical explanation depth"},
            {"query": "Explain containerization", "min_length": 80, "max_length": 1200, "description": "Concept explanation thoroughness"},
            {"query": "How does cloud computing work?", "min_length": 100, "max_length": 1500, "description": "Complex topic explanation"},
            {"query": "What is Kubernetes?", "min_length": 80, "max_length": 1200, "description": "Technology explanation detail"},
            {"query": "Describe microservices", "min_length": 90, "max_length": 1300, "description": "Architecture explanation completeness"},
            
            # Error and edge case responses (5 tests)
            {"query": "Fix my computer", "min_length": 30, "max_length": 600, "description": "Vague request response appropriateness"},
            {"query": "Make it work", "min_length": 25, "max_length": 500, "description": "Unclear request response"},
            {"query": "I need help with something", "min_length": 40, "max_length": 600, "description": "General help request response"},
            {"query": "This is broken", "min_length": 35, "max_length": 500, "description": "Problem report response"},
            {"query": "Can you solve all my problems?", "min_length": 30, "max_length": 400, "description": "Unrealistic request response"}
        ]
        
        results = []
        passed = 0
        
        for test_case in test_cases:
            try:
                response = agent.process_query(test_case["query"], session_id)
                
                response_length = len(response.response)
                length_check = test_case["min_length"] <= response_length <= test_case["max_length"]
                has_suggestions = len(response.suggestions) > 0
                
                success = response.success and length_check
                
                if success:
                    passed += 1
                
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": success,
                    "response_length": response_length,
                    "min_length": test_case["min_length"],
                    "max_length": test_case["max_length"],
                    "length_check_passed": length_check,
                    "has_suggestions": has_suggestions,
                    "suggestion_count": len(response.suggestions),
                    "confidence": response.confidence
                }
                
                results.append(result)
                
            except Exception as e:
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": False,
                    "error": str(e)
                }
                results.append(result)
        
        return {
            "passed": passed,
            "total": len(test_cases),
            "success_rate": (passed / len(test_cases)) * 100,
            "results": results
        }
    
    def _test_error_handling(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test error handling capabilities - 20 comprehensive tests"""
        test_cases = [
            # Empty and minimal input tests (5 tests)
            {"query": "", "description": "Empty query handling"},
            {"query": " ", "description": "Space-only query handling"},
            {"query": "\n", "description": "Newline-only query handling"},
            {"query": "\t", "description": "Tab-only query handling"},
            {"query": "   \n  \t  ", "description": "Whitespace-only query handling"},
            
            # Nonsense and random input tests (5 tests)
            {"query": "xyzabc nonsense query 12345", "description": "Nonsense query handling"},
            {"query": "asldkfj qwerty uiop zxcvbn", "description": "Random keyboard input"},
            {"query": "123456789 !@#$%^&*()", "description": "Numbers and symbols"},
            {"query": "lorem ipsum dolor sit amet", "description": "Latin placeholder text"},
            {"query": "jfkdlsjfklds jfkdlsjf kdjfklds", "description": "Complete gibberish"},
            
            # Oversized input tests (5 tests)
            {"query": "?" * 1000, "description": "Very long query (1000 chars)"},
            {"query": "a" * 500, "description": "Long repeated character"},
            {"query": "This is a very long query that goes on and on and on. " * 20, "description": "Long repeated sentence"},
            {"query": "test " * 250, "description": "Long repeated word"},
            {"query": "How does this work? " * 50, "description": "Long repeated question"},
            
            # Special characters and edge cases (5 tests)
            {"query": "🚀🔥💯🎯⚡", "description": "Emoji-only query"},
            {"query": "SELECT * FROM users; DROP TABLE users;", "description": "SQL injection attempt"},
            {"query": "<script>alert('test')</script>", "description": "HTML/XSS attempt"},
            {"query": "../../../etc/passwd", "description": "Path traversal attempt"},
            {"query": "\\x00\\x01\\x02\\x03", "description": "Binary/control characters"}
        ]
        
        results = []
        passed = 0
        
        for test_case in test_cases:
            try:
                response = agent.process_query(test_case["query"], session_id)
                
                # Error handling success means we get a response without crashes
                success = response is not None and hasattr(response, 'success')
                
                if success:
                    passed += 1
                
                result = {
                    "query": test_case["query"][:50] + "..." if len(test_case["query"]) > 50 else test_case["query"],
                    "description": test_case["description"],
                    "success": success,
                    "response_received": response is not None,
                    "graceful_handling": success
                }
                
                results.append(result)
                
            except Exception as e:
                result = {
                    "query": test_case["query"][:50] + "..." if len(test_case["query"]) > 50 else test_case["query"],
                    "description": test_case["description"],
                    "success": False,
                    "error": str(e),
                    "graceful_handling": False
                }
                results.append(result)
        
        return {
            "passed": passed,
            "total": len(test_cases),
            "success_rate": (passed / len(test_cases)) * 100,
            "results": results
        }
    
    def _test_performance(self, agent: BaseAgent, session_id: str) -> Dict[str, Any]:
        """Test performance metrics - 20 comprehensive performance tests"""
        test_queries = [
            # Short queries (5 tests)
            "Hello",
            "Hi",
            "Help",
            "Thanks",
            "Yes",
            
            # Medium queries (5 tests)
            "What can you do?",
            "How does this work?",
            "Explain Docker basics",
            "Install new software",
            "Fix connection issues",
            
            # Long queries (5 tests)
            "Can you help me understand how containerization works in modern software development?",
            "What are the best practices for setting up a production Docker environment with security considerations?",
            "How do I troubleshoot network connectivity issues between multiple Docker containers in a complex deployment?",
            "Explain the differences between Docker, Kubernetes, and other container orchestration platforms in detail",
            "What steps should I follow to migrate from a monolithic application to a microservices architecture using containers?",
            
            # Technical queries (5 tests)
            "Docker run -p 8080:80 nginx",
            "kubectl get pods --all-namespaces",
            "terraform apply -var-file=production.tfvars",
            "aws ec2 describe-instances --region us-east-1",
            "docker-compose up -d --scale web=3"
        ]
        
        response_times = []
        confidences = []
        successful_responses = 0
        response_lengths = []
        memory_usage = []
        
        for i, query in enumerate(test_queries):
            try:
                # Get memory stats before
                memory_before = self._get_memory_stats(agent)
                
                start_time = time.time()
                response = agent.process_query(query, session_id)
                response_time = (time.time() - start_time) * 1000
                
                # Get memory stats after
                memory_after = self._get_memory_stats(agent)
                memory_used = memory_after - memory_before
                
                response_times.append(response_time)
                confidences.append(response.confidence)
                response_lengths.append(len(response.response))
                memory_usage.append(memory_used)
                
                if response.success:
                    successful_responses += 1
                    
            except Exception as e:
                response_times.append(0)
                confidences.append(0)
                response_lengths.append(0)
                memory_usage.append(0)
        
        # Calculate performance metrics
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        avg_response_length = sum(response_lengths) / len(response_lengths) if response_lengths else 0
        
        # Performance categorization
        fast_responses = sum(1 for rt in response_times if rt < 200)
        medium_responses = sum(1 for rt in response_times if 200 <= rt < 1000)
        slow_responses = sum(1 for rt in response_times if rt >= 1000)
        
        return {
            "total_queries": len(test_queries),
            "successful_responses": successful_responses,
            "success_rate": (successful_responses / len(test_queries)) * 100,
            "average_response_time_ms": round(avg_response_time, 2),
            "average_confidence": round(avg_confidence, 3),
            "average_response_length": round(avg_response_length, 1),
            "min_response_time_ms": round(min(response_times), 2) if response_times else 0,
            "max_response_time_ms": round(max(response_times), 2) if response_times else 0,
            "performance_breakdown": {
                "fast_responses_under_200ms": fast_responses,
                "medium_responses_200_1000ms": medium_responses,
                "slow_responses_over_1000ms": slow_responses
            },
            "response_times": [round(rt, 2) for rt in response_times],
            "confidences": [round(c, 3) for c in confidences],
            "response_lengths": response_lengths,
            "memory_efficiency": {
                "average_memory_per_query": round(sum(memory_usage) / len(memory_usage), 2) if memory_usage else 0,
                "max_memory_usage": max(memory_usage) if memory_usage else 0
            }
        }
    
    def _get_memory_stats(self, agent: BaseAgent) -> int:
        """Get basic memory statistics"""
        try:
            # Simple memory tracking - count interactions in memory
            memory_stats = agent.memory.get_memory_stats()
            return memory_stats.get('total_interactions', 0)
        except:
            return 0
    
    def _run_test_cases(self, agent: BaseAgent, session_id: str, test_cases: List[Dict], category_name: str) -> Dict[str, Any]:
        """Generic test case runner"""
        results = []
        passed = 0
        
        for test_case in test_cases:
            try:
                start_time = time.time()
                response = agent.process_query(test_case["query"], session_id)
                response_time = (time.time() - start_time) * 1000
                
                # Check intent if specified
                intent_check = True
                if "expected_intent" in test_case:
                    intent_check = response.intent == test_case["expected_intent"]
                
                # Check confidence
                confidence_check = response.confidence >= test_case["min_confidence"]
                
                success = response.success and intent_check and confidence_check
                
                if success:
                    passed += 1
                
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": success,
                    "response": response.response[:100] + "..." if len(response.response) > 100 else response.response,
                    "confidence": response.confidence,
                    "intent": response.intent,
                    "expected_intent": test_case.get("expected_intent", "N/A"),
                    "intent_check_passed": intent_check,
                    "confidence_check_passed": confidence_check,
                    "response_time_ms": round(response_time, 2)
                }
                
                results.append(result)
                
            except Exception as e:
                result = {
                    "query": test_case["query"],
                    "description": test_case["description"],
                    "success": False,
                    "error": str(e),
                    "response_time_ms": 0
                }
                results.append(result)
        
        return {
            "passed": passed,
            "total": len(test_cases),
            "success_rate": (passed / len(test_cases)) * 100,
            "results": results
        }
    
    def _calculate_overall_performance(self):
        """Calculate overall performance metrics"""
        total_tests = 0
        total_passed = 0
        
        for category, results in self.results["test_categories"].items():
            if "passed" in results and "total" in results:
                total_tests += results["total"]
                total_passed += results["passed"]
        
        overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        self.results["overall_performance"] = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "overall_success_rate": round(overall_success_rate, 2),
            "agent_version": self.results["agent_info"]["version"],
            "capabilities_tested": list(self.results["test_categories"].keys())
        }
    
    def _print_category_summary(self, category_name: str, results: Dict[str, Any]):
        """Print summary for a test category"""
        if "passed" in results and "total" in results:
            success_rate = results["success_rate"]
            print(f"   📊 {results['passed']}/{results['total']} tests passed ({success_rate:.1f}%)")
        else:
            print(f"   📊 Performance metrics recorded")
    
    def _print_final_summary(self):
        """Print final test summary with scaling recommendations"""
        print("\n" + "=" * 60)
        print("🏁 FINAL TEST SUMMARY")
        print("=" * 60)
        
        overall = self.results["overall_performance"]
        print(f"📊 Overall Success Rate: {overall['overall_success_rate']}%")
        print(f"📊 Total Tests: {overall['total_passed']}/{overall['total_tests']}")
        print(f"🤖 Agent Version: {overall['agent_version']}")
        
        print(f"\n📈 Category Breakdown:")
        categories_at_100 = []
        categories_needing_work = []
        
        for category, results in self.results["test_categories"].items():
            if "success_rate" in results:
                success_rate = results['success_rate']
                print(f"   • {category}: {success_rate:.1f}%")
                
                if success_rate >= 100.0:
                    categories_at_100.append(category)
                elif success_rate < 80.0:
                    categories_needing_work.append(category)
        
        performance = self.results["test_categories"].get("Performance", {})
        if performance:
            print(f"\n⚡ Performance Metrics:")
            print(f"   • Avg Response Time: {performance['average_response_time_ms']}ms")
            print(f"   • Avg Confidence: {performance['average_confidence']}")
            if "performance_breakdown" in performance:
                breakdown = performance["performance_breakdown"]
                print(f"   • Fast Responses (<200ms): {breakdown['fast_responses_under_200ms']}")
                print(f"   • Medium Responses (200-1000ms): {breakdown['medium_responses_200_1000ms']}")
                print(f"   • Slow Responses (>1000ms): {breakdown['slow_responses_over_1000ms']}")
        
        # Scaling recommendations
        print(f"\n🎯 SCALING RECOMMENDATIONS:")
        
        if categories_at_100:
            print(f"✅ Ready for 50-test scaling: {', '.join(categories_at_100)}")
            
        if categories_needing_work:
            print(f"🔧 Need improvement before scaling: {', '.join(categories_needing_work)}")
            
        # Overall scaling decision
        if overall['overall_success_rate'] >= 100.0:
            next_level = "50 tests per category"
            print(f"🚀 NEXT PHASE: Scale to {next_level}")
        elif overall['overall_success_rate'] >= 90.0:
            next_level = "Fix remaining issues, then scale to 50 tests"
            print(f"🎯 NEXT PHASE: {next_level}")
        else:
            next_level = "Fix critical issues before scaling"
            print(f"⚠️ NEXT PHASE: {next_level}")
            
        self.results["scaling_recommendation"] = {
            "current_test_count": 20,
            "categories_at_100_percent": categories_at_100,
            "categories_needing_work": categories_needing_work,
            "next_phase": next_level,
            "ready_for_scaling": len(categories_at_100) >= 3
        }
        
        print(f"\n💾 Results saved to: agent_test_results_v{self.version}.json")
    
    def _save_results(self):
        """Save test results to versioned file"""
        filename = f"agent_test_results_v{self.version}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Test results saved to: {filename}")


if __name__ == "__main__":
    tester = AgentCapabilityTester()
    tester.run_complete_test_suite()
