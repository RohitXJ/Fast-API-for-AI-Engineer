from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inference") 

app = FastAPI() 

class PredictRequest(BaseModel): 
    feature_val: float 

@app.post("/predict") 
def predict(data: PredictRequest): 
    # (1) Log incoming feature context 
    logger.info(f"Inference request received for feature: {data.feature_val}") 
 
    # (2) Simulated Inference Logic 
    prediction = "Low Risk" if data.feature_val < 0.5 else "High Risk" 
    confidence = 0.95 
 
    # (3) Log the result for monitoring 
    logger.info(f"Prediction: {prediction} | Confidence: {confidence}") 
 
    return {"prediction": prediction, "confidence": confidence} 