"""
Assignment: Add Logging to a Predictor 
1. Take your "House Price Predictor" API from Module 3. 
2. Add a logger named price_model. 
3. In the /predict endpoint, log the square_feet input and the final estimated_price 
output. 
4. Implement the latency middleware from Example 3 to track how long the math takes. 
5. Run the API and perform 3 different predictions via the /docs page, then check your 
terminal to see the logs.
"""

from fastapi import FastAPI, HTTPException, status, Request
from contextlib import asynccontextmanager
from pydantic import BaseModel
import time
import logging

logging.basicConfig(level=logging.INFO) 
price_model = logging.getLogger("price_model")
perform = logging.getLogger("performance")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        perform.info("Loading Model..")
        start_time = time.time()
        time.sleep(2)
        end_time = time.time()
        perform.info(f"Model Loaded in {end_time-start_time:.4f}..")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model Loading Error"
        )
    else:
        yield

    perform.info("Unloading Model and Shutting Down Server..")

class InputData(BaseModel):
    square_feet: int

class OutputData(BaseModel):
    estimated_price: float

app =FastAPI(lifespan=lifespan)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    perform.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s")
    return response

@app.post('/predict', response_model=OutputData)
def predict(data: InputData):
    try:
        price_model.info(f"square_feet : {data.square_feet}")
        prediction = (data.square_feet * 5.574) + 4500.03
        price_model.info(f"prediction : {prediction}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in model prediction"
        )
    return OutputData(
        estimated_price=prediction
    )