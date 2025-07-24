# Technology Stack

## Framework & Core Libraries
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management using Python type annotations
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping (ORM)
- **Uvicorn**: ASGI web server implementation for Python

## Database
- **PostgreSQL**: Primary database (hosted on Neon)
- **psycopg2-binary**: PostgreSQL adapter for Python
- **Alembic**: Database migration tool for SQLAlchemy

## Development & Deployment
- **python-dotenv**: Environment variable management
- **pyngrok**: Ngrok integration for local development tunneling
- **httpx**: HTTP client for health checks
- **APScheduler**: Background task scheduling

## Common Commands

### Development
```bash
# Run development server with ngrok tunneling
python dev.py

# Run production server
python main.py

# Install dependencies
pip install -r requirements.txt
```

### Database
```bash
# Initialize database (handled automatically on startup)
# Database tables are created via SQLAlchemy Base.metadata.create_all()

# Run migrations (if using Alembic)
alembic upgrade head
```

### Environment Setup
- Copy `.env` file and configure `DATABASE_URL` and `NGROK_URL`
- Ensure PostgreSQL database is accessible
- Python 3.7+ required

## Architecture Patterns
- **Dependency Injection**: FastAPI's dependency system for database sessions
- **Service Layer Pattern**: Business logic separated into service classes
- **Repository Pattern**: Database operations abstracted through SQLAlchemy models
- **Async Context Managers**: Application lifespan management for startup/shutdown