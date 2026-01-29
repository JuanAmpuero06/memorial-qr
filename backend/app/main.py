from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from typing import List
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
import os # Para leer el .env
from fastapi.middleware.cors import CORSMiddleware # <--- IMPORTAR

# Importamos todos nuestros módulos
from . import models, database, schemas, crud, auth

# Crear tablas en BD
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Memorial QR API", version="0.1.0")

# --- CONFIGURACIÓN DE CORS (Permitir conexión con React) ---
origins = [
    "http://localhost:5173", # Puerto por defecto de Vite
    "http://localhost:3000", # Puerto alternativo común
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir GET, POST, PUT, DELETE
    allow_headers=["*"], # Permitir Tokens y Auth headers
)

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

# --- 5. CREAR MEMORIAL (Protegido) ---
@app.post("/memorials/", response_model=schemas.MemorialResponse)
def create_memorial(
    memorial: schemas.MemorialCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user) # <--- EL GUARDIÁN
):
    # current_user viene del token. Usamos su ID para crear el memorial.
    return crud.create_memorial(db=db, memorial=memorial, user_id=current_user.id)

# --- 6. VER MIS MEMORIALES (Protegido) ---
@app.get("/memorials/", response_model=List[schemas.MemorialResponse])
def read_my_memorials(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_memorials_by_user(db=db, user_id=current_user.id)

# --- 7. DESCARGAR IMAGEN QR (Protegido) ---
@app.get("/memorials/{slug}/qr")
def get_qr_code(slug: str, current_user: models.User = Depends(auth.get_current_user)):
    # 1. Construir la URL final (Ej: http://localhost:3000/view/abuelo-pedro-xxxx)
    base_url = os.getenv("FRONTEND_URL", "http://localhost:3000/view")
    target_url = f"{base_url}/{slug}"
    
    # 2. Generar el QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # H = Alta corrección (soporta daños)
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    # 3. Crear la imagen en memoria (Ram)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 4. Convertir a Bytes para enviarla por HTTP
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # 5. Devolver como respuesta de imagen
    return StreamingResponse(img_byte_arr, media_type="image/png")

# --- 8. VER MEMORIAL PÚBLICO (Sin candado) ---
@app.get("/public/memorials/{slug}", response_model=schemas.PublicMemorial)
def read_public_memorial(slug: str, db: Session = Depends(get_db)):
    db_memorial = crud.get_memorial_by_slug(db, slug=slug)
    if db_memorial is None:
        raise HTTPException(status_code=404, detail="Memorial no encontrado")
    return db_memorial