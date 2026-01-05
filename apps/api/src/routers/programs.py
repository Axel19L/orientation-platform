"""
Router para programas educativos.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.programs import ProgramFilters, ProgramListResponse, ProgramResponse
from src.services.program_service import ProgramService

router = APIRouter()


@router.get(
    "",
    response_model=ProgramListResponse,
    summary="Listar programas",
    description="Lista programas educativos con filtros opcionales.",
)
def list_programs(
    area: str | None = Query(None, description="Filtrar por área de conocimiento"),
    program_type: str | None = Query(None, alias="type", description="Tipo de programa"),
    modality: str | None = Query(None, description="Modalidad de cursado"),
    province: str | None = Query(None, description="Provincia de la institución"),
    work_compatible: bool | None = Query(None, description="Compatible con trabajo"),
    max_duration: float | None = Query(None, description="Duración máxima en años"),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Items por página"),
    db: Session = Depends(get_db),
) -> ProgramListResponse:
    """Lista programas con filtros y paginación."""
    filters = ProgramFilters(
        area=area,
        type=program_type,
        modality=modality,
        province=province,
        work_compatible=work_compatible,
        max_duration=max_duration,
    )
    service = ProgramService(db)
    return service.list(filters=filters, page=page, per_page=per_page)


@router.get(
    "/{program_id}",
    response_model=ProgramResponse,
    summary="Obtener programa",
    description="Obtiene el detalle de un programa por su ID.",
)
def get_program(
    program_id: UUID,
    db: Session = Depends(get_db),
) -> ProgramResponse:
    """Obtiene un programa por ID."""
    service = ProgramService(db)
    program = service.get_by_id(program_id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Programa no encontrado",
        )
    return program
