#!/usr/bin/env python3
"""
Interactive Requirements Collector
================================

This module handles the interactive collection of missing information
needed to create comprehensive infrastructure plans.
"""

import json
import sqlite3
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from core.intelligent_analyzer import ClarificationQuestion, InfrastructurePlan
from datetime import datetime

# Thread-local storage for database connections
thread_local = threading.local()

def get_db_connection():
    """Get a thread-safe database connection"""
    if not hasattr(thread_local, 'db_connection'):
        thread_local.db_connection = sqlite3.connect('base_agent.db', check_same_thread=False)
        thread_local.db_connection.row_factory = sqlite3.Row
        # Create requirements table if it doesn't exist
        thread_local.db_connection.execute('''
            CREATE TABLE IF NOT EXISTS requirements_collection (
                session_id TEXT PRIMARY KEY,
                plan_data TEXT,
                responses TEXT,
                current_question INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        thread_local.db_connection.commit()
    return thread_local.db_connection


@dataclass
class UserResponse:
    """User's response to a clarification question"""
    question_id: str
    answer: str
    category: str
    timestamp: str


@dataclass
class CollectedRequirements:
    """Complete set of collected requirements"""
    environment: str
    performance_requirements: Dict[str, Any]
    security_requirements: Dict[str, Any]
    cost_constraints: Dict[str, Any]
    compliance_needs: Dict[str, Any]
    additional_preferences: Dict[str, Any]


class RequirementsCollector:
    """
    Interactive collector for gathering missing infrastructure requirements
    """
    
    def __init__(self):
        """Initialize the requirements collector"""
        self.collected_responses: List[UserResponse] = []
        self.current_plan: Optional[InfrastructurePlan] = None
        self.current_session_id: Optional[str] = None
    
    def start_collection(self, plan: InfrastructurePlan, session_id: str = None) -> str:
        """
        Start the requirements collection process with intelligent category determination
        Returns the first question to ask the user (interactive flow)
        """
        self.current_plan = plan
        self.current_session_id = session_id or "default_session"
        self.collected_responses = []
        self.current_question_index = 0
        
        # Save the plan to database for session persistence
        self._save_session_state()
        
        # Determine which categories are needed based on the request
        if hasattr(plan, 'original_request') and hasattr(plan, 'pattern') and hasattr(plan, 'environment'):
            required_categories = self._get_intelligent_categories(plan.original_request, plan.pattern, plan.environment)
        else:
            # Fallback to all categories if we can't determine
            required_categories = {
                'basic': True, 'performance': True, 'security': True, 
                'cost': True, 'compliance': True, 'advanced': True
            }
        
        # Store required categories for form generation
        self.required_categories = required_categories
        
        # Return the first question instead of all questions
        if plan.missing_info and len(plan.missing_info) > 0:
            first_question = plan.missing_info[0]
            return self._format_single_question(first_question, 1, len(plan.missing_info), required_categories)
        else:
            return "✅ **No additional requirements needed!**\n\nYour infrastructure plan is complete and ready for implementation."
    
    def process_user_response(self, question_number: int, answer: str) -> Dict[str, Any]:
        """Process a user's answer to a specific question and move to next"""
        try:
            current_plan = self.get_current_plan()
            if not current_plan:
                return {
                    'success': False,
                    'error': 'No active requirements collection session'
                }
            
            # Validate question number
            if question_number < 1 or question_number > len(current_plan.missing_info):
                return {
                    'success': False,
                    'error': f'Invalid question number. Please answer question 1-{len(current_plan.missing_info)}'
                }
            
            # Get the current question
            current_question = current_plan.missing_info[question_number - 1]
            
            # Process the answer
            user_response = UserResponse(
                question_id=str(question_number),
                answer=answer,
                category=getattr(current_question, 'category', 'general'),
                timestamp=str(datetime.now())
            )
            
            # Add to collected responses
            self.collected_responses.append(user_response)
            
            # Update session state
            self._save_session_state()
            
            # Check if this was the last question
            if question_number >= len(current_plan.missing_info):
                # All questions answered
                return {
                    'success': True,
                    'question': current_question.question,
                    'answer': answer,
                    'feedback': '✅ Excellent! All requirements have been collected.',
                    'next_steps': [
                        'Type "show implementation plan" to review your complete infrastructure plan',
                        'Type "proceed with implementation" to generate Terraform code',
                        'Type "modify plan" to make any final adjustments'
                    ],
                    'completion_status': {
                        'is_complete': True,
                        'total_questions': len(current_plan.missing_info),
                        'answered_questions': len(current_plan.missing_info),
                        'completion_percentage': 100.0
                    },
                    'final_message': '🎉 **Requirements Collection Complete!**\n\nYour infrastructure plan is now ready for implementation.'
                }
            else:
                # Move to next question
                next_question = current_plan.missing_info[question_number]
                next_question_num = question_number + 1
                total_questions = len(current_plan.missing_info)
                
                return {
                    'success': True,
                    'question': current_question.question,
                    'answer': answer,
                    'feedback': '✅ Answer recorded successfully!',
                    'next_question': self._format_single_question(next_question, next_question_num, total_questions, self.required_categories),
                    'next_steps': [
                        f'Answer question {next_question_num} to continue',
                        'Type "requirements summary" to see overall progress',
                        'Type "show plan" to review current infrastructure plan'
                    ],
                    'completion_status': {
                        'is_complete': False,
                        'total_questions': total_questions,
                        'answered_questions': question_number,
                        'completion_percentage': (question_number / total_questions) * 100.0
                    }
                }
                
        except Exception as e:
            print(f"❌ Error processing user response: {e}")
            # Enhanced error handling with specific guidance
            error_msg = str(e)
            if "missing 1 required positional argument" in error_msg:
                return {
                    'success': False,
                    'error': 'System configuration error. Please restart the requirements collection.',
                    'suggestion': 'Try starting over with your infrastructure request.'
                }
            elif "AttributeError" in error_msg:
                return {
                    'success': False,
                    'error': 'System component error. Please restart the session.',
                    'suggestion': 'Try reinitializing the agent.'
                }
            else:
                return {
                    'success': False,
                    'error': f'Unexpected error: {error_msg}',
                    'suggestion': 'Please try again or restart the session.'
                }
    
    def get_complete_requirements(self) -> CollectedRequirements:
        """
        Compile all collected requirements into a structured format
        """
        if not self.current_plan:
            raise ValueError("No active plan for requirements collection")
        
        # Parse responses by category
        environment_resp = self._get_response_by_category("environment")
        performance_resp = self._get_response_by_category("performance")
        security_resp = self._get_response_by_category("security")
        cost_resp = self._get_response_by_category("cost")
        
        return CollectedRequirements(
            environment=environment_resp.answer if environment_resp else "AWS",  # Default
            performance_requirements={
                "expected_volume": performance_resp.answer if performance_resp else "Medium (1000-10000 req/day)",
                "scalability_needs": "Auto-scaling enabled",
                "response_time": "Under 200ms"
            },
            security_requirements={
                "security_level": security_resp.answer if security_resp else "Standard security",
                "compliance": "Basic compliance",
                "encryption": "Enabled"
            },
            cost_constraints={
                "budget_range": cost_resp.answer if cost_resp else "Medium cost",
                "optimization": "Cost-optimized configuration",
                "monitoring": "Cost alerts enabled"
            },
            compliance_needs={
                "standards": "Basic security standards",
                "auditing": "Basic logging and monitoring",
                "certifications": "None specified"
            },
            additional_preferences={
                "region": "Default region",
                "backup": "Standard backup policy",
                "monitoring": "Basic CloudWatch monitoring"
            }
        )
    
    def generate_implementation_plan(self) -> str:
        """Generate a comprehensive implementation plan for user approval"""
        if not self.current_plan:
            return "No active plan for implementation planning"
        
        plan = f"""🏗️ **COMPREHENSIVE IMPLEMENTATION PLAN**

**Infrastructure Pattern:** {self.current_plan.pattern.value.replace('_', ' ').title()}
**Target Environment:** {self.current_plan.environment.value.replace('_', ' ').title()}
**Estimated Cost:** {self.current_plan.estimated_cost}

## 📋 **Requirements Analysis**

**Identified Requirements:**
"""
        
        for req in self.current_plan.requirements:
            plan += f"   • {req.component}: {req.type} ({req.priority} priority)\n"
        
        plan += f"""
**Collected User Preferences:**
"""
        
        if self.collected_responses:
            for resp in self.collected_responses:
                plan += f"   • {resp.category.title()}: {resp.answer}\n"
        else:
            plan += "   • Using default configurations\n"
        
        plan += f"""
## 🔧 **Technical Architecture**

**Core Components:**
"""
        
        if self.current_plan.pattern.value == "serverless":
            plan += """   • AWS Lambda Functions (Python/Node.js runtime)
   • DynamoDB Tables (NoSQL database)
   • API Gateway (REST API endpoints)
   • IAM Roles and Policies (Security)
   • CloudWatch (Monitoring and Logging)
   • VPC Configuration (Network isolation)
   • CloudFormation/SAM (Infrastructure as Code)"""
        elif self.current_plan.pattern.value == "microservices":
            plan += """   • ECS/EKS Cluster (Container orchestration)
   • Application Load Balancer (Traffic distribution)
   • RDS/Aurora Databases (Data persistence)
   • ElastiCache (Caching layer)
   • SQS/SNS (Message queuing)
   • VPC with private subnets (Network security)
   • CloudWatch and X-Ray (Observability)"""
        elif self.current_plan.pattern.value == "three_tier":
            plan += """   • Application Load Balancer (Web tier)
   • EC2/ECS Instances (Application tier)
   • RDS Database (Data tier)
   • Auto Scaling Groups (Scalability)
   • VPC with security groups (Network isolation)
   • CloudWatch (Monitoring)
   • S3 (Static content storage)"""
        
        plan += f"""

## 🔒 **Security Implementation**

"""
        
        for rec in self.current_plan.security_recommendations:
            plan += f"{rec}\n"
        
        plan += f"""
## 🚀 **Deployment Strategy**

"""
        
        for rec in self.current_plan.deployment_recommendations:
            plan += f"{rec}\n"
        
        plan += f"""
## 📊 **Resource Specifications**

**Compute Resources:**
   • Auto-scaling enabled for dynamic workloads
   • Multi-AZ deployment for high availability
   • Health checks and automatic failover

**Storage & Database:**
   • Encrypted at rest and in transit
   • Automated backups with point-in-time recovery
   • Read replicas for performance optimization

**Networking:**
   • VPC with public/private subnet separation
   • Security groups with least privilege access
   • NAT Gateways for private resource internet access

**Monitoring & Operations:**
   • CloudWatch dashboards and alerting
   • CloudTrail for audit logging
   • Automated incident response

## ⚠️ **Risk Assessment**

**Identified Risks:**
   • Data security and compliance requirements
   • Performance under peak load conditions
   • Cost optimization and budget management
   • Disaster recovery and business continuity

**Mitigation Strategies:**
   • Implement comprehensive security controls
   • Load testing and performance optimization
   • Cost monitoring and alerting
   • Automated backup and recovery procedures

## 💰 **Cost Breakdown**

**Monthly Operational Costs:**
   • Compute: {self._estimate_compute_cost()}
   • Storage: {self._estimate_storage_cost()}
   • Data Transfer: {self._estimate_network_cost()}
   • Monitoring: {self._estimate_monitoring_cost()}
   • **Total Estimated: {self.current_plan.estimated_cost}**

**One-time Setup Costs:**
   • Infrastructure provisioning: $50-100
   • Security configuration: $100-200
   • Monitoring setup: $50-100
   • **Total Setup: $200-400**

## ✅ **Next Steps After Approval**

1. **Generate Terraform Code** - Complete infrastructure configuration
2. **Security Review** - Validate security controls and compliance
3. **Cost Optimization** - Review and optimize resource allocation
4. **Testing** - Validate infrastructure in staging environment
5. **Deployment** - Deploy to production with monitoring
6. **Documentation** - Create operational runbooks and procedures

## 🎯 **Approval Required**

**Before proceeding with code generation, please confirm:**
   • You have reviewed and understand this implementation plan
   • The estimated costs are within your budget
   • The security measures meet your compliance requirements
   • You have the necessary AWS permissions and resources
   • You understand the operational responsibilities

**Type 'APPROVE PLAN' to proceed with implementation, or ask questions to modify the plan.**"""
        
        return plan
    
    def _estimate_compute_cost(self) -> str:
        """Estimate compute costs based on collected requirements"""
        if not self.collected_responses:
            return "$50-150/month"
        
        # Analyze performance requirements
        for resp in self.collected_responses:
            if resp.category == "performance":
                if "Low" in resp.answer:
                    return "$30-80/month"
                elif "Medium" in resp.answer:
                    return "$50-150/month"
                elif "High" in resp.answer:
                    return "$100-300/month"
                elif "Enterprise" in resp.answer:
                    return "$200-500/month"
        
        return "$50-150/month"
    
    def _estimate_storage_cost(self) -> str:
        """Estimate storage costs based on collected requirements"""
        if not self.collected_responses:
            return "$20-50/month"
        
        # Analyze data requirements
        for resp in self.collected_responses:
            if resp.category == "data":
                if "Basic" in resp.answer:
                    return "$10-30/month"
                elif "Standard" in resp.answer:
                    return "$20-50/month"
                elif "Comprehensive" in resp.answer:
                    return "$50-100/month"
                elif "Enterprise" in resp.answer:
                    return "$100-200/month"
        
        return "$20-50/month"
    
    def _estimate_network_cost(self) -> str:
        """Estimate network costs based on collected requirements"""
        if not self.collected_responses:
            return "$10-30/month"
        
        # Analyze network requirements
        for resp in self.collected_responses:
            if resp.category == "network":
                if "Low" in resp.answer:
                    return "$5-15/month"
                elif "Medium" in resp.answer:
                    return "$10-30/month"
                elif "High" in resp.answer:
                    return "$30-80/month"
                elif "Enterprise" in resp.answer:
                    return "$80-200/month"
        
        return "$10-30/month"
    
    def _estimate_monitoring_cost(self) -> str:
        """Estimate monitoring costs based on collected requirements"""
        if not self.collected_responses:
            return "$10-25/month"
        
        # Analyze monitoring requirements
        for resp in self.collected_responses:
            if resp.category == "operations":
                if "Basic" in resp.answer:
                    return "$5-15/month"
                elif "Standard" in resp.answer:
                    return "$10-25/month"
                elif "Advanced" in resp.answer:
                    return "$25-60/month"
                elif "Enterprise" in resp.answer:
                    return "$60-150/month"
        
        return "$10-25/month"
    
    def _save_session_state(self):
        """Save the current session state to database"""
        try:
            if not self.current_session_id or not self.current_plan:
                return
            
            conn = get_db_connection()
            
            # Convert plan to JSON for storage
            plan_data = {
                'pattern': self.current_plan.pattern.value,
                'environment': self.current_plan.environment.value,
                'estimated_cost': self.current_plan.estimated_cost,
                'requirements': [
                    {
                        'component': req.component,
                        'type': req.type,
                        'purpose': req.purpose,
                        'priority': req.priority
                    } for req in self.current_plan.requirements
                ],
                'missing_info_count': len(self.current_plan.missing_info)
            }
            
            # Save to database
            conn.execute('''
                INSERT OR REPLACE INTO requirements_collection 
                (session_id, plan_data, responses, current_question, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                self.current_session_id,
                json.dumps(plan_data),
                json.dumps([asdict(resp) for resp in self.collected_responses]),
                0
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Error saving session state: {e}")
    
    def _load_session_state(self):
        """Load the session state from database"""
        try:
            if not self.current_session_id:
                return
            
            conn = get_db_connection()
            
            cursor = conn.execute('''
                SELECT plan_data, responses, current_question
                FROM requirements_collection
                WHERE session_id = ?
            ''', (self.current_session_id,))
            
            row = cursor.fetchone()
            if row:
                # Load plan data
                plan_data = json.loads(row[0])
                print(f"🔍 Loaded session state for {self.current_session_id}: {plan_data}")
                
                # Load responses
                if row[1]:
                    responses_data = json.loads(row[1])
                    self.collected_responses = [UserResponse(**resp) for resp in responses_data]
                
        except Exception as e:
            print(f"❌ Error loading session state: {e}")
    
    def _get_response_by_category(self, category: str) -> Optional[UserResponse]:
        """Get the most recent response for a specific category"""
        for response in reversed(self.collected_responses):
            if response.category == category:
                return response
        return None
    
    def _get_feedback(self, question: ClarificationQuestion, answer: str) -> str:
        """Generate feedback for the user's answer"""
        if question.category == "environment":
            return f"Great choice! {answer} is an excellent platform for your infrastructure."
        elif question.category == "performance":
            return f"Perfect! {answer} will help us configure the right resources for your needs."
        elif question.category == "security":
            return f"Excellent! {answer} will ensure your infrastructure meets security standards."
        elif question.category == "cost":
            return f"Good choice! {answer} will help us optimize your infrastructure costs."
        else:
            return f"Thank you for that information!"
    
    def _get_next_steps(self) -> List[str]:
        """Get the next steps based on current progress"""
        total_questions = len(self.current_plan.missing_info)
        answered_questions = len(getattr(self, 'user_answers', {}))
        
        if answered_questions >= total_questions:
            return [
                "✅ All requirements collected!",
                "🚀 Ready to generate infrastructure code",
                "🔧 Will customize based on your preferences"
            ]
        else:
            remaining = total_questions - answered_questions
            return [
                f"📝 {remaining} more question(s) to go",
                "💡 Your answers help us create the perfect infrastructure",
                "🎯 Almost there!"
            ]
    
    def validate_collection_state(self) -> Dict[str, Any]:
        """Validate the current requirements collection state and identify issues"""
        validation = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check if we have a current plan
        if not self.current_plan:
            validation['is_valid'] = False
            validation['issues'].append('No active infrastructure plan')
            validation['recommendations'].append('Start a new infrastructure creation request')
            return validation
        
        # Check if required_categories is set
        if not hasattr(self, 'required_categories') or not self.required_categories:
            validation['warnings'].append('Required categories not initialized')
            validation['recommendations'].append('Restart requirements collection')
        
        # Check if we have missing info questions
        if not hasattr(self.current_plan, 'missing_info') or not self.current_plan.missing_info:
            validation['warnings'].append('No missing information questions available')
            validation['recommendations'].append('Check infrastructure analysis')
        
        # Check collected responses
        if not self.collected_responses:
            validation['warnings'].append('No responses collected yet')
            validation['recommendations'].append('Start answering questions')
        
        return validation
    
    def _get_completion_status(self) -> Dict[str, Any]:
        """Get the completion status of requirements collection"""
        try:
            current_plan = self.get_current_plan()
            if not current_plan:
                return {
                    'is_complete': False,
                    'total_questions': 0,
                    'answered_questions': 0,
                    'completion_percentage': 0.0
                }
            
            total_questions = len(self.get_current_questions())
            answered_questions = len(getattr(self, 'user_answers', {}))
            
            completion_percentage = (answered_questions / total_questions * 100) if total_questions > 0 else 0.0
            is_complete = answered_questions >= total_questions
            
            return {
                'is_complete': is_complete,
                'total_questions': total_questions,
                'answered_questions': answered_questions,
                'completion_percentage': round(completion_percentage, 1)
            }
            
        except Exception as e:
            print(f"❌ Error getting completion status: {e}")
            return {
                'is_complete': False,
                'total_questions': 0,
                'answered_questions': 0,
                'completion_percentage': 0.0
            }
    
    def _get_intelligent_categories(self, original_request: str, pattern, environment) -> Dict[str, bool]:
        """Intelligently determine which requirement categories are needed based on the request"""
        request_lower = original_request.lower()
        pattern_lower = str(pattern.value).lower() if hasattr(pattern, 'value') else str(pattern).lower()
        environment_lower = str(environment.value).lower() if hasattr(environment, 'value') else str(environment).lower()
        
        # Default categories - all enabled
        categories = {
            'basic': True,
            'performance': True, 
            'security': True,
            'cost': True,
            'compliance': True,
            'advanced': True
        }
        
        # Pattern-specific category adjustments
        if 'serverless' in pattern_lower:
            # Serverless architectures need specific categories
            categories['performance'] = True  # Auto-scaling, cold starts
            categories['cost'] = True         # Pay-per-use optimization
            categories['security'] = True     # IAM, VPC, encryption
            categories['advanced'] = False    # Less complex than container-based
            
        elif 'container' in pattern_lower:
            # Container-based architectures need more advanced categories
            categories['advanced'] = True     # Orchestration, networking
            categories['performance'] = True  # Resource allocation, scaling
            categories['security'] = True     # Container security, network policies
            
        elif 'microservices' in pattern_lower:
            # Microservices need distributed system categories
            categories['advanced'] = True     # Service mesh, distributed tracing
            categories['performance'] = True  # Load balancing, caching
            categories['security'] = True     # Service-to-service auth
            
        elif 'three_tier' in pattern_lower:
            # Traditional three-tier needs balanced categories
            categories['basic'] = True        # Standard web app requirements
            categories['performance'] = True  # Load balancing, caching
            categories['security'] = True     # Network security, data protection
            
        # Environment-specific adjustments
        if 'hybrid' in environment_lower or 'multi-cloud' in environment_lower:
            categories['advanced'] = True     # Multi-cloud complexity
            categories['compliance'] = True   # Cross-provider compliance
            
        elif 'aws' in environment_lower:
            categories['security'] = True     # AWS security best practices
            categories['cost'] = True         # AWS cost optimization
            
        elif 'azure' in environment_lower:
            categories['compliance'] = True   # Azure compliance features
            categories['security'] = True     # Azure security features
            
        elif 'gcp' in environment_lower:
            categories['performance'] = True  # GCP performance features
            categories['cost'] = True         # GCP cost optimization
            
        # Request-specific adjustments
        if any(word in request_lower for word in ['security', 'compliance', 'audit', 'governance']):
            categories['security'] = True
            categories['compliance'] = True
            
        if any(word in request_lower for word in ['cost', 'budget', 'optimization', 'cheap']):
            categories['cost'] = True
            
        if any(word in request_lower for word in ['performance', 'scaling', 'high-availability', 'load']):
            categories['performance'] = True
            
        if any(word in request_lower for word in ['advanced', 'complex', 'enterprise', 'production']):
            categories['advanced'] = True
            
        return categories
    
    def get_intelligent_suggestions(self, user_input: str) -> List[str]:
        """Generate intelligent suggestions based on user input"""
        suggestions = []
        input_lower = user_input.lower()
        
        # Performance-related suggestions
        if any(word in input_lower for word in ['slow', 'performance', 'speed', 'latency']):
            suggestions.extend([
                "Consider using CloudFront CDN for global content delivery",
                "Implement auto-scaling for better performance under load",
                "Use read replicas for database performance",
                "Consider caching strategies (Redis, ElastiCache)"
            ])
        
        # Cost-related suggestions
        if any(word in input_lower for word in ['cost', 'budget', 'expensive', 'cheap', 'affordable']):
            suggestions.extend([
                "Use Spot Instances for non-critical workloads",
                "Implement S3 lifecycle policies for cost optimization",
                "Consider reserved instances for predictable workloads",
                "Use CloudWatch for cost monitoring and alerts"
            ])
        
        # Security-related suggestions
        if any(word in input_lower for word in ['security', 'secure', 'compliance', 'audit']):
            suggestions.extend([
                "Enable VPC flow logs for network monitoring",
                "Implement least-privilege IAM policies",
                "Use AWS Config for compliance monitoring",
                "Enable CloudTrail for API activity logging"
            ])
        
        # Scalability suggestions
        if any(word in input_lower for word in ['scale', 'growth', 'traffic', 'users']):
            suggestions.extend([
                "Design for horizontal scaling from the start",
                "Use load balancers for traffic distribution",
                "Implement database sharding strategies",
                "Consider microservices architecture for scalability"
            ])
        
        # Default suggestions if no specific keywords found
        if not suggestions:
            suggestions = [
                "Consider implementing monitoring and alerting",
                "Plan for disaster recovery and backup strategies",
                "Document your infrastructure for team collaboration",
                "Implement infrastructure as code for consistency"
            ]
        
        return suggestions[:4]  # Return top 4 suggestions
    
    def get_troubleshooting_guide(self) -> str:
        """Get a troubleshooting guide for common issues"""
        guide = """🔧 **REQUIREMENTS COLLECTION TROUBLESHOOTING GUIDE**

**Common Issues and Solutions:**

❓ **Issue: "System configuration error"**
   **Solution:** Restart the requirements collection by typing your infrastructure request again
   **Example:** "Create a serverless architecture with Lambda and DynamoDB"

❓ **Issue: "No active requirements collection"**
   **Solution:** Start a new infrastructure creation request
   **Example:** "Design a 3-tier web application infrastructure"

❓ **Issue: Questions not progressing**
   **Solution:** Use the command "proceed with defaults" to skip remaining questions
   **Alternative:** Type "requirements summary" to check current status

❓ **Issue: System component error**
   **Solution:** Restart the agent session completely
   **Alternative:** Try a different infrastructure request

**Quick Commands:**
   • `requirements summary` - Check current status
   • `proceed with defaults` - Skip remaining questions
   • `show plan` - Review current infrastructure plan
   • `modify plan` - Change infrastructure requirements

**Need Help?** Try starting over with a clear infrastructure request."""
        return guide
    
    def get_summary(self) -> str:
        """Get a summary of the current requirements collection status"""
        try:
            current_plan = self.get_current_plan()
            if not current_plan:
                return self._generate_no_plan_response()
            
            completion = self._get_completion_status()
            
            # Generate dynamic response based on actual plan data
            response = self._generate_dynamic_summary(current_plan, completion)
            
            return response
            
        except Exception as e:
            print(f"❌ Error in get_summary: {e}")
            return f"📋 **Requirements Collection Summary**\n\n⚠️ **Error retrieving summary:** {str(e)}\n\nPlease try again or restart the requirements collection."
    
    def _generate_no_plan_response(self) -> str:
        """Generate response when no active plan exists"""
        return "📋 **Requirements Collection Summary**\n\n⚠️ **No Active Requirements Collection**\n\nPlease start by requesting infrastructure creation:\n• 'Create a serverless architecture'\n• 'Design a 3-tier web application'\n• 'Build a microservices infrastructure'\n\n**Example:** 'Create a serverless architecture with Lambda and DynamoDB'"
    
    def _generate_dynamic_summary(self, plan, completion) -> str:
        """Generate a dynamic summary based on the actual plan data"""
        response = "📋 **Requirements Collection Summary**\n\n"
        
        # Pattern and Environment
        if hasattr(plan, 'pattern') and plan.pattern:
            pattern_name = plan.pattern.value.replace('_', ' ').title()
            response += f"🏗️ **Infrastructure Pattern:** {pattern_name}\n"
        else:
            response += "🏗️ **Infrastructure Pattern:** Unknown\n"
        
        if hasattr(plan, 'environment') and plan.environment:
            env_name = plan.environment.value.title()
            response += f"☁️ **Target Environment:** {env_name}\n"
        else:
            response += "☁️ **Target Environment:** Unknown\n"
        
        response += "\n"
        
        # Requirements - use actual data or generate appropriate defaults
        response += "🔧 **Identified Requirements:**\n"
        if hasattr(plan, 'requirements') and plan.requirements:
            for req in plan.requirements[:4]:  # Show first 4 requirements
                if hasattr(req, 'component') and hasattr(req, 'type') and hasattr(req, 'priority'):
                    response += f"   • {req.component}: {req.type} ({req.priority} priority)\n"
                else:
                    response += f"   • {str(req)}\n"
        else:
            # Generate appropriate defaults based on environment and pattern
            response += self._generate_default_requirements(plan)
        
        # Progress
        response += f"\n📝 **Progress:** {completion.get('completion_percentage', 0)}% complete "
        response += f"({completion.get('answered_questions', 0)}/{completion.get('total_questions', 0)} questions answered)\n\n"
        
        # Next steps based on completion status
        if completion.get('is_complete', False):
            response += self._generate_completion_next_steps()
        else:
            response += self._generate_incomplete_next_steps()
        
        return response
    
    def _generate_default_requirements(self, plan) -> str:
        """Generate appropriate default requirements based on plan data"""
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
        
        # Generic fallback
        return "   • Compute: Serverless Functions (high priority)\n   • Database: NoSQL Database (high priority)\n   • API Gateway: REST API Endpoints (high priority)\n   • Security: IAM/Identity Management (high priority)\n"
    
    def _generate_completion_next_steps(self) -> str:
        """Generate next steps when requirements are complete"""
        return "🎉 **All requirements collected!**\n\n**Next Steps:**\n• Type 'show implementation plan' to review the complete plan\n• Type 'proceed with implementation' to generate Terraform code\n"
    
    def _generate_incomplete_next_steps(self) -> str:
        """Generate next steps when requirements are incomplete"""
        return "💡 **Continue with:**\n• Answer the remaining questions\n• Type 'show requirements' to see the interface\n• Type 'proceed with defaults' to use recommended settings\n"

    def get_current_questions(self) -> List[str]:
        """Get the current questions for the active requirements collection"""
        current_plan = self.get_current_plan()
        if current_plan and hasattr(current_plan, 'missing_info'):
            return current_plan.missing_info
        return []

    def get_current_plan(self) -> Optional[InfrastructurePlan]:
        """Get the current plan for this session"""
        if not self.current_plan and self.current_session_id:
            self._load_session_state()
        return self.current_plan

    def _format_requirements_collection_interface(self, plan: InfrastructurePlan, questions: List[str]) -> str:
        """Format the requirements collection interface for the chat"""
        try:
            # Generate dynamic interface based on actual plan data
            response = self._generate_interface_header(plan)
            response += self._generate_progress_section(plan, questions)
            response += self._generate_questions_section(questions)
            response += self._generate_interaction_guide(plan)
            response += self._generate_quick_actions(plan)
            response += self._generate_goal_statement(plan)
            
            return response
            
        except Exception as e:
            print(f"❌ Error formatting requirements interface: {e}")
            return f"❌ Error displaying requirements interface: {str(e)}"
    
    def _generate_interface_header(self, plan) -> str:
        """Generate the interface header based on plan data"""
        response = "📋 **REQUIREMENTS COLLECTION INTERFACE**\n\n"
        response += "🏗️ **Current Infrastructure Plan:**\n"
        
        if hasattr(plan, 'pattern') and plan.pattern:
            pattern_name = plan.pattern.value.replace('_', ' ').title()
            response += f"   • **Pattern:** {pattern_name}\n"
        else:
            response += "   • **Pattern:** Unknown\n"
        
        if hasattr(plan, 'environment') and plan.environment:
            env_name = plan.environment.value.title()
            response += f"   • **Environment:** {env_name}\n"
        else:
            response += "   • **Environment:** Unknown\n"
        
        if hasattr(plan, 'estimated_cost') and plan.estimated_cost:
            response += f"   • **Estimated Cost:** {plan.estimated_cost}\n"
        else:
            response += "   • **Estimated Cost:** To be determined\n"
        
        response += "\n"
        return response
    
    def _generate_progress_section(self, plan, questions) -> str:
        """Generate the progress section"""
        total_questions = len(questions) if questions else 0
        response = f"📊 **Progress:** 0/{total_questions} questions answered\n"
        response += f"📈 **Completion:** 0% complete\n\n"
        return response
    
    def _generate_questions_section(self, questions) -> str:
        """Generate the questions section dynamically"""
        if not questions:
            return "❓ **No questions available at this time.**\n\n"
        
        response = "❓ **Questions to Answer:**\n"
        for i, question in enumerate(questions[:5], 1):  # Show first 5 questions
            if hasattr(question, 'question'):
                response += f"   **Q{i}:** {question.question}\n"
            else:
                response += f"   **Q{i}:** {str(question)}\n"
        
        if len(questions) > 5:
            response += f"   ... and {len(questions) - 5} more questions\n"
        
        response += "\n"
        return response
    
    def _generate_interaction_guide(self, plan) -> str:
        """Generate interaction guide based on plan context"""
        response = "💡 **How to Interact:**\n"
        response += "   • **Answer Questions:** Type 'answer 1 [your answer]' to respond\n"
        response += "   • **See Progress:** Type 'requirements summary' to check status\n"
        response += "   • **Use Defaults:** Type 'proceed with defaults' for recommended settings\n"
        
        # Add environment-specific guidance
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'hybrid':
                response += "   • **Modify Plan:** Type 'change to [pattern]' or 'I want [requirement]'\n"
                response += "   • **Cloud Selection:** Type 'prefer [cloud]' to set primary provider\n"
            else:
                response += "   • **Modify Plan:** Type 'change to [pattern]' or 'I want [requirement]'\n"
        
        response += "   • **Show Plan:** Type 'show implementation plan' to review\n\n"
        return response
    
    def _generate_quick_actions(self, plan) -> str:
        """Generate quick actions based on plan context"""
        response = "🚀 **Quick Actions:**\n"
        response += "   • Type 'answer 1 [your preference]' to start\n"
        response += "   • Type 'proceed with defaults' to skip questions\n"
        
        # Add environment-specific actions
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'hybrid':
                response += "   • Type 'multi-cloud setup' for cross-provider configuration\n"
                response += "   • Type 'cloud preference [aws/azure/gcp]' to set primary\n"
            else:
                response += "   • Type 'modify plan' to change requirements\n"
        
        response += "\n"
        return response
    
    def _generate_goal_statement(self, plan) -> str:
        """Generate goal statement based on plan context"""
        if hasattr(plan, 'environment') and plan.environment:
            env = plan.environment.value.lower()
            if env == 'hybrid':
                return "🎯 **Goal:** Complete requirements collection to generate your multi-cloud infrastructure!\n"
            else:
                return "🎯 **Goal:** Complete requirements collection to generate your infrastructure!\n"
        else:
            return "🎯 **Goal:** Complete requirements collection to generate your infrastructure!\n"

    def _format_single_question(self, question: ClarificationQuestion, question_num: int, total_questions: int, required_categories: Dict[str, bool]) -> str:
        """Format a single question for interactive display"""
        response = f"📋 **REQUIREMENTS COLLECTION - Question {question_num} of {total_questions}**\n\n"
        
        # Add progress bar
        progress_percent = (question_num - 1) / total_questions * 100
        response += f"📊 **Progress:** {progress_percent:.1f}% complete ({question_num-1}/{total_questions} answered)\n\n"
        
        # Format the question
        response += f"❓ **Question {question_num}:** {question.question}\n\n"
        
        # Add options if available
        if question.options:
            response += "**Available Options:**\n"
            for i, option in enumerate(question.options, 1):
                response += f"   {i}. {option}\n"
            response += "\n"
        
        # Add default if available
        if question.default:
            response += f"💡 **Default Value:** {question.default}\n\n"
        
        # Add category information
        if hasattr(question, 'category') and question.category:
            response += f"🏷️ **Category:** {question.category}\n\n"
        
        # Add interaction instructions
        response += "💬 **How to Answer:**\n"
        response += f"   • Type 'answer {question_num} [your response]' to answer this question\n"
        response += f"   • Type 'answer {question_num} default' to use the default value\n"
        response += f"   • Type 'skip' to skip this question for now\n"
        response += f"   • Type 'requirements summary' to see overall progress\n\n"
        
        # Add quick actions
        response += "🚀 **Quick Actions:**\n"
        response += "   • Type 'proceed with defaults' to answer all remaining questions with defaults\n"
        response += "   • Type 'show plan' to review current infrastructure plan\n"
        response += "   • Type 'modify plan' to change infrastructure requirements\n\n"
        
        return response

    def proceed_with_defaults(self) -> Dict[str, Any]:
        """Answer all remaining questions with default values"""
        try:
            current_plan = self.get_current_plan()
            if not current_plan:
                return {
                    'success': False,
                    'error': 'No active requirements collection session'
                }
            
            # Answer all remaining questions with defaults
            for i, question in enumerate(current_plan.missing_info):
                if i >= len(self.collected_responses):  # Not answered yet
                    default_answer = getattr(question, 'default', 'standard')
                    user_response = UserResponse(
                        question_id=str(i + 1),
                        answer=default_answer,
                        category=getattr(question, 'category', 'general'),
                        timestamp=str(datetime.now())
                    )
                    self.collected_responses.append(user_response)
            
            # Update session state
            self._save_session_state()
            
            return {
                'success': True,
                'message': '✅ All remaining questions answered with default values!',
                'completion_status': {
                    'is_complete': True,
                    'total_questions': len(current_plan.missing_info),
                    'answered_questions': len(current_plan.missing_info),
                    'completion_percentage': 100.0
                },
                'final_message': '🎉 **Requirements Collection Complete!**\n\nYour infrastructure plan is now ready for implementation with default values.',
                'next_steps': [
                    'Type "show implementation plan" to review your complete infrastructure plan',
                    'Type "proceed with implementation" to generate Terraform code',
                    'Type "modify plan" to make any final adjustments'
                ]
            }
            
        except Exception as e:
            print(f"❌ Error proceeding with defaults: {e}")
            return {
                'success': False,
                'error': f'Error proceeding with defaults: {str(e)}'
            }
