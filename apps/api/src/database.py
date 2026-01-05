"""
Configuración de la base de datos.

Usa SQLAlchemy 2.0 con patrón async-compatible.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.config import get_settings

settings = get_settings()

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries en desarrollo
    pool_pre_ping=True,  # Verificar conexión antes de usar
)

# Crear session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency que provee una sesión de base de datos.

    Uso:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
