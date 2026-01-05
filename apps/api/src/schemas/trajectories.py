"""
Schemas para trayectorias de estudiantes.
"""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.base import BaseSchema, PaginatedResponse, TrajectoryOutcome
from src.schemas.programs import InstitutionBrief


class TrajectoryProgramBrief(BaseSchema):
    """Programa breve para trayectoria."""

    id: UUID
    name: str
    institution: InstitutionBrief | None = None


class TrajectoryBase(BaseModel):
    """Campos base de la trayectoria."""

    title: str = Field(..., max_length=200, description="Título descriptivo")
    summary: str = Field(..., max_length=500, description="Resumen corto")
    story: str = Field(..., description="Historia completa")
    challenges: str | None = Field(None, description="Desafíos enfrentados")
    alternatives: str | None = Field(None, description="Alternativas consideradas")
    outcome: TrajectoryOutcome = Field(..., description="Resultado de la trayectoria")
    tags: list[str] | None = Field(None, description="Tags para categorizar")
    context: dict[str, Any] | None = Field(None, description="Contexto adicional")
    year_started: int | None = Field(None, ge=2000, le=2030, description="Año de inicio")


class TrajectoryResponse(BaseSchema, TrajectoryBase):
    """Schema de respuesta completa de trayectoria."""

    id: UUID
    program: TrajectoryProgramBrief | None = None
    is_verified: bool


class TrajectoryBrief(BaseSchema):
    """Schema breve de trayectoria para listados."""

    id: UUID
    title: str
    summary: str
    outcome: TrajectoryOutcome
    tags: list[str] | None
    program: TrajectoryProgramBrief | None = None


class TrajectoryListResponse(PaginatedResponse):
    """Respuesta paginada de trayectorias."""

    items: list[TrajectoryBrief]


class TrajectoryFilters(BaseModel):
    """Filtros para búsqueda de trayectorias."""

    tags: list[str] | None = None
    outcome: str | None = None
    area: str | None = None
