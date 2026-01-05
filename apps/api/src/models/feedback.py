"""
Modelo de feedback.
"""

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class Feedback(BaseModel):
    """Feedback de usuario sobre recomendaciones/trayectorias/programas."""

    __tablename__ = "feedback"

    profile_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True
    )
    target_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'recommendation', 'trajectory', 'program'
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, rating={self.rating})>"
