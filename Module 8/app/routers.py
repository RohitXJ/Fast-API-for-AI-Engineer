# app/routers.py

from fastapi import APIRouter, Depends
from typing import Annotated
from app.dependencies import get_active_model

router = APIRouter()

@router.post("/predict")
def predict(
    feature: float,
    model = Depends(get_active_model)
):
    """
    model is decided BEFORE this runs
    """
    return model(feature)
