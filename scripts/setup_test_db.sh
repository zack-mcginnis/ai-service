#!/bin/bash

echo "Setting up test database..."

# Wait for database to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

# Create test database
PGPASSWORD=postgres psql -h db -U postgres -c "DROP DATABASE IF EXISTS ai_service_test;"
PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE ai_service_test;"

# Run migrations on test database
DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_service_test alembic upgrade head

echo "Test database setup complete" 