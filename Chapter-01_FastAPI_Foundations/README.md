# Chapter 1: FastAPI Foundations

## Summary

This chapter introduces the fundamental role of an API (Application Programming Interface) as a "wrapper" for machine learning models. It distinguishes between **offline ML** (development in notebooks) and **online ML** (production-ready services).

Key concepts covered:
- **API as a Model Wrapper**: An API makes an ML model accessible to other systems (like mobile apps) using a standard language like JSON, without requiring them to handle the model's specific Python environment.
- **Offline vs. Online ML**: Offline ML focuses on training and evaluation with static data, while online ML involves deploying the model as a 24/7 service to provide real-time predictions (inference).
- **Inference Data Flow**: In a production API, data follows a strict path:
    1.  **Request**: A user sends data (e.g., in JSON format) to a specific URL endpoint.
    2.  **Validation**: The API, using a library like Pydantic, checks if the incoming data has the correct format and data types.
    3.  **Inference**: The validated data is passed to the ML model to get a prediction.
    4.  **Response**: The prediction is sent back to the user, typically in JSON format.
- **Environment Management**: Production APIs are often packaged in **containers** (like Docker) to bundle the model, its dependencies, and libraries, ensuring it runs consistently across different servers.

## Application Code Example

This example demonstrates a minimal "Hello World" API using FastAPI.

### 1. Create the Python file

Create a file named `main.py` inside the `Chapter-01_FastAPI_Foundations` directory with the following content:

```python
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a "route" or "endpoint"
@app.get("/")
def read_root():
    """
    This endpoint returns a welcome message.
    """
    return {"message": "Hello, World! Welcome to your first FastAPI application."}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """
    This endpoint takes a path parameter `item_id` and an optional query parameter `q`.
    """
    return {"item_id": item_id, "q": q}
```

### 2. Install Dependencies

To run the application, you need to install FastAPI and an ASGI server like Uvicorn.

```bash
pip install "fastapi[all]"
```

### 3. Run the Application

Navigate to the `Chapter-01_FastAPI_Foundations` directory in your terminal and run the following command:

```bash
uvicorn main:app --reload
```

### 4. Access the API

Once the server is running, you can access the API endpoints:

-   **Root endpoint**: Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000). You should see the JSON response:
    ```json
    {"message":"Hello, World! Welcome to your first FastAPI application."}
    ```
-   **Items endpoint**: Go to [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery). You should see:
    ```json
    {"item_id":5,"q":"somequery"}
    ```

FastAPI also automatically generates interactive API documentation. You can access it at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
