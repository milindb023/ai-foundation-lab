FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for compiling python packages if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding and cross-encoder models for faster run-time execution
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the backend source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
