"""
Modelos SQLAlchemy para la base de datos.
"""

from src.models.feedback import Feedback
from src.models.institution import Institution
from src.models.profile import Profile
from src.models.program import Program
from src.models.recommendation import Recommendation
from src.models.trajectory import Trajectory

__all__ = [
    "Profile",
    "Institution",
    "Program",
    "Trajectory",
    "Recommendation",
    "Feedback",
]
