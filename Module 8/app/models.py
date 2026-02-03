# app/models.py

def model_v1(data: float):
    return {
        "model": "v1_linear",
        "prediction": data * 100
    }

def model_v2(data: float):
    return {
        "model": "v2_xgboost",
        "prediction": data * 120 + 50
    }
