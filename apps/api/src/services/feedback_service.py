"""
Servicio para gestión de feedback.
"""

from sqlalchemy.orm import Session

from src.models.feedback import Feedback
from src.schemas.feedback import FeedbackCreate, FeedbackResponse


class FeedbackService:
    """Servicio para operaciones de feedback."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: FeedbackCreate) -> FeedbackResponse:
        """Crea un nuevo feedback."""
        feedback = Feedback(
            profile_id=data.profile_id,
            target_type=data.target_type.value,
            target_id=data.target_id,
            rating=data.rating,
            comment=data.comment,
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return FeedbackResponse(
            id=feedback.id,
            created_at=feedback.created_at,
            message="¡Gracias por tu feedback!",
        )
