"""
Memory Management System for the Multi-Agent Infrastructure Intelligence Platform.

This module provides advanced memory management capabilities including
episodic memory, semantic memory, and knowledge graph integration.
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import asyncio
from enum import Enum
import sqlite3
import threading
from collections import defaultdict

from ..base_platform import BasePlatformComponent, PlatformConfig, Task


class MemoryType(Enum):
    """Types of memory storage."""
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # General knowledge and facts
    PROCEDURAL = "procedural"  # How to do things
    WORKING = "working"  # Temporary information
    LONG_TERM = "long_term"  # Persistent knowledge
    SHORT_TERM = "short_term"  # Recent information


class MemoryPriority(Enum):
    """Priority levels for memory retention."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    ESSENTIAL = 5


@dataclass
class Memory:
    """Represents a memory item."""
    id: str
    type: MemoryType
    content: Any
    priority: MemoryPriority
    importance: float  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    relationships: List[str] = field(default_factory=list)  # IDs of related memories
    decay_rate: float = 0.1  # How quickly this memory fades
    ttl: Optional[timedelta] = None  # Time to live


@dataclass
class MemoryQuery:
    """Query for searching memories."""
    tags: List[str] = field(default_factory=list)
    memory_types: List[MemoryType] = field(default_factory=list)
    min_importance: float = 0.0
    max_age: Optional[timedelta] = None
    limit: int = 10
    include_content: bool = True


@dataclass
class MemoryStats:
    """Statistics about memory usage."""
    total_memories: int
    memories_by_type: Dict[MemoryType, int]
    memories_by_priority: Dict[MemoryPriority, int]
    average_importance: float
    oldest_memory: Optional[datetime]
    newest_memory: Optional[datetime]
    total_access_count: int


