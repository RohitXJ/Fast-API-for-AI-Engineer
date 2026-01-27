from fastapi import FastAPI
from schema import PredictResponse, PredictRequest

app = FastAPI()

@app.post("/predict", response_model=PredictResponse)
def predict_price(request: PredictRequest):
    """
    Dummy house price prediction endpoint
    """

    # Dummy logic (placeholder for ML model)
    estimated_price = request.area * request.rooms * 100

    return PredictResponse(
        estimated_price=estimated_price,
        status="success"
    )