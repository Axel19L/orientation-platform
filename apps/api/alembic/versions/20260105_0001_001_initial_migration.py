"""Initial migration - Create all tables

Revision ID: 001
Revises:
Create Date: 2026-01-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear tabla institutions
    op.create_table(
        "institutions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("short_name", sa.String(length=50), nullable=True),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("province", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=200), nullable=True),
        sa.Column("website", sa.String(length=500), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Crear tabla profiles
    op.create_table(
        "profiles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("province", sa.String(length=100), nullable=True),
        sa.Column("locality", sa.String(length=200), nullable=True),
        sa.Column("works_while_studying", sa.String(length=20), nullable=True),
        sa.Column("preferred_modality", sa.String(length=20), nullable=True),
        sa.Column("max_weekly_hours", sa.Integer(), nullable=True),
        sa.Column("has_technical_degree", sa.Boolean(), nullable=True),
        sa.Column("interest_areas", postgresql.ARRAY(sa.String(length=50)), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Crear tabla programs
    op.create_table(
        "programs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("duration_years", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("modality", sa.String(length=20), nullable=False),
        sa.Column("weekly_hours", sa.Integer(), nullable=True),
        sa.Column("shift", sa.String(length=20), nullable=True),
        sa.Column("area", sa.String(length=50), nullable=False),
        sa.Column("work_compatible", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("requirements", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_programs_area", "programs", ["area"], unique=False)
    op.create_index("idx_programs_type", "programs", ["type"], unique=False)
    op.create_index("idx_programs_modality", "programs", ["modality"], unique=False)
    op.create_index("idx_programs_institution", "programs", ["institution_id"], unique=False)

    # Crear tabla trajectories
    op.create_table(
        "trajectories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("program_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=False),
        sa.Column("story", sa.Text(), nullable=False),
        sa.Column("challenges", sa.Text(), nullable=True),
        sa.Column("alternatives", sa.Text(), nullable=True),
        sa.Column("outcome", sa.String(length=20), nullable=False),
        sa.Column("tags", postgresql.ARRAY(sa.String(length=50)), nullable=True),
        sa.Column("context", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("year_started", sa.Integer(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["program_id"], ["programs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_trajectories_program", "trajectories", ["program_id"], unique=False)
    op.create_index("idx_trajectories_outcome", "trajectories", ["outcome"], unique=False)
    op.create_index(
        "idx_trajectories_tags",
        "trajectories",
        ["tags"],
        unique=False,
        postgresql_using="gin",
    )

    # Crear tabla recommendations
    op.create_table(
        "recommendations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("programs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_recommendations_profile", "recommendations", ["profile_id"], unique=False)

    # Crear tabla feedback
    op.create_table(
        "feedback",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("profile_id", sa.UUID(), nullable=True),
        sa.Column("target_type", sa.String(length=20), nullable=False),
        sa.Column("target_id", sa.UUID(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_feedback_target", "feedback", ["target_type", "target_id"], unique=False)


def downgrade() -> None:
    op.drop_table("feedback")
    op.drop_table("recommendations")
    op.drop_table("trajectories")
    op.drop_table("programs")
    op.drop_table("profiles")
    op.drop_table("institutions")
