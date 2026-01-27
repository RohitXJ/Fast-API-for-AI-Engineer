# Chapter 2: Request and Response Handling

## Summary

This chapter covers the minimum syntax an AI Engineer needs to get started with FastAPI. It focuses on the two primary HTTP operations used in machine learning services: `GET` for health checks and `POST` for model inference.

Key concepts covered:
-   **Environment and Installation**: A FastAPI application requires a server to run. We use **Uvicorn**, a high-performance ASGI server, to handle network communication.
-   **The FastAPI "App" Instance**: The `app = FastAPI()` instance is the central object of your application, acting as a hub for all your API routes.
-   **Paths and Operations (`GET` vs. `POST`)**:
    -   **`GET`**: Used for simple "read" operations. In AI services, its primary use is for **health checks**—an endpoint that monitoring systems can call to verify that the service is running correctly.
    -   **`POST`**: Used to "create" or "send" data to the server. This is the standard for **model inference**, where you send a request body containing the features (e.g., text, numbers, image data) needed for a prediction.
-   **The Development Server**: You cannot run a FastAPI app like a regular Python script. You must use a server like Uvicorn. The `--reload` flag is useful during development as it automatically restarts the server whenever you change your code.
-   **Automatic Documentation**: FastAPI automatically generates a user interface for your API, which you can access at `/docs`. This "Swagger UI" allows you to test your endpoints interactively from the browser.

## Application Code Example

This example combines the concepts of a health check and a dummy inference endpoint into a single application. It introduces the use of Pydantic's `BaseModel` to define the structure of the data your API expects in a `POST` request.

### 1. Create the Python file

Create a file named `main.py` inside the `Chapter-02_Request_Response_Handling` directory with the following content:

```python
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Define the data model for the request body
class ModelInput(BaseModel):
    """
    Defines the structure of the input data for the prediction endpoint.
    It expects a single field 'text' of type string.
    """
    text: str

# 2. Create an instance of the FastAPI class
app = FastAPI(
    title="Basic Inference API",
    description="A simple API to demonstrate GET and POST methods.",
    version="1.0",
)

# 3. Define a GET endpoint for health checks
@app.get("/health")
def health_check():
    """
    Endpoint to check if the API is running.
    Returns the status 'ok' if the service is active.
    """
    return {"status": "ok"}

# 4. Define a POST endpoint for model inference
@app.post("/predict")
def predict(data: ModelInput):
    """
    Endpoint to get a 'prediction'.
    It takes a JSON with a 'text' field and returns a dummy prediction.
    """
    # In a real application, you would pass 'data.text' to your ML model
    # For this example, we return a fixed response
    prediction = "positive"
    confidence = 0.95
    
    return {"prediction": prediction, "confidence": confidence}
```

### 2. Install Dependencies

If you haven't already, install FastAPI and Uvicorn. Pydantic is included with FastAPI.

```bash
pip install "fastapi[all]"
```

### 3. Run the Application

Navigate to the `Chapter-02_Request_Response_Handling` directory and run the server:

```bash
uvicorn main:app --reload
```

### 4. Access the API

Once the server is running, you can interact with the endpoints:

-   **Health Check (GET)**: Open your browser and go to [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health). You should see:
    ```json
    {"status":"ok"}
    ```

-   **Interactive Docs (Swagger UI)**: Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Here you can see both endpoints. For the `/predict` endpoint, you can click "Try it out" and provide a JSON request body like this to test it:
    ```json
    {
      "text": "I love FastAPI!"
    }
    ```
    Executing it will show you the dummy response:
    ```json
    {
      "prediction": "positive",
      "confidence": 0.95
    }
    ```
