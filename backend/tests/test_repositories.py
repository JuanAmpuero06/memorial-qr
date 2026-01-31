"""
Tests para repositorios
"""
import pytest
from sqlalchemy.orm import Session

from app.repositories import UserRepository, MemorialRepository, CondolenceRepository, VisitRepository
from app.schemas import UserCreate, MemorialCreate, CondolenceCreate
from app.models import User, Memorial


class TestUserRepository:
    """Tests para UserRepository"""
    
    @pytest.mark.unit
    def test_create_user(self, db: Session):
        """Test crear usuario"""
        user_data = UserCreate(email="nuevo@example.com", password="password123")
        user = UserRepository.create(db, user_data)
        
        assert user.id is not None
        assert user.email == "nuevo@example.com"
        assert user.hashed_password != "password123"  # Debe estar hasheado
    
    @pytest.mark.unit
    def test_get_by_id(self, db: Session, test_user: User):
        """Test obtener usuario por ID"""
        found_user = UserRepository.get_by_id(db, test_user.id)
        
        assert found_user is not None
        assert found_user.id == test_user.id
        assert found_user.email == test_user.email
    
    @pytest.mark.unit
    def test_get_by_id_not_found(self, db: Session):
        """Test obtener usuario inexistente"""
        found_user = UserRepository.get_by_id(db, 99999)
        
        assert found_user is None
    
    @pytest.mark.unit
    def test_get_by_email(self, db: Session, test_user: User):
        """Test obtener usuario por email"""
        found_user = UserRepository.get_by_email(db, test_user.email)
        
        assert found_user is not None
        assert found_user.email == test_user.email
    
    @pytest.mark.unit
    def test_get_by_email_not_found(self, db: Session):
        """Test obtener usuario por email inexistente"""
        found_user = UserRepository.get_by_email(db, "noexiste@example.com")
        
        assert found_user is None
    
    @pytest.mark.unit
    def test_exists_by_email_true(self, db: Session, test_user: User):
        """Test verificar email existente"""
        exists = UserRepository.exists_by_email(db, test_user.email)
        
        assert exists is True
    
    @pytest.mark.unit
    def test_exists_by_email_false(self, db: Session):
        """Test verificar email inexistente"""
        exists = UserRepository.exists_by_email(db, "noexiste@example.com")
        
        assert exists is False


class TestMemorialRepository:
    """Tests para MemorialRepository"""
    
    @pytest.mark.unit
    def test_create_memorial(self, db: Session, test_user: User):
        """Test crear memorial"""
        memorial_data = MemorialCreate(
            name="María García",
            epitaph="Descansa en paz",
            bio="Una madre amorosa",
            birth_date="1945-06-20",
            death_date="2023-12-01"
        )
        memorial = MemorialRepository.create(db, memorial_data, test_user.id)
        
        assert memorial.id is not None
        assert memorial.name == "María García"
        assert memorial.slug is not None
        assert "maria-garcia" in memorial.slug
        assert memorial.owner_id == test_user.id
    
    @pytest.mark.unit
    def test_get_by_id(self, db: Session, test_memorial: Memorial):
        """Test obtener memorial por ID"""
        found = MemorialRepository.get_by_id(db, test_memorial.id)
        
        assert found is not None
        assert found.id == test_memorial.id
        assert found.name == test_memorial.name
    
    @pytest.mark.unit
    def test_get_by_slug(self, db: Session, test_memorial: Memorial):
        """Test obtener memorial por slug"""
        found = MemorialRepository.get_by_slug(db, test_memorial.slug)
        
        assert found is not None
        assert found.slug == test_memorial.slug
    
    @pytest.mark.unit
    def test_get_by_slug_not_found(self, db: Session):
        """Test obtener memorial por slug inexistente"""
        found = MemorialRepository.get_by_slug(db, "slug-inexistente")
        
        assert found is None
    
    @pytest.mark.unit
    def test_get_by_user(self, db: Session, test_user: User, multiple_memorials: list):
        """Test obtener memoriales de un usuario"""
        memorials = MemorialRepository.get_by_user(db, test_user.id)
        
        assert len(memorials) == 3
        for memorial in memorials:
            assert memorial.owner_id == test_user.id
    
    @pytest.mark.unit
    def test_get_by_user_empty(self, db: Session, test_user: User):
        """Test obtener memoriales de usuario sin memoriales"""
        memorials = MemorialRepository.get_by_user(db, test_user.id)
        
        assert len(memorials) == 0
    
    @pytest.mark.unit
    def test_update_memorial(self, db: Session, test_memorial: Memorial):
        """Test actualizar memorial"""
        update_data = {
            "name": "Juan Pérez Actualizado",
            "epitaph": "Nuevo epitafio"
        }
        updated = MemorialRepository.update(db, test_memorial, update_data)
        
        assert updated.name == "Juan Pérez Actualizado"
        assert updated.epitaph == "Nuevo epitafio"
    
    @pytest.mark.unit
    def test_update_image(self, db: Session, test_memorial: Memorial):
        """Test actualizar imagen del memorial"""
        updated = MemorialRepository.update_image(db, test_memorial, "nueva_imagen.jpg")
        
        assert updated.image_filename == "nueva_imagen.jpg"
    
    @pytest.mark.unit
    def test_delete_memorial(self, db: Session, test_memorial: Memorial):
        """Test eliminar memorial"""
        memorial_id = test_memorial.id
        MemorialRepository.delete(db, test_memorial)
        
        found = MemorialRepository.get_by_id(db, memorial_id)
        assert found is None
    
    @pytest.mark.unit
    def test_create_memorial_unique_slug(self, db: Session, test_user: User):
        """Test que se generan slugs únicos"""
        memorial_data = MemorialCreate(
            name="María García",
            epitaph="Test",
            birth_date="1945-01-01",
            death_date="2023-01-01"
        )
        
        memorial1 = MemorialRepository.create(db, memorial_data, test_user.id)
        memorial2 = MemorialRepository.create(db, memorial_data, test_user.id)
        
        assert memorial1.slug != memorial2.slug


