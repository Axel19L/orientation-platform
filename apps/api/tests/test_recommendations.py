"""
Tests para el motor de recomendaciones.
"""

import pytest

from src.models.institution import Institution
from src.models.profile import Profile
from src.models.program import Program
from src.services.recommendation_service import RecommendationService


class TestRecommendationScoring:
    """Tests para el scoring de recomendaciones."""

    def test_interest_match_scores_highest(self, db):
        """Test que el match de intereses tiene el peso más alto."""
        # Crear institución
        institution = Institution(
            name="Universidad Test",
            short_name="UT",
            type="university",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        # Crear programa en tecnología
        program = Program(
            institution_id=institution.id,
            name="Tecnicatura en Programación",
            type="technical",
            modality="in_person",
            area="technology",
            duration_years=2,
        )
        db.add(program)
        db.commit()
        db.refresh(program)

        # Crear perfil con interés en tecnología
        profile = Profile(interest_areas=["technology"])
        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Calcular score
        service = RecommendationService(db)
        score, reasons = service._calculate_score(profile, program)

        # Verificar que hay razón de interest_match
        interest_reason = next((r for r in reasons if r.factor == "interest_match"), None)
        assert interest_reason is not None
        assert interest_reason.weight == 0.4
        assert "Tecnología" in interest_reason.description

    def test_work_compatible_adds_score(self, db):
        """Test que la compatibilidad con trabajo suma al score."""
        institution = Institution(
            name="UTN",
            short_name="UTN",
            type="university",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        program = Program(
            institution_id=institution.id,
            name="Ingeniería en Sistemas",
            type="degree",
            modality="in_person",
            area="technology",
            work_compatible=True,
            shift="evening",
        )
        db.add(program)
        db.commit()
        db.refresh(program)

        profile = Profile(
            works_while_studying="yes",
            interest_areas=["technology"],
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        score, reasons = service._calculate_score(profile, program)

        work_reason = next((r for r in reasons if r.factor == "work_compatible"), None)
        assert work_reason is not None
        assert "Compatible con trabajo" in work_reason.description

    def test_modality_match_hybrid_partial_score(self, db):
        """Test que modalidad híbrida da score parcial."""
        institution = Institution(
            name="UBA",
            type="university",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        program = Program(
            institution_id=institution.id,
            name="Economía",
            type="degree",
            modality="hybrid",
            area="business",
        )
        db.add(program)
        db.commit()
        db.refresh(program)

        profile = Profile(preferred_modality="remote")
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        score, reasons = service._calculate_score(profile, program)

        modality_reason = next((r for r in reasons if r.factor == "modality_match"), None)
        assert modality_reason is not None
        # Híbrido da 50% del peso cuando preferencia es otra
        assert modality_reason.contribution < modality_reason.weight

    def test_location_match(self, db):
        """Test que la ubicación coincidente suma."""
        institution = Institution(
            name="UNC",
            type="university",
            province="Córdoba",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        program = Program(
            institution_id=institution.id,
            name="Medicina",
            type="degree",
            modality="in_person",
            area="health",
        )
        db.add(program)
        db.commit()
        db.refresh(program)

        profile = Profile(province="Córdoba")
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        score, reasons = service._calculate_score(profile, program)

        location_reason = next((r for r in reasons if r.factor == "location"), None)
        assert location_reason is not None
        assert "tu provincia" in location_reason.description

    def test_short_duration_preferred(self, db):
        """Test que duraciones cortas suman más."""
        institution = Institution(
            name="ISFD",
            type="institute",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        short_program = Program(
            institution_id=institution.id,
            name="Tecnicatura",
            type="technical",
            modality="in_person",
            area="technology",
            duration_years=2,
        )
        db.add(short_program)
        db.commit()
        db.refresh(short_program)

        profile = Profile()
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        score, reasons = service._calculate_score(profile, short_program)

        duration_reason = next((r for r in reasons if r.factor == "duration"), None)
        assert duration_reason is not None
        assert "corta" in duration_reason.description


class TestRecommendationGeneration:
    """Tests para la generación completa de recomendaciones."""

    def test_generate_returns_sorted_by_score(self, db):
        """Test que las recomendaciones están ordenadas por score."""
        institution = Institution(
            name="Universidad",
            type="university",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        # Programa que matchea bien
        good_match = Program(
            institution_id=institution.id,
            name="Sistemas",
            type="technical",
            modality="hybrid",
            area="technology",
            work_compatible=True,
            duration_years=2,
        )
        # Programa que matchea mal
        poor_match = Program(
            institution_id=institution.id,
            name="Filosofía",
            type="degree",
            modality="in_person",
            area="social_sciences",
            duration_years=5,
        )
        db.add_all([good_match, poor_match])
        db.commit()

        profile = Profile(
            interest_areas=["technology"],
            works_while_studying="yes",
            preferred_modality="hybrid",
            province="Buenos Aires",
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        result = service.generate(profile.id, limit=10)

        assert len(result.programs) >= 1
        # El primero debe ser el de tecnología
        assert result.programs[0].program.name == "Sistemas"
        # Los scores deben estar ordenados descendentemente
        scores = [p.score for p in result.programs]
        assert scores == sorted(scores, reverse=True)

    def test_generate_with_invalid_profile(self, db):
        """Test que falla con perfil inexistente."""
        import uuid

        service = RecommendationService(db)

        with pytest.raises(ValueError, match="Perfil no encontrado"):
            service.generate(uuid.uuid4())

    def test_recommendation_includes_reasons(self, db):
        """Test que cada recomendación incluye razones."""
        institution = Institution(
            name="UTN",
            type="university",
            province="Buenos Aires",
            is_public=True,
        )
        db.add(institution)
        db.commit()
        db.refresh(institution)

        program = Program(
            institution_id=institution.id,
            name="Programación",
            type="technical",
            modality="in_person",
            area="technology",
            duration_years=2,
        )
        db.add(program)
        db.commit()

        profile = Profile(interest_areas=["technology"])
        db.add(profile)
        db.commit()
        db.refresh(profile)

        service = RecommendationService(db)
        result = service.generate(profile.id)

        assert len(result.programs) > 0
        first = result.programs[0]
        assert len(first.reasons) > 0
        # Cada razón debe tener todos los campos
        for reason in first.reasons:
            assert reason.factor
            assert reason.description
            assert reason.weight >= 0
            assert reason.contribution >= 0
