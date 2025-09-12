"""
Vector Search Module with FAISS Integration.

This module provides efficient vector similarity search capabilities using FAISS
for local, non-LLM semantic search and retrieval.
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import json
import pickle
import logging
from pathlib import Path

from ..base_platform import BasePlatformComponent, PlatformConfig, Task, ComponentStatus


@dataclass
class SearchResult:
    """Result of vector search."""
    id: str
    content: str
    score: float
    metadata: Dict[str, Any]


@dataclass
class VectorIndex:
    """Vector index configuration."""
    name: str
    dimension: int
    index_type: str  # flat, ivf, hnsw
    description: str
    created_at: datetime


class VectorSearchEngine(BasePlatformComponent):
    """
    Vector search engine using FAISS for semantic similarity search.
    
    Provides capabilities for:
    - Document indexing
    - Semantic search
    - Similarity retrieval
    - Infrastructure knowledge search
    """
    
    def __init__(self, config: PlatformConfig, index_path: str = "vector_index"):
        super().__init__(config)
        self.index_path = Path(index_path)
        self.index_path.mkdir(exist_ok=True)
        
        self.sentence_model = None
        self.indexes: Dict[str, faiss.Index] = {}
        self.document_store: Dict[str, Dict[str, Any]] = {}
        self.index_metadata: Dict[str, VectorIndex] = {}
        
        # Default embedding dimension for all-MiniLM-L6-v2
        self.embedding_dimension = 384
        
    async def initialize(self) -> bool:
        """Initialize the vector search engine."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info("Initializing Vector Search Engine")
            
            # Load Sentence Transformer model
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.logger.info("Loaded Sentence Transformer model for embeddings")
            except Exception as e:
                self.logger.error(f"Failed to load Sentence Transformer: {str(e)}")
                return False
            
            # Load existing indexes
            await self._load_existing_indexes()
            
            self.status = ComponentStatus.READY
            self.logger.info("Vector Search Engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Search Engine: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the vector search engine."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info("Vector Search Engine started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Vector Search Engine: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the vector search engine."""
        try:
            # Save indexes before stopping
            await self.save_indexes()
            self.status = ComponentStatus.STOPPED
            self.logger.info("Vector Search Engine stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop Vector Search Engine: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        return {
            "status": self.status.value,
            "sentence_model_loaded": self.sentence_model is not None,
            "indexes": len(self.indexes),
            "documents": len(self.document_store),
            "healthy": self.status == ComponentStatus.RUNNING
        }
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.task_type == "search":
            index_name = task.parameters.get("index_name", "")
            query = task.parameters.get("query", "")
            k = task.parameters.get("k", 10)
            return await self.search(index_name, query, k)
        elif task.task_type == "add_documents":
            index_name = task.parameters.get("index_name", "")
            documents = task.parameters.get("documents", [])
            return await self.add_documents(index_name, documents)
        return {"status": "completed", "task_id": task.id}
    
    async def _load_existing_indexes(self):
        """Load existing vector indexes from disk."""
        try:
            metadata_file = self.index_path / "index_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata_data = json.load(f)
                
                for index_name, metadata in metadata_data.items():
                    # Load index metadata
                    self.index_metadata[index_name] = VectorIndex(
                        name=metadata['name'],
                        dimension=metadata['dimension'],
                        index_type=metadata['index_type'],
                        description=metadata['description'],
                        created_at=datetime.fromisoformat(metadata['created_at'])
                    )
                    
                    # Load FAISS index
                    index_file = self.index_path / f"{index_name}.index"
                    if index_file.exists():
                        self.indexes[index_name] = faiss.read_index(str(index_file))
                        self.logger.info(f"Loaded index: {index_name}")
            
            # Load document store
            doc_store_file = self.index_path / "document_store.pkl"
            if doc_store_file.exists():
                with open(doc_store_file, 'rb') as f:
                    self.document_store = pickle.load(f)
                self.logger.info(f"Loaded {len(self.document_store)} documents")
                
        except Exception as e:
            self.logger.warning(f"Failed to load existing indexes: {str(e)}")
    
    async def create_index(self, name: str, index_type: str = "flat", description: str = "") -> bool:
        """Create a new vector index."""
        try:
            if name in self.indexes:
                self.logger.warning(f"Index {name} already exists")
                return False
            
            # Create FAISS index based on type
            if index_type == "flat":
                index = faiss.IndexFlatIP(self.embedding_dimension)  # Inner product for cosine similarity
            elif index_type == "ivf":
                quantizer = faiss.IndexFlatIP(self.embedding_dimension)
                index = faiss.IndexIVFFlat(quantizer, self.embedding_dimension, 100)
            elif index_type == "hnsw":
                index = faiss.IndexHNSWFlat(self.embedding_dimension, 32)
            else:
                self.logger.error(f"Unsupported index type: {index_type}")
                return False
            
            self.indexes[name] = index
            self.index_metadata[name] = VectorIndex(
                name=name,
                dimension=self.embedding_dimension,
                index_type=index_type,
                description=description,
                created_at=datetime.now()
            )
            
            self.logger.info(f"Created index: {name} (type: {index_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create index {name}: {str(e)}")
            return False
    
    async def add_documents(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to a vector index."""
        try:
            if index_name not in self.indexes:
                self.logger.error(f"Index {index_name} not found")
                return False
            
            if not self.sentence_model:
                self.logger.error("Sentence model not loaded")
                return False
            
            # Prepare documents
            texts = []
            doc_ids = []
            
            for doc in documents:
                doc_id = doc.get('id', f"doc_{len(self.document_store)}")
                content = doc.get('content', '')
                
                if not content:
                    continue
                
                texts.append(content)
                doc_ids.append(doc_id)
                
                # Store document metadata
                self.document_store[doc_id] = {
                    'content': content,
                    'metadata': doc.get('metadata', {}),
                    'index_name': index_name,
                    'added_at': datetime.now().isoformat()
                }
            
            if not texts:
                self.logger.warning("No valid documents to add")
                return False
            
            # Generate embeddings
            embeddings = self.sentence_model.encode(texts)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to index
            index = self.indexes[index_name]
            
            # Train index if needed (for IVF)
            if hasattr(index, 'is_trained') and not index.is_trained:
                if len(embeddings) >= 100:  # Minimum for training
                    index.train(embeddings)
                else:
                    self.logger.warning("Not enough documents for training IVF index")
            
            # Add vectors to index
            index.add(embeddings)
            
            self.logger.info(f"Added {len(texts)} documents to index {index_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add documents to {index_name}: {str(e)}")
            return False
    
    async def search(self, index_name: str, query: str, k: int = 10, 
                    score_threshold: float = 0.0) -> List[SearchResult]:
        """Search for similar documents in the index."""
        try:
            if index_name not in self.indexes:
                self.logger.error(f"Index {index_name} not found")
                return []
            
            if not self.sentence_model:
                self.logger.error("Sentence model not loaded")
                return []
            
            # Generate query embedding
            query_embedding = self.sentence_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search index
            index = self.indexes[index_name]
            scores, indices = index.search(query_embedding, k)
            
            # Convert to search results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:  # FAISS returns -1 for empty results
                    continue
                
                if score < score_threshold:
                    continue
                
                # Find document by index
                doc_id = self._find_document_by_index(index_name, idx)
                if doc_id and doc_id in self.document_store:
                    doc = self.document_store[doc_id]
                    results.append(SearchResult(
                        id=doc_id,
                        content=doc['content'],
                        score=float(score),
                        metadata=doc['metadata']
                    ))
            
            self.logger.info(f"Found {len(results)} results for query in {index_name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to search index {index_name}: {str(e)}")
            return []
    
    def _find_document_by_index(self, index_name: str, idx: int) -> Optional[str]:
        """Find document ID by index position."""
        # This is a simplified approach - in production, you'd want a more robust mapping
        count = 0
        for doc_id, doc in self.document_store.items():
            if doc.get('index_name') == index_name:
                if count == idx:
                    return doc_id
                count += 1
        return None
    
    async def search_across_indexes(self, query: str, k: int = 10, 
                                  score_threshold: float = 0.0) -> List[SearchResult]:
        """Search across all indexes."""
        all_results = []
        
        for index_name in self.indexes.keys():
            results = await self.search(index_name, query, k, score_threshold)
            all_results.extend(results)
        
        # Sort by score and return top k
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[:k]
    
    async def add_infrastructure_knowledge(self, knowledge_entries: List[Dict[str, Any]]) -> bool:
        """Add infrastructure knowledge to the search index."""
        try:
            # Ensure infrastructure index exists
            if "infrastructure" not in self.indexes:
                await self.create_index("infrastructure", "flat", "Infrastructure knowledge base")
            
            # Prepare documents
            documents = []
            for entry in knowledge_entries:
                doc = {
                    'id': entry.get('id', f"infra_{len(documents)}"),
                    'content': f"{entry.get('title', '')} {entry.get('content', '')}",
                    'metadata': {
                        'category': entry.get('category', ''),
                        'tags': entry.get('tags', []),
                        'confidence': entry.get('confidence', 0.0)
                    }
                }
                documents.append(doc)
            
            return await self.add_documents("infrastructure", documents)
            
        except Exception as e:
            self.logger.error(f"Failed to add infrastructure knowledge: {str(e)}")
            return False
    
    async def search_infrastructure_knowledge(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search infrastructure knowledge base."""
        return await self.search("infrastructure", query, k, score_threshold=0.3)
    
    async def save_indexes(self) -> bool:
        """Save indexes to disk."""
        try:
            # Save FAISS indexes
            for name, index in self.indexes.items():
                index_file = self.index_path / f"{name}.index"
                faiss.write_index(index, str(index_file))
            
            # Save metadata
            metadata_data = {}
            for name, metadata in self.index_metadata.items():
                metadata_data[name] = {
                    'name': metadata.name,
                    'dimension': metadata.dimension,
                    'index_type': metadata.index_type,
                    'description': metadata.description,
                    'created_at': metadata.created_at.isoformat()
                }
            
            metadata_file = self.index_path / "index_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata_data, f, indent=2)
            
            # Save document store
            doc_store_file = self.index_path / "document_store.pkl"
            with open(doc_store_file, 'wb') as f:
                pickle.dump(self.document_store, f)
            
            self.logger.info("Saved all indexes to disk")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save indexes: {str(e)}")
            return False
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """Get statistics for an index."""
        if index_name not in self.indexes:
            return {}
        
        index = self.indexes[index_name]
        metadata = self.index_metadata.get(index_name)
        
        # Count documents in this index
        doc_count = sum(1 for doc in self.document_store.values() 
                       if doc.get('index_name') == index_name)
        
        return {
            'name': index_name,
            'dimension': index.d,
            'total_vectors': index.ntotal,
            'document_count': doc_count,
            'index_type': metadata.index_type if metadata else 'unknown',
            'description': metadata.description if metadata else '',
            'created_at': metadata.created_at.isoformat() if metadata else None
        }
    
    def get_all_index_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all indexes."""
        return {name: self.get_index_stats(name) for name in self.indexes.keys()}
    
    async def delete_index(self, index_name: str) -> bool:
        """Delete an index and its documents."""
        try:
            if index_name not in self.indexes:
                self.logger.warning(f"Index {index_name} not found")
                return False
            
            # Remove documents from store
            docs_to_remove = [doc_id for doc_id, doc in self.document_store.items() 
                            if doc.get('index_name') == index_name]
            
            for doc_id in docs_to_remove:
                del self.document_store[doc_id]
            
            # Remove index
            del self.indexes[index_name]
            del self.index_metadata[index_name]
            
            # Remove files
            index_file = self.index_path / f"{index_name}.index"
            if index_file.exists():
                index_file.unlink()
            
            self.logger.info(f"Deleted index {index_name} and {len(docs_to_remove)} documents")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete index {index_name}: {str(e)}")
            return False
