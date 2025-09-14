"""
Local Models Module
Provides local LLM integration capabilities
"""

from .local_model_wrapper import (
    LocalModelWrapper,
    ModelResponse,
    get_local_model,
    is_local_model_available,
    generate_with_local_model
)

__all__ = [
    'LocalModelWrapper',
    'ModelResponse', 
    'get_local_model',
    'is_local_model_available',
    'generate_with_local_model'
]
