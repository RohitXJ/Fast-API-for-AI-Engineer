from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class InputTemp(BaseModel):
    celsius: float

@app.post("/analyze")
def analyze(data: InputTemp):
    if data.celsius < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Physics violation: Temperature too low"
        )
    elif data.celsius > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sensor limit exceeded"
        )
    else:
        return {
            "status": "normal"
            }