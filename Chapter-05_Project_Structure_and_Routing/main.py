from typing import List
from fastapi import FastAPI 
from pydantic import BaseModel 
 
app = FastAPI() 
 
class Transaction(BaseModel): 
    amount: float 
    is_international: bool 
 
@app.post("/predict-batch") 
def predict_batch(items: List[Transaction]):
    results = [] 
    for item in items:
        # Simulation: Logic for fraud detection 
        is_fraud = item.amount > 10000 and item.is_international 
        results.append({"fraud_risk": is_fraud}) 
    return results