#!/usr/bin/env python3
"""
Local Intelligent Agents Platform
Building truly intelligent infrastructure agents - local first, no cost, no LLM
"""

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Local Intelligent Agents",
    description="Building truly intelligent infrastructure agents - local first, no cost, no LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Local Intelligent Agents Platform",
        "description": "Building truly intelligent infrastructure agents - local first, no cost, no LLM",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-09-13T21:40:00Z"}

@app.get("/agents")
async def list_agents():
    """List available agents"""
    return {
        "agents": [
            {
                "name": "terraform",
                "description": "Infrastructure as Code Intelligence",
                "capabilities": ["design", "generate", "troubleshoot", "optimize"]
            },
            {
                "name": "ansible",
                "description": "Configuration Management Intelligence",
                "capabilities": ["configure", "deploy", "harden", "automate"]
            },
            {
                "name": "kubernetes",
                "description": "Container Orchestration Intelligence",
                "capabilities": ["orchestrate", "scale", "secure", "monitor"]
            },
            {
                "name": "security",
                "description": "Security Intelligence",
                "capabilities": ["assess", "harden", "comply", "monitor"]
            },
            {
                "name": "monitoring",
                "description": "Observability Intelligence",
                "capabilities": ["monitor", "alert", "analyze", "optimize"]
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Local Intelligent Agents Platform...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🌐 Web Interface: http://localhost:8000")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

