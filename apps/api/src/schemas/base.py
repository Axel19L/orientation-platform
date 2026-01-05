"""
Schemas base compartidos.
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Schema base con configuración común."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TimestampMixin(BaseModel):
    """Mixin para timestamps."""

    created_at: datetime
    updated_at: datetime | None = None


class WorksWhileStudying(str, Enum):
    """Opciones para si trabaja mientras estudia."""

    YES = "yes"
    NO = "no"
    MAYBE = "maybe"


class Modality(str, Enum):
    """Modalidades de cursado."""

    IN_PERSON = "in_person"
    REMOTE = "remote"
    HYBRID = "hybrid"
    NO_PREFERENCE = "no_preference"


class ProgramType(str, Enum):
    """Tipos de programa educativo."""

    DEGREE = "degree"  # Carrera universitaria
    TECHNICAL = "technical"  # Tecnicatura
    COURSE = "course"  # Curso/diplomatura


class InstitutionType(str, Enum):
    """Tipos de institución."""

    UNIVERSITY = "university"
    INSTITUTE = "institute"
    OTHER = "other"


class Shift(str, Enum):
    """Turnos de cursado."""

    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    FLEXIBLE = "flexible"


class TrajectoryOutcome(str, Enum):
    """Resultados posibles de una trayectoria."""

    COMPLETED = "completed"
    SWITCHED = "switched"
    DROPPED = "dropped"
    IN_PROGRESS = "in_progress"


class FeedbackTargetType(str, Enum):
    """Tipos de target para feedback."""

    RECOMMENDATION = "recommendation"
    TRAJECTORY = "trajectory"
    PROGRAM = "program"


class InterestArea(str, Enum):
    """Áreas de interés predefinidas."""

    TECHNOLOGY = "technology"
    HEALTH = "health"
    SOCIAL_SCIENCES = "social_sciences"
    EXACT_SCIENCES = "exact_sciences"
    ARTS = "arts"
    BUSINESS = "business"
    EDUCATION = "education"
    ENGINEERING = "engineering"
    LAW = "law"
    COMMUNICATION = "communication"
    AGRICULTURE = "agriculture"
    TRADES = "trades"


class PaginatedResponse(BaseSchema):
    """Respuesta paginada genérica."""

    total: int
    page: int
    per_page: int
    pages: int


class UUIDMixin(BaseModel):
    """Mixin para ID UUID."""

    id: UUID
