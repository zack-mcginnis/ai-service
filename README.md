# AI Service API

## Backend Services

Start the backend services:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## Reference App Setup

The reference app is a React application that demonstrates how to interact with the AI Service API.

### Prerequisites
- Node.js (v18 or later)
- npm (comes with Node.js)

### Setup Steps

1. Navigate to the reference app directory:
```bash
cd reference-app
```

2. Install dependencies:
```bash
npm install
npm install --save-dev @types/node  # Required for TypeScript type definitions
```

3. Create a .env file:
```bash
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

4. Start the development server:
```bash
npm start
```

The app will be available at `http://localhost:3000`

### Development Notes

- The reference app communicates with the API service running at `http://localhost:8000`
- Make sure the backend services (docker-compose) are running before starting the reference app
- The app supports hot reloading - changes to the code will automatically refresh the browser
- Environment variables must start with `REACT_APP_` to be accessible in the React app

### Available Features

- Select AI provider and model from dropdown menus
- Send prompts to the AI service
- View conversation history
- Error handling and loading states
- Responsive design

### Troubleshooting

1. If you see CORS errors:
   - Ensure the backend API is running
   - Check that the REACT_APP_API_URL is correct in .env
   - Verify the API's CORS settings allow requests from localhost:3000

2. If the API is unreachable:
   - Confirm the backend services are running (`docker ps`)
   - Check the API logs (`docker-compose logs api`)
   - Verify the port mappings in docker-compose.yml

## API Documentation

Once running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

### AI API
- `GET /generate` - Generate AI response
  ```json
  // Example Request
  GET /generate?input=Your prompt text here&provider=deepseek&ai_model=deepseek-r1:1.5b
  
  // Response
  {
    "output": "AI generated response text"
  }
  ```

  ```bash
  # Example curl command
  curl "http://localhost:8000/generate?input=Write%20a%20hello%20world%20program&provider=deepseek&ai_model=deepseek-r1:1.5b"
  ```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google AI API key
- `AI_API_KEY` - API key for the AI service (optional)
- `OLLAMA_API_URL` - URL for Ollama API (default: http://ollama:11434)

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

### Deepseek (Local via Ollama)
- deepseek-r1:1.5b

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
