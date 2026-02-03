# Module 8: Model Lifecycle, Versioning & Safe Updates in FastAPI

This module addresses the critical challenge of managing AI model lifecycles in a production environment. Once a model is deployed, its journey is far from over. We need robust strategies for updating models, rolling back to previous versions, and managing multiple versions simultaneously without causing service disruptions.

## Key Concepts

### 1. The Model Lifecycle in Production
In a real-world AI service, the model lifecycle is a continuous loop:
1.  **Training & Validation:** Models are built and evaluated offline.
2.  **Deployment (Startup):** The model is packaged and loaded into memory when the API server starts. FastAPI's `startup` events are perfect for this.
3.  **Monitoring:** The API logs the model's performance, prediction confidence, and resource usage.
4.  **Replacement/Update:** A new model version is ready. Simply overwriting the old model file ("hot-swapping") is dangerous and can lead to memory crashes or corrupted states.

### 2. Model Versioning Strategies
To safely manage updates, we use structured versioning.

#### A) Versioned Endpoints with `APIRouter`
This strategy involves creating unique URL paths for each model version. It's explicit and clear for API consumers.
-   **Old Version:** `POST /api/v1/predict`
-   **New Version:** `POST /api/v2/predict`

This allows clients to migrate to the new version at their own pace. It is ideal when the new model has a different input schema or output structure.

#### B) Dependency Injection for Safe Swapping
FastAPI's `Depends` system provides a powerful and flexible way to manage model versions. Instead of hardcoding a model call, an endpoint "depends" on a function that provides the active model. This allows us to switch the model centrally (e.g., via an environment variable) without touching the endpoint code.

## Code Walkthrough: Dependency-Injected Model Switching

The code in the `app/` directory demonstrates the Dependency Injection strategy for a "smooth rollout."

### How It Works
The application uses an environment variable `ACTIVE_MODEL` to decide which model logic to execute for the `/predict` endpoint.

-   **`models.py`**: Defines two distinct dummy models.
    ```python
    # app/models.py
    def model_v1(data: float):
        return { "model": "v1_linear", "prediction": data * 100 }

    def model_v2(data: float):
        return { "model": "v2_xgboost", "prediction": data * 120 + 50 }
    ```

-   **`dependencies.py`**: This is the core of the switching logic. The `get_active_model` function reads the `ACTIVE_MODEL` environment variable on every request and returns the corresponding model function. It defaults to `v1`.
    ```python
    # app/dependencies.py
    import os
    from app.models import model_v1, model_v2

    def get_active_model():
        active = os.getenv("ACTIVE_MODEL", "v1")
        if active == "v2":
            return model_v2
        return model_v1
    ```

-   **`routers.py`**: The endpoint uses `Depends` to inject the model returned by `get_active_model`. FastAPI runs the dependency function and passes its return value to the `model` parameter.
    ```python
    # app/routers.py
    from fastapi import APIRouter, Depends
    from app.dependencies import get_active_model

    router = APIRouter()

    @router.post("/predict")
    def predict(
        feature: float,
        model = Depends(get_active_model)
    ):
        return model(feature)
    ```

### How to Run This Module
1.  **Navigate to the app directory:**
    ```sh
    cd "Module 8"
    ```

2.  **Set the Active Model (using the `.env` file):**
    The project uses `python-dotenv` to load environment variables from a `.env` file.

    To use the `v1` model, your `.env` file should look like this:
    ```
    ACTIVE_MODEL="v1"
    ```

    To switch to the `v2` model, change it to:
    ```
    ACTIVE_MODEL="v2"
    ```

3.  **Install dependencies and run the server:**
    ```sh
    # Assuming you have a virtual environment set up
    pip install "fastapi[all]" python-dotenv
    uvicorn app.main:app --reload --app-dir .
    ```
    *Note: The `--app-dir .` flag tells uvicorn to look for the `app` package in the current directory.*

4.  **Test the endpoint:**
    Open a new terminal and use `curl` to send requests.

    *If `ACTIVE_MODEL="v1"`:*
    ```sh
    curl -X POST "http://127.0.0.1:8000/predict?feature=10" -H "accept: application/json"
    ```
    **Response:** `{"model":"v1_linear","prediction":1000}`

    *If `ACTIVE_MODEL="v2"`:*
    ```sh
    curl -X POST "http://127.0.0.1:8000/predict?feature=10" -H "accept: application/json"
    ```
    **Response:** `{"model":"v2_xgboost","prediction":1250}`

This demonstrates a "smooth rollout"—the model logic was updated just by changing an environment variable, with no code changes or service restart required.
