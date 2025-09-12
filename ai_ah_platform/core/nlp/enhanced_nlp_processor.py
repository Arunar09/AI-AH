"""
Enhanced Natural Language Processing Module with spaCy Integration.

This module provides advanced NLP capabilities using spaCy, NLTK, and
Sentence Transformers for local, non-LLM processing.
"""

import spacy
import nltk
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import re
import json
import logging
from pathlib import Path

from ..base_platform import BasePlatformComponent, PlatformConfig, Task, ComponentStatus


@dataclass
class NLPResult:
    """Results of NLP processing."""
    text: str
    intent: str
    entities: List[Dict[str, Any]]
    sentiment: Dict[str, float]
    keywords: List[str]
    embeddings: Optional[np.ndarray] = None
    confidence: float = 0.0
    processing_time: float = 0.0


@dataclass
class IntentPattern:
    """Intent recognition pattern."""
    name: str
    pattern: str
    confidence: float
    parameters: Dict[str, Any]


class EnhancedNLPProcessor(BasePlatformComponent):
    """
    Enhanced NLP processor with spaCy, NLTK, and Sentence Transformers.
    
    Provides advanced NLP capabilities for:
    - Intent recognition
    - Entity extraction
    - Sentiment analysis
    - Text similarity
    - Infrastructure-specific processing
    """
    
    def __init__(self, config: PlatformConfig):
        super().__init__(config)
        self.nlp_model = None
        self.sentence_model = None
        self.intent_patterns: List[IntentPattern] = []
        self.infrastructure_entities = set()
        
        # Download required NLTK data
        self._download_nltk_data()
        
    def _download_nltk_data(self):
        """Download required NLTK data."""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            self.logger.warning(f"Failed to download NLTK data: {str(e)}")
    
    async def initialize(self) -> bool:
        """Initialize the enhanced NLP processor."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info("Initializing Enhanced NLP Processor")
            
            # Load spaCy model
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
                self.logger.info("Loaded spaCy model: en_core_web_sm")
            except OSError:
                self.logger.warning("spaCy model not found, using basic processing")
                self.nlp_model = None
            
            # Load Sentence Transformer model
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.logger.info("Loaded Sentence Transformer model")
            except Exception as e:
                self.logger.warning(f"Failed to load Sentence Transformer: {str(e)}")
                self.sentence_model = None
            
            # Initialize infrastructure-specific patterns
            self._initialize_infrastructure_patterns()
            
            # Initialize infrastructure entities
            self._initialize_infrastructure_entities()
            
            self.status = ComponentStatus.READY
            self.logger.info("Enhanced NLP Processor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Enhanced NLP Processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the enhanced NLP processor."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info("Enhanced NLP Processor started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Enhanced NLP Processor: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the enhanced NLP processor."""
        try:
            self.status = ComponentStatus.STOPPED
            self.logger.info("Enhanced NLP Processor stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop Enhanced NLP Processor: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return {
            "status": self.status.value,
            "spacy_loaded": self.nlp_model is not None,
            "sentence_model_loaded": self.sentence_model is not None,
            "intent_patterns": len(self.intent_patterns),
            "infrastructure_entities": len(self.infrastructure_entities),
            "healthy": self.status == ComponentStatus.RUNNING
        }
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.task_type == "process_text":
            text = task.parameters.get("text", "")
            return self.process_text(text)
        elif task.task_type == "calculate_similarity":
            text1 = task.parameters.get("text1", "")
            text2 = task.parameters.get("text2", "")
            return {"similarity": self.calculate_similarity(text1, text2)}
        return {"status": "completed", "task_id": task.id}
    
    def _initialize_infrastructure_patterns(self):
        """Initialize infrastructure-specific intent patterns."""
        self.intent_patterns = [
            IntentPattern(
                name="create_infrastructure",
                pattern=r"(create|build|deploy|setup|provision).*(infrastructure|infra|resources|services)",
                confidence=0.9,
                parameters={"action": "create", "domain": "infrastructure"}
            ),
            IntentPattern(
                name="modify_infrastructure",
                pattern=r"(modify|update|change|edit|scale).*(infrastructure|infra|resources|services)",
                confidence=0.9,
                parameters={"action": "modify", "domain": "infrastructure"}
            ),
            IntentPattern(
                name="delete_infrastructure",
                pattern=r"(delete|remove|destroy|teardown).*(infrastructure|infra|resources|services)",
                confidence=0.9,
                parameters={"action": "delete", "domain": "infrastructure"}
            ),
            IntentPattern(
                name="monitor_infrastructure",
                pattern=r"(monitor|watch|observe|track).*(infrastructure|infra|resources|services|performance)",
                confidence=0.9,
                parameters={"action": "monitor", "domain": "infrastructure"}
            ),
            IntentPattern(
                name="troubleshoot",
                pattern=r"(troubleshoot|debug|fix|resolve|diagnose).*(issue|problem|error|failure)",
                confidence=0.9,
                parameters={"action": "troubleshoot", "domain": "support"}
            ),
            IntentPattern(
                name="cost_optimization",
                pattern=r"(optimize|reduce|minimize|save).*(cost|budget|expense|money)",
                confidence=0.9,
                parameters={"action": "optimize", "domain": "cost"}
            ),
            IntentPattern(
                name="security_analysis",
                pattern=r"(secure|security|vulnerability|threat|compliance).*(analysis|audit|check)",
                confidence=0.9,
                parameters={"action": "analyze", "domain": "security"}
            ),
            IntentPattern(
                name="performance_analysis",
                pattern=r"(performance|optimize|speed|latency|throughput).*(analysis|improvement|tuning)",
                confidence=0.9,
                parameters={"action": "analyze", "domain": "performance"}
            )
        ]
    
    def _initialize_infrastructure_entities(self):
        """Initialize infrastructure-specific entity vocabulary."""
        self.infrastructure_entities = {
            # Cloud Providers
            'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 'google cloud',
            'digitalocean', 'linode', 'vultr', 'heroku',
            
            # Infrastructure Components
            'ec2', 's3', 'rds', 'lambda', 'vpc', 'subnet', 'security group',
            'kubernetes', 'k8s', 'docker', 'container', 'pod', 'service',
            'terraform', 'ansible', 'puppet', 'chef',
            'nginx', 'apache', 'load balancer', 'api gateway',
            
            # Monitoring Tools
            'prometheus', 'grafana', 'elk', 'elasticsearch', 'logstash', 'kibana',
            'jaeger', 'zipkin', 'newrelic', 'datadog', 'splunk',
            
            # Databases
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'dynamodb', 'cassandra', 'influxdb',
            
            # Security
            'ssl', 'tls', 'certificate', 'firewall', 'vpn', 'iam', 'rbac',
            'oauth', 'jwt', 'encryption', 'hashing'
        }
    
    def process_text(self, text: str) -> NLPResult:
        """Process text with enhanced NLP capabilities."""
        start_time = datetime.now()
        
        try:
            # Basic text preprocessing
            processed_text = self._preprocess_text(text)
            
            # Intent recognition
            intent = self._recognize_intent(processed_text)
            
            # Entity extraction
            entities = self._extract_entities(processed_text)
            
            # Sentiment analysis
            sentiment = self._analyze_sentiment(processed_text)
            
            # Keyword extraction
            keywords = self._extract_keywords(processed_text)
            
            # Generate embeddings
            embeddings = self._generate_embeddings(processed_text)
            
            # Calculate confidence
            confidence = self._calculate_confidence(intent, entities, keywords)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return NLPResult(
                text=processed_text,
                intent=intent,
                entities=entities,
                sentiment=sentiment,
                keywords=keywords,
                embeddings=embeddings,
                confidence=confidence,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Failed to process text: {str(e)}")
            return NLPResult(
                text=text,
                intent="unknown",
                entities=[],
                sentiment={"positive": 0.0, "negative": 0.0, "neutral": 1.0},
                keywords=[],
                confidence=0.0,
                processing_time=0.0
            )
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better analysis."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep infrastructure terms
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        
        return text
    
    def _recognize_intent(self, text: str) -> str:
        """Recognize intent using pattern matching and spaCy."""
        best_intent = "unknown"
        best_confidence = 0.0
        
        # Pattern-based intent recognition
        for pattern in self.intent_patterns:
            if re.search(pattern.pattern, text, re.IGNORECASE):
                if pattern.confidence > best_confidence:
                    best_intent = pattern.name
                    best_confidence = pattern.confidence
        
        # spaCy-based intent recognition (if available)
        if self.nlp_model:
            doc = self.nlp_model(text)
            
            # Check for action verbs
            action_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
            infrastructure_terms = [token.text for token in doc if token.text in self.infrastructure_entities]
            
            if action_verbs and infrastructure_terms:
                # Boost confidence for infrastructure-related actions
                best_confidence = min(best_confidence + 0.1, 1.0)
        
        return best_intent
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using spaCy and custom patterns."""
        entities = []
        
        # spaCy entity extraction
        if self.nlp_model:
            doc = self.nlp_model(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 0.8
                })
        
        # Custom infrastructure entity extraction
        for entity in self.infrastructure_entities:
            if entity in text:
                start_pos = text.find(entity)
                if start_pos != -1:
                    entities.append({
                        "text": entity,
                        "label": "INFRASTRUCTURE",
                        "start": start_pos,
                        "end": start_pos + len(entity),
                        "confidence": 0.9
                    })
        
        # Remove duplicates
        unique_entities = []
        seen_texts = set()
        for entity in entities:
            if entity["text"] not in seen_texts:
                unique_entities.append(entity)
                seen_texts.add(entity["text"])
        
        return unique_entities
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using NLTK VADER."""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            
            return {
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "compound": scores["compound"]
            }
        except Exception as e:
            self.logger.warning(f"Sentiment analysis failed: {str(e)}")
            return {"positive": 0.0, "negative": 0.0, "neutral": 1.0, "compound": 0.0}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords using NLTK and custom logic."""
        try:
            from nltk.corpus import stopwords
            from nltk.tokenize import word_tokenize
            from nltk.tag import pos_tag
            
            # Tokenize and tag
            tokens = word_tokenize(text)
            tagged_tokens = pos_tag(tokens)
            
            # Filter for meaningful words
            stop_words = set(stopwords.words('english'))
            keywords = []
            
            for word, tag in tagged_tokens:
                if (word.lower() not in stop_words and 
                    len(word) > 2 and 
                    tag in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
                    keywords.append(word.lower())
            
            # Add infrastructure-specific terms
            for entity in self.infrastructure_entities:
                if entity in text and entity not in keywords:
                    keywords.append(entity)
            
            return list(set(keywords))  # Remove duplicates
            
        except Exception as e:
            self.logger.warning(f"Keyword extraction failed: {str(e)}")
            return text.split()[:10]  # Fallback to simple word splitting
    
    def _generate_embeddings(self, text: str) -> Optional[np.ndarray]:
        """Generate text embeddings using Sentence Transformers."""
        if self.sentence_model:
            try:
                embeddings = self.sentence_model.encode([text])
                return embeddings[0]
            except Exception as e:
                self.logger.warning(f"Embedding generation failed: {str(e)}")
        return None
    
    def _calculate_confidence(self, intent: str, entities: List[Dict], keywords: List[str]) -> float:
        """Calculate confidence score for the analysis."""
        confidence = 0.0
        
        # Intent confidence
        if intent != "unknown":
            confidence += 0.4
        
        # Entity confidence
        if entities:
            confidence += 0.3
        
        # Keyword confidence
        if keywords:
            confidence += 0.2
        
        # Infrastructure-specific boost
        infrastructure_entities = [e for e in entities if e.get("label") == "INFRASTRUCTURE"]
        if infrastructure_entities:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        if self.sentence_model:
            try:
                embeddings1 = self.sentence_model.encode([text1])
                embeddings2 = self.sentence_model.encode([text2])
                
                # Calculate cosine similarity
                similarity = np.dot(embeddings1[0], embeddings2[0]) / (
                    np.linalg.norm(embeddings1[0]) * np.linalg.norm(embeddings2[0])
                )
                return float(similarity)
            except Exception as e:
                self.logger.warning(f"Similarity calculation failed: {str(e)}")
        
        # Fallback to simple word overlap
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0.0
    
    def find_similar_queries(self, query: str, query_list: List[str], threshold: float = 0.7) -> List[Tuple[str, float]]:
        """Find similar queries from a list."""
        similar_queries = []
        
        for other_query in query_list:
            similarity = self.calculate_similarity(query, other_query)
            if similarity >= threshold:
                similar_queries.append((other_query, similarity))
        
        # Sort by similarity score
        similar_queries.sort(key=lambda x: x[1], reverse=True)
        return similar_queries
    
    def generate_nlp_report(self, result: NLPResult) -> str:
        """Generate a human-readable NLP analysis report."""
        report_parts = [
            f"# NLP Analysis Report",
            f"**Text**: {result.text}",
            f"**Processing Time**: {result.processing_time:.3f}s",
            f"**Confidence**: {result.confidence:.2f}",
            "",
            "## Intent Recognition",
            f"**Detected Intent**: {result.intent}",
            "",
            "## Entity Extraction",
        ]
        
        if result.entities:
            for entity in result.entities:
                report_parts.append(f"- **{entity['text']}** ({entity['label']}) - Confidence: {entity['confidence']:.2f}")
        else:
            report_parts.append("No entities detected")
        
        report_parts.extend([
            "",
            "## Sentiment Analysis",
            f"- **Positive**: {result.sentiment['positive']:.2f}",
            f"- **Negative**: {result.sentiment['negative']:.2f}",
            f"- **Neutral**: {result.sentiment['neutral']:.2f}",
            f"- **Compound**: {result.sentiment['compound']:.2f}",
            "",
            "## Keywords",
            ", ".join(result.keywords) if result.keywords else "No keywords extracted"
        ])
        
        return "\n".join(report_parts)
