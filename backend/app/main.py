from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from typing import List

# Importamos todos nuestros módulos
from . import models, database, schemas, crud, auth

# Crear tablas en BD
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Memorial QR API", version="0.1.0")

# Dependencia para obtener la sesión de BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. ENDPOINT DE SALUD (Health Check) ---
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "online", "status": "Todo correcto 🚀"}
    except Exception as e:
        return {"database": "offline", "error": str(e)}

# --- 2. ENDPOINT DE REGISTRO (El que te faltaba) ---
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si email ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    # Crear usuario
    return crud.create_user(db=db, user=user)

# --- 3. ENDPOINT DE LOGIN (Obtener Token) ---
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar usuario
    user = crud.get_user_by_email(db, email=form_data.username)
    
    # Verificar contraseña
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar Token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- 4. ENDPOINT PROTEGIDO (Prueba de seguridad) ---
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user