"""
Modelo de institución educativa.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Institution(BaseModel):
    """Institución educativa (universidad, instituto, etc.)."""

    __tablename__ = "institutions"

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'university', 'institute', 'other'
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str | None] = mapped_column(String(200), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Relaciones
    programs: Mapped[list["Program"]] = relationship(  # noqa: F821
        "Program", back_populates="institution", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Institution(id={self.id}, short_name={self.short_name})>"
