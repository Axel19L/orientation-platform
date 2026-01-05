"""
Servicio para gestión de trayectorias.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from src.models.trajectory import Trajectory
from src.schemas.trajectories import (
    TrajectoryFilters,
    TrajectoryListResponse,
    TrajectoryResponse,
)


class TrajectoryService:
    """Servicio para operaciones de trayectorias."""

    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        filters: TrajectoryFilters | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> TrajectoryListResponse:
        """Lista trayectorias con filtros y paginación."""
        query = (
            self.db.query(Trajectory)
            .options(joinedload(Trajectory.program))
            .filter(Trajectory.is_verified == True)  # Solo verificadas
        )

        # Aplicar filtros
        if filters:
            if filters.outcome:
                query = query.filter(Trajectory.outcome == filters.outcome)
            if filters.tags:
                # Filtrar por tags (al menos uno debe coincidir)
                query = query.filter(Trajectory.tags.overlap(filters.tags))
            if filters.area:
                query = query.join(Trajectory.program).filter(
                    Trajectory.program.has(area=filters.area)
                )

        # Contar total
        total = query.count()

        # Paginación
        offset = (page - 1) * per_page
        trajectories = query.offset(offset).limit(per_page).all()

        # Calcular páginas
        pages = (total + per_page - 1) // per_page

        return TrajectoryListResponse(
            items=trajectories,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
        )

    def get_by_id(self, trajectory_id: UUID) -> TrajectoryResponse | None:
        """Obtiene una trayectoria por ID."""
        trajectory = (
            self.db.query(Trajectory)
            .options(joinedload(Trajectory.program))
            .filter(Trajectory.id == trajectory_id)
            .first()
        )
        if not trajectory:
            return None
        return TrajectoryResponse.model_validate(trajectory)
