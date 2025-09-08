import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # More verbose logging
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ai_ah.log", encoding='utf-8')
    ]
)

# Set log level for uvicorn and fastapi
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.DEBUG)
logging.getLogger("fastapi").setLevel(logging.DEBUG)

# Create workspace directory
workspace_dir = Path("./workspace")
workspace_dir.mkdir(exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="AI-AH API",
    description="Agentic AI for Infrastructure Management",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from api.routes import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "status": "AI-AH is running",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    logging.info("Starting AI-AH server...")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down AI-AH server...")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
