"""
Schemas Pydantic para validación y serialización.
"""

from src.schemas.feedback import FeedbackCreate, FeedbackResponse
from src.schemas.profiles import ProfileCreate, ProfileResponse, ProfileUpdate
from src.schemas.programs import (
    InstitutionResponse,
    ProgramFilters,
    ProgramListResponse,
    ProgramResponse,
)
from src.schemas.recommendations import (
    RecommendationCreate,
    RecommendationResponse,
)
from src.schemas.trajectories import (
    TrajectoryFilters,
    TrajectoryListResponse,
    TrajectoryResponse,
)

__all__ = [
    "ProfileCreate",
    "ProfileUpdate",
    "ProfileResponse",
    "ProgramResponse",
    "ProgramListResponse",
    "ProgramFilters",
    "InstitutionResponse",
    "TrajectoryResponse",
    "TrajectoryListResponse",
    "TrajectoryFilters",
    "RecommendationCreate",
    "RecommendationResponse",
    "FeedbackCreate",
    "FeedbackResponse",
]
