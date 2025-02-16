# AI Service API

A FastAPI-based Python service that interacts with AI models and returns data to clients.

## Technology Stack

- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Docker (Containerization)
- Pydantic (Data Validation)
- Uvicorn (ASGI Server)

## Prerequisites

- Docker
- Docker Compose

## Project Structure

- `main.py` - FastAPI application and routes
- `models.py` - SQLAlchemy models
- `schemas.py` - Pydantic models for request/response
- `database.py` - Database connection setup
- `run.py` - Script to run the server
- `docker-compose.yml` - Docker services configuration
- `Dockerfile` - API service container configuration
- `.env` - Environment variables

## Getting Started

Start the services:
```bash
docker-compose up --build
```

This will:
- Build and start the API container
- Start the PostgreSQL database
- Create necessary database tables
- Enable hot-reload for development

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

### Examples API
- `POST /examples/` - Create a new example
  ```json
  {
    "name": "example name"
  }
  ```
- `GET /examples/` - List all examples
- `GET /examples/{example_id}` - Get specific example

### AI API
- `GET /ai/generate` - Generate AI response
  ```json
  // Request
  {
    "input": "Your prompt text here",
    "config": {
      "provider": "openai",  // or "anthropic" or "gemini"
      "ai_model": "gpt-3.5-turbo"  // model name for the selected provider
    }
  }
  
  // Response
  {
    "output": "AI generated response text"
  }
  ```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google AI API key
- `AI_API_KEY` - API key for the AI service (optional)

## Supported Models

### OpenAI
- gpt-4
- gpt-3.5-turbo

### Anthropic
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-2.1

### Google
- gemini-pro
- gemini-pro-vision

## Development Commands

```bash
# Start services
docker-compose up
# Start services in background
docker-compose up -d
#View logs
docker-compose logs -f
#Stop services
docker-compose down
# Rebuild containers
docker-compose up --build
```

## Database Setup

1. Access the PostgreSQL container:
```bash
docker exec -it ai-service-db bash
```

2. Create a new database:
```bash
CREATE DATABASE ai_service;
```

3. Create a new user:
```bash
CREATE USER ai_service_user WITH PASSWORD 'password';
```

## Database Migrations

The project uses Alembic for database migrations. Migrations will run automatically when starting the containers.

### Manual Migration Commands

```bash
# Generate a new migration
docker-compose exec api alembic revision --autogenerate -m "Description of changes"

# Run migrations
docker-compose exec api alembic upgrade head

# Rollback last migration
docker-compose exec api alembic downgrade -1
```

## Testing

The project includes tests for all endpoints and AI services. Tests use mocking to avoid making actual API calls.

### Running Tests

1. Set up test database and run all tests:
```bash
docker-compose exec api bash -c "chmod +x scripts/setup_test_db.sh && ./scripts/setup_test_db.sh && pytest"
```

2. Run specific test file (after setup):
```bash
docker-compose exec api bash -c "./scripts/setup_test_db.sh && pytest tests/test_endpoints.py"
docker-compose exec api bash -c "./scripts/setup_test_db.sh && pytest tests/test_ai_services.py"
docker-compose exec api bash -c "./scripts/setup_test_db.sh && pytest tests/test_ai_endpoint.py"
```

3. Run tests with detailed output:
```bash
docker-compose exec api pytest -v
```

4. Run tests with print output:
```bash
docker-compose exec api pytest -s
```

### Test Structure

- `tests/test_endpoints.py` - Tests for basic CRUD endpoints
- `tests/test_ai_services.py` - Tests for AI service integrations (mocked)
- `tests/test_ai_endpoint.py` - Tests for AI generation endpoint (mocked)

### Mocking Strategy

The tests use `unittest.mock` and `pytest-mock` to:
- Mock API client instances
- Mock API responses
- Verify correct API calls
- Test error handling

No actual API calls are made during testing, making the tests:
- Fast
- Reliable
- Independent of API availability
- Free of API usage costs

### Environment Variables for Testing

Tests require the following environment variables:
- `OPENAI_API_KEY` - For OpenAI tests
- `ANTHROPIC_API_KEY` - For Anthropic tests
- `GOOGLE_API_KEY` - For Gemini tests

Tests will be skipped if the corresponding API key is not set.
