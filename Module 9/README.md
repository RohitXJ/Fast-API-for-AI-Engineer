# Module 9: Securing AI APIs for Production AI Systems

This module focuses on the essential security layer required for production-ready AI APIs. Protecting your model endpoints from unauthorized access is critical for both data privacy and managing infrastructure costs. We implement a robust authentication system using JSON Web Tokens (JWT) and OAuth2.

## Key Concepts

### 1. Authentication vs. Authorization
-   **Authentication:** Verifying *who* the user is (e.g., logging in with a username and password).
-   **Authorization:** Determining *what* the user is allowed to do (e.g., access a specific prediction endpoint).

### 2. Password Hashing
Storing plain-text passwords is a major security risk. We use `passlib` with the `bcrypt` algorithm to securely hash passwords before storing them in our "database."

### 3. JSON Web Tokens (JWT)
JWT is a compact, URL-safe means of representing claims to be transferred between two parties.
-   **Header:** Specifies the algorithm used (e.g., HS256).
-   **Payload:** Contains user data (e.g., username) and expiration time.
-   **Signature:** Ensures the token hasn't been tampered with.

### 4. OAuth2 Password Flow
We use FastAPI's built-in `OAuth2PasswordBearer` and `OAuth2PasswordRequestForm`. This is a standard flow where the user exchanges a username/password for an `access_token`, which is then used for subsequent requests.

## Code Walkthrough

The `main.py` file demonstrates a complete security workflow.

### Security Setup
-   **`SECRET_KEY`**: A unique string used to sign the JWT.
-   **`ALGORITHM`**: The signing algorithm (HS256).
-   **`CryptContext`**: Manages password hashing and verification.

### Endpoints
-   **`POST /signup`**: Hashes the provided password and stores it in a dictionary (simulating a database).
-   **`POST /login`**: Validates credentials and returns a signed JWT.
-   **`POST /predict`**: A protected endpoint that requires a valid Bearer token. It uses `Depends(oauth2_scheme)` to enforce authentication.

```python
@app.post("/predict")
def predict(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username = payload.get("sub")
    return {"user": username, "prediction": "This is a dummy AI result!"}
```

## How to Run This Module

1.  **Navigate to the module directory:**
    ```sh
    cd "Module 9"
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the `Module 9` directory:
    ```env
    SECRET_KEY="your-super-secret-key-here"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

3.  **Install dependencies:**
    ```sh
    pip install "fastapi[standard]" passlib[bcrypt] python-jose[cryptography] python-dotenv
    ```

4.  **Run the server:**
    ```sh
    fastapi dev main.py
    ```

5.  **Test the workflow:**
    -   **Sign up:** Create a user account.
    -   **Login:** Get your `access_token`.
    -   **Predict:** Use the token in the `Authorization` header (`Bearer <token>`) to access the model.
