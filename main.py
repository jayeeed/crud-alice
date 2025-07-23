from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from routes import router
from database import init_database
from health import health_start, health_stop
from config import HOST, PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_database()
    health_start()
    yield
    # Shutdown logic
    health_stop()


app = FastAPI(lifespan=lifespan)

# Include routes
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
