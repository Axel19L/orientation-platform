"""
Modelo de trayectoria de estudiante.
"""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Trajectory(BaseModel):
    """Historia/trayectoria de un estudiante (anonimizada)."""

    __tablename__ = "trajectories"

    program_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("programs.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    story: Mapped[str] = mapped_column(Text, nullable=False)
    challenges: Mapped[str | None] = mapped_column(Text, nullable=True)
    alternatives: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'completed', 'switched', 'dropped', 'in_progress'
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String(50)), nullable=True)
    context: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    year_started: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relaciones
    program: Mapped["Program | None"] = relationship(  # noqa: F821
        "Program", back_populates="trajectories"
    )

    def __repr__(self) -> str:
        return f"<Trajectory(id={self.id}, title={self.title[:30]})>"
