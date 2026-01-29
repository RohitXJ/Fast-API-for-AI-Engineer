# Module 7: Logging, Monitoring & Observability for AI APIs

This module focuses on the critical aspects of making your AI APIs production-ready by implementing robust logging, monitoring, and observability. By the end of this module, you will understand how to effectively use logging to track application behavior, monitor performance, and debug issues.

## Key Concepts

### 1. Structured Logging with Python's `logging` Module
Using Python's built-in `logging` library is fundamental for recording events, errors, and informational messages. We can create and configure named loggers to distinguish between different parts of the application (e.g., service lifecycle, inference, performance).

**Example (`main.py`):** Logging application lifecycle events like model loading and unloading.
```python
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
```

### 2. Logging Inference-Specific Details
For AI services, it's crucial to log the context of each prediction request. This includes the input features and the resulting model output (e.g., prediction and confidence scores). This data is invaluable for debugging, monitoring model drift, and auditing.

**Example (`main1.py`):** Logging the input feature and the final prediction.
```python
from fastapi import FastAPI
from pydantic import BaseModel 
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inference") 

class PredictRequest(BaseModel): 
    feature_val: float 

@app.post("/predict") 
def predict(data: PredictRequest): 
    # Log incoming feature context 
    logger.info(f"Inference request received for feature: {data.feature_val}") 
 
    # Simulated Inference Logic 
    prediction = "Low Risk" if data.feature_val < 0.5 else "High Risk" 
    confidence = 0.95 
 
    # Log the result for monitoring 
    logger.info(f"Prediction: {prediction} | Confidence: {confidence}") 
 
    return {"prediction": prediction, "confidence": confidence}
```

### 3. Performance Monitoring with Middleware
FastAPI middleware allows you to intercept incoming requests and outgoing responses. This is a perfect mechanism for measuring and logging the processing time (latency) for each API endpoint, which helps in identifying performance bottlenecks.

**Example (`main2.py`):** A middleware to log request latency.
```python
import time 
import logging 
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
perf = logging.getLogger("performance") 
 
@app.middleware("http")
async def log_latency(request: Request, call_next): 
    start_time = time.time()
 
    response = await call_next(request)
 
    process_time = time.time() - start_time
    perf.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s") 
 
    return response
```

## Assignment: Add Logging to a Predictor

The `house_price.py` file provides a hands-on assignment to apply the concepts learned in this module.

### Task
1.  Take the "House Price Predictor" API from Module 3.
2.  Create a specific logger for the price model (e.g., `price_model`).
3.  In the `/predict` endpoint, log the input `square_feet` and the final `estimated_price` output.
4.  Implement a latency-tracking middleware to monitor how long each prediction takes.
5.  Run the API and make a few prediction requests to observe the log outputs in your terminal.

### Solution (`house_price.py`)
This file contains the complete solution to the assignment, demonstrating how to integrate different loggers for application lifecycle, performance, and model-specific events.
```python
from fastapi import FastAPI, HTTPException, status, Request
from contextlib import asynccontextmanager
from pydantic import BaseModel
import time
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO) 

# Create specific loggers for different concerns
price_model = logging.getLogger("price_model")
perform = logging.getLogger("performance")

@asynccontextmanager
async def lifespan(app: FastAPI):
    perform.info("Loading Model..")
    start_time = time.time()
    time.sleep(2)  # Simulate model loading
    end_time = time.time()
    perform.info(f"Model Loaded in {end_time-start_time:.4f}s")
    yield
    perform.info("Unloading Model and Shutting Down Server..")

# Middleware to log request latency
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    perform.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s")
    return response

class InputData(BaseModel):
    square_feet: int

class OutputData(BaseModel):
    estimated_price: float

app = FastAPI(lifespan=lifespan)

@app.post('/predict', response_model=OutputData)
def predict(data: InputData):
    try:
        # Log input and output of the model
        price_model.info(f"square_feet : {data.square_feet}")
        prediction = (data.square_feet * 5.574) + 4500.03
        price_model.info(f"prediction : {prediction}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in model prediction"
        )
    return OutputData(estimated_price=prediction)
```
