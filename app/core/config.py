import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangChain Gemini API"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Check if the Google API Key is set
if not settings.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")