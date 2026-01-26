from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def check_health():
    return {"status": "Model is Ready"}


@app.post("/predict") 
def get_prediction():
    return {"prediction": "Pass", "confidence": 0.98}