"""
Servicio para gestión de perfiles.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from src.models.profile import Profile
from src.schemas.profiles import ProfileCreate, ProfileResponse, ProfileUpdate


class ProfileService:
    """Servicio para operaciones CRUD de perfiles."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ProfileCreate) -> ProfileResponse:
        """Crea un nuevo perfil."""
        profile = Profile(
            province=data.province,
            locality=data.locality,
            works_while_studying=data.works_while_studying.value if data.works_while_studying else None,
            preferred_modality=data.preferred_modality.value if data.preferred_modality else None,
            max_weekly_hours=data.max_weekly_hours,
            has_technical_degree=data.has_technical_degree,
            interest_areas=[area.value for area in data.interest_areas] if data.interest_areas else None,
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return ProfileResponse.model_validate(profile)

    def get_by_id(self, profile_id: UUID) -> ProfileResponse | None:
        """Obtiene un perfil por ID."""
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None
        return ProfileResponse.model_validate(profile)

    def update(self, profile_id: UUID, data: ProfileUpdate) -> ProfileResponse | None:
        """Actualiza un perfil existente."""
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field == "works_while_studying" and value:
                value = value.value
            elif field == "preferred_modality" and value:
                value = value.value
            elif field == "interest_areas" and value:
                value = [area.value for area in value]
            setattr(profile, field, value)

        self.db.commit()
        self.db.refresh(profile)
        return ProfileResponse.model_validate(profile)
