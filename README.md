# User Management API

A REST API for user management built with FastAPI and SQLModel for ORM.

## Project Structure

```
app/
├── database/       # Database configurations and implementations
├── exceptions/     # Known exceptions
├── models/         # SQLModel entities
├── repositories/   # Data access layer
├── routes/         # API endpoints
├── schemas/        # Pydantic models for request/response
└── utils/          # Utility functions and classes
tests/              # Test suite
├── routes/         # Route tests
dev/                # Image and docker-compose for local development
```

## Requirements

- Python 3.12+
- Docker (optional)
- Make

## Installation

Clone the repository:
```bash
git clone https://github.com/anjosma/crud
cd crud
```

## Running the Application

We can run the application with Docker and using an Python virtual environment:

### Local with Virtual Environment
1. Create and activate the virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 
```

### Using Docker
1. Only execute the make command:
```bash
make up
```

The API will be available at `http://localhost:8000` for both methods.

## API Documentation

After starting the application, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

- `GET /users`: List all users
- `GET /users/{id}`: Get a specific user
- `POST /users`: Create a new user
- `PUT /users/{id}`: Update a user
- `DELETE /users/{id}`: Delete a user

## Testing

### Running Tests locally
```bash
python -m pytest --cov=app --cov-report=html
```

### Running Tests in Docker
```bash
make test
```

## Environment Variables

- `LOG_LEVEL`: Set logging level (default: INFO)
- `PYTHONPATH`: Python path for imports


## Makefile Commands

- `make build`: Build Docker containers
- `make up`: Start the application in Docker containers
- `make down`: Stop the running Docker containers
- `make test`: Run tests in Docker environment
- `make clean`: Clean up Docker containers, volumes, and orphaned containers

## TODO/Future Improvements

### Testing
- Increase unit test coverage.
- Add integration tests for database operations.

### Code
- Improve level of abstraction (logger, API responses, etc)
- Improve exception handling through the code.
- API authentication

### Performance
- Add caching layer (e.g. Redis) for frequently accessed data.
- Change for a more robust database and add performance tests for database operations and API endpoints.
- Monitor metrics (e.g. latency with Prometheus)