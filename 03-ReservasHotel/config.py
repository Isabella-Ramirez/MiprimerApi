"""Configuración de variables de entorno para la aplicación."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Contenedor de variables de configuración leídas de entorno."""

    DATABASE_URL: str = os.getenv('DATABASE_URL')
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 8000))
    RELOAD: bool = os.getenv('RELOAD', 'true').lower() == 'true'


settings = Settings()