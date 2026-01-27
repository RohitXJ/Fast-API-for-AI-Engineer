# Chapter 3: AI Model Inference APIs with Pydantic

## Summary

This chapter focuses on using Pydantic to create robust and reliable AI inference APIs. Pydantic acts as a "data contract," ensuring that the data flowing into and out of your model is always in the correct shape and format. This practice prevents common bugs and makes the API easier to debug and maintain.

Key concepts covered:
-   **The Need for Strict Schemas**: Machine learning models are not flexible with their inputs. A model expecting a vector of 10 floats will crash if it receives 9 floats or a string. Pydantic schemas act as a guard at the entry point of your API, validating all incoming data before it reaches your model.
-   **Pydantic `BaseModel`**: To define a schema, you create a class that inherits from `pydantic.BaseModel`. This class serves as a template for validating the request body.
-   **Field Typing**: You use standard Python type hints (`int`, `float`, `str`, `list`, `bool`) to define the expected data type for each field. Pydantic performs automatic type conversion where possible (e.g., a number sent as a string `"5"` can be converted to an integer `5`).
-   **Optional Fields and Default Values**: Fields can be marked as optional or be given a default value, making the API more flexible.
-   **Request vs. Response Models**:
    -   **Request Model**: Defines the structure and types of data the user must send *to* the API.
    -   **Response Model**: Defines the structure and types of the data the API sends *back* to the user. This is useful for filtering out internal metrics and ensuring a consistent, clean output format.

## Application Code Example

This example implements a dummy house price prediction API. It uses a Pydantic model to validate the incoming request and another to format the response. This ensures data integrity from end to end.

### 1. Create the Python file

Create a file named `main.py` inside the `Chapter-03_AI_Model_Inference_APIs` directory. We will combine the schemas and the app logic into this single file for clarity.

```python
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Define the Request Model
# This model defines the data structure the client must send to the /predict endpoint.
class PredictRequest(BaseModel):
    """
    Request model for house price prediction.
    - area: float, required
    - rooms: int, required
    - zip_code: str, required
    - year_built: int, optional with a default value of 2000
    """
    area: float
    rooms: int
    zip_code: str
    year_built: Optional[int] = 2000

# 2. Define the Response Model
# This model defines the data structure the API will send back to the client.
class PredictResponse(BaseModel):
    """
    Response model containing the prediction result.
    - estimated_price: float
    - status: str
    """
    estimated_price: float
    status: str

# 3. Create the FastAPI App Instance
app = FastAPI(
    title="House Price Prediction API",
    description="An API to demonstrate request and response models with Pydantic.",
    version="1.0"
)

# 4. Create the Prediction Endpoint
@app.post("/predict", response_model=PredictResponse)
def predict_price(request: PredictRequest):
    """
    Calculates a dummy house price based on input features.

    - Uses `PredictRequest` to validate the incoming JSON body.
    - Uses `response_model=PredictResponse` to ensure the output matches the response schema.
    """
    # Dummy prediction logic (in a real scenario, this would be your ML model call)
    # The price is a simple multiplication of area and rooms.
    estimated_price = request.area * request.rooms * 100

    # The function must return data that can be used to construct a PredictResponse model.
    # FastAPI handles the conversion automatically.
    return {
        "estimated_price": estimated_price,
        "status": "success"
    }
```

### 2. Run the Application

Navigate to the `Chapter-03_AI_Model_Inference_APIs` directory and run the server:

```bash
uvicorn main:app --reload
```

### 3. Test the API and Validation

Go to the interactive documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

-   **Test a valid request**:
    Click on the `/predict` endpoint, then "Try it out". Use the following valid JSON body:
    ```json
    {
      "area": 1500.5,
      "rooms": 3,
      "zip_code": "12345"
    }
    ```
    You will get a `200 OK` response with the calculated price:
    ```json
    {
      "estimated_price": 450150,
      "status": "success"
    }
    ```

-   **Test an invalid request**:
    Now, try sending data with an incorrect type. For example, send `area` as a string:
    ```json
    {
      "area": "fifteen-hundred",
      "rooms": 3,
      "zip_code": "12345"
    }
    ```
    FastAPI will automatically reject this request and return a `422 Unprocessable Entity` error with a clear message indicating that the `area` field expects a float (a number), not a string. This demonstrates how Pydantic protects your application from invalid data.
