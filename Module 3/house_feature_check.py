from typing import List
from pydantic import BaseModel

class ouseFeatures(BaseModel):
    quare_feet: int 
    num_bedrooms: int
    has_garden: bool = False
 
class FraudInferenceRequest(BaseModel): 
    transaction_id: str
    feature_vector: List[float]