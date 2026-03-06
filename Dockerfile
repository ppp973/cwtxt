FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir pyrogram==2.0.106 tgcrypto==1.2.5

# Copy app
COPY . .

# Create directories
RUN mkdir -p downloads /tmp/careerwill_sessions && \
    chmod 777 downloads && \
    chmod 777 /tmp/careerwill_sessions

# Run
CMD ["python", "main.py"]
