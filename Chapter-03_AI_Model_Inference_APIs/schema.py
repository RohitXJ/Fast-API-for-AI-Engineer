from typing import Optional
from pydantic import BaseModel

class PredictRequest(BaseModel):
    area: float
    rooms: int
    zip_code: str
    year_built: Optional[int] = 2000

#Create a schema named PredictResponse with two fields: estimated_price (float) and status (str).
class PredictResponse(BaseModel):
    estimated_price: float
    status: str