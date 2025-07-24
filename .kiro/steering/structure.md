# Project Structure

## Root Level Files
- **main.py**: Production application entry point with lifespan management
- **dev.py**: Development server with ngrok integration
- **config.py**: Configuration management and environment variables
- **requirements.txt**: Python dependencies

## Core Application Modules
- **models.py**: Pydantic models for request/response validation
  - `ItemCreate`: Model for creating new items
  - `ItemUpdate`: Model for updating existing items (supports partial updates)

- **database.py**: Database configuration and SQLAlchemy models
  - Database connection setup and session management
  - `Item`: SQLAlchemy model for items table
  - `get_db()`: Dependency for database sessions
  - `init_database()`: Database initialization function

- **routes.py**: FastAPI route definitions and endpoint handlers
  - All API endpoints with proper HTTP methods
  - Request/response handling and validation
  - Dependency injection for database sessions

- **services.py**: Business logic layer
  - `ItemService`: Static class containing all CRUD operations
  - Error handling and logging
  - Database transaction management

- **health.py**: Health monitoring and background tasks
  - Scheduled health checks using APScheduler
  - External service monitoring

## Configuration Files
- **.env**: Environment variables (DATABASE_URL, NGROK_URL)
- **.gitignore**: Git ignore patterns
- **.kiro/**: Kiro IDE configuration and steering rules

## Conventions
- **Logging**: Comprehensive logging throughout all modules using Python's logging module
- **Error Handling**: Consistent HTTPException usage with proper status codes
- **UUID Usage**: All item IDs use UUID4 format
- **Database Sessions**: Always use dependency injection for database access
- **Transaction Management**: Proper commit/rollback handling in service layer
- **Async Patterns**: Async/await used consistently for route handlers