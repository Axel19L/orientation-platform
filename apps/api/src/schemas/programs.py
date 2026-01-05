"""
Schemas para programas e instituciones.
"""

from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.base import (
    BaseSchema,
    InstitutionType,
    Modality,
    PaginatedResponse,
    ProgramType,
    Shift,
)


class InstitutionResponse(BaseSchema):
    """Schema de respuesta para institución."""

    id: UUID
    name: str
    short_name: str | None = None
    type: InstitutionType
    province: str
    city: str | None = None
    website: str | None = None
    is_public: bool


class InstitutionBrief(BaseSchema):
    """Schema breve de institución para listados."""

    id: UUID
    name: str
    short_name: str | None = None


class ProgramBase(BaseModel):
    """Campos base del programa."""

    name: str = Field(..., max_length=300, description="Nombre del programa")
    type: ProgramType = Field(..., description="Tipo de programa")
    duration_years: float | None = Field(None, ge=0.5, le=10, description="Duración en años")
    modality: Modality = Field(..., description="Modalidad de cursado")
    weekly_hours: int | None = Field(None, ge=1, le=60, description="Carga horaria semanal")
    shift: Shift | None = Field(None, description="Turno de cursado")
    area: str = Field(..., max_length=50, description="Área de conocimiento")
    work_compatible: bool | None = Field(None, description="Compatible con trabajo")
    description: str | None = Field(None, description="Descripción del programa")
    requirements: str | None = Field(None, description="Requisitos de ingreso")


class ProgramResponse(BaseSchema, ProgramBase):
    """Schema de respuesta completa del programa."""

    id: UUID
    institution: InstitutionResponse


class ProgramBrief(BaseSchema):
    """Schema breve del programa para listados."""

    id: UUID
    name: str
    type: ProgramType
    duration_years: float | None
    modality: Modality
    weekly_hours: int | None
    shift: Shift | None
    area: str
    work_compatible: bool | None
    institution: InstitutionBrief


class ProgramListResponse(PaginatedResponse):
    """Respuesta paginada de programas."""

    items: list[ProgramBrief]


class ProgramFilters(BaseModel):
    """Filtros para búsqueda de programas."""

    area: str | None = None
    type: str | None = None
    modality: str | None = None
    province: str | None = None
    work_compatible: bool | None = None
    max_duration: float | None = None
