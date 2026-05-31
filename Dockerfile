FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for Git commands
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# 🆕 FIX: Chain both scripts so data is fetched BEFORE generating wrapped stats
CMD python fetch_data.py && python generate_wrapped.py