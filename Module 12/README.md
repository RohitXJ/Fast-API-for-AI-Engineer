# Module 12: End-to-End Production AI Project (Capstone)

This final module integrates all previous concepts—FastAPI, Pydantic, SQLModel, JWT Security, and Docker—into a single, industry-grade AI inference service. It demonstrates how to move beyond "toy" projects into a modular, secure, and auditable production system.

## Key Concepts

### 1. Modular Architecture (Repository Pattern)
To ensure scalability, the application logic is separated into dedicated modules:
- **`auth.py`**: Handles all security concerns (JWT, Hashing).
- **`models.py`**: Centralizes data structures for both the API (Pydantic) and Database (SQLModel).
- **`inference.py`**: Isolates the mathematical/AI logic from the web logic.

### 2. Multi-Layer Security
Production AI services must protect expensive compute resources. This project implements:
- **Password Hashing**: Using `passlib` with Bcrypt to never store raw passwords.
- **JWT Authentication**: Stateless token-based access via OAuth2 for secure `/predict` requests.

### 3. Persistent Auditing & Logging
For compliance and model monitoring, every single inference request is logged to a SQLite database. This allows engineers to audit what data was sent to the model and what result it produced at any given timestamp.

### 4. Optimized Deployment
The included `Dockerfile` uses a **multi-stage build** to create a lightweight, production-ready image, ensuring that only necessary dependencies are included in the final environment.

## Code Walkthrough

### `app/main.py`
The orchestrator of the service:
- **`lifespan`**: Initializes the database and pre-loads the AI model registry before traffic arrives.
- **Dependency Injection**: Uses `get_session` for database access and `get_current_user` for security gates.
- **Endpoints**: Provides `/signup`, `/login`, and the secure `/predict` workflow.

### `tests/test_main.py`
Ensures reliability through automated verification:
- Uses an **In-Memory SQLite database** (`sqlite://`) for lightning-fast tests.
- Utilizes `StaticPool` to maintain database state throughout the test lifecycle without creating temporary files.

## How to Run This Module

1.  **Navigate to the module directory:**
    ```sh
    cd "Module 12"
    ```

2.  **Option A: Local Execution**
    ```sh
    # Install dependencies
    pip install -r requirements.txt
    # Run the server
    python -m uvicorn app.main:app --reload
    ```

3.  **Option B: Docker Deployment**
    ```sh
    # Build the optimized image
    docker build -t production-ai-service .
    # Run the container
    docker run -p 8000:8000 production-ai-service
    ```

4.  **Running Tests**
    Verify the system's integrity with one command:
    ```sh
    python -m pytest tests/test_main.py
    ```

5.  **Interactive Exploration**
    Open `http://localhost:8000/docs` to access the Swagger UI, where you can create a user, login to get a token, and test the secure AI prediction endpoint.
