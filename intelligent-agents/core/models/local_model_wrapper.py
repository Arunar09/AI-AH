"""
Local Model Wrapper for CodeLlama Integration
Provides a unified interface for local LLM models
"""

import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("⚠️ llama-cpp-python not available. Local model features will be disabled.")

@dataclass
class ModelResponse:
    """Response from local model"""
    content: str
    confidence: float
    tokens_used: int
    model_name: str
    response_time: float

class LocalModelWrapper:
    """Wrapper for local LLM models using llama-cpp-python"""
    
    def __init__(self, model_path: str = None, model_name: str = "CodeLlama-7B-Instruct"):
        self.logger = logging.getLogger(__name__)
        self.model_path = model_path or self._find_codelama_model()
        self.model_name = model_name
        self.model = None
        self.is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and self.model_path:
            self._load_model()
        else:
            self.logger.warning("Local model not available")
    
    def _find_codelama_model(self) -> Optional[str]:
        """Find CodeLlama model in common locations"""
        possible_paths = [
            r"C:\Users\arunk\.lmstudio\models\TheBloke\codellama\codellama-7b-instruct.Q5_K_M.gguf",
            os.path.expanduser("~/.lmstudio/models/TheBloke/codellama/codellama-7b-instruct.Q5_K_M.gguf"),
            "./models/codellama-7b-instruct.Q5_K_M.gguf",
            "./codellama-7b-instruct.Q5_K_M.gguf"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.logger.info(f"Found CodeLlama model at: {path}")
                return path
        
        self.logger.warning("CodeLlama model not found in common locations")
        return None
    
    def _load_model(self):
        """Load the local model"""
        try:
            if not self.model_path or not os.path.exists(self.model_path):
                self.logger.error(f"Model file not found: {self.model_path}")
                return
            
            self.logger.info(f"Loading CodeLlama model from: {self.model_path}")
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=4096,  # Context window
                n_threads=4,  # Number of threads
                verbose=False
            )
            self.is_loaded = True
            self.logger.info("✅ CodeLlama model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load CodeLlama model: {e}")
            self.is_loaded = False
    
    def generate_response(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> ModelResponse:
        """Generate response using local model"""
        if not self.is_loaded or not self.model:
            return ModelResponse(
                content="Local model not available",
                confidence=0.0,
                tokens_used=0,
                model_name=self.model_name,
                response_time=0.0
            )
        
        try:
            import time
            start_time = time.time()
            
            # Generate response
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["</s>", "\n\n\n"],  # Stop tokens
                echo=False
            )
            
            response_time = time.time() - start_time
            
            content = response['choices'][0]['text'].strip()
            tokens_used = response['usage']['completion_tokens']
            
            return ModelResponse(
                content=content,
                confidence=0.8,  # Local models typically have good confidence
                tokens_used=tokens_used,
                model_name=self.model_name,
                response_time=response_time
            )
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return ModelResponse(
                content=f"Error: {str(e)}",
                confidence=0.0,
                tokens_used=0,
                model_name=self.model_name,
                response_time=0.0
            )
    
    def generate_terraform_code(self, requirements: Dict[str, Any]) -> str:
        """Generate Terraform code using local model"""
        prompt = self._create_terraform_prompt(requirements)
        response = self.generate_response(prompt, max_tokens=1024, temperature=0.3)
        return response.content
    
    def _create_terraform_prompt(self, requirements: Dict[str, Any]) -> str:
        """Create a specialized prompt for Terraform code generation"""
        project_name = requirements.get('project_name', 'my-project')
        cloud_provider = requirements.get('cloud_provider', 'AWS')
        user_load = requirements.get('user_load', '1000')
        budget = requirements.get('budget', '100')
        
        prompt = f"""<s>[INST] You are an expert Terraform engineer. Generate production-ready Terraform code for the following requirements:

Project: {project_name}
Cloud Provider: {cloud_provider}
Expected User Load: {user_load} users
Monthly Budget: ${budget}

Requirements:
- Create a scalable infrastructure
- Include proper security groups and networking
- Use best practices for resource naming and tagging
- Include cost optimization measures
- Add monitoring and logging

Generate only the Terraform code, no explanations. Use proper formatting and indentation.

[/INST]"""
        
        return prompt
    
    def is_available(self) -> bool:
        """Check if local model is available"""
        return self.is_loaded and self.model is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "model_path": self.model_path,
            "is_loaded": self.is_loaded,
            "is_available": self.is_available(),
            "llama_cpp_available": LLAMA_CPP_AVAILABLE
        }

# Global instance
_local_model = None

def get_local_model() -> LocalModelWrapper:
    """Get or create global local model instance"""
    global _local_model
    if _local_model is None:
        _local_model = LocalModelWrapper()
    return _local_model

def is_local_model_available() -> bool:
    """Check if local model is available"""
    return get_local_model().is_available()

def generate_with_local_model(prompt: str, **kwargs) -> ModelResponse:
    """Generate response using local model"""
    return get_local_model().generate_response(prompt, **kwargs)
