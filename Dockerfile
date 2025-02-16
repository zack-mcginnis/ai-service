FROM python:3.11-slim

WORKDIR /app

# Install postgresql-client for database management
RUN apt-get update && apt-get install -y postgresql-client netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create script to wait for database and run migrations
COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"] 