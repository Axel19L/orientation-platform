"""
Modelo de recomendación.
"""

import uuid

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Recommendation(BaseModel):
    """Recomendación generada para un perfil."""

    __tablename__ = "recommendations"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )
    programs: Mapped[list] = mapped_column(
        JSONB().with_variant(JSON(), "sqlite"), nullable=False, default=list
    )

    # Relaciones
    profile: Mapped["Profile"] = relationship("Profile")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, profile_id={self.profile_id})>"
