# Use an official Python image.
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy your requirements (if you have a requirements.txt)
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . /app

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run uvicorn using host 0.0.0.0 and port 8080
CMD ["uvicorn", "api:app", "--host=0.0.0.0", "--port=8080"]
