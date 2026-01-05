"""
Configuración de la aplicación.

Usa pydantic-settings para cargar variables de entorno.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql://orientation:orientation@localhost:5432/orientation_db"

    # Environment
    environment: str = "development"
    debug: bool = True

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Orientation Platform API"

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Retorna la lista de orígenes CORS permitidos."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Retorna True si estamos en desarrollo."""
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Retorna la configuración de la aplicación.

    Usa lru_cache para evitar crear múltiples instancias.
    """
    return Settings()
