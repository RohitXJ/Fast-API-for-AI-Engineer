# (1) Start from the official Python base image
FROM python:3.9

# (2) Set the working directory inside the container
WORKDIR /code

# (3) Copy only requirements first to use Docker Cache
COPY ./requirements.txt /code/requirements.txt

# (4) Install dependencies (cached if unchanged)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5) Copy the actual model code and weights
COPY ./app /code/app

# (6) Run the production server on port 80
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
