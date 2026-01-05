"""
Aplicación principal FastAPI.
"""

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __version__
from src.config import get_settings
from src.routers import feedback, profiles, programs, recommendations, trajectories

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación."""
    # Startup
    print(f"🚀 Starting {settings.project_name} v{__version__}")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.project_name,
    description="API para la plataforma de orientación vocacional",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check() -> dict[str, Any]:
    """
    Endpoint de health check.

    Retorna el estado de la API y metadatos básicos.
    """
    return {
        "status": "healthy",
        "version": __version__,
        "environment": settings.environment,
        "timestamp": datetime.now(UTC).isoformat(),
    }


# Registrar routers
app.include_router(
    profiles.router,
    prefix=f"{settings.api_v1_prefix}/profiles",
    tags=["Profiles"],
)

app.include_router(
    programs.router,
    prefix=f"{settings.api_v1_prefix}/programs",
    tags=["Programs"],
)

app.include_router(
    trajectories.router,
    prefix=f"{settings.api_v1_prefix}/trajectories",
    tags=["Trajectories"],
)

app.include_router(
    recommendations.router,
    prefix=f"{settings.api_v1_prefix}/recommendations",
    tags=["Recommendations"],
)

app.include_router(
    feedback.router,
    prefix=f"{settings.api_v1_prefix}/feedback",
    tags=["Feedback"],
)


# Root endpoint
@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Endpoint raíz con información básica."""
    return {
        "message": "Bienvenido a Orientation Platform API",
        "docs": "/docs",
        "health": "/health",
    }
