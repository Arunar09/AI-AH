"""
Data processing module for the AI-AH Platform.

This module provides comprehensive data processing capabilities including:
- CSV/Excel data processing with pandas
- Statistical analysis with NumPy and SciPy
- Data visualization insights
- Infrastructure metrics analysis
"""

from .data_processor import DataProcessor, DataSource, DataAnalysis

__all__ = [
    'DataProcessor',
    'DataSource', 
    'DataAnalysis'
]

