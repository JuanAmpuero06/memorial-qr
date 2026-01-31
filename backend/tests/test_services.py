"""
Tests para servicios
"""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services import AuthService, MemorialService
from app.services.condolence import CondolenceService
from app.services.timeline import TimelineService
from app.services.analytics import AnalyticsService
from app.schemas import MemorialCreate, MemorialUpdate, CondolenceCreate, TimelineEventCreate
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
    
    @pytest.mark.unit
    def test_create_token_different_emails(self):
        """Test que tokens diferentes emails generan tokens diferentes"""
        token1 = AuthService.create_token("user1@example.com")
        token2 = AuthService.create_token("user2@example.com")
        
        assert token1 != token2


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
    
    @pytest.mark.unit
    def test_create_memorial_generates_slug(self, db: Session, test_user: User):
        """Test que crear memorial genera slug automáticamente"""
        memorial_data = MemorialCreate(
            name="María José García López",
            epitaph="Test",
            birth_date="1940-01-01",
            death_date="2024-01-01"
        )
        memorial = MemorialService.create_memorial(db, memorial_data, test_user.id)
        
        assert memorial.slug is not None
        assert "maria-jose" in memorial.slug.lower()


class TestCondolenceService:
    """Tests para CondolenceService"""
    
    @pytest.mark.unit
    def test_create_condolence(self, db: Session, test_memorial: Memorial):
        """Test crear condolencia"""
        condolence_data = CondolenceCreate(
            author_name="María García",
            message="Siempre te recordaremos"
        )
        condolence = CondolenceService.create_condolence(
            db, test_memorial.slug, condolence_data, "127.0.0.1"
        )
        
        assert condolence.id is not None
        assert condolence.author_name == "María García"
        assert condolence.message == "Siempre te recordaremos"
    
    @pytest.mark.unit
    def test_create_condolence_memorial_not_found(self, db: Session):
        """Test crear condolencia en memorial inexistente"""
        condolence_data = CondolenceCreate(
            author_name="Test",
            message="Test message"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            CondolenceService.create_condolence(db, "slug-inexistente", condolence_data)
        
        assert exc_info.value.status_code == 404
    
    @pytest.mark.unit
    def test_get_condolences(self, db: Session, test_memorial: Memorial):
        """Test obtener condolencias"""
        # Crear algunas condolencias
        for i in range(3):
            condolence_data = CondolenceCreate(
                author_name=f"Autor {i}",
                message=f"Mensaje {i}"
            )
            CondolenceService.create_condolence(db, test_memorial.slug, condolence_data)
        
        result = CondolenceService.get_condolences(db, test_memorial.slug, approved_only=False)
        
        assert result.total >= 3


class TestTimelineService:
    """Tests para TimelineService"""
    
    @pytest.mark.unit
    def test_create_timeline_event(self, db: Session, test_user: User, test_memorial: Memorial):
        """Test crear evento en timeline"""
        event_data = TimelineEventCreate(
            title="Nacimiento",
            description="Nació en Madrid",
            event_date="1950-03-15"
        )
        event = TimelineService.create_event(db, test_memorial.id, test_user.id, event_data)
        
        assert event.id is not None
        assert event.title == "Nacimiento"
    
    @pytest.mark.unit
    def test_create_timeline_event_not_owner(self, db: Session, test_user_2: User, test_memorial: Memorial):
        """Test crear evento sin ser propietario"""
        event_data = TimelineEventCreate(
            title="Test",
            event_date="1950-01-01"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            TimelineService.create_event(db, test_memorial.id, test_user_2.id, event_data)
        
        assert exc_info.value.status_code == 403
    
    @pytest.mark.unit
    def test_create_timeline_event_memorial_not_found(self, db: Session, test_user: User):
        """Test crear evento en memorial inexistente"""
        event_data = TimelineEventCreate(
            title="Test",
            event_date="1950-01-01"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            TimelineService.create_event(db, 99999, test_user.id, event_data)
        
        assert exc_info.value.status_code == 404


class TestAnalyticsService:
    """Tests para AnalyticsService"""
    
    @pytest.mark.unit
    def test_register_visit(self, db: Session, test_memorial: Memorial):
        """Test registrar visita"""
        visit = AnalyticsService.register_visit(
            db, test_memorial.id, "127.0.0.1", "TestBrowser"
        )
        
        assert visit.id is not None
        assert visit.memorial_id == test_memorial.id
    
    @pytest.mark.unit
    def test_get_memorial_stats(self, db: Session, test_memorial: Memorial):
        """Test obtener estadísticas de memorial"""
        # Registrar algunas visitas
        for _ in range(5):
            AnalyticsService.register_visit(db, test_memorial.id)
        
        stats = AnalyticsService.get_memorial_stats(db, test_memorial.id)
        
        assert stats.total_visits >= 5
        assert stats.today_visits >= 5
    
    @pytest.mark.unit
    def test_get_dashboard_analytics(self, db: Session, test_user: User, test_memorial: Memorial):
        """Test obtener analytics del dashboard"""
        # Registrar algunas visitas
        for _ in range(3):
            AnalyticsService.register_visit(db, test_memorial.id)
        
        analytics = AnalyticsService.get_dashboard_analytics(db, test_user.id)
        
        assert analytics.total_memorials >= 1
        assert analytics.total_visits >= 3
