# -----------------------------
# Mock ML Model Registry
# -----------------------------

model_registry = {}

def load_weights(model_name: str):
    # Simulated model loading
    print(f"Loading {model_name}...")
    return f"Model artifact: {model_name}_v1.0"

def perform_inference(data: list[float]) -> str:
    # Simulated inference logic
    total = sum(data)
    if total > 5.0:
        return "High Value"
    else:
        return "Low Value"
