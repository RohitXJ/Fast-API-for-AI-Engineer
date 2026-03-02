# Module 11: MLOps Foundations for AI Engineers

This module introduces fundamental MLOps (Machine Learning Operations) concepts, focusing on how to manage model lifecycles, maintain a model registry, and implement versioned inference endpoints for smooth production rollouts.

## Key Concepts

### 1. Model Registry
A model registry is a centralized system to track model metadata, including versions, training dates, and deployment status. In this simulation, we use **SQLModel** (a wrapper around SQLAlchemy and Pydantic) to store this metadata in a SQLite database.

### 2. Versioned Routers (API Versioning)
To avoid breaking changes for consumers, AI APIs should support multiple model versions simultaneously. Using FastAPI's `APIRouter`, we can isolate logic for `v1` (legacy/stable) and `v2` (improved/beta) models, allowing clients to migrate at their own pace.

### 3. Lifespan Events
Modern FastAPI applications use an `asynccontextmanager` to handle startup and shutdown logic. This is critical in MLOps for:
- Initializing database connections or tables.
- Pre-loading heavy ML models into memory before the API starts accepting requests.
- Cleaning up resources when the service stops.

## Code Walkthrough

### `app/main.py`
The core logic of the MLOps service:
- **`ModelRegistry`**: A SQLModel table definition for tracking model metadata.
- **`v1_router` & `v2_router`**: Separate routers that prefix endpoints with `/v1` and `/v2`.
- **`lifespan`**: Ensures the database is initialized and a default model entry exists before the server starts.
- **`/registry`**: An endpoint to query the current state of all models in the system.
- **`/health`**: Reports system status and which model versions are currently loaded.

### `Dockerfile`
A production-ready container definition:
- Uses `python:3.11-slim` for a smaller image footprint.
- Installs `fastapi`, `uvicorn`, and `sqlmodel` directly.
- Sets the `WORKDIR` to `/MLOps` and exposes port `8000`.
- Uses `uvicorn` as the ASGI server to run the application.

```dockerfile
FROM python:3.11-slim
WORKDIR /MLOps
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel
COPY ./app /MLOps/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## How to Run This Module

1.  **Navigate to the module directory:**
    ```sh
    cd "Module 11"
    ```

2.  **Build the Docker image:**
    ```sh
    docker build -t mlops-foundations .
    ```

3.  **Run the container:**
    ```sh
    docker run -d --name mlops-container -p 8000:8000 mlops-foundations
    ```

4.  **Verify the deployment:**
    -   **Interactive Docs:** Open `http://localhost:8000/docs` to test both V1 and V2 prediction endpoints.
    -   **Check Registry:** Visit `http://localhost:8000/registry` to see the registered model metadata.
    -   **Health Check:** Visit `http://localhost:8000/health` to confirm production readiness.

5.  **Stop the container:**
    ```sh
    docker stop mlops-container
    ```