class TestCondolenceRepository:
    """Tests para CondolenceRepository"""
    
    @pytest.mark.unit
    def test_create_condolence(self, db: Session, test_memorial: Memorial):
        """Test crear condolencia"""
        condolence_data = CondolenceCreate(
            author_name="María García",
            message="Siempre te recordaremos"
        )
        condolence = CondolenceRepository.create(
            db, test_memorial.id, condolence_data, "127.0.0.1"
        )
        
        assert condolence.id is not None
        assert condolence.author_name == "María García"
        assert condolence.memorial_id == test_memorial.id
    
    @pytest.mark.unit
    def test_get_by_memorial(self, db: Session, test_memorial: Memorial):
        """Test obtener condolencias por memorial"""
        # Crear condolencias
        for i in range(3):
            condolence_data = CondolenceCreate(
                author_name=f"Autor {i}",
                message=f"Mensaje {i}"
            )
            CondolenceRepository.create(db, test_memorial.id, condolence_data)
        
        condolences, total = CondolenceRepository.get_by_memorial(db, test_memorial.id)
        
        assert total >= 3
        assert len(condolences) >= 3
    
    @pytest.mark.unit
    def test_get_by_memorial_with_pagination(self, db: Session, test_memorial: Memorial):
        """Test paginación de condolencias"""
        # Crear 5 condolencias
        for i in range(5):
            condolence_data = CondolenceCreate(
                author_name=f"Autor {i}",
                message=f"Mensaje {i}"
            )
            CondolenceRepository.create(db, test_memorial.id, condolence_data)
        
        condolences, total = CondolenceRepository.get_by_memorial(
            db, test_memorial.id, limit=2, offset=0
        )
        
        assert total >= 5
        assert len(condolences) == 2


class TestVisitRepository:
    """Tests para VisitRepository"""
    
    @pytest.mark.unit
    def test_create_visit(self, db: Session, test_memorial: Memorial):
        """Test crear visita"""
        visit = VisitRepository.create(
            db, test_memorial.id, "127.0.0.1", "TestBrowser", "/memorial"
        )
        
        assert visit.id is not None
        assert visit.memorial_id == test_memorial.id
        assert visit.ip_address == "127.0.0.1"
    
    @pytest.mark.unit
    def test_get_total_count(self, db: Session, test_memorial: Memorial):
        """Test contar visitas totales"""
        # Crear visitas
        for _ in range(3):
            VisitRepository.create(db, test_memorial.id)
        
        count = VisitRepository.get_total_count(db, test_memorial.id)
        
        assert count >= 3
    
    @pytest.mark.unit
    def test_get_today_count(self, db: Session, test_memorial: Memorial):
        """Test contar visitas de hoy"""
        # Crear visitas
        for _ in range(2):
            VisitRepository.create(db, test_memorial.id)
        
        count = VisitRepository.get_today_count(db, test_memorial.id)
        
        assert count >= 2
