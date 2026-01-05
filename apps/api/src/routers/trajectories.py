"""
Router para trayectorias de estudiantes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.trajectories import (
    TrajectoryFilters,
    TrajectoryListResponse,
    TrajectoryResponse,
)
from src.services.trajectory_service import TrajectoryService

router = APIRouter()


@router.get(
    "",
    response_model=TrajectoryListResponse,
    summary="Listar trayectorias",
    description="Lista trayectorias de estudiantes con filtros opcionales.",
)
def list_trajectories(
    tags: str | None = Query(None, description="Tags separados por coma"),
    outcome: str | None = Query(None, description="Resultado de la trayectoria"),
    area: str | None = Query(None, description="Área del programa relacionado"),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db),
) -> TrajectoryListResponse:
    """Lista trayectorias con filtros y paginación."""
    filters = TrajectoryFilters(
        tags=tags.split(",") if tags else None,
        outcome=outcome,
        area=area,
    )
    service = TrajectoryService(db)
    return service.list(filters=filters, page=page, per_page=per_page)


@router.get(
    "/{trajectory_id}",
    response_model=TrajectoryResponse,
    summary="Obtener trayectoria",
    description="Obtiene el detalle completo de una trayectoria.",
)
def get_trajectory(
    trajectory_id: UUID,
    db: Session = Depends(get_db),
) -> TrajectoryResponse:
    """Obtiene una trayectoria por ID."""
    service = TrajectoryService(db)
    trajectory = service.get_by_id(trajectory_id)
    if not trajectory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trayectoria no encontrada",
        )
    return trajectory
