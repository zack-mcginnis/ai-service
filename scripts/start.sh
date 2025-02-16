#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Create test database if it doesn't exist
echo "Creating test database if it doesn't exist..."
PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE ai_service_test;" || true

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Run migrations for test database
echo "Running migrations for test database..."
DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_service_test alembic upgrade head

# Start the application
echo "Starting application..."
python run.py 