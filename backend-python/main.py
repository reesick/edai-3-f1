"""AlgoVisual Backend - Clean entry point"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import router
from routes.custom import router as custom_router
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AlgoVisual API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"➤ {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"✓ {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}s)")
    
    return response

# Include routes
app.include_router(router)
app.include_router(custom_router, prefix="/api/custom", tags=["custom"])

@app.get("/")
async def root():
    return {"message": "AlgoVisual API", "version": "2.0.0"}
