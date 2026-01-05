"""
Schemas para feedback de usuarios.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.base import BaseSchema, FeedbackTargetType


class FeedbackCreate(BaseModel):
    """Schema para crear feedback."""

    profile_id: UUID | None = Field(None, description="ID del perfil (opcional)")
    target_type: FeedbackTargetType = Field(..., description="Tipo de elemento evaluado")
    target_id: UUID = Field(..., description="ID del elemento evaluado")
    rating: int = Field(..., ge=1, le=5, description="Calificación 1-5")
    comment: str | None = Field(None, max_length=1000, description="Comentario opcional")


class FeedbackResponse(BaseSchema):
    """Respuesta de feedback."""

    id: UUID
    created_at: datetime
    message: str = "¡Gracias por tu feedback!"
