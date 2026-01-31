"""
Tests para servicios
"""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services import AuthService, MemorialService
from app.schemas import MemorialCreate, MemorialUpdate
from app.models import User, Memorial


class TestAuthService:
    """Tests para AuthService"""
    
    @pytest.mark.unit
    def test_authenticate_user_success(self, db: Session, test_user: User):
        """Test autenticación exitosa"""
        user = AuthService.authenticate_user(db, "test@example.com", "testpassword123")
        
        assert user is not None
        assert user.email == "test@example.com"
    
    @pytest.mark.unit
    def test_authenticate_user_wrong_password(self, db: Session, test_user: User):
        """Test autenticación con contraseña incorrecta"""
        with pytest.raises(HTTPException) as exc_info:
            AuthService.authenticate_user(db, "test@example.com", "wrongpassword")
        
        assert exc_info.value.status_code == 401
        assert "Email o contraseña incorrectos" in exc_info.value.detail
    
    @pytest.mark.unit
    def test_authenticate_user_wrong_email(self, db: Session, test_user: User):
        """Test autenticación con email inexistente"""
        with pytest.raises(HTTPException) as exc_info:
            AuthService.authenticate_user(db, "noexiste@example.com", "testpassword123")
        
        assert exc_info.value.status_code == 401
    
    @pytest.mark.unit
    def test_create_token(self):
        """Test creación de token"""
        token = AuthService.create_token("test@example.com")
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50  # Los JWT son largos


class TestMemorialService:
    """Tests para MemorialService"""
    
    @pytest.mark.unit
    def test_create_memorial(self, db: Session, test_user: User):
        """Test crear memorial"""
        memorial_data = MemorialCreate(
            name="Test Memorial",
            epitaph="Test epitaph",
            bio="Test bio",
            birth_date="1950-01-01",
            death_date="2024-01-01"
        )
        memorial = MemorialService.create_memorial(db, memorial_data, test_user.id)
        
        assert memorial.id is not None
        assert memorial.name == "Test Memorial"
        assert memorial.owner_id == test_user.id
    
    @pytest.mark.unit
    def test_get_user_memorials(self, db: Session, test_user: User, multiple_memorials: list):
        """Test obtener memoriales de usuario"""
        memorials = MemorialService.get_user_memorials(db, test_user.id)
        
        assert len(memorials) == 3
    
    @pytest.mark.unit
    def test_get_user_memorials_empty(self, db: Session, test_user: User):
        """Test obtener memoriales de usuario sin memoriales"""
        memorials = MemorialService.get_user_memorials(db, test_user.id)
        
        assert len(memorials) == 0
    
    @pytest.mark.unit
    def test_get_public_memorial(self, db: Session, test_memorial: Memorial):
        """Test obtener memorial público"""
        memorial = MemorialService.get_public_memorial(db, test_memorial.slug)
        
        assert memorial is not None
        assert memorial.name == test_memorial.name
    
    @pytest.mark.unit
    def test_get_public_memorial_not_found(self, db: Session):
        """Test obtener memorial público inexistente"""
        with pytest.raises(HTTPException) as exc_info:
            MemorialService.get_public_memorial(db, "slug-inexistente")
        
        assert exc_info.value.status_code == 404
    
    @pytest.mark.unit
    def test_get_memorial_by_id(self, db: Session, test_user: User, test_memorial: Memorial):
        """Test obtener memorial por ID"""
        memorial = MemorialService.get_memorial_by_id(db, test_memorial.id, test_user)
        
        assert memorial.id == test_memorial.id
    
    @pytest.mark.unit
    def test_get_memorial_by_id_not_owner(self, db: Session, test_user_2: User, test_memorial: Memorial):
        """Test obtener memorial de otro usuario"""
        with pytest.raises(HTTPException) as exc_info:
            MemorialService.get_memorial_by_id(db, test_memorial.id, test_user_2)
        
        assert exc_info.value.status_code == 403
    
    @pytest.mark.unit
    def test_update_memorial(self, db: Session, test_user: User, test_memorial: Memorial):
        """Test actualizar memorial"""
        update_data = MemorialUpdate(
            name="Nombre Actualizado",
            epitaph="Epitafio Actualizado"
        )
        updated = MemorialService.update_memorial(db, test_memorial.id, update_data, test_user)
        
        assert updated.name == "Nombre Actualizado"
        assert updated.epitaph == "Epitafio Actualizado"
    
    @pytest.mark.unit
    def test_update_memorial_not_owner(self, db: Session, test_user_2: User, test_memorial: Memorial):
        """Test actualizar memorial de otro usuario"""
        update_data = MemorialUpdate(name="Nuevo Nombre")
        
        with pytest.raises(HTTPException) as exc_info:
            MemorialService.update_memorial(db, test_memorial.id, update_data, test_user_2)
        
        assert exc_info.value.status_code == 403
    
    @pytest.mark.unit
    def test_delete_memorial(self, db: Session, test_user: User, test_memorial: Memorial):
        """Test eliminar memorial"""
        memorial_id = test_memorial.id
        result = MemorialService.delete_memorial(db, memorial_id, test_user)
        
        assert result["message"] == "Memorial eliminado exitosamente"
    
    @pytest.mark.unit
    def test_delete_memorial_not_owner(self, db: Session, test_user_2: User, test_memorial: Memorial):
        """Test eliminar memorial de otro usuario"""
        with pytest.raises(HTTPException) as exc_info:
            MemorialService.delete_memorial(db, test_memorial.id, test_user_2)
        
        assert exc_info.value.status_code == 403
