"""
Tests para endpoints de la API
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, Memorial


class TestAuthEndpoints:
    """Tests para endpoints de autenticación"""
    
    @pytest.mark.integration
    def test_register_success(self, client: TestClient):
        """Test registro exitoso"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "nuevo@example.com", "password": "password123"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "nuevo@example.com"
        assert "id" in data
    
    @pytest.mark.integration
    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """Test registro con email duplicado"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": test_user.email, "password": "password123"}
        )
        
        assert response.status_code == 400
        assert "ya está registrado" in response.json()["detail"]
    
    @pytest.mark.integration
    def test_register_invalid_email(self, client: TestClient):
        """Test registro con email inválido"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "email-invalido", "password": "password123"}
        )
        
        assert response.status_code == 422
    
    @pytest.mark.integration
    def test_login_success(self, client: TestClient, test_user: User):
        """Test login exitoso"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user.email, "password": "testpassword123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.integration
    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login con contraseña incorrecta"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": test_user.email, "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.integration
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login con usuario inexistente"""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "noexiste@example.com", "password": "password123"}
        )
        
        assert response.status_code == 401


class TestUserEndpoints:
    """Tests para endpoints de usuarios"""
    
    @pytest.mark.integration
    def test_get_current_user(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test obtener usuario actual"""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
    
    @pytest.mark.integration
    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test obtener usuario sin autenticación"""
        response = client.get("/api/v1/users/me")
        
        assert response.status_code == 401


class TestMemorialEndpoints:
    """Tests para endpoints de memoriales"""
    
    @pytest.mark.integration
    def test_create_memorial(self, client: TestClient, auth_headers: dict):
        """Test crear memorial"""
        response = client.post(
            "/memorials/",
            headers=auth_headers,
            json={
                "name": "Test Memorial",
                "epitaph": "Test epitaph",
                "bio": "Test bio",
                "birth_date": "1950-01-01",
                "death_date": "2024-01-01"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Memorial"
        assert "slug" in data
    
    @pytest.mark.integration
    def test_create_memorial_unauthorized(self, client: TestClient):
        """Test crear memorial sin autenticación"""
        response = client.post(
            "/memorials/",
            json={"name": "Test Memorial"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.integration
    def test_get_my_memorials(self, client: TestClient, auth_headers: dict, multiple_memorials: list):
        """Test obtener mis memoriales"""
        response = client.get("/memorials/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    @pytest.mark.integration
    def test_get_my_memorials_empty(self, client: TestClient, auth_headers: dict):
        """Test obtener memoriales vacío"""
        response = client.get("/memorials/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    @pytest.mark.integration
    def test_get_public_memorial(self, client: TestClient, test_memorial: Memorial):
        """Test obtener memorial público"""
        response = client.get(f"/public/memorials/{test_memorial.slug}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_memorial.name
    
    @pytest.mark.integration
    def test_get_public_memorial_not_found(self, client: TestClient):
        """Test obtener memorial público inexistente"""
        response = client.get("/public/memorials/slug-inexistente")
        
        assert response.status_code == 404
    
    @pytest.mark.integration
    def test_update_memorial(self, client: TestClient, auth_headers: dict, test_memorial: Memorial):
        """Test actualizar memorial"""
        response = client.put(
            f"/memorials/{test_memorial.id}",
            headers=auth_headers,
            json={"name": "Nombre Actualizado"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Nombre Actualizado"
    
    @pytest.mark.integration
    def test_delete_memorial(self, client: TestClient, auth_headers: dict, test_memorial: Memorial):
        """Test eliminar memorial"""
        response = client.delete(
            f"/memorials/{test_memorial.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert "eliminado" in response.json()["message"]


class TestAnalyticsEndpoints:
    """Tests para endpoints de analytics"""
    
    @pytest.mark.integration
    def test_register_visit(self, client: TestClient, test_memorial: Memorial):
        """Test registrar visita"""
        response = client.post(f"/analytics/visit/{test_memorial.slug}")
        
        assert response.status_code == 200
        assert "Visita registrada" in response.json()["message"]
    
    @pytest.mark.integration
    def test_register_visit_not_found(self, client: TestClient):
        """Test registrar visita en memorial inexistente"""
        response = client.post("/analytics/visit/slug-inexistente")
        
        assert response.status_code == 200
        assert "error" in response.json()
    
    @pytest.mark.integration
    def test_get_reactions(self, client: TestClient, test_memorial: Memorial):
        """Test obtener reacciones"""
        response = client.get(f"/analytics/reactions/{test_memorial.slug}")
        
        assert response.status_code == 200
        data = response.json()
        assert "counts" in data
        assert "user_reactions" in data
    
    @pytest.mark.integration
    def test_toggle_reaction(self, client: TestClient, test_memorial: Memorial):
        """Test toggle de reacción"""
        response = client.post(
            f"/analytics/reactions/{test_memorial.slug}",
            json={"reaction_type": "heart", "visitor_id": "test_visitor_123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "counts" in data
    
    @pytest.mark.integration
    def test_toggle_reaction_invalid_type(self, client: TestClient, test_memorial: Memorial):
        """Test toggle con tipo de reacción inválido"""
        response = client.post(
            f"/analytics/reactions/{test_memorial.slug}",
            json={"reaction_type": "invalid_type", "visitor_id": "test_visitor"}
        )
        
        assert response.status_code == 200
        assert "error" in response.json()
    
    @pytest.mark.integration
    def test_dashboard_analytics(self, client: TestClient, auth_headers: dict, test_memorial: Memorial):
        """Test obtener analytics del dashboard"""
        response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_memorials" in data
        assert "total_visits" in data


class TestHealthEndpoints:
    """Tests para endpoints de health check"""
    
    @pytest.mark.integration
    def test_root(self, client: TestClient):
        """Test endpoint raíz"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "Memorial QR API" in data["message"]
    
    @pytest.mark.integration
    def test_health_check(self, client: TestClient):
        """Test health check"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "unhealthy"]
