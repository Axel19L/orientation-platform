"""
Modelo de perfil de estudiante.
"""

from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class Profile(BaseModel):
    """Perfil de un estudiante (sin datos personales identificables)."""

    __tablename__ = "profiles"

    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    locality: Mapped[str | None] = mapped_column(String(200), nullable=True)
    works_while_studying: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # 'yes', 'no', 'maybe'
    preferred_modality: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # 'in_person', 'remote', 'hybrid', 'no_preference'
    max_weekly_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    has_technical_degree: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    interest_areas: Mapped[list[str] | None] = mapped_column(
        ARRAY(String(50)).with_variant(JSON(), "sqlite"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<Profile(id={self.id}, province={self.province})>"
