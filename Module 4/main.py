from fastapi import FastAPI
from contextlib import asynccontextmanager

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup logic
    ml_model["weights"] = "Heavy Model Weights Loaded"
    print("Model is Ready!")

    yield  # Application runs here

    #Shutdown logic (optional cleanup)
    ml_model.clear()
    print("Model unloaded")


app = FastAPI(lifespan=lifespan)

@app.get("/predict")
def predict():
    # Accessing the pre-loaded global model
    return {"result": ml_model["weights"]}