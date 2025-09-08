from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

class BaseAgent(ABC):
    """Base class for all infrastructure agents."""
    
    def __init__(self, work_dir: str = "./workspace"):
        self.work_dir = Path(work_dir).resolve()
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.state: Dict[str, Any] = {}
    
    @abstractmethod
    async def initialize(self):
        """Initialize the agent with required configurations."""
        pass
    
    @abstractmethod
    async def plan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an execution plan."""
        pass
    
    @abstractmethod
    async def apply(self, plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Apply the configuration or plan."""
        pass
    
    @abstractmethod
    async def destroy(self) -> Dict[str, Any]:
        """Destroy managed resources."""
        pass
    
    def set_work_dir(self, path: str) -> None:
        """Set the working directory for the agent."""
        self.work_dir = Path(path).resolve()
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent."""
        return self.state
    
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update the agent's state."""
        self.state.update(new_state)
