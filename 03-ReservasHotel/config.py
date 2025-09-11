import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 8000))
    DEBUG: bool = os.getenv('DEBUG', 'true').lower() == 'true'
    RELOAD: bool = os.getenv('RELOAD', 'true').lower() == 'true'
    ENV: str = os.getenv('ENV', 'development')

settings = Settings()