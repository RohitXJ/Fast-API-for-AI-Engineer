import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger("ai_service") 
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Simulate loading heavy model weights 
    logger.info("Starting model loading process...") 
    logger.info("Model weights loaded successfully. Version: 2.1.0")

    yield

    logger.info("Starting Model unloading process...") 
    logger.info("Model shutdown successfully.")

app = FastAPI(lifespan=lifespan) 