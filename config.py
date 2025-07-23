import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Ngrok configuration
NGROK_URL = os.getenv("NGROK_URL", "rational-bison-kind.ngrok-free.app")

# Server configuration
HOST = "0.0.0.0"
PORT = 8000
