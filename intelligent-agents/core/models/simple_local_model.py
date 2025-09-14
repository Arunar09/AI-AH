"""
Simple Local Model Integration
Direct integration without complex imports
"""

import os
import sys
from typing import Dict, Any, Optional
import logging
import signal
from contextlib import contextmanager

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False

class SimpleLocalModel:
    """Simple wrapper for CodeLlama model"""
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.model_path = self._find_model()
        self.logger = logging.getLogger(__name__)
        
        if LLAMA_CPP_AVAILABLE and self.model_path:
            self._load_model()
    
    def _find_model(self) -> Optional[str]:
        """Find CodeLlama model"""
        possible_paths = [
            r"C:\Users\arunk\.lmstudio\models\TheBloke\codellama\codellama-7b-instruct.Q5_K_M.gguf",
            os.path.expanduser("~/.lmstudio/models/TheBloke/codellama/codellama-7b-instruct.Q5_K_M.gguf"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _load_model(self):
        """Load the model"""
        try:
            if not self.model_path:
                return
            
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=1024,  # Smaller context for faster inference
                n_threads=4,  # More threads for better performance
                n_gpu_layers=0,  # CPU only for compatibility
                verbose=False,
                use_mmap=True,  # Memory mapping for faster loading
                use_mlock=False  # Don't lock memory
            )
            self.is_loaded = True
            print("✅ CodeLlama model loaded successfully")
            
        except Exception as e:
            print(f"❌ Failed to load CodeLlama model: {e}")
            self.is_loaded = False
    
    def generate_response(self, prompt: str, max_tokens: int = 256, timeout: int = 15) -> str:
        """Generate response with optimized settings for speed and timeout"""
        if not self.is_loaded or not self.model:
            return "Local model not available"
        
        try:
            # Optimize for speed: smaller max_tokens, lower temperature
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=0.1,  # Lower temperature for faster, more deterministic output
                top_p=0.9,  # Nucleus sampling for faster generation
                stop=["</s>", "\n\n\n", "```"],  # More stop tokens
                echo=False,
                repeat_penalty=1.1  # Prevent repetition
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if model is available"""
        return self.is_loaded and self.model is not None

# Global instance
_simple_model = None

def get_simple_model() -> SimpleLocalModel:
    """Get global model instance"""
    global _simple_model
    if _simple_model is None:
        _simple_model = SimpleLocalModel()
    return _simple_model

def is_simple_model_available() -> bool:
    """Check if simple model is available"""
    return get_simple_model().is_available()
