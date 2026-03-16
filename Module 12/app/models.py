from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

# -----------------------------
# SQLModel Definitions
# -----------------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

class PredictionRequest(SQLModel):
    feature_vector: list[float]

class PredictionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    input_data: str
    prediction: str
