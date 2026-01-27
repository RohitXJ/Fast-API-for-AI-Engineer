# Chapter 4: Validation and Error Handling

## Summary

This chapter explains how to manage the lifecycle of a machine learning model within a FastAPI application. A common performance bottleneck in AI services is repeatedly loading a large model from disk for every inference request. The ideal approach is to load the model into memory once when the application starts and keep it available for all subsequent requests.

FastAPI provides a clean and modern way to manage these startup and shutdown events using a **`lifespan`** context manager. This is the recommended method for handling resources that need to be initialized before the application starts serving requests and cleaned up when it shuts down.

### Important Note on `on_event`

You may find older tutorials or documentation (including the PDF for this chapter) that use the `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators. **These decorators are now deprecated.**

The `lifespan` context manager replaces them and offers a more robust and explicit way to handle the application's lifecycle. You should always use `lifespan` for new applications.

## Application Code Example

This example demonstrates how to use the `lifespan` context manager to load a "model" into memory at startup and clear it during shutdown.

### 1. Create the Python file

Create a file named `main.py` inside the `Chapter-04_Validation_and_Error_Handling` directory with the following content:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

# This dictionary will act as a simple in-memory "store" for our model
ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    # In a real application, this is where you would load your ML model,
    # establish database connections, or initialize other resources.
    ml_model["weights"] = "Heavy Model Weights Loaded"
    print("Model is Ready!")

    yield  # The application runs here, between startup and shutdown

    # --- SHUTDOWN LOGIC ---
    # This code runs after the application is stopped.
    # It's the perfect place for cleanup tasks.
    ml_model.clear()
    print("Model unloaded and resources cleaned up.")


# Create the FastAPI app and pass the lifespan manager to it
app = FastAPI(lifespan=lifespan)

@app.get("/predict")
def predict():
    # This endpoint can now access the model that was loaded at startup
    # without needing to load it again.
    return {"result": ml_model["weights"]}

```

### 2. How the Code Works

-   **`@asynccontextmanager`**: This decorator from Python's `contextlib` turns a generator function into a context manager that can be used with `async with`.
-   **`lifespan(app: FastAPI)`**: This is our lifespan management function.
    -   **Startup**: All code *before* the `yield` statement is executed when the application starts up. We simulate loading a model by populating the `ml_model` dictionary.
    -   **Shutdown**: All code *after* the `yield` statement is executed when the application is shutting down. We clean up by clearing the dictionary.
-   **`app = FastAPI(lifespan=lifespan)`**: We link our `lifespan` function to the FastAPI app instance here. This tells FastAPI to execute our startup and shutdown logic.

### 3. Run the Application

Navigate to the `Chapter-04_Validation_and_Error_Handling` directory and run the server:

```bash
uvicorn main:app --reload
```

### 4. Observe the Lifecycle Events

When you run the server, you will see the startup message in your console:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
Model is Ready!
INFO:     Started server process [54321]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

-   **Make a Prediction**: Go to [http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict) in your browser. You will see the response, confirming the "model" was loaded and is accessible:
    ```json
    {"result":"Heavy Model Weights Loaded"}
    ```

-   **Stop the Server**: Press `Ctrl+C` in your console. You will see the shutdown message printed as the application closes, confirming the cleanup logic was executed:
    ```
    INFO:     Shutting down
    INFO:     Waiting for application shutdown.
    Model unloaded and resources cleaned up.
    INFO:     Application shutdown complete.
    INFO:     Finished server process [54321]
    ```
