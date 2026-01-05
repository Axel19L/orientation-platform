"""
Schemas para recomendaciones.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.base import BaseSchema
from src.schemas.programs import InstitutionBrief


class ReasonDetail(BaseSchema):
    """Detalle de una razón de recomendación."""

    factor: str = Field(..., description="Factor que contribuye al score")
    description: str = Field(..., description="Descripción legible")
    weight: float = Field(..., ge=0, le=1, description="Peso del factor")
    contribution: float = Field(..., description="Contribución al score final")


class MatchedTrajectory(BaseSchema):
    """Trayectoria que matchea con el perfil."""

    id: UUID
    title: str
    match_reason: str = Field(..., description="Por qué matchea")


class RecommendedProgramBrief(BaseSchema):
    """Programa recomendado breve."""

    id: UUID
    name: str
    institution: InstitutionBrief


class RecommendedProgram(BaseSchema):
    """Programa recomendado con score y razones."""

    program_id: UUID
    program: RecommendedProgramBrief
    score: float = Field(..., ge=0, le=1, description="Score de recomendación")
    reasons: list[ReasonDetail] = Field(..., description="Razones del score")
    matched_trajectories: list[MatchedTrajectory] = Field(
        default_factory=list, description="Trayectorias similares"
    )


class RecommendationCreate(BaseModel):
    """Schema para solicitar recomendaciones."""

    profile_id: UUID = Field(..., description="ID del perfil")
    limit: int = Field(10, ge=1, le=50, description="Cantidad máxima de recomendaciones")


class RecommendationResponse(BaseSchema):
    """Respuesta de recomendaciones."""

    id: UUID
    profile_id: UUID
    created_at: datetime
    programs: list[RecommendedProgram]
