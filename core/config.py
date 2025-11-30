from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split(",")
OPC_URL = os.getenv("OPC_URL")
OPC_USERNAME = os.getenv("OPC_USERNAME")
OPC_PASSWORD = os.getenv("OPC_PASSWORD")
OPC_NAMESPACE = int(os.getenv("OPC_NAMESPACE", 2))  # Default to 2 if not set

