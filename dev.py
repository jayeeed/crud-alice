from fastapi import FastAPI
import uvicorn
from pyngrok import ngrok
from routes import router
from database import init_database
from config import NGROK_URL, HOST, PORT

app = FastAPI(title="CRUD API", description="Simple CRUD API with PostgreSQL")

# Include routes
app.include_router(router)


# Initialize database on startup
@app.on_event("startup")
async def startup():
    init_database()


# Setup ngrok
custom_domain = NGROK_URL
public_url = ngrok.connect(addr=PORT, url=custom_domain)
print(f"Public URL: {public_url}")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
