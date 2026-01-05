"""
Schemas para perfiles de estudiantes.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base import BaseSchema, InterestArea, Modality, WorksWhileStudying


class ProfileBase(BaseModel):
    """Campos base del perfil."""

    province: str | None = Field(None, max_length=100, description="Provincia de residencia")
    locality: str | None = Field(None, max_length=200, description="Localidad/ciudad")
    works_while_studying: WorksWhileStudying | None = Field(
        None, description="Si trabaja mientras estudia"
    )
    preferred_modality: Modality | None = Field(None, description="Modalidad preferida")
    max_weekly_hours: int | None = Field(
        None, ge=1, le=80, description="Horas semanales disponibles"
    )
    has_technical_degree: bool | None = Field(
        None, description="Si tiene título técnico secundario"
    )
    interest_areas: list[InterestArea] | None = Field(None, description="Áreas de interés")


class ProfileCreate(ProfileBase):
    """Schema para crear un perfil."""

    pass


class ProfileUpdate(ProfileBase):
    """Schema para actualizar un perfil (todos los campos opcionales)."""

    pass


class ProfileResponse(BaseSchema, ProfileBase):
    """Schema de respuesta del perfil."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
