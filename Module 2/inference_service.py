from fastapi import FastAPI

app = FastAPI()

@app.get("/info")
def info():
    return {"model": "ResNet50", "version": 1.2}

@app.post("/inference")
def inference():
    return {"result": "Label_A"}