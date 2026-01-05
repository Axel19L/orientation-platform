"""
Router para recomendaciones.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.recommendations import (
    RecommendationCreate,
    RecommendationResponse,
)
from src.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generar recomendaciones",
    description="Genera recomendaciones de programas para un perfil.",
)
def create_recommendation(
    data: RecommendationCreate,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Genera recomendaciones para un perfil."""
    service = RecommendationService(db)
    try:
        recommendation = service.generate(data.profile_id, data.limit)
        return recommendation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
    summary="Obtener recomendación",
    description="Obtiene una recomendación guardada por su ID.",
)
def get_recommendation(
    recommendation_id: UUID,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    """Obtiene una recomendación por ID."""
    service = RecommendationService(db)
    recommendation = service.get_by_id(recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada",
        )
    return recommendation
