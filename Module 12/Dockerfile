# Stage 1: Build & Dependencies
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app ./app

# Add local path to PYTHONPATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=$PYTHONPATH:/app

EXPOSE 8000

# Exec form for graceful shutdowns
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
