# Stage 1: API Service
FROM python:3.11-slim as api

WORKDIR /app

# Install postgresql-client and curl for healthchecks
RUN apt-get update && \
    apt-get install -y postgresql-client netcat-traditional curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create script to wait for database and run migrations
COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

# Stage 2: Ollama Service
FROM ollama/ollama:latest as ollama

# Install necessary tools
RUN apt-get update && \
    apt-get install -y util-linux && \
    rm -rf /var/lib/apt/lists/*

# Create a script to initialize swap and start Ollama
COPY scripts/start-ollama.sh /start-ollama.sh
RUN chmod +x /start-ollama.sh

ENTRYPOINT ["/start-ollama.sh"] 