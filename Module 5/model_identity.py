from fastapi import FastAPI
from pydantic import BaseModel

class ModelInput(BaseModel):
    feature_a: float
    feature_b: float
    category: str

class ModelOutput(BaseModel):
    prediction_score: float
    status: str

app = FastAPI()

@app.post("/predict", response_model=ModelOutput)
def predict(data: ModelInput):
    score = 0.0
    if data.category == 'test':
        score = data.feature_a + data.feature_b
    return ModelOutput(
        prediction_score= score,
        status='predicted'
    )
