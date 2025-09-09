"""
Main FastAPI application for the Multi-Agent Infrastructure Intelligence Platform.

This module creates and configures the FastAPI application with all routes,
middleware, and error handling.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pathlib import Path
import uvicorn
import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, Any

# Import routes
from .routes.agent_routes import router as agent_router
from .routes.platform_routes import router as platform_router
from .websocket.websocket_routes import router as websocket_router
from .middleware.auth_middleware import auth_router, check_rate_limit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting AI-AH Multi-Agent Infrastructure Intelligence Platform")
    logger.info("Initializing platform components...")
    
    # Initialize platform components here
    # This would include starting agents, loading configurations, etc.
    
    logger.info("Platform startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI-AH Platform")
    logger.info("Cleaning up platform components...")
    
    # Cleanup platform components here
    # This would include stopping agents, saving state, etc.
    
    logger.info("Platform shutdown completed")


# Create FastAPI application
app = FastAPI(
    title="AI-AH Multi-Agent Infrastructure Intelligence Platform",
    description="""
    A comprehensive platform for intelligent infrastructure management using specialized AI agents.
    
    ## Features
    
    * **Terraform Agent** - Infrastructure provisioning and management
    * **Ansible Agent** - Configuration management and automation
    * **Kubernetes Agent** - Container orchestration and deployment
    * **Security Agent** - Security hardening and compliance management
    * **Monitoring Agent** - Infrastructure monitoring and observability
    
    ## Authentication
    
    The API supports both JWT tokens and API keys for authentication.
    
    * JWT tokens are obtained through the `/auth/login` endpoint
    * API keys can be used with the `X-API-Key` header
    
    ## WebSocket Support
    
    Real-time communication is available through WebSocket endpoints for:
    
    * Agent updates and notifications
    * Task progress monitoring
    * Live conversation with agents
    
    ## Rate Limiting
    
    API requests are rate-limited to prevent abuse. Default limits:
    * 1000 requests per hour per user
    * Rate limit headers are included in responses
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Custom middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing information."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": time.time(),
                "path": str(request.url)
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": time.time(),
                "path": str(request.url)
            }
        }
    )


# Include routers
app.include_router(auth_router)
app.include_router(agent_router)
app.include_router(platform_router)
app.include_router(websocket_router)

# Mount static files for web UI
ui_path = Path(__file__).parent.parent / "ui" / "web"
if ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(ui_path)), name="static")


# Web UI endpoint
@app.get("/", response_class=HTMLResponse, tags=["web-ui"])
async def web_ui():
    """Serve the web UI."""
    ui_path = Path(__file__).parent.parent / "ui" / "web" / "index.html"
    if ui_path.exists():
        return HTMLResponse(content=ui_path.read_text(), status_code=200)
    else:
        return HTMLResponse(content="""
        <html>
            <head><title>AI-AH Platform</title></head>
            <body>
                <h1>AI-AH Multi-Agent Infrastructure Intelligence Platform</h1>
                <p>Web UI files not found. Please check the installation.</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """, status_code=200)

# API info endpoint
@app.get("/api", tags=["api-info"])
async def api_info():
    """API information endpoint."""
    return {
        "message": "Welcome to AI-AH Multi-Agent Infrastructure Intelligence Platform",
        "version": "2.0.0",
        "status": "running",
        "documentation": "/docs",
        "health_check": "/api/v1/platform/health",
        "features": [
            "Terraform Infrastructure Provisioning",
            "Ansible Configuration Management",
            "Kubernetes Orchestration",
            "Security & Compliance Management",
            "Monitoring & Observability"
        ],
        "endpoints": {
            "agents": "/api/v1/agents",
            "platform": "/api/v1/platform",
            "websocket": "/ws",
            "authentication": "/auth"
        }
    }


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }


# Custom OpenAPI schema
def custom_openapi():
    """Custom OpenAPI schema with additional information."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI-AH Multi-Agent Infrastructure Intelligence Platform",
        version="2.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /auth/login"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key for authentication"
        }
    }
    
    # Add global security
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"ApiKeyAuth": []}
    ]
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.ai-ah-platform.com",
            "description": "Production server"
        }
    ]
    
    # Add contact information
    openapi_schema["info"]["contact"] = {
        "name": "AI-AH Platform Team",
        "email": "support@ai-ah-platform.com",
        "url": "https://ai-ah-platform.com"
    }
    
    # Add license information
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "platform.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
