# Module 10: Deploying AI Models with FastAPI (Docker & Minimal DevOps)

This module focuses on the transition from a local development environment to a portable, production-ready containerized application. We use Docker to package our FastAPI application, its dependencies, and the environment into a single image that can run anywhere.

## Key Concepts

### 1. Why Docker for AI APIs?
-   **Consistency:** "It works on my machine" is solved. The environment is identical in development, testing, and production.
-   **Isolation:** AI models often require specific versions of libraries (e.g., PyTorch, TensorFlow). Docker prevents version conflicts with other applications.
-   **Scalability:** Containers can be easily replicated across a cluster (e.g., using Kubernetes or Docker Swarm) to handle high traffic.

### 2. The Dockerfile
A `Dockerfile` is a script containing instructions to build a Docker image.
-   **`FROM`**: Sets the base image (e.g., `python:3.9`).
-   **`WORKDIR`**: Sets the working directory inside the container.
-   **`COPY`**: Transfers files from your local machine to the container.
-   **`RUN`**: Executes commands (like `pip install`).
-   **`CMD`**: Specifies the command to run when the container starts.

### 3. Production Server
While `fastapi dev` (or `uvicorn --reload`) is great for development, production requires a more stable setup. We use the `fastapi run` command which is optimized for production environments.

## Code Walkthrough

### `app/main.py`
A simple FastAPI app with a prediction endpoint and a health check endpoint.
-   **`/health`**: Critical for monitoring. Cloud providers use this to check if your container is still alive.
-   **`/predict`**: Simulated model logic that processes a feature vector.

### `Dockerfile`
The build process is optimized using Docker's layer caching:
1.  **Start from Python base.**
2.  **Copy `requirements.txt` and install first.** This ensures that if you change your code but not your dependencies, the `pip install` step is skipped during the next build, making it much faster.
3.  **Copy the application code.**
4.  **Launch with `fastapi run`.**

```dockerfile
FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

## How to Run This Module

1.  **Navigate to the module directory:**
    ```sh
    cd "Module 10"
    ```

2.  **Build the Docker image:**
    ```sh
    docker build -t fastapi-ai-model .
    ```

3.  **Run the container:**
    ```sh
    docker run -d --name my-model-container -p 8080:80 fastapi-ai-model
    ```
    *Note: This maps port 80 inside the container to port 8080 on your host machine.*

4.  **Verify the deployment:**
    -   Open your browser at `http://localhost:8080/`
    -   Check the health endpoint: `http://localhost:8080/health`
    -   Test the prediction endpoint using `curl` or documentation (`/docs`):
        ```sh
        curl -X POST "http://localhost:8080/predict" 
             -H "Content-Type: application/json" 
             -d '{"feature_vector": [1.2, 2.3, 3.4]}'
        ```

5.  **Stop the container:**
    ```sh
    docker stop my-model-container
    ```
