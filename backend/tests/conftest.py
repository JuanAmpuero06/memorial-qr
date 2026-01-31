"""
Configuración de fixtures para tests
"""
import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base, get_db
from app.models import User, Memorial
from app.core.security import get_password_hash
from app.services import AuthService


# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Crear base de datos limpia para cada test
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Cliente de test con base de datos inyectada
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """
    Crear usuario de prueba
    """
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_user_2(db: Session) -> User:
    """
    Crear segundo usuario de prueba
    """
    user = User(
        email="test2@example.com",
        hashed_password=get_password_hash("testpassword456")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> Dict[str, str]:
    """
    Headers de autenticación para usuario de prueba
    """
    token = AuthService.create_token(test_user.email)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_memorial(db: Session, test_user: User) -> Memorial:
    """
    Crear memorial de prueba
    """
    memorial = Memorial(
        name="Juan Pérez",
        slug="juan-perez-abc123",
        epitaph="Siempre en nuestros corazones",
        bio="Una persona maravillosa",
        birth_date="1950-03-15",
        death_date="2024-01-20",
        owner_id=test_user.id
    )
    db.add(memorial)
    db.commit()
    db.refresh(memorial)
    return memorial


@pytest.fixture
def multiple_memorials(db: Session, test_user: User) -> list:
    """
    Crear múltiples memoriales de prueba
    """
    memorials = []
    for i in range(3):
        memorial = Memorial(
            name=f"Persona {i+1}",
            slug=f"persona-{i+1}-test{i}",
            epitaph=f"Epitafio {i+1}",
            owner_id=test_user.id
        )
        db.add(memorial)
        memorials.append(memorial)
    db.commit()
    for m in memorials:
        db.refresh(m)
    return memorials
