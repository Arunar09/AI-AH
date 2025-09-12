"""
Search module for the AI-AH Platform.

This module provides advanced search capabilities including:
- Vector similarity search with FAISS
- Semantic search and retrieval
- Infrastructure knowledge search
- Document indexing and search
"""

from .vector_search import VectorSearchEngine, SearchResult, VectorIndex

__all__ = [
    'VectorSearchEngine',
    'SearchResult',
    'VectorIndex'
]

