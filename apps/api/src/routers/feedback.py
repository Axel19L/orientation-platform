"""
Router para feedback de usuarios.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.feedback import FeedbackCreate, FeedbackResponse
from src.services.feedback_service import FeedbackService

router = APIRouter()


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar feedback",
    description="Envía feedback sobre una recomendación, trayectoria o programa.",
)
def create_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
) -> FeedbackResponse:
    """Crea un nuevo feedback."""
    service = FeedbackService(db)
    feedback = service.create(data)
    return feedback
