"""
Intelligence module for the AI-AH Platform.

This module provides local intelligence capabilities including:
- Knowledge base management
- Pattern recognition
- Decision making
- Response generation
"""

from .local_knowledge_base import LocalKnowledgeBase, KnowledgeEntry, InfrastructurePattern

__all__ = [
    'LocalKnowledgeBase',
    'KnowledgeEntry', 
    'InfrastructurePattern'
]
