import time 
import logging 
from fastapi import FastAPI, Request
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
perf = logging.getLogger("performance") 
server = logging.getLogger("ai_service")

app = FastAPI() 
 
@app.middleware("http")
async def log_latency(request: Request, call_next): 
    start_time = time.time()
 
    response = await call_next(request)
 
    process_time = time.time() - start_time
    perf.info(f"Path: {request.url.path} | Latency: {process_time:.4f}s") 
 
    return response

class PredictRequest(BaseModel): 
    feature_val: float 

@app.post("/predict") 
def predict(data: PredictRequest): 
    server.info(f"Inference request received for feature: {data.feature_val}") 
 
    prediction = "Low Risk" if data.feature_val < 0.5 else "High Risk" 
    confidence = 0.95 

    server.info(f"Prediction: {prediction} | Confidence: {confidence}") 
 
    return {"prediction": prediction, "confidence": confidence}