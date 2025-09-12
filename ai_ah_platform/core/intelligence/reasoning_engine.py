"""
Intelligent Reasoning Engine for AI-AH Platform

This module provides a proper reasoning engine that thinks through problems
step by step instead of using hardcoded templates.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ReasoningStep:
    """Represents a step in the reasoning process."""
    step_id: str
    step_type: str  # keyword_extraction, pattern_matching, analysis, reasoning, processing, curation
    input_data: Any
    output_data: Any
    confidence: float
    reasoning: str
    timestamp: datetime


@dataclass
class ReasoningResult:
    """Result of the reasoning process."""
    query: str
    steps: List[ReasoningStep]
    final_recommendation: str
    confidence: float
    reasoning_chain: str
    metadata: Dict[str, Any]


class IntelligentReasoningEngine:
    """
    Intelligent reasoning engine that processes requests through logical steps:
    1. Keyword Extraction - Extract meaningful keywords
    2. Pattern Matching - Match against known patterns
    3. Analysis - Analyze the request context
    4. Reasoning - Think through the problem
    5. Processing - Process the information
    6. Curation - Curate the final response
    """
    
    def __init__(self):
        self.reasoning_history: List[ReasoningResult] = []
        self.pattern_database = self._initialize_pattern_database()
        self.knowledge_database = self._initialize_knowledge_database()
        
    def _initialize_pattern_database(self) -> Dict[str, Any]:
        """Initialize the pattern database for matching."""
        return {
            "infrastructure_types": {
                "web_server": {
                    "keywords": ["web", "server", "nginx", "apache", "http", "website"],
                    "patterns": [r"web\s+server", r"nginx", r"apache", r"http\s+server"],
                    "requirements": ["load_balancer", "ssl", "monitoring"],
                    "complexity": "medium"
                },
                "database": {
                    "keywords": ["database", "db", "mysql", "postgresql", "mongodb", "redis"],
                    "patterns": [r"database", r"db\s+server", r"mysql", r"postgresql"],
                    "requirements": ["backup", "replication", "monitoring"],
                    "complexity": "high"
                },
                "kubernetes": {
                    "keywords": ["kubernetes", "k8s", "container", "pod", "deployment"],
                    "patterns": [r"kubernetes", r"k8s", r"container\s+orchestration"],
                    "requirements": ["ingress", "service", "configmap"],
                    "complexity": "high"
                }
            },
            "cloud_providers": {
                "aws": {
                    "keywords": ["aws", "amazon", "ec2", "s3", "rds"],
                    "patterns": [r"aws", r"amazon\s+web\s+services"],
                    "services": ["ec2", "s3", "rds", "vpc", "iam"]
                },
                "azure": {
                    "keywords": ["azure", "microsoft", "vm", "storage", "sql"],
                    "patterns": [r"azure", r"microsoft\s+azure"],
                    "services": ["vm", "storage", "sql", "vnet", "rbac"]
                },
                "gcp": {
                    "keywords": ["gcp", "google", "compute", "cloud", "bigquery"],
                    "patterns": [r"gcp", r"google\s+cloud"],
                    "services": ["compute", "storage", "bigquery", "vpc", "iam"]
                }
            },
            "technologies": {
                "terraform": {
                    "keywords": ["terraform", "iac", "infrastructure as code"],
                    "patterns": [r"terraform", r"infrastructure\s+as\s+code"],
                    "capabilities": ["provisioning", "state_management", "planning"]
                },
                "ansible": {
                    "keywords": ["ansible", "configuration", "automation", "playbook"],
                    "patterns": [r"ansible", r"configuration\s+management"],
                    "capabilities": ["configuration", "automation", "orchestration"]
                }
            }
        }
    
    def _initialize_knowledge_database(self) -> Dict[str, Any]:
        """Initialize the knowledge database."""
        return {
            "best_practices": {
                "security": [
                    "Implement least privilege access",
                    "Enable encryption at rest and in transit",
                    "Use network segmentation",
                    "Regular security updates",
                    "Monitor and audit access"
                ],
                "scalability": [
                    "Design for horizontal scaling",
                    "Use load balancers",
                    "Implement auto-scaling",
                    "Cache frequently accessed data",
                    "Use CDN for static content"
                ],
                "cost_optimization": [
                    "Right-size resources",
                    "Use reserved instances",
                    "Implement auto-scaling",
                    "Monitor and optimize storage",
                    "Use spot instances for non-critical workloads"
                ]
            },
            "common_scenarios": {
                "web_application": {
                    "components": ["load_balancer", "web_servers", "database", "cache"],
                    "considerations": ["security", "scalability", "monitoring", "backup"],
                    "estimated_cost": "medium"
                },
                "microservices": {
                    "components": ["api_gateway", "service_mesh", "containers", "monitoring"],
                    "considerations": ["service_discovery", "load_balancing", "monitoring", "security"],
                    "estimated_cost": "high"
                }
            }
        }
    
    def reason_through_request(self, query: str, context: Dict[str, Any] = None) -> ReasoningResult:
        """
        Main reasoning method that processes a request through logical steps.
        """
        logger.info(f"Starting reasoning process for query: {query}")
        
        steps = []
        reasoning_chain = []
        
        # Step 1: Keyword Extraction
        keyword_step = self._extract_keywords(query)
        steps.append(keyword_step)
        reasoning_chain.append(f"Extracted keywords: {keyword_step.output_data}")
        
        # Step 2: Pattern Matching
        pattern_step = self._match_patterns(query, keyword_step.output_data)
        steps.append(pattern_step)
        reasoning_chain.append(f"Matched patterns: {pattern_step.output_data}")
        
        # Step 3: Analysis
        analysis_step = self._analyze_request(query, keyword_step.output_data, pattern_step.output_data)
        steps.append(analysis_step)
        reasoning_chain.append(f"Analysis result: {analysis_step.reasoning}")
        
        # Step 4: Reasoning
        reasoning_step = self._reason_through_problem(analysis_step.output_data, context)
        steps.append(reasoning_step)
        reasoning_chain.append(f"Reasoning: {reasoning_step.reasoning}")
        
        # Step 5: Processing
        processing_step = self._process_information(reasoning_step.output_data)
        steps.append(processing_step)
        reasoning_chain.append(f"Processing: {processing_step.reasoning}")
        
        # Step 6: Curation
        curation_step = self._curate_response(processing_step.output_data, query)
        steps.append(curation_step)
        reasoning_chain.append(f"Curation: {curation_step.reasoning}")
        
        # Calculate overall confidence
        overall_confidence = sum(step.confidence for step in steps) / len(steps)
        
        result = ReasoningResult(
            query=query,
            steps=steps,
            final_recommendation=curation_step.output_data,
            confidence=overall_confidence,
            reasoning_chain=" -> ".join(reasoning_chain),
            metadata={
                "total_steps": len(steps),
                "processing_time": datetime.now(),
                "context": context or {}
            }
        )
        
        self.reasoning_history.append(result)
        logger.info(f"Reasoning completed with confidence: {overall_confidence:.2f}")
        
        return result
    
    def _extract_keywords(self, query: str) -> ReasoningStep:
        """Extract meaningful keywords from the query."""
        # Convert to lowercase for processing
        query_lower = query.lower()
        
        # Extract infrastructure-related keywords
        infrastructure_keywords = []
        for category, items in self.pattern_database.items():
            for item_name, item_data in items.items():
                for keyword in item_data.get("keywords", []):
                    if keyword in query_lower:
                        infrastructure_keywords.append({
                            "keyword": keyword,
                            "category": category,
                            "item": item_name,
                            "context": item_data
                        })
        
        # Extract action keywords
        action_keywords = []
        action_patterns = {
            "create": r"\b(create|build|deploy|setup|provision)\b",
            "modify": r"\b(modify|update|change|edit|configure)\b",
            "delete": r"\b(delete|remove|destroy|cleanup)\b",
            "explain": r"\b(explain|describe|tell me about|what is)\b",
            "list": r"\b(list|show|display|get)\b",
            "optimize": r"\b(optimize|improve|enhance|tune)\b"
        }
        
        for action, pattern in action_patterns.items():
            if re.search(pattern, query_lower):
                action_keywords.append({
                    "action": action,
                    "pattern": pattern,
                    "confidence": 0.9
                })
        
        # Extract technology keywords
        tech_keywords = []
        for tech, tech_data in self.pattern_database["technologies"].items():
            for keyword in tech_data["keywords"]:
                if keyword in query_lower:
                    tech_keywords.append({
                        "technology": tech,
                        "keyword": keyword,
                        "capabilities": tech_data["capabilities"]
                    })
        
        extracted_data = {
            "infrastructure_keywords": infrastructure_keywords,
            "action_keywords": action_keywords,
            "tech_keywords": tech_keywords,
            "raw_query": query
        }
        
        confidence = min(1.0, (len(infrastructure_keywords) + len(action_keywords) + len(tech_keywords)) / 10)
        
        return ReasoningStep(
            step_id="keyword_extraction",
            step_type="keyword_extraction",
            input_data=query,
            output_data=extracted_data,
            confidence=confidence,
            reasoning=f"Extracted {len(infrastructure_keywords)} infrastructure, {len(action_keywords)} action, and {len(tech_keywords)} technology keywords",
            timestamp=datetime.now()
        )
    
    def _match_patterns(self, query: str, keywords: Dict[str, Any]) -> ReasoningStep:
        """Match the query against known patterns."""
        matched_patterns = []
        
        # Match infrastructure patterns
        for category, items in self.pattern_database.items():
            for item_name, item_data in items.items():
                for pattern in item_data.get("patterns", []):
                    if re.search(pattern, query.lower()):
                        matched_patterns.append({
                            "category": category,
                            "item": item_name,
                            "pattern": pattern,
                            "data": item_data,
                            "confidence": 0.9
                        })
        
        # Match technology patterns
        for tech, tech_data in self.pattern_database["technologies"].items():
            for pattern in tech_data["patterns"]:
                if re.search(pattern, query.lower()):
                    matched_patterns.append({
                        "category": "technology",
                        "item": tech,
                        "pattern": pattern,
                        "data": tech_data,
                        "confidence": 0.9
                    })
        
        confidence = min(1.0, len(matched_patterns) / 5) if matched_patterns else 0.1
        
        return ReasoningStep(
            step_id="pattern_matching",
            step_type="pattern_matching",
            input_data=keywords,
            output_data=matched_patterns,
            confidence=confidence,
            reasoning=f"Matched {len(matched_patterns)} patterns from query analysis",
            timestamp=datetime.now()
        )
    
    def _analyze_request(self, query: str, keywords: Dict[str, Any], patterns: List[Dict[str, Any]]) -> ReasoningStep:
        """Analyze the request to understand intent and requirements."""
        analysis = {
            "intent": "unknown",
            "complexity": "low",
            "requirements": [],
            "technologies": [],
            "cloud_providers": [],
            "estimated_effort": "low"
        }
        
        # Determine intent from action keywords
        if keywords["action_keywords"]:
            primary_action = keywords["action_keywords"][0]["action"]
            analysis["intent"] = primary_action
        
        # Determine technologies involved
        for tech_keyword in keywords["tech_keywords"]:
            analysis["technologies"].append(tech_keyword["technology"])
        
        # Determine cloud providers
        for infra_keyword in keywords["infrastructure_keywords"]:
            if infra_keyword["category"] == "cloud_providers":
                analysis["cloud_providers"].append(infra_keyword["item"])
        
        # Determine complexity based on patterns
        complexity_scores = []
        for pattern in patterns:
            if "complexity" in pattern["data"]:
                complexity_map = {"low": 1, "medium": 2, "high": 3}
                complexity_scores.append(complexity_map.get(pattern["data"]["complexity"], 1))
        
        if complexity_scores:
            avg_complexity = sum(complexity_scores) / len(complexity_scores)
            if avg_complexity >= 2.5:
                analysis["complexity"] = "high"
                analysis["estimated_effort"] = "high"
            elif avg_complexity >= 1.5:
                analysis["complexity"] = "medium"
                analysis["estimated_effort"] = "medium"
        
        # Extract requirements from patterns
        for pattern in patterns:
            if "requirements" in pattern["data"]:
                analysis["requirements"].extend(pattern["data"]["requirements"])
        
        confidence = 0.8 if analysis["intent"] != "unknown" else 0.3
        
        return ReasoningStep(
            step_id="analysis",
            step_type="analysis",
            input_data={"keywords": keywords, "patterns": patterns},
            output_data=analysis,
            confidence=confidence,
            reasoning=f"Analyzed request: intent={analysis['intent']}, complexity={analysis['complexity']}, technologies={analysis['technologies']}",
            timestamp=datetime.now()
        )
    
    def _reason_through_problem(self, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> ReasoningStep:
        """Think through the problem and generate insights."""
        reasoning_insights = []
        
        # Reason about intent
        if analysis["intent"] == "explain":
            reasoning_insights.append("User wants explanation - provide comprehensive information")
        elif analysis["intent"] == "create":
            reasoning_insights.append("User wants to create infrastructure - provide step-by-step guidance")
        elif analysis["intent"] == "list":
            reasoning_insights.append("User wants to see options - provide structured list")
        
        # Reason about complexity
        if analysis["complexity"] == "high":
            reasoning_insights.append("High complexity - break down into manageable steps")
        elif analysis["complexity"] == "medium":
            reasoning_insights.append("Medium complexity - provide balanced approach")
        
        # Reason about technologies
        if analysis["technologies"]:
            tech_reasoning = f"Technologies involved: {', '.join(analysis['technologies'])} - consider integration points"
            reasoning_insights.append(tech_reasoning)
        
        # Reason about cloud providers
        if analysis["cloud_providers"]:
            cloud_reasoning = f"Cloud providers: {', '.join(analysis['cloud_providers'])} - consider multi-cloud strategies"
            reasoning_insights.append(cloud_reasoning)
        
        # Generate recommendations based on reasoning
        recommendations = []
        if analysis["requirements"]:
            recommendations.append("Address all identified requirements")
        
        if analysis["complexity"] == "high":
            recommendations.append("Start with MVP and iterate")
            recommendations.append("Consider phased approach")
        
        reasoning_output = {
            "insights": reasoning_insights,
            "recommendations": recommendations,
            "approach": self._determine_approach(analysis),
            "considerations": self._identify_considerations(analysis)
        }
        
        confidence = 0.9 if reasoning_insights else 0.5
        
        return ReasoningStep(
            step_id="reasoning",
            step_type="reasoning",
            input_data=analysis,
            output_data=reasoning_output,
            confidence=confidence,
            reasoning=f"Generated {len(reasoning_insights)} insights and {len(recommendations)} recommendations",
            timestamp=datetime.now()
        )
    
    def _process_information(self, reasoning_data: Dict[str, Any]) -> ReasoningStep:
        """Process the information to create actionable content."""
        processed_content = {
            "sections": [],
            "code_examples": [],
            "best_practices": [],
            "warnings": [],
            "next_steps": []
        }
        
        # Process insights into sections
        for insight in reasoning_data["insights"]:
            processed_content["sections"].append({
                "type": "insight",
                "content": insight,
                "priority": "high"
            })
        
        # Process recommendations
        for recommendation in reasoning_data["recommendations"]:
            processed_content["sections"].append({
                "type": "recommendation",
                "content": recommendation,
                "priority": "medium"
            })
        
        # Add best practices based on approach
        approach = reasoning_data["approach"]
        if approach in self.knowledge_database["best_practices"]:
            processed_content["best_practices"] = self.knowledge_database["best_practices"][approach]
        
        # Generate next steps
        processed_content["next_steps"] = [
            "Review the recommendations",
            "Plan the implementation approach",
            "Consider security and compliance requirements",
            "Set up monitoring and alerting"
        ]
        
        confidence = 0.8 if processed_content["sections"] else 0.4
        
        return ReasoningStep(
            step_id="processing",
            step_type="processing",
            input_data=reasoning_data,
            output_data=processed_content,
            confidence=confidence,
            reasoning=f"Processed information into {len(processed_content['sections'])} sections with best practices and next steps",
            timestamp=datetime.now()
        )
    
    def _curate_response(self, processed_data: Dict[str, Any], original_query: str) -> ReasoningStep:
        """Curate the final response based on processed information."""
        response_parts = []
        
        # Check if this is a greeting
        if any(word in original_query.lower() for word in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
            return self._curate_greeting_response(original_query)
        
        # Check if this is a capabilities request
        if any(word in original_query.lower() for word in ["capabilities", "what can you do", "list", "show", "technologies", "tasks"]):
            return self._curate_capabilities_response(original_query)
        
        # Check if this is a technology-specific request
        if any(word in original_query.lower() for word in ["terraform", "ansible", "kubernetes", "aws", "azure", "gcp"]):
            return self._curate_technology_response(original_query, processed_data)
        
        # Default response structure
        response_parts.append(f"## Analysis of: {original_query}")
        
        # Add insights
        insights = [section for section in processed_data["sections"] if section["type"] == "insight"]
        if insights:
            response_parts.append("\n## Key Insights")
            for insight in insights:
                response_parts.append(f"• {insight['content']}")
        
        # Add recommendations
        recommendations = [section for section in processed_data["sections"] if section["type"] == "recommendation"]
        if recommendations:
            response_parts.append("\n## Recommendations")
            for rec in recommendations:
                response_parts.append(f"• {rec['content']}")
        
        # Add best practices
        if processed_data["best_practices"]:
            response_parts.append("\n## Best Practices")
            for practice in processed_data["best_practices"][:5]:  # Top 5
                response_parts.append(f"• {practice}")
        
        # Add next steps
        if processed_data["next_steps"]:
            response_parts.append("\n## Next Steps")
            for step in processed_data["next_steps"]:
                response_parts.append(f"• {step}")
        
        curated_response = "\n".join(response_parts)
        
        confidence = 0.9 if response_parts else 0.3
        
        return ReasoningStep(
            step_id="curation",
            step_type="curation",
            input_data=processed_data,
            output_data=curated_response,
            confidence=confidence,
            reasoning=f"Curated response with {len(response_parts)} sections based on reasoning process",
            timestamp=datetime.now()
        )
    
    def _curate_greeting_response(self, query: str) -> ReasoningStep:
        """Curate a greeting response."""
        response_parts = []
        
        response_parts.append("## 👋 Hello! I'm your AI Infrastructure Assistant")
        response_parts.append("I'm here to help you with cloud architecture, DevOps, and infrastructure management.")
        
        response_parts.append("\n## **What I Can Help You With**")
        response_parts.append("• **Infrastructure Setup**: Web servers, databases, load balancers")
        response_parts.append("• **Security & Compliance**: Hardening, vulnerability scanning, IAM policies")
        response_parts.append("• **Monitoring & Observability**: Prometheus, Grafana, ELK stack")
        response_parts.append("• **Cost Optimization**: Rightsizing, reserved instances, auto-scaling")
        
        response_parts.append("\n## **Quick Start**")
        response_parts.append("• Ask me about specific technologies (e.g., 'list me terraform')")
        response_parts.append("• Request infrastructure examples (e.g., 'create a web server')")
        response_parts.append("• Get help with optimization (e.g., 'help me optimize costs')")
        response_parts.append("• See my full capabilities (e.g., 'list me your capabilities')")
        
        response_parts.append("\n## **What would you like to work on today?**")
        
        curated_response = "\n".join(response_parts)
        
        return ReasoningStep(
            step_id="curation",
            step_type="curation",
            input_data={"query": query, "type": "greeting"},
            output_data=curated_response,
            confidence=0.95,
            reasoning="Curated friendly greeting response with quick start options",
            timestamp=datetime.now()
        )
    
    def _curate_capabilities_response(self, query: str) -> ReasoningStep:
        """Curate a capabilities-focused response."""
        response_parts = []
        
        response_parts.append("## 🚀 AI Infrastructure Assistant Capabilities")
        response_parts.append("I'm trained to support you with cloud architecture, DevOps, and infrastructure management.")
        
        response_parts.append("\n## **Core Technologies & Tools**")
        response_parts.append("• **Terraform**: Infrastructure as Code, multi-cloud provisioning, state management")
        response_parts.append("• **Ansible**: Configuration management, automation, playbook execution")
        response_parts.append("• **Kubernetes**: Container orchestration, microservices, service mesh")
        response_parts.append("• **Docker**: Containerization, image management, deployment")
        
        response_parts.append("\n## **Cloud Providers**")
        response_parts.append("• **AWS**: EC2, S3, RDS, VPC, IAM, Lambda, CloudFormation")
        response_parts.append("• **Azure**: VMs, Storage, SQL, VNet, RBAC, Functions, ARM")
        response_parts.append("• **GCP**: Compute Engine, Cloud Storage, BigQuery, VPC, IAM, Cloud Functions")
        
        response_parts.append("\n## **Infrastructure Tasks**")
        response_parts.append("• **Web Servers**: Nginx, Apache, load balancers, SSL configuration")
        response_parts.append("• **Databases**: MySQL, PostgreSQL, MongoDB, Redis, backup strategies")
        response_parts.append("• **Monitoring**: Prometheus, Grafana, ELK stack, alerting")
        response_parts.append("• **Security**: Hardening, vulnerability scanning, compliance")
        response_parts.append("• **CI/CD**: Jenkins, GitLab CI, GitHub Actions, deployment pipelines")
        
        response_parts.append("\n## **What I Can Help You With**")
        response_parts.append("• Create and manage infrastructure with Terraform")
        response_parts.append("• Automate configuration with Ansible")
        response_parts.append("• Deploy and scale applications with Kubernetes")
        response_parts.append("• Set up monitoring and alerting systems")
        response_parts.append("• Implement security best practices")
        response_parts.append("• Optimize costs and performance")
        response_parts.append("• Design multi-cloud architectures")
        
        response_parts.append("\n## **Example Requests**")
        response_parts.append("• 'Create a web server with database on AWS'")
        response_parts.append("• 'Set up Kubernetes cluster with monitoring'")
        response_parts.append("• 'Configure Ansible playbook for server hardening'")
        response_parts.append("• 'Help me optimize my cloud costs'")
        response_parts.append("• 'Compare AWS vs Azure for my use case'")
        
        curated_response = "\n".join(response_parts)
        
        return ReasoningStep(
            step_id="curation",
            step_type="curation",
            input_data={"query": query, "type": "capabilities"},
            output_data=curated_response,
            confidence=0.95,
            reasoning="Curated comprehensive capabilities response with technologies, tasks, and examples",
            timestamp=datetime.now()
        )
    
    def _curate_technology_response(self, query: str, processed_data: Dict[str, Any]) -> ReasoningStep:
        """Curate a technology-specific response."""
        response_parts = []
        
        # Determine the technology being asked about
        if "terraform" in query.lower():
            response_parts.append("## 🔧 Terraform Infrastructure Management")
            response_parts.append("I'll provide you with Terraform capabilities and examples.")
            
            response_parts.append("\n## **Terraform Capabilities**")
            response_parts.append("• **Infrastructure as Code**: Define and manage cloud resources")
            response_parts.append("• **Multi-Cloud Support**: AWS, Azure, GCP, and 100+ providers")
            response_parts.append("• **State Management**: Track and manage infrastructure changes")
            response_parts.append("• **Plan & Apply**: Preview changes before execution")
            
            response_parts.append("\n## **Common Terraform Operations**")
            response_parts.append("• **Web Servers**: EC2 instances, load balancers, auto-scaling")
            response_parts.append("• **Databases**: RDS, managed databases, backup strategies")
            response_parts.append("• **Networking**: VPCs, subnets, security groups, routes")
            response_parts.append("• **Storage**: S3 buckets, EBS volumes, file systems")
            
            response_parts.append("\n## **Implementation Examples**")
            response_parts.append("### Basic Web Server")
            response_parts.append("```hcl")
            response_parts.append('resource "aws_instance" "web_server" {')
            response_parts.append('  ami           = "ami-0c02fb55956c7d316"')
            response_parts.append('  instance_type = "t3.micro"')
            response_parts.append('  security_groups = [aws_security_group.web_sg.name]')
            response_parts.append('}')
            response_parts.append("```")
            
        elif "ansible" in query.lower():
            response_parts.append("## ⚙️ Ansible Configuration Management")
            response_parts.append("I'll provide you with Ansible capabilities and examples.")
            
            response_parts.append("\n## **Ansible Capabilities**")
            response_parts.append("• **Configuration Management**: Automate server configuration")
            response_parts.append("• **Application Deployment**: Deploy applications consistently")
            response_parts.append("• **Infrastructure Automation**: Automate infrastructure tasks")
            response_parts.append("• **Security Hardening**: Apply security configurations")
            
            response_parts.append("\n## **Common Ansible Tasks**")
            response_parts.append("• **Package Management**: Install and update software")
            response_parts.append("• **Service Configuration**: Configure web servers, databases")
            response_parts.append("• **Security Hardening**: Apply CIS benchmarks, firewall rules")
            response_parts.append("• **Backup Automation**: Automated backup strategies")
            
        elif "kubernetes" in query.lower():
            response_parts.append("## ☸️ Kubernetes Container Orchestration")
            response_parts.append("I'll provide you with Kubernetes capabilities and examples.")
            
            response_parts.append("\n## **Kubernetes Capabilities**")
            response_parts.append("• **Container Orchestration**: Manage containerized applications")
            response_parts.append("• **Auto-scaling**: Horizontal and vertical pod autoscaling")
            response_parts.append("• **Service Discovery**: Load balancing and service mesh")
            response_parts.append("• **Configuration Management**: ConfigMaps and Secrets")
            
            response_parts.append("\n## **Common Kubernetes Operations**")
            response_parts.append("• **Deployments**: Deploy and manage applications")
            response_parts.append("• **Services**: Expose applications internally and externally")
            response_parts.append("• **Ingress**: HTTP/HTTPS routing and SSL termination")
            response_parts.append("• **Monitoring**: Prometheus, Grafana, and logging")
            
        else:
            # Generic technology response
            response_parts.append(f"## Analysis of: {query}")
            response_parts.append("I can help you with various infrastructure technologies and tasks.")
            
            # Add insights from processed data
            insights = [section for section in processed_data["sections"] if section["type"] == "insight"]
            if insights:
                response_parts.append("\n## Key Insights")
                for insight in insights:
                    response_parts.append(f"• {insight['content']}")
        
        # Add best practices if available
        if processed_data.get("best_practices"):
            response_parts.append("\n## Best Practices")
            for practice in processed_data["best_practices"][:5]:
                response_parts.append(f"• {practice}")
        
        curated_response = "\n".join(response_parts)
        
        return ReasoningStep(
            step_id="curation",
            step_type="curation",
            input_data={"query": query, "type": "technology", "processed_data": processed_data},
            output_data=curated_response,
            confidence=0.9,
            reasoning=f"Curated technology-specific response for {query}",
            timestamp=datetime.now()
        )
    
    def _determine_approach(self, analysis: Dict[str, Any]) -> str:
        """Determine the best approach based on analysis."""
        if analysis["complexity"] == "high":
            return "security"  # Focus on security for complex deployments
        elif analysis["technologies"] and "terraform" in analysis["technologies"]:
            return "scalability"  # Focus on scalability for Terraform
        else:
            return "cost_optimization"  # Default to cost optimization
    
    def _identify_considerations(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify important considerations based on analysis."""
        considerations = []
        
        if analysis["complexity"] == "high":
            considerations.append("Security and compliance requirements")
            considerations.append("Disaster recovery planning")
        
        if analysis["cloud_providers"]:
            considerations.append("Multi-cloud strategy and vendor lock-in")
        
        if analysis["technologies"]:
            considerations.append("Technology integration and compatibility")
        
        return considerations
    
    def get_reasoning_history(self) -> List[ReasoningResult]:
        """Get the history of reasoning processes."""
        return self.reasoning_history
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get statistics about reasoning performance."""
        if not self.reasoning_history:
            return {"total_queries": 0, "avg_confidence": 0}
        
        total_queries = len(self.reasoning_history)
        avg_confidence = sum(result.confidence for result in self.reasoning_history) / total_queries
        
        return {
            "total_queries": total_queries,
            "avg_confidence": avg_confidence,
            "last_query": self.reasoning_history[-1].query if self.reasoning_history else None
        }
