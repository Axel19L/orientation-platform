"""
Tests para endpoints de health check y root.
"""

from fastapi.testclient import TestClient

from src import __version__


def test_health_check(client: TestClient):
    """Test del endpoint /health."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == __version__
    assert "timestamp" in data


def test_root(client: TestClient):
    """Test del endpoint raíz."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"


def test_openapi_docs(client: TestClient):
    """Test que la documentación OpenAPI está disponible."""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Orientation Platform API"
