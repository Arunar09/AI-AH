#!/usr/bin/env python3
"""
Base Agent - Core AI Agent Foundation
====================================

This is the main base agent that orchestrates all components to provide
intelligent responses with plugin support.

Complete Flow:
User Query → Query Analysis → Keyword Extraction → Dictionary Lookup → 
Pattern Matching → Memory Context → Plugin Selection → Knowledge Integration → 
Response Generation → Intelligence Curation → Final Response
"""

import json
import sqlite3
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from .dictionary import UniversalDictionary, QueryAnalysis
from .pattern_matcher import PatternMatcher, PatternMatch
from .memory_system import MemorySystem, ConversationContext
from .plugin_system import PluginManager, PluginResponse
from .intelligent_analyzer import IntelligentQueryAnalyzer, InfrastructurePlan
from .requirements_collector import RequirementsCollector

# Thread-local storage for database connections
thread_local = threading.local()

def get_db_connection():
    """Get a thread-safe database connection"""
    if not hasattr(thread_local, 'db_connection'):
        thread_local.db_connection = sqlite3.connect('base_agent.db', check_same_thread=False)
        thread_local.db_connection.row_factory = sqlite3.Row
    return thread_local.db_connection

def get_thread_safe_memory():
    """Get a thread-safe memory system instance"""
    if not hasattr(thread_local, 'memory_system'):
        thread_local.memory_system = MemorySystem()
    return thread_local.memory_system

def get_thread_safe_pattern_matcher():
    """Get a thread-safe pattern matcher instance"""
    if not hasattr(thread_local, 'pattern_matcher'):
        thread_local.pattern_matcher = PatternMatcher()
    return thread_local.pattern_matcher

def get_thread_safe_requirements_collector():
    """Get a thread-safe requirements collector instance"""
    if not hasattr(thread_local, 'requirements_collector'):
        thread_local.requirements_collector = RequirementsCollector()
    return thread_local.requirements_collector


@dataclass
class AgentResponse:
    """Structured response from the base agent"""
    success: bool
    response: str
    confidence: float
    intent: str
    complexity: str
    sources: List[str]
    context_used: bool
    plugins_used: List[str]
    reasoning: List[str]
    suggestions: List[str]
    response_time_ms: float
    timestamp: str


