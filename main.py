#!/usr/bin/env python3
"""
AI-AH Multi-Agent Infrastructure Intelligence Platform - Main Entry Point

This is the main entry point for the AI-AH platform. It provides a simple
way to start the platform with the new unified architecture.
"""

import sys
import os
from pathlib import Path

# Add platform to Python path
platform_path = Path(__file__).parent / "ai_ah_platform"
sys.path.insert(0, str(platform_path))

# Import and run the platform
from ai_ah_platform.api.main import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI-AH Multi-Agent Infrastructure Intelligence Platform...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🌐 Web Interface: http://localhost:8000")
    print("🔌 WebSocket: ws://localhost:8000/ws/connect")
    print("=" * 60)
    
            uvicorn.run(
                "ai_ah_platform.api.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                log_level="info"
            )
