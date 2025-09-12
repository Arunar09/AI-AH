"""
Intelligence module for the AI-AH Platform.

This module provides local intelligence capabilities including:
- Knowledge base management
- Pattern recognition
- Decision making
- Response generation
- Enhanced NLP processing
- Vector search capabilities
"""

from .local_knowledge_base import LocalKnowledgeBase, KnowledgeEntry, InfrastructurePattern

# Optional imports for enhanced components
try:
    from ..nlp.enhanced_nlp_processor import EnhancedNLPProcessor, NLPResult, IntentPattern
    from ..search.vector_search import VectorSearchEngine, SearchResult, VectorIndex
    from ..data.data_processor import DataProcessor, DataSource, DataAnalysis
    ENHANCED_COMPONENTS_AVAILABLE = True
except ImportError as e:
    # Enhanced components not available, use fallback
    ENHANCED_COMPONENTS_AVAILABLE = False
    print(f"Warning: Enhanced components not available: {e}")

__all__ = [
    'LocalKnowledgeBase',
    'KnowledgeEntry', 
    'InfrastructurePattern'
]

if ENHANCED_COMPONENTS_AVAILABLE:
    __all__.extend([
        'EnhancedNLPProcessor',
        'NLPResult',
        'IntentPattern',
        'VectorSearchEngine',
        'SearchResult',
        'VectorIndex',
        'DataProcessor',
        'DataSource',
        'DataAnalysis'
    ])

