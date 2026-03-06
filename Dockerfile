FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories with proper permissions
RUN mkdir -p downloads /tmp/careerwill_sessions && \
    chmod 777 downloads && \
    chmod 777 /tmp/careerwill_sessions

# Run the bot
CMD ["python", "main.py"]
