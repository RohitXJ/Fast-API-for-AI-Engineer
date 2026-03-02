# Use a slim image to keep the footprint small
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /MLOps

# Install dependencies directly to keep the simulation simple
# In a real project, you would use a requirements.txt file [cite: 108]
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel

# Copy the app folder containing main.py into the container
COPY ./app /MLOps/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application using uvicorn
# We point to app.main:app because main.py is inside the app/ directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]