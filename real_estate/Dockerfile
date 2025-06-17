FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required for Reflex frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Initialize reflex (creates necessary directories)
RUN reflex init

# Build the frontend
RUN reflex export --frontend-only

# Expose the ports Reflex uses
EXPOSE 3000 8000

# Command to run the application
CMD ["reflex", "run", "--env", "prod", "--backend-only"]
