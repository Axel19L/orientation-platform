"""
Tests para endpoints de perfiles.
"""

from fastapi.testclient import TestClient


def test_create_profile(client: TestClient):
    """Test crear un perfil nuevo."""
    profile_data = {
        "province": "Buenos Aires",
        "locality": "La Plata",
        "works_while_studying": "yes",
        "preferred_modality": "hybrid",
        "max_weekly_hours": 25,
        "has_technical_degree": False,
        "interest_areas": ["technology", "business"],
    }

    response = client.post("/api/v1/profiles", json=profile_data)

    assert response.status_code == 201
    data = response.json()
    assert data["province"] == "Buenos Aires"
    assert data["locality"] == "La Plata"
    assert data["works_while_studying"] == "yes"
    assert data["preferred_modality"] == "hybrid"
    assert data["max_weekly_hours"] == 25
    assert data["has_technical_degree"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_profile_minimal(client: TestClient):
    """Test crear un perfil con datos mínimos."""
    profile_data = {}

    response = client.post("/api/v1/profiles", json=profile_data)

    assert response.status_code == 201
    data = response.json()
    assert data["province"] is None
    assert "id" in data


def test_get_profile(client: TestClient):
    """Test obtener un perfil por ID."""
    # Primero crear el perfil
    profile_data = {"province": "Córdoba"}
    create_response = client.post("/api/v1/profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Luego obtenerlo
    response = client.get(f"/api/v1/profiles/{profile_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == profile_id
    assert data["province"] == "Córdoba"


def test_get_profile_not_found(client: TestClient):
    """Test obtener un perfil que no existe."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/profiles/{fake_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Perfil no encontrado"


def test_update_profile(client: TestClient):
    """Test actualizar un perfil."""
    # Crear perfil
    profile_data = {"province": "Santa Fe", "max_weekly_hours": 20}
    create_response = client.post("/api/v1/profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Actualizar
    update_data = {"max_weekly_hours": 30, "interest_areas": ["health"]}
    response = client.patch(f"/api/v1/profiles/{profile_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["province"] == "Santa Fe"  # No cambió
    assert data["max_weekly_hours"] == 30  # Cambió
    assert data["interest_areas"] == ["health"]  # Nuevo


def test_update_profile_not_found(client: TestClient):
    """Test actualizar un perfil que no existe."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/api/v1/profiles/{fake_id}", json={"province": "Test"})

    assert response.status_code == 404
