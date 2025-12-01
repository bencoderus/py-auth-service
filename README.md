# Auth Service

A FastAPI-based authentication service with JWT token support, user management, and distributed rate limiting using Redis.

## Features

- **User Authentication**: Register and login with email and password
- **JWT Tokens**: Access and refresh token generation with configurable expiration
- **Password Security**: Bcrypt hashing for secure password storage
- **Rate Limiting**: Distributed rate limiting using Redis (5 requests per 60 seconds on auth endpoints)
- **Database**: PostgreSQL for persistent data storage
- **Async Support**: Fully asynchronous operations using SQLAlchemy async
- **Docker Support**: Docker and Docker Compose setup for easy deployment

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache/Rate Limiting**: Redis
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: Bcrypt
- **Migration**: Alembic
- **Python**: 3.13+

## Prerequisites

- Python 3.13 or higher
- PostgreSQL 16 or higher
- Redis 7 or higher
- Docker and Docker Compose (optional, for containerized setup)

## Project Structure

```
auth-service/
├── src/
│   ├── auth/
│   │   ├── router.py              # Auth endpoints (login, register)
│   │   ├── services/
│   │   │   ├── auth_service.py    # Authentication logic
│   │   │   ├── jwt_service.py     # JWT token generation/verification
│   │   │   └── password_hash.py   # Password hashing utilities
│   │   └── validator.py           # Request validation schemas
│   ├── user/
│   │   ├── router.py              # User endpoints
│   │   └── repository.py          # User database operations
│   ├── common/
│   │   └── dependencies/
│   │       └── rate_limiter.py    # Rate limiting dependency
│   ├── redis_client.py            # Redis client wrapper
│   ├── db.py                      # Database configuration
│   └── main.py                    # FastAPI app initialization
├── alembic/                       # Database migrations
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
├── pyproject.toml                 # Project dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd auth-service
```

### 2. Environment Configuration

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=auth_db
POSTGRES_PORT=5432
DB_CONNECTION_STRING=postgresql://postgres:your_secure_password@localhost:5432/auth_db

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Application Configuration
APP_ENV=development
APP_PORT=8000
JWT_SECRET=your-secure-jwt-secret-key
```

### 3. Installation

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Start Redis cache
- Build and start the FastAPI application
- Run database migrations automatically

The application will be available at `http://localhost:8000`

#### Option B: Local Setup

**Install dependencies:**

```bash
pip install -r requirements.txt
# or using uv
uv sync
```

**Start PostgreSQL:**

```bash
# Using Homebrew (macOS)
brew services start postgresql

# Or using Docker
docker run -d \
  --name auth-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=auth_db \
  -p 5432:5432 \
  postgres:16-alpine
```

**Start Redis:**

```bash
# Using Homebrew (macOS)
brew services start redis

# Or using Docker
docker run -d \
  --name auth-redis \
  -p 6379:6379 \
  redis:7-alpine
```

**Run database migrations:**

```bash
alembic upgrade head
```

**Start the application:**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}

Response:
{
  "status": true,
  "message": "User created successfully",
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response:
{
  "status": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": {
      "accessToken": "jwt_token",
      "refreshToken": "refresh_token",
      "expiresAt": "2024-12-01T12:00:00",
      "refreshExpiresAt": "2024-12-08T12:00:00"
    }
  }
}
```

### Rate Limiting

Both `/auth/register` and `/auth/login` endpoints are rate limited to **5 requests per 60 seconds** per client IP.

When rate limit is exceeded:
```
HTTP 429 Too Many Requests

{
  "status": false,
  "message": "Rate limit exceeded. Maximum 5 requests per 60 seconds allowed."
}
```

## Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Makefile Commands

```bash
make help          # Show available commands
make install       # Install dependencies
make run           # Run the application
make migrate       # Run database migrations
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers
```

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and the connection string in `.env` is correct:

```bash
psql postgresql://postgres:password@localhost:5432/auth_db
```

### Redis Connection Error

Ensure Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

### Port Already in Use

If port 8000 is already in use, change `APP_PORT` in `.env` or use:

```bash
uvicorn src.main:app --port 8001
```

### Database Migration Issues

Reset the database (caution: deletes all data):

```bash
# Drop all tables
alembic downgrade base

# Re-apply migrations
alembic upgrade head
```

## Docker Cleanup

To remove all containers and volumes:

```bash
docker-compose down -v
```