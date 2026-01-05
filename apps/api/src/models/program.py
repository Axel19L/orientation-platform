"""
Modelo de programa educativo.
"""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Program(BaseModel):
    """Programa educativo (carrera, tecnicatura, curso)."""

    __tablename__ = "programs"

    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'degree', 'technical', 'course'
    duration_years: Mapped[float | None] = mapped_column(Numeric(3, 1), nullable=True)
    modality: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'in_person', 'remote', 'hybrid'
    weekly_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shift: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # 'morning', 'afternoon', 'evening', 'flexible'
    area: Mapped[str] = mapped_column(String(50), nullable=False)
    work_compatible: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relaciones
    institution: Mapped["Institution"] = relationship(  # noqa: F821
        "Institution", back_populates="programs"
    )
    trajectories: Mapped[list["Trajectory"]] = relationship(  # noqa: F821
        "Trajectory", back_populates="program", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Program(id={self.id}, name={self.name})>"
