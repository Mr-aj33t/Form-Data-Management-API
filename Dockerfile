# Use an official lightweight Python base image.
# "slim-buster" is smaller in size and suitable for deployments.
FROM python:3.12-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install all dependencies.
# Using --no-cache-dir to reduce image size by avoiding pip cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Expose port 8000 (FastAPI runs on this port by default).
# This is mainly for documentation; actual mapping happens in docker-compose.
EXPOSE 8000

# Set the command to run the FastAPI app when the container starts.
# --host 0.0.0.0 allows external access to the server from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
