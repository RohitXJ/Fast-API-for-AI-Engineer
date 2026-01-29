# Module 5: Building Prediction Endpoints

This module focuses on building prediction endpoints using FastAPI. It covers both batch and single prediction scenarios.

## Batch Predictions

The `main.py` file demonstrates how to create a batch prediction endpoint. The `/predict-batch` endpoint accepts a list of transactions and returns a fraud risk prediction for each transaction.

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/predict-batch" -H "Content-Type: application/json" -d '[
  {"amount": 5000, "is_international": false},
  {"amount": 15000, "is_international": true}
]'
```

### Example Response

```json
[
  {"fraud_risk": false},
  {"fraud_risk": true}
]
```

## Single Predictions

The `model_identity.py` file shows how to create a single prediction endpoint. The `/predict` endpoint accepts a single data point and returns a prediction score.

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{
  "feature_a": 0.5,
  "feature_b": 0.3,
  "category": "test"
}'
```

### Example Response

```json
{
  "prediction_score": 0.8,
  "status": "predicted"
}
```
