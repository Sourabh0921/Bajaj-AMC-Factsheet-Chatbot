FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

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

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PORT=10000

EXPOSE $PORT

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=10000", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
