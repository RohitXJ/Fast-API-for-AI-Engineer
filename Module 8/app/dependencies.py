# app/dependencies.py

import os
from app.models import model_v1, model_v2

def get_active_model():
    """
    This runs on EVERY request
    """
    active = os.getenv("ACTIVE_MODEL", "v1")

    if active == "v2":
        return model_v2

    return model_v1
