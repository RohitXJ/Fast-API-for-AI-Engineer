from fastapi import FastAPI 
from pydantic import BaseModel 
 
app = FastAPI() 
 
class ModelInput(BaseModel): 
    feature_vector: list[float] 
 
@app.get("/") 
def read_root(): 
    return {"status": "Model Server Live"} 
 
@app.post("/predict") 
def predict(data: ModelInput): 
    # Simulated model logic 
    prediction = sum(data.feature_vector) * 0.5 
    return {"prediction": prediction}

@app.get("/health")
def health():
    return {"status": "ok"}
