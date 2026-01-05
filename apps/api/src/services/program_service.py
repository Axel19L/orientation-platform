"""
Servicio para gestión de programas.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from src.models.program import Program
from src.schemas.programs import ProgramFilters, ProgramListResponse, ProgramResponse


class ProgramService:
    """Servicio para operaciones de programas."""

    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        filters: ProgramFilters | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> ProgramListResponse:
        """Lista programas con filtros y paginación."""
        query = self.db.query(Program).options(joinedload(Program.institution))

        # Aplicar filtros
        if filters:
            if filters.area:
                query = query.filter(Program.area == filters.area)
            if filters.type:
                query = query.filter(Program.type == filters.type)
            if filters.modality:
                query = query.filter(Program.modality == filters.modality)
            if filters.work_compatible is not None:
                query = query.filter(Program.work_compatible == filters.work_compatible)
            if filters.max_duration:
                query = query.filter(Program.duration_years <= filters.max_duration)
            if filters.province:
                query = query.join(Program.institution).filter(
                    Program.institution.has(province=filters.province)
                )

        # Contar total
        total = query.count()

        # Paginación
        offset = (page - 1) * per_page
        programs = query.offset(offset).limit(per_page).all()

        # Calcular páginas
        pages = (total + per_page - 1) // per_page

        return ProgramListResponse(
            items=programs,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

    def get_by_id(self, program_id: UUID) -> ProgramResponse | None:
        """Obtiene un programa por ID."""
        program = (
            self.db.query(Program)
            .options(joinedload(Program.institution))
            .filter(Program.id == program_id)
            .first()
        )
        if not program:
            return None
        return ProgramResponse.model_validate(program)
