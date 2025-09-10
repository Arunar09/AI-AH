"""
Natural Language Processing components for the Multi-Agent Infrastructure Intelligence Platform.

This module provides NLP capabilities for understanding user requests,
extracting requirements, and generating natural language responses.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import re
import json
from enum import Enum

from ..base_platform import BasePlatformComponent, PlatformConfig, Task


class IntentType(Enum):
    """Types of user intents."""
    CREATE_INFRASTRUCTURE = "create_infrastructure"
    MODIFY_INFRASTRUCTURE = "modify_infrastructure"
    DELETE_INFRASTRUCTURE = "delete_infrastructure"
    MONITOR_INFRASTRUCTURE = "monitor_infrastructure"
    TROUBLESHOOT = "troubleshoot"
    GET_STATUS = "get_status"
    GET_HELP = "get_help"
    UNKNOWN = "unknown"


class EntityType(Enum):
    """Types of entities in user requests."""
    CLOUD_PROVIDER = "cloud_provider"
    SERVICE = "service"
    RESOURCE_TYPE = "resource_type"
    REGION = "region"
    SIZE = "size"
    QUANTITY = "quantity"
    ENVIRONMENT = "environment"
    APPLICATION = "application"
    DATABASE = "database"
    NETWORK = "network"
    SECURITY = "security"
    MONITORING = "monitoring"


@dataclass
class Intent:
    """Represents a detected intent."""
    type: IntentType
    confidence: float
    parameters: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Entity:
    """Represents an extracted entity."""
    type: EntityType
    value: str
    confidence: float
    start_pos: int
    end_pos: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedRequest:
    """Represents a parsed user request."""
    original_text: str
    intent: Intent
    entities: List[Entity]
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class NaturalLanguageProcessor(BasePlatformComponent):
    """
    Natural Language Processor for understanding user requests.
    
    Provides intent recognition, entity extraction, and requirement parsing
    for infrastructure-related requests.
    """
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        
        # Intent patterns
        self.intent_patterns = {
            IntentType.CREATE_INFRASTRUCTURE: [
                r"create", r"deploy", r"provision", r"set up", r"build",
                r"launch", r"spin up", r"initialize"
            ],
            IntentType.MODIFY_INFRASTRUCTURE: [
                r"modify", r"update", r"change", r"edit", r"adjust",
                r"scale", r"resize", r"upgrade", r"downgrade"
            ],
            IntentType.DELETE_INFRASTRUCTURE: [
                r"delete", r"remove", r"destroy", r"tear down",
                r"clean up", r"terminate"
            ],
            IntentType.MONITOR_INFRASTRUCTURE: [
                r"monitor", r"watch", r"observe", r"track", r"check",
                r"status", r"health", r"metrics"
            ],
            IntentType.TROUBLESHOOT: [
                r"fix", r"resolve", r"troubleshoot", r"debug", r"error",
                r"issue", r"problem", r"broken"
            ],
            IntentType.GET_STATUS: [
                r"status", r"state", r"condition", r"health", r"running"
            ],
            IntentType.GET_HELP: [
                r"help", r"assist", r"guide", r"how to", r"what is"
            ]
        }
        
        # Entity patterns
        self.entity_patterns = {
            EntityType.CLOUD_PROVIDER: [
                r"aws", r"amazon web services", r"azure", r"microsoft azure",
                r"gcp", r"google cloud", r"digital ocean", r"linode"
            ],
            EntityType.SERVICE: [
                r"ec2", r"lambda", r"s3", r"rds", r"vpc", r"iam",
                r"kubernetes", r"docker", r"terraform", r"ansible"
            ],
            EntityType.RESOURCE_TYPE: [
                r"server", r"instance", r"database", r"load balancer",
                r"storage", r"network", r"security group", r"subnet"
            ],
            EntityType.REGION: [
                r"us-east-1", r"us-west-2", r"eu-west-1", r"ap-southeast-1",
                r"eastus", r"westus2", r"westeurope", r"eastasia"
            ],
            EntityType.SIZE: [
                r"small", r"medium", r"large", r"xlarge", r"micro",
                r"t2\.micro", r"t3\.small", r"m5\.large", r"c5\.xlarge"
            ],
            EntityType.QUANTITY: [
                r"\d+", r"one", r"two", r"three", r"four", r"five",
                r"several", r"multiple", r"few", r"many"
            ],
            EntityType.ENVIRONMENT: [
                r"development", r"dev", r"staging", r"production", r"prod",
                r"test", r"testing", r"qa", r"preprod"
            ],
            EntityType.APPLICATION: [
                r"web app", r"api", r"microservice", r"frontend", r"backend",
                r"application", r"service", r"app"
            ],
            EntityType.DATABASE: [
                r"mysql", r"postgresql", r"mongodb", r"redis", r"elasticsearch",
                r"database", r"db", r"sql", r"nosql"
            ],
            EntityType.NETWORK: [
                r"vpc", r"subnet", r"security group", r"load balancer",
                r"nat gateway", r"internet gateway", r"route table"
            ],
            EntityType.SECURITY: [
                r"ssl", r"tls", r"certificate", r"encryption", r"firewall",
                r"access control", r"permissions", r"roles"
            ],
            EntityType.MONITORING: [
                r"cloudwatch", r"prometheus", r"grafana", r"datadog",
                r"monitoring", r"logging", r"alerting", r"metrics"
            ]
        }
        
        # Compile patterns for efficiency
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficiency."""
        self.compiled_intent_patterns = {}
        for intent_type, patterns in self.intent_patterns.items():
            self.compiled_intent_patterns[intent_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        
        self.compiled_entity_patterns = {}
        for entity_type, patterns in self.entity_patterns.items():
            self.compiled_entity_patterns[entity_type] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    async def initialize(self) -> bool:
        """Initialize the NLP processor."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info("Initializing Natural Language Processor")
            
            # Initialize any required models or services
            await self._initialize_models()
            
            self.status = ComponentStatus.READY
            self.logger.info("Natural Language Processor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize NLP processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the NLP processor."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info("Natural Language Processor started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start NLP processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the NLP processor."""
        try:
            self.status = ComponentStatus.STOPPED
            self.logger.info("Natural Language Processor stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop NLP processor: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the NLP processor."""
        return {
            "status": self.status.value,
            "intent_patterns": len(self.intent_patterns),
            "entity_patterns": len(self.entity_patterns),
            "last_check": datetime.now().isoformat()
        }
    
    async def parse_request(self, text: str) -> ParsedRequest:
        """Parse a user request and extract intent and entities."""
        try:
            # Detect intent
            intent = await self._detect_intent(text)
            
            # Extract entities
            entities = await self._extract_entities(text)
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(intent, entities)
            
            return ParsedRequest(
                original_text=text,
                intent=intent,
                entities=entities,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing request: {str(e)}")
            return ParsedRequest(
                original_text=text,
                intent=Intent(IntentType.UNKNOWN, 0.0),
                entities=[],
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def _detect_intent(self, text: str) -> Intent:
        """Detect the intent from the text."""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent_type, patterns in self.compiled_intent_patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if pattern.search(text_lower):
                    matches += 1
                    score += 1.0
            
            if matches > 0:
                intent_scores[intent_type] = score / len(patterns)
        
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return Intent(
                type=best_intent[0],
                confidence=best_intent[1],
                parameters=self._extract_intent_parameters(text, best_intent[0])
            )
        else:
            return Intent(IntentType.UNKNOWN, 0.0)
    
    async def _extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from the text."""
        entities = []
        text_lower = text.lower()
        
        for entity_type, patterns in self.compiled_entity_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text_lower):
                    entity = Entity(
                        type=entity_type,
                        value=match.group(),
                        confidence=0.8,  # Could be improved with ML models
                        start_pos=match.start(),
                        end_pos=match.end(),
                        metadata={"pattern": pattern.pattern}
                    )
                    entities.append(entity)
        
        return entities
    
    def _calculate_confidence(self, intent: Intent, entities: List[Entity]) -> float:
        """Calculate overall confidence for the parsed request."""
        intent_weight = 0.7
        entity_weight = 0.3
        
        intent_score = intent.confidence * intent_weight
        entity_score = (sum(e.confidence for e in entities) / max(len(entities), 1)) * entity_weight
        
        return min(intent_score + entity_score, 1.0)
    
    def _extract_intent_parameters(self, text: str, intent_type: IntentType) -> Dict[str, Any]:
        """Extract parameters specific to the intent type."""
        parameters = {}
        
        if intent_type == IntentType.CREATE_INFRASTRUCTURE:
            parameters.update(self._extract_creation_parameters(text))
        elif intent_type == IntentType.MODIFY_INFRASTRUCTURE:
            parameters.update(self._extract_modification_parameters(text))
        elif intent_type == IntentType.DELETE_INFRASTRUCTURE:
            parameters.update(self._extract_deletion_parameters(text))
        elif intent_type == IntentType.MONITOR_INFRASTRUCTURE:
            parameters.update(self._extract_monitoring_parameters(text))
        
        return parameters
    
    def _extract_creation_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters for infrastructure creation."""
        parameters = {}
        
        # Extract quantity
        quantity_match = re.search(r'(\d+)\s+(?:instances?|servers?|resources?)', text, re.IGNORECASE)
        if quantity_match:
            parameters["quantity"] = int(quantity_match.group(1))
        
        # Extract environment
        env_match = re.search(r'(development|dev|staging|production|prod|test)', text, re.IGNORECASE)
        if env_match:
            parameters["environment"] = env_match.group(1).lower()
        
        return parameters
    
    def _extract_modification_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters for infrastructure modification."""
        parameters = {}
        
        # Extract scaling information
        scale_match = re.search(r'scale\s+(up|down|out|in)', text, re.IGNORECASE)
        if scale_match:
            parameters["scale_direction"] = scale_match.group(1)
        
        # Extract size information
        size_match = re.search(r'(small|medium|large|xlarge|micro)', text, re.IGNORECASE)
        if size_match:
            parameters["size"] = size_match.group(1).lower()
        
        return parameters
    
    def _extract_deletion_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters for infrastructure deletion."""
        parameters = {}
        
        # Extract confirmation
        confirm_match = re.search(r'(yes|confirm|sure|delete)', text, re.IGNORECASE)
        if confirm_match:
            parameters["confirmed"] = True
        
        return parameters
    
    def _extract_monitoring_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters for monitoring requests."""
        parameters = {}
        
        # Extract time range
        time_match = re.search(r'(last|past|previous)\s+(\d+)\s+(hours?|days?|weeks?)', text, re.IGNORECASE)
        if time_match:
            parameters["time_range"] = {
                "value": int(time_match.group(2)),
                "unit": time_match.group(3).lower()
            }
        
        return parameters
    
    async def _initialize_models(self):
        """Initialize any required ML models or services."""
        # This could be extended to load pre-trained models
        # For now, we use rule-based approaches
        pass
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.name == "parse_request":
            return await self.parse_request(task.metadata.get("text", ""))
        else:
            return {"status": "unknown_task", "task_id": task.id}
    
    def generate_response(self, parsed_request: ParsedRequest, 
                         context: Dict[str, Any] = None) -> str:
        """Generate a natural language response based on parsed request."""
        intent = parsed_request.intent
        entities = parsed_request.entities
        
        if intent.type == IntentType.CREATE_INFRASTRUCTURE:
            return self._generate_creation_response(intent, entities, context)
        elif intent.type == IntentType.MODIFY_INFRASTRUCTURE:
            return self._generate_modification_response(intent, entities, context)
        elif intent.type == IntentType.DELETE_INFRASTRUCTURE:
            return self._generate_deletion_response(intent, entities, context)
        elif intent.type == IntentType.MONITOR_INFRASTRUCTURE:
            return self._generate_monitoring_response(intent, entities, context)
        elif intent.type == IntentType.TROUBLESHOOT:
            return self._generate_troubleshooting_response(intent, entities, context)
        elif intent.type == IntentType.GET_HELP:
            return self._generate_help_response(intent, entities, context)
        else:
            return "I understand you need help with infrastructure. Could you please provide more details about what you'd like to do?"
    
    def _generate_creation_response(self, intent: Intent, entities: List[Entity], 
                                  context: Dict[str, Any] = None) -> str:
        """Generate response for infrastructure creation requests."""
        cloud_providers = [e.value for e in entities if e.type == EntityType.CLOUD_PROVIDER]
        services = [e.value for e in entities if e.type == EntityType.SERVICE]
        
        response = "I'll help you create the infrastructure. "
        
        if cloud_providers:
            response += f"I see you want to use {', '.join(cloud_providers)}. "
        
        if services:
            response += f"You mentioned {', '.join(services)}. "
        
        response += "Let me gather some additional requirements to create the best solution for you."
        
        return response
    
    def _generate_modification_response(self, intent: Intent, entities: List[Entity], 
                                      context: Dict[str, Any] = None) -> str:
        """Generate response for infrastructure modification requests."""
        return "I'll help you modify your infrastructure. Let me analyze the current setup and propose the best changes."
    
    def _generate_deletion_response(self, intent: Intent, entities: List[Entity], 
                                  context: Dict[str, Any] = None) -> str:
        """Generate response for infrastructure deletion requests."""
        return "I'll help you safely remove the infrastructure. Let me first show you what will be deleted and get your confirmation."
    
    def _generate_monitoring_response(self, intent: Intent, entities: List[Entity], 
                                    context: Dict[str, Any] = None) -> str:
        """Generate response for monitoring requests."""
        return "I'll help you set up monitoring for your infrastructure. Let me show you the current status and available monitoring options."
    
    def _generate_troubleshooting_response(self, intent: Intent, entities: List[Entity], 
                                         context: Dict[str, Any] = None) -> str:
        """Generate response for troubleshooting requests."""
        return "I'll help you troubleshoot the issue. Let me analyze the problem and provide solutions."
    
    def _generate_help_response(self, intent: Intent, entities: List[Entity], 
                              context: Dict[str, Any] = None) -> str:
        """Generate response for help requests."""
        return "I'm here to help with your infrastructure needs. I can assist with creating, modifying, monitoring, and troubleshooting your infrastructure."
