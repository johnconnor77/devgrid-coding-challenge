# Use the official Python image from the Docker Hub
FROM python:3.9.12-slim

LABEL authors="johnconnor"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OPEN_WEATHER_API_KEY=84008e83eafc8464f948c0f39addf5dd

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose the port FastAPI runs on
EXPOSE 8000