class MemoryManager(BasePlatformComponent):
    """
    Advanced Memory Manager for the platform.
    
    Provides sophisticated memory management with different memory types,
    automatic decay, relationship tracking, and intelligent retrieval.
    """
    
    def __init__(self, config: PlatformConfig, db_path: str = "memory.db"):
        super().__init__(config)
        self.db_path = db_path
        self.memories: Dict[str, Memory] = {}
        self.memory_index: Dict[str, List[str]] = defaultdict(list)  # tag -> memory_ids
        self.relationship_graph: Dict[str, List[str]] = defaultdict(list)  # memory_id -> related_ids
        self.access_patterns: Dict[str, List[datetime]] = defaultdict(list)
        self.lock = threading.RLock()
        
        # Memory decay settings
        self.decay_enabled = True
        self.decay_interval = timedelta(hours=1)
        self.last_decay = datetime.now()
        
        # Memory limits
        self.max_memories = 10000
        self.max_working_memories = 100
        self.max_short_term_memories = 1000
    
    async def initialize(self) -> bool:
        """Initialize the memory manager."""
        try:
            self.status = ComponentStatus.INITIALIZING
            self.logger.info("Initializing Memory Manager")
            
            # Initialize database
            await self._initialize_database()
            
            # Load existing memories
            await self._load_memories()
            
            # Start decay process
            if self.decay_enabled:
                asyncio.create_task(self._decay_process())
            
            self.status = ComponentStatus.READY
            self.logger.info("Memory Manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Memory Manager: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def start(self) -> bool:
        """Start the memory manager."""
        try:
            self.status = ComponentStatus.RUNNING
            self.logger.info("Memory Manager started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start Memory Manager: {str(e)}")
            self.status = ComponentStatus.ERROR
            return False
    
    async def stop(self) -> bool:
        """Stop the memory manager."""
        try:
            # Save all memories
            await self._save_memories()
            
            self.status = ComponentStatus.STOPPED
            self.logger.info("Memory Manager stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop Memory Manager: {str(e)}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the memory manager."""
        with self.lock:
            stats = self._calculate_stats()
            return {
                "status": self.status.value,
                "total_memories": stats.total_memories,
                "memories_by_type": {t.value: c for t, c in stats.memories_by_type.items()},
                "memories_by_priority": {p.value: c for p, c in stats.memories_by_priority.items()},
                "average_importance": stats.average_importance,
                "last_decay": self.last_decay.isoformat(),
                "last_check": datetime.now().isoformat()
            }
    
    async def store_memory(self, content: Any, memory_type: MemoryType,
                          priority: MemoryPriority = MemoryPriority.NORMAL,
                          importance: float = 0.5, tags: List[str] = None,
                          metadata: Dict[str, Any] = None,
                          ttl: Optional[timedelta] = None) -> str:
        """Store a memory item."""
        with self.lock:
            memory_id = str(uuid.uuid4())
            memory = Memory(
                id=memory_id,
                type=memory_type,
                content=content,
                priority=priority,
                importance=importance,
                tags=tags or [],
                metadata=metadata or {},
                ttl=ttl
            )
            
            self.memories[memory_id] = memory
            
            # Update index
            for tag in memory.tags:
                self.memory_index[tag].append(memory_id)
            
            # Check memory limits
            await self._enforce_memory_limits()
            
            self.logger.info(f"Stored memory: {memory_id} (type: {memory_type.value})")
            return memory_id
    
    async def retrieve_memories(self, query: MemoryQuery) -> List[Memory]:
        """Retrieve memories based on query criteria."""
        with self.lock:
            candidates = []
            
            # Filter by tags
            if query.tags:
                tag_memories = set()
                for tag in query.tags:
                    if tag in self.memory_index:
                        tag_memories.update(self.memory_index[tag])
                candidates = [self.memories[mid] for mid in tag_memories if mid in self.memories]
            else:
                candidates = list(self.memories.values())
            
            # Filter by memory types
            if query.memory_types:
                candidates = [m for m in candidates if m.type in query.memory_types]
            
            # Filter by importance
            candidates = [m for m in candidates if m.importance >= query.min_importance]
            
            # Filter by age
            if query.max_age:
                cutoff_time = datetime.now() - query.max_age
                candidates = [m for m in candidates if m.created_at >= cutoff_time]
            
            # Sort by relevance (importance + recency + access count)
            candidates.sort(key=lambda m: (
                m.importance,
                m.access_count,
                (datetime.now() - m.created_at).total_seconds()
            ), reverse=True)
            
            # Update access patterns
            for memory in candidates[:query.limit]:
                memory.last_accessed = datetime.now()
                memory.access_count += 1
                self.access_patterns[memory.id].append(datetime.now())
            
            return candidates[:query.limit]
    
    async def get_memory(self, memory_id: str) -> Optional[Memory]:
        """Get a specific memory by ID."""
        with self.lock:
            if memory_id in self.memories:
                memory = self.memories[memory_id]
                memory.last_accessed = datetime.now()
                memory.access_count += 1
                self.access_patterns[memory_id].append(datetime.now())
                return memory
            return None
    
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing memory."""
        with self.lock:
            if memory_id not in self.memories:
                return False
            
            memory = self.memories[memory_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(memory, key):
                    setattr(memory, key, value)
                elif key in memory.metadata:
                    memory.metadata[key] = value
            
            memory.last_accessed = datetime.now()
            self.logger.info(f"Updated memory: {memory_id}")
            return True
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory."""
        with self.lock:
            if memory_id not in self.memories:
                return False
            
            memory = self.memories[memory_id]
            
            # Remove from index
            for tag in memory.tags:
                if tag in self.memory_index:
                    self.memory_index[tag] = [mid for mid in self.memory_index[tag] if mid != memory_id]
            
            # Remove relationships
            if memory_id in self.relationship_graph:
                del self.relationship_graph[memory_id]
            
            # Remove from memories
            del self.memories[memory_id]
            
            self.logger.info(f"Deleted memory: {memory_id}")
            return True
    
    async def add_relationship(self, memory_id1: str, memory_id2: str, 
                             relationship_type: str = "related") -> bool:
        """Add a relationship between two memories."""
        with self.lock:
            if memory_id1 not in self.memories or memory_id2 not in self.memories:
                return False
            
            if memory_id2 not in self.relationship_graph[memory_id1]:
                self.relationship_graph[memory_id1].append(memory_id2)
            
            if memory_id1 not in self.relationship_graph[memory_id2]:
                self.relationship_graph[memory_id2].append(memory_id1)
            
            # Update memory metadata
            self.memories[memory_id1].relationships.append(memory_id2)
            self.memories[memory_id2].relationships.append(memory_id1)
            
            self.logger.info(f"Added relationship between {memory_id1} and {memory_id2}")
            return True
    
    async def get_related_memories(self, memory_id: str, limit: int = 5) -> List[Memory]:
        """Get memories related to a specific memory."""
        with self.lock:
            if memory_id not in self.relationship_graph:
                return []
            
            related_ids = self.relationship_graph[memory_id]
            related_memories = []
            
            for rid in related_ids[:limit]:
                if rid in self.memories:
                    memory = self.memories[rid]
                    memory.last_accessed = datetime.now()
                    memory.access_count += 1
                    related_memories.append(memory)
            
            return related_memories
    
    async def search_memories(self, search_text: str, limit: int = 10) -> List[Memory]:
        """Search memories by content."""
        with self.lock:
            results = []
            search_lower = search_text.lower()
            
            for memory in self.memories.values():
                # Search in content
                if isinstance(memory.content, str) and search_lower in memory.content.lower():
                    results.append(memory)
                elif isinstance(memory.content, dict):
                    content_str = json.dumps(memory.content).lower()
                    if search_lower in content_str:
                        results.append(memory)
                
                # Search in tags
                for tag in memory.tags:
                    if search_lower in tag.lower():
                        results.append(memory)
                        break
            
            # Sort by relevance
            results.sort(key=lambda m: (
                m.importance,
                m.access_count,
                (datetime.now() - m.created_at).total_seconds()
            ), reverse=True)
            
            # Update access patterns
            for memory in results[:limit]:
                memory.last_accessed = datetime.now()
                memory.access_count += 1
                self.access_patterns[memory.id].append(datetime.now())
            
            return results[:limit]
    
    async def get_memory_stats(self) -> MemoryStats:
        """Get statistics about memory usage."""
        with self.lock:
            return self._calculate_stats()
    
    def _calculate_stats(self) -> MemoryStats:
        """Calculate memory statistics."""
        memories = list(self.memories.values())
        
        memories_by_type = defaultdict(int)
        memories_by_priority = defaultdict(int)
        total_importance = 0.0
        oldest_memory = None
        newest_memory = None
        total_access_count = 0
        
        for memory in memories:
            memories_by_type[memory.type] += 1
            memories_by_priority[memory.priority] += 1
            total_importance += memory.importance
            total_access_count += memory.access_count
            
            if oldest_memory is None or memory.created_at < oldest_memory:
                oldest_memory = memory.created_at
            
            if newest_memory is None or memory.created_at > newest_memory:
                newest_memory = memory.created_at
        
        return MemoryStats(
            total_memories=len(memories),
            memories_by_type=dict(memories_by_type),
            memories_by_priority=dict(memories_by_priority),
            average_importance=total_importance / len(memories) if memories else 0.0,
            oldest_memory=oldest_memory,
            newest_memory=newest_memory,
            total_access_count=total_access_count
        )
    
    async def _initialize_database(self):
        """Initialize the SQLite database for persistent storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    importance REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    access_count INTEGER NOT NULL,
                    tags TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    relationships TEXT NOT NULL,
                    decay_rate REAL NOT NULL,
                    ttl TEXT
                )
            ''')
            conn.commit()
    
    async def _load_memories(self):
        """Load memories from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM memories')
            rows = cursor.fetchall()
            
            for row in rows:
                memory = Memory(
                    id=row[0],
                    type=MemoryType(row[1]),
                    content=json.loads(row[2]),
                    priority=MemoryPriority(row[3]),
                    importance=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    last_accessed=datetime.fromisoformat(row[6]),
                    access_count=row[7],
                    tags=json.loads(row[8]),
                    metadata=json.loads(row[9]),
                    relationships=json.loads(row[10]),
                    decay_rate=row[11],
                    ttl=timedelta.fromisoformat(row[12]) if row[12] else None
                )
                
                self.memories[memory.id] = memory
                
                # Update index
                for tag in memory.tags:
                    self.memory_index[tag].append(memory.id)
                
                # Update relationship graph
                for rel_id in memory.relationships:
                    self.relationship_graph[memory.id].append(rel_id)
    
    async def _save_memories(self):
        """Save memories to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memories')  # Clear existing data
            
            for memory in self.memories.values():
                cursor.execute('''
                    INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory.id,
                    memory.type.value,
                    json.dumps(memory.content),
                    memory.priority.value,
                    memory.importance,
                    memory.created_at.isoformat(),
                    memory.last_accessed.isoformat(),
                    memory.access_count,
                    json.dumps(memory.tags),
                    json.dumps(memory.metadata),
                    json.dumps(memory.relationships),
                    memory.decay_rate,
                    memory.ttl.isoformat() if memory.ttl else None
                ))
            
            conn.commit()
    
    async def _enforce_memory_limits(self):
        """Enforce memory limits by removing old, less important memories."""
        if len(self.memories) <= self.max_memories:
            return
        
        # Sort memories by importance and recency
        memories = list(self.memories.values())
        memories.sort(key=lambda m: (
            m.importance,
            m.access_count,
            (datetime.now() - m.created_at).total_seconds()
        ))
        
        # Remove bottom 10%
        to_remove = memories[:len(memories) // 10]
        for memory in to_remove:
            await self.delete_memory(memory.id)
    
    async def _decay_process(self):
        """Background process for memory decay."""
        while self.status == ComponentStatus.RUNNING:
            try:
                await asyncio.sleep(self.decay_interval.total_seconds())
                
                if datetime.now() - self.last_decay >= self.decay_interval:
                    await self._apply_decay()
                    self.last_decay = datetime.now()
                    
            except Exception as e:
                self.logger.error(f"Error in decay process: {str(e)}")
    
    async def _apply_decay(self):
        """Apply decay to memories."""
        with self.lock:
            current_time = datetime.now()
            to_remove = []
            
            for memory in self.memories.values():
                # Check TTL
                if memory.ttl and current_time - memory.created_at > memory.ttl:
                    to_remove.append(memory.id)
                    continue
                
                # Apply decay
                time_since_access = current_time - memory.last_accessed
                decay_factor = memory.decay_rate * (time_since_access.total_seconds() / 3600)  # Hours
                
                memory.importance = max(0.0, memory.importance - decay_factor)
                
                # Remove very low importance memories
                if memory.importance < 0.1 and memory.priority == MemoryPriority.LOW:
                    to_remove.append(memory.id)
            
            # Remove decayed memories
            for memory_id in to_remove:
                await self.delete_memory(memory_id)
    
    async def _execute_task_impl(self, task: Task) -> Any:
        """Implementation-specific task execution."""
        if task.name == "store_memory":
            return await self.store_memory(
                content=task.metadata.get("content"),
                memory_type=MemoryType(task.metadata.get("type", "episodic")),
                priority=MemoryPriority(task.metadata.get("priority", "normal")),
                importance=task.metadata.get("importance", 0.5),
                tags=task.metadata.get("tags", []),
                metadata=task.metadata.get("metadata", {})
            )
        elif task.name == "retrieve_memories":
            query = MemoryQuery(
                tags=task.metadata.get("tags", []),
                memory_types=[MemoryType(t) for t in task.metadata.get("types", [])],
                min_importance=task.metadata.get("min_importance", 0.0),
                limit=task.metadata.get("limit", 10)
            )
            return await self.retrieve_memories(query)
        elif task.name == "search_memories":
            return await self.search_memories(
                search_text=task.metadata.get("search_text", ""),
                limit=task.metadata.get("limit", 10)
            )
        else:
            return {"status": "unknown_task", "task_id": task.id}
