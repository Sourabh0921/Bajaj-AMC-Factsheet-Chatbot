FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install system dependencies first
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PORT=10000

# Expose port for Render
EXPOSE $PORT

# Command for Render startup
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=10000", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
