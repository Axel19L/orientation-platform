"""
Router para perfiles de estudiantes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.profiles import ProfileCreate, ProfileResponse, ProfileUpdate
from src.services.profile_service import ProfileService

router = APIRouter()


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear perfil",
    description="Crea un nuevo perfil de estudiante.",
)
def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """Crea un nuevo perfil de estudiante."""
    service = ProfileService(db)
    profile = service.create(profile_data)
    return profile


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Obtener perfil",
    description="Obtiene un perfil por su ID.",
)
def get_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """Obtiene un perfil por ID."""
    service = ProfileService(db)
    profile = service.get_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado",
        )
    return profile


@router.patch(
    "/{profile_id}",
    response_model=ProfileResponse,
    summary="Actualizar perfil",
    description="Actualiza parcialmente un perfil existente.",
)
def update_profile(
    profile_id: UUID,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
) -> ProfileResponse:
    """Actualiza un perfil existente."""
    service = ProfileService(db)
    profile = service.update(profile_id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado",
        )
    return profile
