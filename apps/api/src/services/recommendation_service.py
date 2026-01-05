"""
Servicio de recomendaciones.

Motor de recomendaciones v1 basado en reglas explicables.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from src.models.profile import Profile
from src.models.program import Program
from src.models.recommendation import Recommendation
from src.models.trajectory import Trajectory
from src.schemas.recommendations import (
    MatchedTrajectory,
    ReasonDetail,
    RecommendationResponse,
    RecommendedProgram,
    RecommendedProgramBrief,
)
from src.schemas.programs import InstitutionBrief


class RecommendationService:
    """
    Motor de recomendaciones basado en reglas.

    Factores de scoring:
    - interest_match: Coincidencia con áreas de interés (0.4)
    - work_compatible: Compatibilidad con trabajo (0.25)
    - modality_match: Coincidencia de modalidad (0.15)
    - location: Disponibilidad en la provincia (0.1)
    - duration: Preferencia por duraciones menores (0.1)
    """

    # Pesos de cada factor
    WEIGHTS = {
        "interest_match": 0.40,
        "work_compatible": 0.25,
        "modality_match": 0.15,
        "location": 0.10,
        "duration": 0.10,
    }

    def __init__(self, db: Session):
        self.db = db

    def generate(self, profile_id: UUID, limit: int = 10) -> RecommendationResponse:
        """Genera recomendaciones para un perfil."""
        # Obtener perfil
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise ValueError("Perfil no encontrado")

        # Obtener todos los programas
        programs = (
            self.db.query(Program)
            .options(joinedload(Program.institution))
            .all()
        )

        # Calcular scores
        scored_programs = []
        for program in programs:
            score, reasons = self._calculate_score(profile, program)
            if score > 0:
                matched_trajectories = self._find_matching_trajectories(profile, program)
                scored_programs.append({
                    "program": program,
                    "score": score,
                    "reasons": reasons,
                    "matched_trajectories": matched_trajectories,
                })

        # Ordenar por score y limitar
        scored_programs.sort(key=lambda x: x["score"], reverse=True)
        top_programs = scored_programs[:limit]

        # Crear respuesta
        recommended_programs = [
            RecommendedProgram(
                program_id=p["program"].id,
                program=RecommendedProgramBrief(
                    id=p["program"].id,
                    name=p["program"].name,
                    institution=InstitutionBrief(
                        id=p["program"].institution.id,
                        name=p["program"].institution.name,
                        short_name=p["program"].institution.short_name,
                    ),
                ),
                score=round(p["score"], 3),
                reasons=p["reasons"],
                matched_trajectories=p["matched_trajectories"],
            )
            for p in top_programs
        ]

        # Guardar recomendación
        recommendation = Recommendation(
            profile_id=profile_id,
            programs=[
                {
                    "program_id": str(rp.program_id),
                    "score": rp.score,
                    "reasons": [r.model_dump(mode='json') for r in rp.reasons],
                    "matched_trajectories": [mt.model_dump(mode='json') for mt in rp.matched_trajectories],
                }
                for rp in recommended_programs
            ],
        )
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)

        return RecommendationResponse(
            id=recommendation.id,
            profile_id=profile_id,
            created_at=recommendation.created_at,
            programs=recommended_programs,
        )

    def _calculate_score(
        self, profile: Profile, program: Program
    ) -> tuple[float, list[ReasonDetail]]:
        """
        Calcula el score de un programa para un perfil.

        Retorna el score total y la lista de razones.
        """
        score = 0.0
        reasons = []

        # 1. Interest Match (40%)
        if profile.interest_areas and program.area:
            if program.area in profile.interest_areas:
                contribution = self.WEIGHTS["interest_match"]
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="interest_match",
                        description=f"Coincide con tu interés en {self._area_display_name(program.area)}",
                        weight=self.WEIGHTS["interest_match"],
                        contribution=round(contribution, 3),
                    )
                )

        # 2. Work Compatible (25%)
        if profile.works_while_studying in ["yes", "maybe"]:
            if program.work_compatible:
                contribution = self.WEIGHTS["work_compatible"]
                score += contribution
                shift_text = self._shift_display_name(program.shift) if program.shift else ""
                reasons.append(
                    ReasonDetail(
                        factor="work_compatible",
                        description=f"Compatible con trabajo{f' ({shift_text})' if shift_text else ''}",
                        weight=self.WEIGHTS["work_compatible"],
                        contribution=round(contribution, 3),
                    )
                )
            elif program.shift == "evening":
                # Turno noche parcialmente compatible
                contribution = self.WEIGHTS["work_compatible"] * 0.7
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="work_compatible",
                        description="Turno noche, puede ser compatible con trabajo",
                        weight=self.WEIGHTS["work_compatible"],
                        contribution=round(contribution, 3),
                    )
                )

        # 3. Modality Match (15%)
        if profile.preferred_modality and profile.preferred_modality != "no_preference":
            if program.modality == profile.preferred_modality:
                contribution = self.WEIGHTS["modality_match"]
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="modality_match",
                        description=f"Modalidad {self._modality_display_name(program.modality)} como preferís",
                        weight=self.WEIGHTS["modality_match"],
                        contribution=round(contribution, 3),
                    )
                )
            elif program.modality == "hybrid":
                # Híbrido siempre suma algo
                contribution = self.WEIGHTS["modality_match"] * 0.5
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="modality_match",
                        description="Modalidad híbrida (flexible)",
                        weight=self.WEIGHTS["modality_match"],
                        contribution=round(contribution, 3),
                    )
                )

        # 4. Location (10%)
        if profile.province:
            if program.institution.province == profile.province:
                contribution = self.WEIGHTS["location"]
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="location",
                        description="Disponible en tu provincia",
                        weight=self.WEIGHTS["location"],
                        contribution=round(contribution, 3),
                    )
                )
            elif program.modality == "remote":
                # Virtual disponible desde cualquier lugar
                contribution = self.WEIGHTS["location"] * 0.8
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="location",
                        description="100% virtual, accesible desde cualquier lugar",
                        weight=self.WEIGHTS["location"],
                        contribution=round(contribution, 3),
                    )
                )

        # 5. Duration (10%)
        if program.duration_years:
            if program.duration_years <= 3:
                contribution = self.WEIGHTS["duration"]
                score += contribution
                duration_text = f"{program.duration_years} años" if program.duration_years > 1 else "1 año"
                reasons.append(
                    ReasonDetail(
                        factor="duration",
                        description=f"Duración corta ({duration_text})",
                        weight=self.WEIGHTS["duration"],
                        contribution=round(contribution, 3),
                    )
                )
            elif program.duration_years <= 5:
                contribution = self.WEIGHTS["duration"] * 0.5
                score += contribution
                reasons.append(
                    ReasonDetail(
                        factor="duration",
                        description=f"Duración media ({program.duration_years} años)",
                        weight=self.WEIGHTS["duration"],
                        contribution=round(contribution, 3),
                    )
                )

        return score, reasons

    def _find_matching_trajectories(
        self, profile: Profile, program: Program
    ) -> list[MatchedTrajectory]:
        """Encuentra trayectorias que coinciden con el perfil y programa."""
        trajectories = (
            self.db.query(Trajectory)
            .filter(Trajectory.program_id == program.id)
            .filter(Trajectory.is_verified == True)
            .limit(3)
            .all()
        )

        matched = []
        for traj in trajectories:
            match_reason = self._get_trajectory_match_reason(profile, traj)
            if match_reason:
                matched.append(
                    MatchedTrajectory(
                        id=traj.id,
                        title=traj.title,
                        match_reason=match_reason,
                    )
                )

        return matched

    def _get_trajectory_match_reason(self, profile: Profile, trajectory: Trajectory) -> str | None:
        """Determina por qué una trayectoria coincide con el perfil."""
        context = trajectory.context or {}

        # Buscar coincidencias en el contexto
        if profile.works_while_studying == "yes" and context.get("worked_while_studying"):
            return "También trabajaba mientras estudiaba"

        if profile.province and context.get("province") == profile.province:
            return f"Estudió en {profile.province}"

        if trajectory.tags:
            if "first_generation" in trajectory.tags:
                return "Primera generación universitaria en su familia"
            if "career_change" in trajectory.tags:
                return "Cambió de carrera durante el camino"
            if "remote_learning" in trajectory.tags and profile.preferred_modality == "remote":
                return "Estudió de forma virtual"

        # Match genérico
        return "Eligió este programa en una situación similar"

    def get_by_id(self, recommendation_id: UUID) -> RecommendationResponse | None:
        """Obtiene una recomendación por ID."""
        recommendation = (
            self.db.query(Recommendation)
            .filter(Recommendation.id == recommendation_id)
            .first()
        )
        if not recommendation:
            return None

        # Reconstruir la respuesta desde el JSON guardado
        programs = []
        for p in recommendation.programs:
            # Cargar el programa completo desde la BD
            program = self.db.query(Program).filter(Program.id == p["program_id"]).first()
            program_brief = None
            if program:
                program_brief = RecommendedProgramBrief(
                    id=program.id,
                    name=program.name,
                    type=program.type,
                    duration_years=program.duration_years,
                    modality=program.modality,
                    area=program.area,
                    institution_name=program.institution.short_name if program.institution else None,
                )
            
            programs.append(
                RecommendedProgram(
                    program_id=p["program_id"],
                    program=program_brief,
                    score=p["score"],
                    reasons=[ReasonDetail(**r) for r in p["reasons"]],
                    matched_trajectories=[MatchedTrajectory(**mt) for mt in p.get("matched_trajectories", [])],
                )
            )

        return RecommendationResponse(
            id=recommendation.id,
            profile_id=recommendation.profile_id,
            created_at=recommendation.created_at,
            programs=programs,
        )

    @staticmethod
    def _area_display_name(area: str) -> str:
        """Convierte el código de área a nombre legible."""
        names = {
            "technology": "Tecnología",
            "health": "Salud",
            "social_sciences": "Ciencias Sociales",
            "exact_sciences": "Ciencias Exactas",
            "arts": "Arte y Diseño",
            "business": "Negocios",
            "education": "Educación",
            "engineering": "Ingeniería",
            "law": "Derecho",
            "communication": "Comunicación",
            "agriculture": "Agro y Ambiente",
            "trades": "Oficios",
        }
        return names.get(area, area.replace("_", " ").title())

    @staticmethod
    def _modality_display_name(modality: str) -> str:
        """Convierte el código de modalidad a nombre legible."""
        names = {
            "in_person": "presencial",
            "remote": "virtual",
            "hybrid": "híbrida",
        }
        return names.get(modality, modality)

    @staticmethod
    def _shift_display_name(shift: str) -> str:
        """Convierte el código de turno a nombre legible."""
        names = {
            "morning": "turno mañana",
            "afternoon": "turno tarde",
            "evening": "turno noche",
            "flexible": "horario flexible",
        }
        return names.get(shift, shift)