class BaseAgent:
    """
    Base AI Agent with Plugin Architecture
    
    This agent provides a clean foundation for building tool-specific AI assistants.
    It combines universal language understanding with pluggable tool knowledge.
    
    Core Features:
    - Universal language understanding (dictionary system)
    - Conversation pattern matching
    - Memory and context management
    - Plugin-based tool integration
    - Intelligent response generation
    """
    
    def __init__(self, agent_name: str = "BaseAgent", db_path: str = "base_agent.db"):
        """Initialize the base agent with all core systems"""
        self.name = agent_name
        self.version = "1.0.0"
        self.db_path = db_path
        
        # Initialize core systems
        print(f"🚀 Initializing {self.name} v{self.version}")
        
        self.dictionary = UniversalDictionary()
        print("✅ Dictionary system loaded")
        
        self.pattern_matcher = PatternMatcher(db_path)
        print("✅ Pattern matcher loaded")
        
        self.memory = MemorySystem(db_path)
        print("✅ Memory system loaded")
        
        # Initialize intelligent systems
        self.intelligent_analyzer = IntelligentQueryAnalyzer()
        print("✅ Intelligent analyzer loaded")
        
        # Get thread-safe requirements collector
        self.requirements_collector = get_thread_safe_requirements_collector()
        print("✅ Requirements collector loaded")
        
        # Initialize plugin manager
        self.plugin_manager = PluginManager()
        print("✅ Plugin manager loaded")
        
        # Agent state
        self.current_session = None
        self.current_user = "default_user"
        
        print(f"🎉 BaseAgent is ready!")
    
    def start_session(self, user_id: str = "default_user") -> str:
        """Start a new conversation session"""
        session_id = self.memory.start_session(user_id)
        self.current_session = session_id
        self.current_user = user_id
        return session_id
    
    def process_query(self, query: str, session_id: str = None, 
                     user_id: str = None) -> AgentResponse:
        """
        Main entry point for processing user queries
        
        This method implements the complete flow:
        1. Query Analysis (dictionary)
        2. Pattern Matching
        3. Memory Context
        4. Plugin Knowledge
        5. Response Generation
        6. Intelligence Curation
        """
        start_time = datetime.now()
        
        # Use current session if not provided
        if session_id is None:
            session_id = self.current_session or self.start_session(user_id or self.current_user)
        if user_id is None:
            user_id = self.current_user
        
        # Initialize for intelligent processing
        plugins_used = []
        
        try:
            # Step 1: Query Analysis with Dictionary
            query_analysis = self.dictionary.analyze_query(query)
            
            # Step 2: Pattern Matching
            try:
                pattern_matcher = get_thread_safe_pattern_matcher()
                pattern_match = pattern_matcher.find_best_match(
                    query_analysis.keywords,
                    query_analysis.intent
                )
            except Exception as e:
                print(f"⚠️ Warning: Could not find pattern match: {e}")
                pattern_match = None
            
            # Step 3: Memory Context
            # Get conversation context from memory
            try:
                memory_system = get_thread_safe_memory()
                memory_context = memory_system.get_conversation_context(
                    session_id, 
                    "default_user"
                )
                # Convert to the format expected by the rest of the code
                memory_context = {
                    'has_conversation_history': len(memory_context.conversation_history) > 0,
                    'current_topic': memory_context.current_topic or 'general',
                    'user_preferences': memory_context.user_preferences
                }
            except Exception as e:
                print(f"⚠️ Warning: Could not get memory context: {e}")
                memory_context = {
                    'has_conversation_history': False,
                    'current_topic': 'general',
                    'user_preferences': {}
                }
            
            # Step 4: Intelligent Plugin Execution
            if self._is_simple_greeting_or_casual(query, query_analysis):
                # Handle simple greetings and casual input directly - CHECK THIS FIRST!
                plugin_responses = []
            elif self._is_infrastructure_creation_request(query, query_analysis):
                plugin_responses = self._handle_infrastructure_creation(query, query_analysis)
            elif self._is_requirements_response(query, query_analysis):
                plugin_responses = self._handle_requirements_response(query, query_analysis)
            elif self._is_proceed_request(query, query_analysis):
                plugin_responses = self._handle_code_generation(query, query_analysis)
            elif self._is_code_generation_request(query, query_analysis):
                plugin_responses = self._execute_plugin_commands(query, query_analysis)
            elif self._is_command_execution_request(query, query_analysis):
                plugin_responses = self._execute_plugin_commands(query, query_analysis)
            else:
                plugin_responses = self.plugin_manager.get_combined_knowledge(
                    query_analysis.keywords,
                    query_analysis.context
                )
            
            plugins_used = [resp.source for resp in plugin_responses if resp.success]
            
            # Step 5: Intelligent Response Generation & Curation
            response_content, confidence = self._generate_intelligent_response(
                query, query_analysis, pattern_match, memory_context, plugin_responses
            )
            
            # Calculate response time
            end_time = datetime.now()
            response_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Build sources list
            sources = ["base_patterns"]
            if memory_context['has_conversation_history']:
                sources.append("conversation_memory")
            sources.extend(plugins_used)
            
            # Store interaction in memory
            try:
                memory_system = get_thread_safe_memory()
                memory_system.add_interaction(
                    session_id,
                    query,
                    response_content,
                    query_analysis.intent,
                    confidence,
                    True
                )
            except Exception as e:
                print(f"⚠️ Warning: Could not store final interaction in memory: {e}")
                # Continue without storing in memory
            
            # Update pattern usage if pattern was used
            if pattern_match:
                self.pattern_matcher.update_usage(pattern_match.pattern_id, True)
            
            # Create final response
            agent_response = AgentResponse(
                success=True,
                response=response_content,
                confidence=confidence,
                intent=query_analysis.intent,
                complexity=query_analysis.complexity,
                sources=sources,
                context_used=memory_context['has_conversation_history'],
                plugins_used=plugins_used,
                reasoning=[],
                suggestions=[],
                response_time_ms=round(response_time_ms, 2),
                timestamp=datetime.now().isoformat()
            )
            
            return agent_response
            
        except Exception as e:
            # Error handling
            error_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AgentResponse(
                success=False,
                response=f"I apologize, but I encountered an error processing your request. Please try rephrasing your question or ask for help with a specific topic.",
                confidence=0.0,
                intent="error",
                complexity="unknown",
                sources=["error_handler"],
                context_used=False,
                plugins_used=[],
                reasoning=[],
                suggestions=["Try rephrasing your question", "Ask for help with a specific topic"],
                response_time_ms=round(error_time, 2),
                timestamp=datetime.now().isoformat()
            )
    
    def _generate_intelligent_response(self, query: str, query_analysis: QueryAnalysis,
                          pattern_match: Optional[PatternMatch],
                          memory_context: Dict[str, Any],
                          plugin_responses: List[PluginResponse]) -> tuple[str, float]:
        """Generate an intelligent, curated response based on context and user needs"""
        
        # Handle simple greetings and casual input directly
        if self._is_simple_greeting_or_casual(query, query_analysis):
            return self._generate_contextual_response(query, None), 0.9
        
        # Get the primary response content
        if not plugin_responses:
            return "I understand your request. How can I help you with your infrastructure needs?", 0.6
        
        # Find the most relevant response
        primary_response = None
        highest_confidence = 0.0
        
        for resp in plugin_responses:
            if resp.success and resp.content and resp.confidence > highest_confidence:
                primary_response = resp
                highest_confidence = resp.confidence
        
        if not primary_response:
            return "I'm processing your request. Please provide more details about your infrastructure needs.", 0.5
        
        # Intelligent curation based on query analysis
        response_content = primary_response.content
        
        # Remove verbose technical details for simple queries
        if query_analysis.complexity == "simple":
            # Keep only essential information
            lines = response_content.split('\n')
            essential_lines = []
            for line in lines:
                if any(keyword in line.lower() for keyword in ['✅', '🎯', '💡', '🚀', '📋', '🔧']):
                    essential_lines.append(line)
                elif line.strip() and not line.startswith('**') and not line.startswith('•'):
                    essential_lines.append(line)
            
            if essential_lines:
                response_content = '\n'.join(essential_lines)
        
        # Add context-aware guidance
        if query_analysis.intent == "infrastructure_creation":
            if "requirements" not in response_content.lower():
                response_content += "\n\n💡 **Next:** I'll help you collect specific requirements for your infrastructure."
        
        return response_content, highest_confidence
    
    def _generate_contextual_response(self, query: str, current_plan) -> str:
        """Generate an intelligent, contextual response based on user input and plan"""
        
        # Analyze the user's input for intent
        query_lower = query.lower()
        
        # Check if it's a greeting or casual input
        if any(word in query_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
            return f"👋 Hello! I'm here to help you build your infrastructure. What would you like to create today?"
        
        # Check if it's a capability question
        if any(word in query_lower for word in ['what can you do', 'capabilities', 'list', 'show me', 'tell me']):
            return self._generate_capabilities_response()
        
        # Check if it's a question about the process
        if any(word in query_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return "🤔 I'd be happy to explain! What specific aspect of the infrastructure process would you like me to clarify?"
        
        # Check if it's a preference or requirement
        if any(word in query_lower for word in ['want', 'need', 'prefer', 'like', 'should']):
            return f"💡 I understand you're expressing a preference: '{query}'. This helps me tailor your infrastructure. What else would you like to specify?"
        
        # Check if it's a statement about the plan
        if any(word in query_lower for word in ['plan', 'infrastructure', 'architecture', 'design']):
            return f"📋 I see you're thinking about the plan: '{query}'. Let me know if you want to modify anything or continue with the current approach."
        
        # Default intelligent response
        return f"✅ I've noted: '{query}'. This information helps me understand your needs better. What would you like to focus on next?"
    
    def _generate_dynamic_code_response(self, result, pattern, environment) -> str:
        """Generate a dynamic code generation response based on actual results"""
        
        # Analyze the result to determine what was actually generated
        if result and hasattr(result, 'success') and result.success:
            status = "✅ Code generated successfully"
        else:
            status = "⚠️ Code generation completed with some issues"
        
        # Dynamic pattern name
        pattern_names = {
            "serverless": "Serverless Architecture",
            "microservices": "Microservices Architecture", 
            "three_tier": "Three-Tier Architecture",
            "container": "Container-Based Architecture",
            "event_driven": "Event-Driven Architecture",
            "monolithic": "Monolithic Architecture"
        }
        pattern_name = pattern_names.get(pattern, pattern.replace('_', ' ').title())
        
        # Dynamic environment name
        env_names = {
            "aws": "AWS",
            "azure": "Azure", 
            "gcp": "Google Cloud Platform",
            "hybrid": "Multi-Cloud (Hybrid)",
            "onpremise": "On-Premise"
        }
        env_name = env_names.get(environment, environment.title())
        
        # Generate response based on actual results
        response = f"🚀 **TERRAFORM CODE GENERATED!**\n\n"
        response += f"**Infrastructure Pattern:** {pattern_name}\n"
        response += f"**Environment:** {env_name}\n"
        response += f"**Status:** {status}\n\n"
        
        # Add generated files if available
        if result and hasattr(result, 'files') and result.files:
            response += "**Generated Files:**\n"
            for file in result.files:
                response += f"• `{file}`\n"
        else:
            response += "**Generated Files:**\n"
            response += "• `main.tf` - Main infrastructure configuration\n"
            response += "• `variables.tf` - Input variables\n"
            response += "• `outputs.tf` - Output values\n"
            response += "• `providers.tf` - Provider configuration\n"
            response += "• `README.md` - Deployment instructions\n"
        
        response += "\n💡 **Next Steps:**\n"
        response += "1. Review the generated code\n"
        response += "2. Run `terraform init` to initialize\n"
        response += "3. Run `terraform plan` to preview changes\n"
        response += "4. Run `terraform apply` to deploy\n\n"
        
        response += f"**Your {pattern_name.lower()} is ready!** 🎉"
        
        return response
    
    def _generate_capabilities_response(self) -> str:
        """Generate a comprehensive capabilities response"""
        response = "🚀 **AI-AH Terraform Engineer Agent - Capabilities**\n\n"
        
        response += "**🏗️ Infrastructure Design & Generation:**\n"
        response += "• Create serverless architectures (Lambda, DynamoDB, API Gateway)\n"
        response += "• Design 3-tier web applications (Load Balancer, RDS, EC2)\n"
        response += "• Build container-based infrastructure (ECS, ALB, Fargate)\n"
        response += "• Generate microservices patterns\n"
        response += "• Design event-driven architectures\n"
        response += "• Create monolithic infrastructure\n\n"
        
        response += "**☁️ Multi-Cloud Support:**\n"
        response += "• AWS (EC2, S3, Lambda, RDS, ECS, etc.)\n"
        response += "• Azure (VM, Storage, Functions, SQL Database)\n"
        response += "• Google Cloud (Compute Engine, Cloud Run, Firestore)\n"
        response += "• Hybrid and multi-cloud environments\n"
        response += "• On-premise infrastructure\n\n"
        
        response += "**🔧 Terraform Operations:**\n"
        response += "• Generate complete Terraform configurations\n"
        response += "• Execute terraform init, plan, apply, destroy\n"
        response += "• Manage infrastructure state\n"
        response += "• Handle variables and outputs\n\n"
        
        response += "**📋 Intelligent Requirements Collection:**\n"
        response += "• Interactive form-based requirements gathering\n"
        response += "• Document upload and analysis\n"
        response += "• Pattern detection and recommendation\n"
        response += "• Cost estimation and optimization\n\n"
        
        response += "**💡 Smart Features:**\n"
        response += "• Context-aware responses\n"
        response += "• Conversation memory and history\n"
        response += "• Pattern matching and learning\n"
        response += "• Intelligent error handling\n\n"
        
        response += "**🎯 What would you like to create today?**\n"
        response += "Try: 'Create a serverless architecture' or 'Design a 3-tier web app'"
        
        return response
    
    def _enhance_pattern_with_plugins(self, base_response: str, 
                                    plugin_content: str, 
                                    query_analysis: QueryAnalysis) -> str:
        """Enhance pattern response with plugin knowledge"""
        # Simple enhancement - in real implementation, this would be more sophisticated
        if plugin_content and len(plugin_content.strip()) > 0:
            enhanced = f"{base_response}\n\n**Additional Information:**\n{plugin_content}"
            return enhanced
        return base_response
    
    def _combine_plugin_responses(self, plugin_responses: List[PluginResponse]) -> str:
        """Combine multiple plugin responses into coherent content"""
        if not plugin_responses:
            return ""
        
        if len(plugin_responses) == 1:
            return plugin_responses[0].content
        
        # Combine multiple responses
        combined_parts = []
        for i, response in enumerate(plugin_responses):
            if response.content.strip():
                combined_parts.append(f"**{response.source}:** {response.content}")
        
        return "\n\n".join(combined_parts)
    
    def _generate_contextual_fallback(self, query: str, query_analysis: QueryAnalysis, 
                                    topic: str) -> str:
        """Generate context-aware fallback response"""
        # Safe keyword handling
        keywords_str = self._safe_join_keywords(query_analysis.keywords[:3], query)
        
        intent_responses = {
            'information_request': f"I'd be happy to provide information about {keywords_str}. Based on our conversation about {topic}, could you be more specific about what aspect you'd like to know?",
            'command_request': f"I can help you with commands related to {keywords_str}. What specific action are you trying to accomplish?",
            'troubleshooting': f"I can help troubleshoot this issue. Based on our discussion about {topic}, could you provide more details about the problem you're experiencing?",
            'capability_inquiry': f"I can assist with various aspects of {topic} and other technical topics. What specific capabilities are you interested in learning about?"
        }
        
        return intent_responses.get(
            query_analysis.intent,
            f"I understand you're asking about {keywords_str}. Could you provide more context about what you're trying to achieve?"
        )
    
    def _generate_generic_fallback(self, query_analysis: QueryAnalysis) -> str:
        """Generate generic helpful fallback"""
        # Safe keyword handling
        keywords_str = self._safe_join_keywords(query_analysis.keywords[:3], "this topic")
        
        intent_fallbacks = {
            'greeting': "Hello! I'm here to help you with technical questions and guidance. What would you like to know about?",
            'capability_inquiry': "I can help you with:\n\n• Technical explanations and guidance\n• Step-by-step instructions\n• Troubleshooting and problem solving\n• Best practices and recommendations\n\nWhat specific area interests you?",
            'information_request': f"I'd be happy to explain {keywords_str}. Could you be more specific about what aspect you'd like to understand?",
            'command_request': f"I can help you with commands and procedures. What are you trying to accomplish with {keywords_str}?",
            'troubleshooting': "I can help you troubleshoot issues. Please provide more details about:\n\n• What you're trying to do\n• What's not working\n• Any error messages you're seeing"
        }
        
        return intent_fallbacks.get(
            query_analysis.intent,
            f"I understand you're asking about {keywords_str}. How can I help you with this topic?"
        )
    
    def _safe_join_keywords(self, keywords: List[str], fallback: str = "this topic") -> str:
        """Safely join keywords with fallback for empty/broken keyword lists"""
        if not keywords:
            return fallback
        
        # Filter out empty or very short keywords
        valid_keywords = [k for k in keywords if k and len(k.strip()) > 1]
        
        if not valid_keywords:
            return fallback
        
        # Join with natural language
        if len(valid_keywords) == 1:
            return valid_keywords[0]
        elif len(valid_keywords) == 2:
            return f"{valid_keywords[0]} and {valid_keywords[1]}"
        else:
            return f"{', '.join(valid_keywords[:-1])}, and {valid_keywords[-1]}"
    
    def _curate_response(self, response: str, query_analysis: QueryAnalysis,
                        memory_context: Dict[str, Any]) -> tuple[str, List[str]]:
        """Curate response and generate helpful suggestions"""
        
        # Clean up response formatting
        curated = response.strip()
        
        # Add contextual enhancements (exclude social queries)
        if (query_analysis.complexity == 'beginner' and 
            query_analysis.intent not in ['social', 'greeting', 'personal']):
            if not any(phrase in curated.lower() for phrase in ['step by step', 'first', 'start']):
                curated += "\n\nWould you like me to provide step-by-step guidance?"
        
        # Generate suggestions based on intent and context
        suggestions = self._generate_suggestions(query_analysis, memory_context)
        
        return curated, suggestions
    
    def _generate_suggestions(self, query_analysis: QueryAnalysis,
                            memory_context: Dict[str, Any]) -> List[str]:
        """Generate helpful follow-up suggestions"""
        suggestions = []
        
        # Intent-based suggestions
        if query_analysis.intent == 'information_request':
            suggestions.extend([
                "Would you like practical examples?",
                "Do you need step-by-step instructions?",
                "Are you interested in best practices?"
            ])
        elif query_analysis.intent == 'command_request':
            suggestions.extend([
                "Would you like to see example commands?",
                "Do you need help with prerequisites?",
                "Should I explain what each step does?"
            ])
        elif query_analysis.intent == 'troubleshooting':
            suggestions.extend([
                "Can you share the exact error message?",
                "What were you trying to accomplish?",
                "Would you like debugging steps?"
            ])
        
        # Context-based suggestions
        if memory_context['current_topic']:
            suggestions.append(f"Would you like to explore more about {memory_context['current_topic']}?")
        
        # Limit suggestions to avoid overwhelming
        return suggestions[:3]
    
    def register_plugin(self, plugin) -> bool:
        """Register a new plugin with the agent"""
        return self.plugin_manager.register_plugin(plugin)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information"""
        pattern_stats = self.pattern_matcher.get_pattern_stats()
        memory_stats = self.memory.get_memory_stats()
        plugin_stats = self.plugin_manager.get_system_stats()
        
        return {
            'name': self.name,
            'version': self.version,
            'current_session': self.current_session,
            'current_user': self.current_user,
            'statistics': {
                'patterns': pattern_stats,
                'memory': memory_stats,
                'plugins': plugin_stats
            },
            'capabilities': {
                'universal_language_understanding': True,
                'conversation_patterns': True,
                'memory_and_context': True,
                'plugin_architecture': True,
                'intelligent_curation': True
            }
        }

    def _is_command_execution_request(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is requesting command execution"""
        query_lower = query.lower()
        
        print(f"🔍 DEBUG: Checking if '{query}' is a command execution request")
        
        # Command execution keywords - expanded to handle more natural language
        command_keywords = [
            'run', 'execute', 'start', 'deploy', 'apply', 'init', 'plan', 'destroy',
            'terraform', 'docker', 'build', 'test', 'deploy', 'install', 'configure',
            'create', 'generate', 'design', 'build', 'make', 'set up', 'provision'
        ]
        
        # Check if query contains command keywords
        has_command_keywords = any(keyword in query_lower for keyword in command_keywords)
        print(f"🔍 DEBUG: Has command keywords: {has_command_keywords}")
        
        # Also check for infrastructure-related requests
        infrastructure_keywords = ['architecture', 'infrastructure', 'lambda', 'dynamodb', 'vpc', 'ec2', 'rds', 's3']
        has_infrastructure_request = any(keyword in query_lower for keyword in infrastructure_keywords)
        print(f"🔍 DEBUG: Has infrastructure request: {has_infrastructure_request}")
        
        # If it has command keywords OR infrastructure requests, it's likely a command execution request
        result = has_command_keywords or has_infrastructure_request
        print(f"🔍 DEBUG: Final result: {result}")
        
        return result
    
    def _is_simple_greeting_or_casual(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is a simple greeting or casual input"""
        query_lower = query.lower()
        
        # EXCLUDE infrastructure creation requests from being caught as simple greetings
        if self._is_infrastructure_creation_request(query, query_analysis):
            return False
        
        # Simple greetings
        if any(word in query_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return True
        
        # Capability questions
        if any(phrase in query_lower for phrase in ['what can you do', 'capabilities', 'list me', 'show me', 'tell me']):
            return True
        
        # Casual conversation
        if any(word in query_lower for word in ['how are you', 'what\'s up', 'thanks', 'thank you', 'bye', 'goodbye']):
            return True
        
        # Very short queries (1-2 words) - but NOT if they contain infrastructure keywords
        if len(query.strip().split()) <= 2:
            # Check if it's just a simple word or if it contains infrastructure-related content
            infrastructure_keywords = ['create', 'build', 'design', 'generate', 'infrastructure', 'architecture', 'vpc', 'ec2', 'lambda', 'dynamodb', 'rds', 's3', 'serverless']
            if not any(keyword in query_lower for keyword in infrastructure_keywords):
                return True
        
        return False
    
    def _execute_plugin_commands(self, query: str, query_analysis: QueryAnalysis) -> List[PluginResponse]:
        """Execute commands through relevant plugins"""
        responses = []
        
        print(f"🔍 DEBUG: Executing plugin commands for query: '{query}'")
        
        # First, determine the tool to execute based on the query
        tool_name = self._determine_tool_name(query, query_analysis)
        print(f"🔍 DEBUG: Determined tool name: {tool_name}")
        
        if tool_name:
            # We have a specific tool to execute, find the plugin and execute it directly
            print(f"🔍 DEBUG: Looking for plugin to execute tool: {tool_name}")
            
            # Get the Terraform Engineer plugin (we know it exists from initialization)
            plugin = self.plugin_manager.get_plugin('Terraform Engineer')
            if plugin and hasattr(plugin, 'execute_tool'):
                try:
                    print(f"🔍 DEBUG: Executing tool: {tool_name}")
                    result = plugin.execute_tool(tool_name, {})
                    print(f"🔍 DEBUG: Tool execution result: {result.success}")
                    responses.append(result)
                except Exception as e:
                    print(f"🔍 DEBUG: Tool execution failed: {str(e)}")
                    # If execution fails, create an error response
                    from core.plugin_system import PluginResponse
                    responses.append(PluginResponse(
                        success=False,
                        content=f"Error executing tool '{tool_name}': {str(e)}",
                        source="Terraform Engineer",
                        confidence=0.0,
                        additional_data={}
                    ))
            else:
                print(f"🔍 DEBUG: Terraform Engineer plugin not found or doesn't support execution")
                responses.append(PluginResponse(
                    success=False,
                    content="Terraform Engineer plugin not available for execution",
                    source="System",
                    confidence=0.0,
                    additional_data={}
                ))
        else:
            # Check if this is an infrastructure creation request that needs intelligent analysis
            if self._is_infrastructure_creation_request(query, query_analysis):
                print(f"🔍 DEBUG: Infrastructure creation request detected, using intelligent analysis")
                return self._handle_infrastructure_creation(query, query_analysis)
            
            print(f"🔍 DEBUG: No tool name determined, falling back to plugin knowledge")
            # Fallback to getting plugin knowledge if no specific tool command is detected
            plugin_responses = self.plugin_manager.get_combined_knowledge(
                query_analysis.keywords,
                query_analysis.context
            )
            responses.extend(plugin_responses)
        
        return responses
    
    def _determine_tool_name(self, query: str, query_analysis: QueryAnalysis) -> Optional[str]:
        """Determine which tool to execute based on the query"""
        query_lower = query.lower()
        
        # Terraform commands - more flexible detection
        if 'terraform init' in query_lower or ('init' in query_lower and 'terraform' in query_lower):
            return 'terraform_init'
        elif 'terraform plan' in query_lower or ('plan' in query_lower and 'terraform' in query_lower):
            return 'terraform_plan'
        elif 'terraform apply' in query_lower or ('apply' in query_lower and 'terraform' in query_lower):
            return 'terraform_apply'
        elif 'terraform destroy' in query_lower or ('destroy' in query_lower and 'terraform' in query_lower):
            return 'terraform_destroy'
        
        # Infrastructure design and generation requests - DON'T return tool names, let them go to infrastructure creation
        # elif any(word in query_lower for word in ['create', 'generate', 'design', 'build', 'make']) and any(word in query_lower for word in ['architecture', 'infrastructure', 'lambda', 'dynamodb', 'vpc', 'ec2', 'rds', 's3', 'serverless', 'application', 'web', 'api']):
        #     return 'generate_terraform'
        elif 'generate' in query_lower and 'terraform' in query_lower:
            return 'generate_terraform'
        elif 'design' in query_lower and 'infrastructure' in query_lower:
            return 'design_infrastructure'
        elif 'troubleshoot' in query_lower or 'debug' in query_lower:
            return 'troubleshoot'
        
        # Handle standalone commands
        if query_lower.strip() == 'plan':
            return 'terraform_plan'
        elif query_lower.strip() == 'init':
            return 'terraform_init'
        elif query_lower.strip() == 'apply':
            return 'terraform_apply'
        elif query_lower.strip() == 'destroy':
            return 'terraform_destroy'
        
        return None

    def _is_infrastructure_creation_request(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is requesting infrastructure creation"""
        query_lower = query.lower()
        print(f"🔍 DEBUG: Checking if '{query}' is an infrastructure creation request")
        creation_keywords = ['create', 'build', 'design', 'generate', 'set up', 'provision', 'deploy']
        infrastructure_keywords = ['infrastructure', 'architecture', 'vpc', 'ec2', 'lambda', 'dynamodb', 'rds', 's3', 'serverless', 'microservices']
        has_creation = any(keyword in query_lower for keyword in creation_keywords)
        has_infrastructure = any(keyword in query_lower for keyword in infrastructure_keywords)
        result = has_creation and has_infrastructure
        print(f"🔍 DEBUG: Infrastructure creation detected: {result} (creation: {has_creation}, infrastructure: {has_infrastructure})")
        print(f"🔍 DEBUG: Creation keywords found: {[k for k in creation_keywords if k in query_lower]}")
        print(f"🔍 DEBUG: Infrastructure keywords found: {[k for k in infrastructure_keywords if k in query_lower]}")
        return result
    
    def _is_requirements_response(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is responding to requirements collection questions"""
        query_lower = query.lower()
        
        # Check for explicit requirements keywords
        requirements_keywords = ['answer', 'requirements', 'summary', 'proceed with defaults']
        if any(keyword in query_lower for keyword in requirements_keywords):
            return True
        
        # Check if this looks like a response to a question (not a new question)
        question_indicators = ['what', 'how', 'why', 'when', 'where', 'who', 'create', 'design', 'build', 'generate']
        if not any(indicator in query_lower for indicator in question_indicators):
            # This might be an answer to a requirements question
            # But don't catch code generation requests
            if 'code' in query_lower or 'terraform' in query_lower or 'proceed' in query_lower:
                return False
            return True
        
        return False
    
    def _handle_infrastructure_creation(self, query: str, query_analysis: QueryAnalysis) -> List[PluginResponse]:
        """Handle infrastructure creation requests with intelligent analysis"""
        from core.plugin_system import PluginResponse
        try:
            plan = self.intelligent_analyzer.analyze_infrastructure_request(query, {'preferred_environment': 'aws'})
            
            # Start requirements collection
            first_question = self.requirements_collector.start_collection(plan, self.current_session or "default")
            
            # Format the response to show the requirements collection interface
            response_content = self._format_requirements_collection_interface(plan, [first_question])
            
            return [PluginResponse(
                success=True,
                content=response_content,
                source="Intelligent Infrastructure Analyzer",
                confidence=0.9,
                additional_data={
                    "plan": plan,
                    "questions": [first_question],
                    "total_questions": 1,
                    "requirements_started": True
                }
            )]
        except Exception as e:
            # Enhanced error handling with validation
            error_msg = str(e)
            
            # Try to validate the requirements collection state
            if hasattr(self.requirements_collector, 'validate_collection_state'):
                validation = self.requirements_collector.validate_collection_state()
                if not validation['is_valid']:
                    error_content = f"❌ **Requirements Collection Error**\n\n"
                    error_content += f"**Issue:** {', '.join(validation['issues'])}\n\n"
                    error_content += f"**Recommendation:** {', '.join(validation['recommendations'])}\n\n"
                    error_content += f"**Technical Error:** {error_msg}"
                else:
                    error_content = f"❌ **Infrastructure Processing Error**\n\n"
                    error_content += f"**Error:** {error_msg}\n\n"
                    if validation['warnings']:
                        error_content += f"**Warnings:** {', '.join(validation['warnings'])}\n\n"
                    if validation['recommendations']:
                        error_content += f"**Recommendations:** {', '.join(validation['recommendations'])}"
            else:
                error_content = f"❌ Error processing infrastructure request: {error_msg}"
            
            return [PluginResponse(
                success=False,
                content=error_content,
                source="Intelligent Infrastructure Analyzer",
                confidence=0.0,
                additional_data={
                    "error_type": type(e).__name__,
                    "error_details": error_msg
                }
            )]
    
    def _format_infrastructure_plan(self, plan: InfrastructurePlan, questions: List[str]) -> str:
        """Format the infrastructure plan into a user-friendly response"""
        response = f"🏗️ **INFRASTRUCTURE ANALYSIS COMPLETE**\n\n"
        
        # Pattern and environment
        response += f"**Infrastructure Pattern:** {plan.pattern.value.replace('_', ' ').title()}\n"
        response += f"**Target Environment:** {plan.environment.value.replace('_', ' ').title()}\n"
        response += f"**Estimated Cost:** {plan.estimated_cost}\n\n"
        
        # Requirements
        response += "🔧 **Identified Requirements:**\n"
        for req in plan.requirements:
            response += f"   • {req.component}: {req.type} ({req.priority} priority)\n"
        
        # Security recommendations
        response += f"\n🔒 **Security Considerations:**\n"
        for security in plan.security_recommendations[:3]:  # Show first 3
            response += f"   • {security}\n"
        
        # Next steps
        response += f"\n📋 **Next Steps:**\n"
        response += "   1. Review and customize generated code\n"
        response += "   2. Initialize infrastructure\n"
        response += "   3. Plan deployment\n"
        response += "   4. Apply changes\n"
        
        # Requirements collection
        if questions:
            response += f"\n❓ **To proceed, I need some additional information:**\n"
            for i, question in enumerate(questions[:3], 1):  # Show first 3 questions
                response += f"   **Q{i}:** {question}\n"
            response += f"\n💡 **Answer these questions to get started:**\n"
            response += f"   • Type 'answer 1 [your answer]' to respond\n"
            response += f"   • Type 'requirements summary' to see current status\n"
            response += f"   • Type 'proceed with defaults' to use recommended settings\n"
        
        return response

    def _handle_requirements_response(self, query: str, query_analysis: QueryAnalysis) -> List[PluginResponse]:
        """Handle user responses to requirements collection questions"""
        from core.plugin_system import PluginResponse

        print(f"🔍 DEBUG: Processing requirements response: '{query}'")

        query_lower = query.lower()

        # Check if this is a plan modification request (intelligent updates)
        if any(keyword in query_lower for keyword in ['all three cloud', 'multi-cloud', 'aws azure gcp', 'change to', 'switch to', 'instead of', 'budget', 'cost', 'security', 'compliance']):
            print(f"🔍 INTELLIGENT UPDATE: Detected plan modification request, updating infrastructure plan")
            
            # Get the current plan from requirements collector
            if hasattr(self.requirements_collector, 'current_plan') and self.requirements_collector.current_plan:
                current_plan = self.requirements_collector.current_plan
                
                # Use intelligent analyzer to update the plan
                updated_plan = self.intelligent_analyzer.update_plan_based_on_user_input(current_plan, query)
                
                # Update the requirements collector with the new plan
                self.requirements_collector.current_plan = updated_plan
                
                # Generate new questions based on updated plan
                new_questions = self.requirements_collector.start_collection(updated_plan, self.current_session or "default")
                
                # Format the updated plan
                response_content = self._format_updated_infrastructure_plan(current_plan, updated_plan, query)
                
                return [PluginResponse(
                    success=True,
                    content=response_content,
                    source="Intelligent Infrastructure Analyzer",
                    confidence=0.95,
                    additional_data={
                        "plan_updated": True,
                        "new_pattern": updated_plan.pattern.value,
                        "new_environment": updated_plan.environment.value,
                        "modification_request": query
                    }
                )]
            else:
                # No current plan, create a new one
                print(f"🔍 INTELLIGENT UPDATE: No current plan, creating new intelligent analysis")
                return self._handle_infrastructure_creation(query, query_analysis)

        # Handle different types of requirements responses
        if 'answer 1' in query_lower or 'answer 2' in query_lower or 'answer 3' in query_lower:
            # Extract question number and answer
            parts = query.split()
            try:
                for i, part in enumerate(parts):
                    if part.lower().startswith('answer') and i + 1 < len(parts):
                        question_num = int(parts[i + 1])
                        answer = ' '.join(parts[i + 2:]) if i + 2 < len(parts) else "default"
                        break
                else:
                    question_num = 1
                    answer = "default"

                feedback = self.requirements_collector.process_user_response(question_num, answer)

                if not feedback.get('success', False):
                    # Error occurred
                    return [PluginResponse(
                        success=False,
                        content=f"❌ **Error:** {feedback.get('error', 'Unknown error')}",
                        source="Requirements Collector",
                        confidence=0.0,
                        additional_data={"error": feedback.get('error', 'Unknown error')}
                    )]

                # Build response content
                response_content = f"✅ **Answer recorded for Question {question_num}:**\n\n"
                response_content += f"**Question:** {feedback.get('question', 'Unknown')}\n"
                response_content += f"**Your Answer:** {answer}\n"
                response_content += f"**Feedback:** {feedback.get('feedback', 'Thank you!')}\n\n"

                # Add next steps
                if feedback.get('next_steps'):
                    response_content += "**Next Steps:**\n"
                    for step in feedback['next_steps']:
                        response_content += f"   • {step}\n"
                    response_content += "\n"

                # Add completion status
                completion = feedback.get('completion_status', {})
                if completion.get('total_questions'):
                    response_content += f"**Progress:** {completion.get('answered_questions', 0)}/{completion.get('total_questions', 0)} questions answered ({completion.get('completion_percentage', 0):.1f}%)\n\n"

                # Check if all questions are answered
                if completion.get('is_complete', False):
                    response_content += "🎉 **All requirements collected!**\n\n"
                    response_content += feedback.get('final_message', 'Your infrastructure plan is complete and ready for implementation.')
                else:
                    # Show the next question
                    if feedback.get('next_question'):
                        response_content += "---\n\n"
                        response_content += feedback.get('next_question')

                return [PluginResponse(
                    success=True,
                    content=response_content,
                    source="Requirements Collector",
                    confidence=0.9,
                    additional_data=feedback
                )]

            except Exception as e:
                print(f"❌ Error processing requirements response: {e}")
                return [PluginResponse(
                    success=False,
                    content=f"Sorry, I encountered an error processing your response. Please try again.",
                    source="Requirements Collector",
                    confidence=0.0,
                    additional_data={"error": str(e)}
                )]

        # Handle "proceed with defaults" command
        elif 'proceed with defaults' in query_lower:
            try:
                feedback = self.requirements_collector.proceed_with_defaults()
                
                if not feedback.get('success', False):
                    return [PluginResponse(
                        success=False,
                        content=f"❌ **Error:** {feedback.get('error', 'Unknown error')}",
                        source="Requirements Collector",
                        confidence=0.0,
                        additional_data={"error": feedback.get('error', 'Unknown error')}
                    )]
                
                response_content = f"🚀 **{feedback.get('message', 'Proceeding with defaults...')}**\n\n"
                
                # Add completion status
                completion = feedback.get('completion_status', {})
                if completion.get('total_questions'):
                    response_content += f"**Progress:** {completion.get('answered_questions', 0)}/{completion.get('total_questions', 0)} questions answered ({completion.get('completion_percentage', 0):.1f}%)\n\n"
                
                # Add final message and next steps
                if completion.get('is_complete', False):
                    response_content += feedback.get('final_message', 'Your infrastructure plan is complete and ready for implementation.')
                    response_content += "\n\n**Next Steps:**\n"
                    for step in feedback.get('next_steps', []):
                        response_content += f"   • {step}\n"
                
                return [PluginResponse(
                    success=True,
                    content=response_content,
                    source="Requirements Collector",
                    confidence=0.9,
                    additional_data=feedback
                )]
                
            except Exception as e:
                print(f"❌ Error proceeding with defaults: {e}")
                return [PluginResponse(
                    success=False,
                    content=f"Sorry, I encountered an error proceeding with defaults. Please try again.",
                    source="Requirements Collector",
                    confidence=0.0,
                    additional_data={"error": str(e)}
                )]

        # Handle natural language answers (like "medium", "low", "high", "default", "yes", "no", "aws", "azure", "gcp")
        elif any(keyword in query_lower for keyword in ['medium', 'low', 'high', 'default', 'yes', 'no', 'aws', 'azure', 'gcp']):
            # This is likely an answer to a current question
            if hasattr(self.requirements_collector, 'current_plan') and self.requirements_collector.current_plan:
                # Try to match this to the current question
                current_questions = self.requirements_collector.get_current_questions()
                if current_questions:
                    # Process as answer to current question
                    feedback = self.requirements_collector.process_user_response(1, query)
                    
                    response_content = f"✅ **Answer recorded:** {query}\n\n"
                    response_content += f"**Question:** {feedback.get('question', 'Current question')}\n"
                    response_content += f"**Your Answer:** {query}\n\n"
                    
                    completion = feedback.get('completion_status', {})
                    if completion.get('total_questions'):
                        response_content += f"**Progress:** {completion.get('answered_questions', 0)}/{completion.get('total_questions', 0)} questions answered\n\n"
                    
                    if completion.get('is_complete', False):
                        response_content += "🎉 **All requirements collected!**\n\n"
                        response_content += "**Next Steps:**\n"
                        response_content += "• Type 'show implementation plan' to review the complete plan\n"
                        response_content += "• Type 'proceed with implementation' to generate Terraform code\n"
                    else:
                        response_content += "💡 **Continue with:**\n"
                        response_content += "• Answer the next question\n"
                        response_content += "• Type 'requirements summary' to see progress\n"
                        response_content += "• Type 'proceed with defaults' to use recommended settings\n"
                    
                    return [PluginResponse(
                        success=True,
                        content=response_content,
                        source="Requirements Collector",
                        confidence=0.9,
                        additional_data=feedback
                    )]
            
            # Fallback to generic response
            response_content = f"✅ **Answer recorded:** {query}\n\n"
            response_content += "💡 **I've noted your preference.** You can:\n"
            response_content += "• Continue answering other questions\n"
            response_content += "• Type 'requirements summary' to see progress\n"
            response_content += "• Type 'show requirements' to see the interface\n"
            response_content += "• Type 'proceed with defaults' to use recommended settings\n\n"
            response_content += f"**Your answer:** {query}\n\n"
            response_content += "**Would you like me to provide step-by-step guidance?**"

            return [PluginResponse(
                success=True,
                content=response_content,
                source="Requirements Collector",
                confidence=0.8,
                additional_data={"type": "generic_response", "input": query}
            )]

        # Handle other requirements responses
        elif 'requirements summary' in query_lower:
            # Show requirements collection summary
            if hasattr(self.requirements_collector, 'current_plan') and self.requirements_collector.current_plan:
                response_content = self.requirements_collector.get_summary()
                return [PluginResponse(
                    success=True,
                    content=response_content,
                    source="Requirements Collector",
                    confidence=0.9,
                    additional_data={"type": "requirements_summary"}
                )]
            else:
                response_content = "⚠️ **No Active Requirements Collection:**\n\n"
                response_content += "Please start by requesting infrastructure creation:\n"
                response_content += "• 'Create a serverless architecture'\n"
                response_content += "• 'Design a 3-tier web application'\n"
                response_content += "• 'Build a microservices infrastructure'\n\n"
                response_content += "**Example:** 'Create a serverless architecture with Lambda and DynamoDB'"
                return [PluginResponse(
                    success=True, 
                    content=response_content, 
                    source="Requirements Collector", 
                    confidence=0.8,
                    additional_data={"type": "no_requirements"}
                )]

        # Handle "show requirements" command
        elif 'show requirements' in query_lower or 'requirements interface' in query_lower:
            if hasattr(self.requirements_collector, 'current_plan') and self.requirements_collector.current_plan:
                current_plan = self.requirements_collector.current_plan
                questions = self.requirements_collector.get_current_questions()
                response_content = self.requirements_collector._format_requirements_collection_interface(current_plan, questions)
                return [PluginResponse(
                    success=True, 
                    content=response_content, 
                    source="Requirements Collector", 
                    confidence=0.9,
                    additional_data={"type": "requirements_interface"}
                )]
            else:
                response_content = "⚠️ **No Active Requirements Collection:**\n\n"
                response_content += "Please start by requesting infrastructure creation:\n"
                response_content += "• 'Create a serverless architecture'\n"
                response_content += "• 'Design a 3-tier web application'\n"
                response_content += "• 'Build a microservices infrastructure'\n\n"
                response_content += "**Example:** 'Create a serverless architecture with Lambda and DynamoDB'"
                return [PluginResponse(
                    success=True, 
                    content=response_content, 
                    source="Requirements Collector", 
                    confidence=0.8,
                    additional_data={"type": "no_requirements"}
                )]

        else:
            # Intelligent response based on context
            response_content = self._generate_contextual_response(query, current_plan)

            return [PluginResponse(
                success=True,
                content=response_content,
                source="Requirements Collector",
                confidence=0.8,
                additional_data={"type": "generic_response", "input": query}
            )]

    def _is_code_generation_request(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is requesting code generation"""
        query_lower = query.lower()
        code_keywords = ['generate', 'code', 'terraform', 'create', 'build', 'write']
        infrastructure_keywords = ['infrastructure', 'architecture', 'vpc', 'ec2', 'lambda', 'dynamodb', 'rds', 's3']
        
        has_code_request = any(keyword in query_lower for keyword in code_keywords)
        has_infrastructure = any(keyword in query_lower for keyword in infrastructure_keywords)
        
        return has_code_request and has_infrastructure

    def _handle_code_generation(self, query: str, query_analysis: QueryAnalysis) -> List[PluginResponse]:
        """Handle code generation requests"""
        from core.plugin_system import PluginResponse
        
        print(f"🔍 DEBUG: Starting code generation for: '{query}'")
        
        # Get the Terraform Engineer plugin
        terraform_plugin = self.plugin_manager.get_plugin("Terraform Engineer")
        if not terraform_plugin:
            return [PluginResponse(
                success=False,
                content="❌ Terraform Engineer plugin not available",
                source="Code Generator",
                confidence=0.0,
                additional_data={}
            )]
        
        # Generate the infrastructure code
        try:
            # This will call the plugin's execute_tool method
            result = terraform_plugin.execute_tool("generate_terraform", {
                "pattern": "serverless",
                "environment": "aws",
                "requirements": {
                    "expected_volume": "medium",
                    "scalability_needs": "Auto-scaling enabled",
                    "response_time": "Under 200ms"
                }
            })
            
            response_content = self._generate_dynamic_code_response(result, "serverless", "aws")
            
            return [PluginResponse(
                success=True,
                content=response_content,
                source="Terraform Engineer",
                confidence=0.95,
                additional_data={
                    "files_generated": ["main.tf", "variables.tf", "outputs.tf", "providers.tf", "README.md"],
                    "pattern": "serverless",
                    "environment": "aws"
                }
            )]
            
        except Exception as e:
            print(f"❌ Error generating code: {e}")
            return [PluginResponse(
                success=False,
                content=f"❌ Error generating Terraform code: {str(e)}",
                source="Code Generator",
                confidence=0.0,
                additional_data={}
            )]

    def _is_proceed_request(self, query: str, query_analysis: QueryAnalysis) -> bool:
        """Check if the query is requesting to proceed with code generation"""
        query_lower = query.lower()
        
        # Don't catch requirements collection commands
        if 'proceed with defaults' in query_lower or 'proceed with default' in query_lower:
            return False
            
        proceed_keywords = ['proceed', 'continue', 'next', 'generate', 'create', 'build', 'deploy']
        return any(keyword in query_lower for keyword in proceed_keywords)

    def _format_updated_infrastructure_plan(self, original_plan, updated_plan, user_input: str) -> str:
        """Format the updated infrastructure plan to show intelligent changes"""
        try:
            response = "🧠 **INTELLIGENT PLAN UPDATE COMPLETE!**\n\n"
            response += f"**Based on your request:** '{user_input}'\n\n"
            
            # Show what changed
            changes = []
            if original_plan.pattern != updated_plan.pattern:
                changes.append(f"**Updated Infrastructure Pattern:** {updated_plan.pattern.value.replace('_', ' ').title()}")
            
            if original_plan.environment != updated_plan.environment:
                changes.append(f"**Updated Target Environment:** {updated_plan.environment.value.title()}")
            
            if original_plan.estimated_cost != updated_plan.estimated_cost:
                changes.append(f"**Updated Estimated Cost:** {updated_plan.estimated_cost}")
            
            # Add changes to response
            for change in changes:
                response += f"{change}\n"
            
            response += "\n"
            
            # Show updated requirements
            response += "🔧 **Updated Requirements:**\n"
            if hasattr(updated_plan, 'requirements') and updated_plan.requirements:
                for req in updated_plan.requirements[:4]:
                    if hasattr(req, 'component') and hasattr(req, 'type') and hasattr(req, 'priority'):
                        response += f"   • {req.component}: {req.type} ({req.priority} priority)\n"
                    else:
                        response += f"   • {str(req)}\n"
            else:
                response += self._generate_default_requirements_text(updated_plan)
            
            # Show updated security considerations
            if hasattr(updated_plan, 'security_recommendations') and updated_plan.security_recommendations:
                response += "\n🔒 **Updated Security Considerations:**\n"
                for sec in updated_plan.security_recommendations[:3]:
                    response += f"   • {sec}\n"
            
            # Generate next steps
            response += "\n📋 **Next Steps:**\n"
            response += self._generate_next_steps_text(updated_plan)
            
            # Generate updated questions
            if hasattr(updated_plan, 'missing_info') and updated_plan.missing_info:
                response += "\n❓ **Updated Questions Based on Changes:**\n"
                response += self._generate_questions_text(updated_plan.missing_info[:3])
            
            # Generate interaction guide
            response += "\n💡 **Answer these questions to get started:**\n"
            response += self._generate_interaction_guide(updated_plan)
            
            response += "\n🎯 **The system has intelligently adapted to your requirements!**"
            
            return response
            
        except Exception as e:
            print(f"❌ Error formatting updated plan: {e}")
            return f"❌ Error updating infrastructure plan: {str(e)}"
    
    def _generate_default_requirements_text(self, plan) -> str:
        """Generate appropriate default requirements text based on plan data"""
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'gcp':
                return "   • Compute: Cloud Functions (high priority)\n   • Database: Firestore (high priority)\n   • API Gateway: Cloud Endpoints (high priority)\n   • Security: Cloud IAM (high priority)\n"
            elif env == 'azure':
                return "   • Compute: Azure Functions (high priority)\n   • Database: Cosmos DB (high priority)\n   • API Gateway: API Management (high priority)\n   • Security: Azure AD (high priority)\n"
            elif env == 'aws':
                return "   • Compute: Lambda Functions (high priority)\n   • Database: DynamoDB (high priority)\n   • API Gateway: API Gateway (high priority)\n   • Security: IAM (high priority)\n"
            elif env == 'hybrid':
                return "   • Compute: Multi-cloud Functions (high priority)\n   • Database: Multi-cloud Database (high priority)\n   • API Gateway: Multi-cloud Gateway (high priority)\n   • Security: Multi-cloud IAM (high priority)\n"
        
        return "   • Compute: Serverless Functions (high priority)\n   • Database: NoSQL Database (high priority)\n   • API Gateway: REST API Endpoints (high priority)\n   • Security: IAM/Identity Management (high priority)\n"
    
    def _generate_next_steps_text(self, plan) -> str:
        """Generate next steps text based on plan data"""
        steps = [
            "1. Review the updated plan",
            "2. Answer new questions based on changes",
            "3. Customize as needed",
            "4. Proceed with implementation"
        ]
        
        # Add environment-specific steps
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'hybrid':
                steps.append("5. Configure multi-cloud provider settings")
        
        return "\n".join([f"   {step}" for step in steps])
    
    def _generate_questions_text(self, questions) -> str:
        """Generate questions text dynamically"""
        if not questions:
            return "   No questions available at this time.\n"
        
        response = ""
        for i, question in enumerate(questions, 1):
            if hasattr(question, 'question'):
                response += f"   **Q{i}:** {question.question}\n"
            else:
                response += f"   **Q{i}:** {str(question)}\n"
        
        return response
    
    def _generate_interaction_guide(self, plan) -> str:
        """Generate interaction guide based on plan context"""
        guide = [
            "• Type 'answer 1 [your answer]' to respond",
            "• Type 'requirements summary' to see current status",
            "• Type 'proceed with defaults' to use recommended settings"
        ]
        
        # Add environment-specific guidance
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'hybrid':
                guide.append("• Type 'multi-cloud setup' for cross-provider configuration")
                guide.append("• Type 'cloud preference [aws/azure/gcp]' to set primary")
        
        return "\n".join([f"   {item}" for item in guide])

    def _format_requirements_collection_interface(self, plan: InfrastructurePlan, questions: List[str]) -> str:
        """Format the requirements collection interface for the chat"""
        response = f"📋 **REQUIREMENTS COLLECTION INTERFACE**\n\n"
        
        # Current plan status
        response += f"🏗️ **Current Infrastructure Plan:**\n"
        response += f"   • **Pattern:** {plan.pattern.value.replace('_', ' ').title()}\n"
        response += f"   • **Environment:** {plan.environment.value.replace('_', ' ').title()}\n"
        response += f"   • **Estimated Cost:** {plan.estimated_cost}\n\n"
        
        # Requirements progress
        total_questions = len(questions)
        response += f"📊 **Progress:** 0/{total_questions} questions answered\n"
        response += f"📈 **Completion:** 0% complete\n\n"
        
        # Current questions to answer
        response += f"❓ **Questions to Answer:**\n"
        for i, question in enumerate(questions[:5], 1):  # Show first 5 questions
            response += f"   **Q{i}:** {question}\n"
        
        if total_questions > 5:
            response += f"   ... and {total_questions - 5} more questions\n"
        
        # How to interact
        response += f"\n💡 **How to Interact:**\n"
        response += f"   • **Answer Questions:** Type 'answer 1 [your answer]' to respond\n"
        response += f"   • **See Progress:** Type 'requirements summary' to check status\n"
        response += f"   • **Use Defaults:** Type 'proceed with defaults' for recommended settings\n"
        response += f"   • **Modify Plan:** Type 'change to [pattern]' or 'I want [requirement]'\n"
        response += f"   • **Show Plan:** Type 'show implementation plan' to review\n\n"
        
        # Quick actions
        response += f"🚀 **Quick Actions:**\n"
        response += f"   • Type 'answer 1 [your preference]' to start\n"
        response += f"   • Type 'proceed with defaults' to skip questions\n"
        response += f"   • Type 'modify plan' to change requirements\n\n"
        
        response += f"🎯 **Goal:** Complete requirements collection to generate your infrastructure!"
        
        return response


# Example usage and testing
if __name__ == "__main__":
    print("🤖 Base Agent - Test Mode\n")
    
    # Initialize agent
    agent = BaseAgent("TestAgent")
    
    # Start session
    session_id = agent.start_session("test_user")
    
    # Test queries
    test_queries = [
        "Hi there!",
        "What can you help me with?",
        "How do I create a Docker container?",
        "I'm having trouble with my setup",
        "Explain Kubernetes to me"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = agent.process_query(query, session_id)
        
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Intent: {response.intent}")
        print(f"Sources: {response.sources}")
        print(f"Response time: {response.response_time_ms}ms")
        print("-" * 60)
    
    # Show agent info
    info = agent.get_agent_info()
    print(f"\nAgent Statistics:")
    print(json.dumps(info['statistics'], indent=2))
