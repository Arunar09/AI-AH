#!/usr/bin/env python3
"""
Intelligent Response Generator

This module generates intelligent, context-aware responses based on analysis results
and knowledge base content.
"""

from typing import Dict, List, Any, Optional
import logging

class IntelligentResponseGenerator:
    """Generates intelligent responses based on analysis and knowledge."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_response(self, analysis: Dict[str, Any], user_query: str, 
                         context: Dict[str, Any] = None) -> str:
        """Generate an intelligent response based on analysis results."""
        
        intent = analysis.get("intent", "unknown")
        agent_type = analysis.get("agent_type", "general")
        confidence = analysis.get("confidence", 0.0)
        knowledge = analysis.get("knowledge", [])
        best_practices = analysis.get("best_practices", [])
        recommendations = analysis.get("recommendations", [])
        reasoning = analysis.get("reasoning", [])
        
        # Generate response based on intent
        if intent == "explain_technology":
            return self._generate_technology_explanation(
                analysis, user_query, knowledge, best_practices, recommendations
            )
        elif intent == "create_infrastructure":
            return self._generate_infrastructure_creation_response(
                analysis, user_query, knowledge, best_practices
            )
        elif intent == "troubleshoot":
            return self._generate_troubleshooting_response(
                analysis, user_query, knowledge, best_practices
            )
        elif intent == "optimize":
            return self._generate_optimization_response(
                analysis, user_query, knowledge, best_practices, recommendations
            )
        elif intent == "compare":
            return self._generate_comparison_response(
                analysis, user_query, knowledge, best_practices
            )
        else:
            return self._generate_general_response(
                analysis, user_query, knowledge, best_practices, recommendations
            )
    
    def _generate_technology_explanation(self, analysis: Dict[str, Any], 
                                       user_query: str, knowledge: List[str],
                                       best_practices: List[str], 
                                       recommendations: List[str]) -> str:
        """Generate technology explanation response."""
        agent_type = analysis.get("agent_type", "general")
        confidence = analysis.get("confidence", 0.0)
        
        response_parts = []
        
        # Main explanation
        if knowledge:
            response_parts.append(f"## {agent_type.title()} Overview")
            for item in knowledge[:3]:  # Top 3 knowledge items
                response_parts.append(f"• {item}")
        
        # Best practices
        if best_practices:
            response_parts.append("\n## Best Practices")
            for practice in best_practices[:3]:  # Top 3 practices
                response_parts.append(f"• {practice}")
        
        # Recommendations
        if recommendations:
            response_parts.append("\n## Recommendations")
            for rec in recommendations[:3]:  # Top 3 recommendations
                response_parts.append(f"• {rec}")
        
        # Add confidence indicator
        if confidence > 0.8:
            response_parts.append(f"\n*Confidence: High ({confidence:.1%})*")
        elif confidence > 0.6:
            response_parts.append(f"\n*Confidence: Medium ({confidence:.1%})*")
        else:
            response_parts.append(f"\n*Confidence: Low ({confidence:.1%})*")
        
        return "\n".join(response_parts) if response_parts else self._generate_fallback_response(user_query)
    
    def _generate_infrastructure_creation_response(self, analysis: Dict[str, Any],
                                                 user_query: str, knowledge: List[str],
                                                 best_practices: List[str]) -> str:
        """Generate infrastructure creation response."""
        agent_type = analysis.get("agent_type", "general")
        
        response_parts = []
        response_parts.append(f"## {agent_type.title()} Infrastructure Setup")
        
        if knowledge:
            response_parts.append("### Key Components:")
            for item in knowledge[:3]:
                response_parts.append(f"• {item}")
        
        if best_practices:
            response_parts.append("\n### Implementation Steps:")
            for i, practice in enumerate(best_practices[:4], 1):
                response_parts.append(f"{i}. {practice}")
        
        response_parts.append("\n### Next Steps:")
        response_parts.append("• Review the architecture requirements")
        response_parts.append("• Implement security best practices")
        response_parts.append("• Set up monitoring and logging")
        
        return "\n".join(response_parts)
    
    def _generate_troubleshooting_response(self, analysis: Dict[str, Any],
                                         user_query: str, knowledge: List[str],
                                         best_practices: List[str]) -> str:
        """Generate troubleshooting response."""
        response_parts = []
        response_parts.append("## Troubleshooting Guide")
        
        if knowledge:
            response_parts.append("### Common Issues:")
            for item in knowledge[:3]:
                response_parts.append(f"• {item}")
        
        if best_practices:
            response_parts.append("\n### Resolution Steps:")
            for i, practice in enumerate(best_practices[:4], 1):
                response_parts.append(f"{i}. {practice}")
        
        response_parts.append("\n### Additional Resources:")
        response_parts.append("• Check system logs for detailed error messages")
        response_parts.append("• Verify configuration settings")
        response_parts.append("• Test connectivity and permissions")
        
        return "\n".join(response_parts)
    
    def _generate_optimization_response(self, analysis: Dict[str, Any],
                                      user_query: str, knowledge: List[str],
                                      best_practices: List[str],
                                      recommendations: List[str]) -> str:
        """Generate optimization response."""
        response_parts = []
        response_parts.append("## Performance Optimization")
        
        if knowledge:
            response_parts.append("### Current State Analysis:")
            for item in knowledge[:2]:
                response_parts.append(f"• {item}")
        
        if recommendations:
            response_parts.append("\n### Optimization Opportunities:")
            for rec in recommendations[:4]:
                response_parts.append(f"• {rec}")
        
        if best_practices:
            response_parts.append("\n### Implementation Guidelines:")
            for practice in best_practices[:3]:
                response_parts.append(f"• {practice}")
        
        return "\n".join(response_parts)
    
    def _generate_comparison_response(self, analysis: Dict[str, Any],
                                    user_query: str, knowledge: List[str],
                                    best_practices: List[str]) -> str:
        """Generate comparison response."""
        response_parts = []
        response_parts.append("## Technology Comparison")
        
        if knowledge:
            response_parts.append("### Key Differences:")
            for item in knowledge[:4]:
                response_parts.append(f"• {item}")
        
        if best_practices:
            response_parts.append("\n### Selection Criteria:")
            for practice in best_practices[:3]:
                response_parts.append(f"• {practice}")
        
        response_parts.append("\n### Recommendation:")
        response_parts.append("Consider your specific requirements, team expertise, and long-term goals when making the final decision.")
        
        return "\n".join(response_parts)
    
    def _generate_general_response(self, analysis: Dict[str, Any],
                                 user_query: str, knowledge: List[str],
                                 best_practices: List[str],
                                 recommendations: List[str]) -> str:
        """Generate general response."""
        agent_type = analysis.get("agent_type", "general")
        confidence = analysis.get("confidence", 0.0)
        
        response_parts = []
        response_parts.append(f"## {agent_type.title()} Assistance")
        
        if knowledge:
            response_parts.append("### Relevant Information:")
            for item in knowledge[:3]:
                response_parts.append(f"• {item}")
        
        if best_practices:
            response_parts.append("\n### Best Practices:")
            for practice in best_practices[:3]:
                response_parts.append(f"• {practice}")
        
        if recommendations:
            response_parts.append("\n### Recommendations:")
            for rec in recommendations[:3]:
                response_parts.append(f"• {rec}")
        
        # Add context-aware suggestions
        if "database" in user_query.lower():
            response_parts.append("\n### Database Considerations:")
            response_parts.append("• Consider data volume and access patterns")
            response_parts.append("• Plan for backup and recovery")
            response_parts.append("• Implement proper indexing strategy")
        
        return "\n".join(response_parts) if response_parts else self._generate_fallback_response(user_query)
    
    def _generate_fallback_response(self, user_query: str) -> str:
        """Generate fallback response when no specific knowledge is available."""
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ["terraform", "ansible", "kubernetes"]):
            return """## Infrastructure Management Help

I can help you with infrastructure management using:
• **Terraform**: Infrastructure as Code
• **Ansible**: Configuration Management  
• **Kubernetes**: Container Orchestration

Please provide more specific details about what you'd like to accomplish."""
        
        elif any(word in query_lower for word in ["aws", "azure", "gcp"]):
            return """## Cloud Platform Assistance

I can help you with cloud platforms:
• **AWS**: Amazon Web Services
• **Azure**: Microsoft Azure
• **GCP**: Google Cloud Platform

What specific cloud service or architecture are you working with?"""
        
        elif any(word in query_lower for word in ["monitoring", "logging", "metrics"]):
            return """## Monitoring & Observability

I can help you with:
• **Monitoring**: System and application monitoring
• **Logging**: Centralized log management
• **Metrics**: Performance and business metrics

What monitoring challenges are you facing?"""
        
        else:
            return """## Infrastructure Intelligence Platform

I'm here to help with infrastructure and DevOps challenges. I can assist with:

• **Infrastructure as Code**: Terraform, Ansible
• **Container Orchestration**: Kubernetes, Docker
• **Cloud Platforms**: AWS, Azure, GCP
• **Monitoring & Security**: Observability, compliance
• **CI/CD**: Deployment pipelines

What would you like to work on today?"""

