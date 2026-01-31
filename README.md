# 🕯️ Memorial QR

<div align="center">

![Memorial QR Logo](https://img.shields.io/badge/Memorial-QR-amber?style=for-the-badge&logo=qrcode&logoColor=white)

**Memoriales digitales accesibles mediante códigos QR**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

[Características](#-características) • [Instalación](#-instalación) • [API](#-api-endpoints) • [Arquitectura](#-arquitectura) • [Contribuir](#-contribuir)

</div>

---

## 📖 Descripción

**Memorial QR** es una aplicación web completa que permite crear memoriales digitales para seres queridos fallecidos, accesibles mediante códigos QR. Diseñada para ser colocada en lápidas, urnas, o cualquier lugar conmemorativo, permite a familiares y amigos acceder a un tributo digital escaneando un código QR.

### 🌟 ¿Por qué Memorial QR?

- **Preserva la memoria**: Crea un espacio digital permanente para honrar a tus seres queridos
- **Acceso instantáneo**: Un simple escaneo de QR desde cualquier smartphone
- **Interacción emocional**: Visitantes pueden dejar reacciones, condolencias y recuerdos
- **Analytics completo**: Visualiza quién visita el memorial y desde dónde

---

## ✨ Características

### 🎯 Funcionalidades Principales

| Característica | Descripción |
|----------------|-------------|
| 🪦 **Memoriales Digitales** | Crea tributos personalizados con foto, biografía, fechas y epitafio |
| 📱 **Códigos QR** | Genera QR únicos para cada memorial, listos para imprimir |
| 🕯️ **Vela Virtual Animada** | Vela realista con animaciones CSS de llama parpadeante |
| 💐 **Sistema de Reacciones** | 5 tipos: 🕯️ Velas, 🌸 Flores, ❤️ Corazones, 🙏 Oraciones, 🕊️ Palomas |
| 📖 **Libro de Condolencias** | Visitantes dejan mensajes con sistema de moderación y destacados |
| 📅 **Línea de Tiempo** | Eventos importantes: nacimiento, logros, matrimonio, etc. |
| 📸 **Galería Multimedia** | Hasta 50 fotos/videos por memorial (10MB máx. cada uno) |
| 📊 **Analytics Completo** | Estadísticas de visitas por día, semana, mes con gráficos |
| 🌍 **Geolocalización** | Mapa de visitantes por país y ciudad (API ip-api.com) |
| 🔒 **Rate Limiting** | Protección contra abuso con SlowAPI |

### 🛠️ Stack Tecnológico

**Backend:**
- 🐍 Python 3.11+ con FastAPI
- 🔐 Autenticación JWT (python-jose)
- 🗄️ PostgreSQL + SQLAlchemy ORM
- 📊 Pydantic para validación
- 🧪 Pytest para testing
- 🚦 SlowAPI para rate limiting

**Frontend:**
- ⚛️ React 18 con Hooks
- ⚡ Vite como bundler
- 🎨 TailwindCSS para estilos
- 📡 Axios para API calls
- 🧪 Vitest + Testing Library

**DevOps:**
- 🐳 Docker & Docker Compose
- 🔀 Traefik como reverse proxy
- 📦 GitHub Actions para CI/CD

---

## � Instalación

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)
- O alternativamente: Python 3.11+, Node.js 18+, PostgreSQL 15+

### 🐳 Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/JuanAmpuero06/memorial-qr.git
cd memorial-qr

# 2. Crear archivo de configuración
cp .env.example .env

# 3. Configurar variables de entorno en .env
DATABASE_URL=postgresql://postgres:password@db:5432/memorial_qr
SECRET_KEY=tu-clave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

# 4. Levantar todos los servicios
docker compose up -d

# 5. Ver logs (opcional)
docker compose logs -f
```

**🌐 Servicios disponibles (con Traefik):**

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost | Aplicación React |
| Backend API | http://localhost/api | API FastAPI |
| Swagger Docs | http://localhost/docs | Documentación interactiva |
| ReDoc | http://localhost/redoc | Documentación alternativa |
| Traefik Dashboard | http://localhost:8080 | Panel de Traefik |
| pgAdmin | http://localhost:5050 | Administración PostgreSQL |

> **Nota:** Traefik actúa como reverse proxy, todo el tráfico HTTP pasa por el puerto 80.

### 💻 Desarrollo Local (Sin Docker)

<details>
<summary><b>Backend (Python/FastAPI)</b></summary>

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://user:password@localhost:5432/memorial_qr"
export SECRET_KEY="tu-clave-secreta"
export BACKEND_URL="http://localhost:8000"

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

</details>

<details>
<summary><b>Frontend (React/Vite)</b></summary>

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar API URL (crear .env.local)
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
```

</details>

> **Nota:** En desarrollo local sin Docker, el frontend usa puerto 5173 y el backend 8000.

---

## 📚 API Endpoints

### 🔐 Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/register` | Registrar nuevo usuario |
| `POST` | `/login` | Iniciar sesión (retorna JWT) |

### 🪦 Memoriales
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/memorials/` | Listar memoriales del usuario |
| `POST` | `/memorials/` | Crear nuevo memorial |
| `GET` | `/public/memorials/{slug}` | Ver memorial público |
| `PUT` | `/memorials/{id}` | Actualizar memorial |
| `DELETE` | `/memorials/{id}` | Eliminar memorial |
| `POST` | `/memorials/{id}/upload-photo` | Subir foto principal |
| `GET` | `/memorials/{slug}/qr` | Descargar código QR |

### 📖 Condolencias
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/condolences/public/{slug}` | Obtener condolencias aprobadas |
| `POST` | `/api/v1/condolences/{slug}` | Enviar nueva condolencia |
| `GET` | `/api/v1/condolences/pending/{slug}` | Ver pendientes (owner) |
| `PATCH` | `/api/v1/condolences/{id}/moderate` | Aprobar/rechazar/destacar |

### 📅 Línea de Tiempo
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/timeline/public/{slug}` | Ver eventos públicos |
| `POST` | `/api/v1/timeline/{memorial_id}` | Crear evento |
| `PUT` | `/api/v1/timeline/{id}` | Actualizar evento |
| `DELETE` | `/api/v1/timeline/{id}` | Eliminar evento |

### 📸 Galería Multimedia
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/gallery/public/{slug}` | Ver galería pública |
| `POST` | `/api/v1/gallery/{memorial_id}` | Subir foto/video |
| `PUT` | `/api/v1/gallery/{id}` | Actualizar metadatos |
| `DELETE` | `/api/v1/gallery/{id}` | Eliminar archivo |

### 📊 Analytics
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/analytics/dashboard` | Estadísticas generales |
| `POST` | `/analytics/visit/{slug}` | Registrar visita |
| `GET` | `/analytics/reactions/{slug}` | Obtener reacciones |
| `POST` | `/analytics/reactions/{slug}` | Agregar reacción |
| `GET` | `/api/v1/analytics/locations/{slug}` | Mapa de visitantes |

> 📖 Documentación interactiva completa en `http://localhost/docs` (Swagger UI)

### 🗄️ Modelos de Base de Datos

```
┌─────────────────┐         ┌──────────────────┐
│      User       │         │    Memorial      │
├─────────────────┤         ├──────────────────┤
│ id              │────────<│ id               │
│ email           │         │ owner_id (FK)    │
│ hashed_password │         │ slug (unique)    │
│ is_active       │         │ name             │
│ created_at      │         │ epitaph, bio     │
└─────────────────┘         │ birth/death_date │
                            │ image_filename   │
                            └────────┬─────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│   Condolence  │          │  TimelineEvent  │          │    MediaItem    │
├───────────────┤          ├─────────────────┤          ├─────────────────┤
│ memorial_id   │          │ memorial_id     │          │ memorial_id     │
│ author_name   │          │ title           │          │ filename        │
│ author_email  │          │ description     │          │ media_type      │
│ message       │          │ event_date      │          │ title, caption  │
│ is_approved   │          │ event_type      │          │ is_featured     │
│ is_featured   │          │ icon            │          │ file_size       │
└───────────────┘          └─────────────────┘          └─────────────────┘

┌───────────────┐          ┌─────────────────┐
│    Visit      │          │    Reaction     │
├───────────────┤          ├─────────────────┤
│ memorial_id   │          │ memorial_id     │
│ ip_address    │          │ visitor_id      │
│ user_agent    │          │ reaction_type   │
│ country       │          │ created_at      │
│ city          │          └─────────────────┘
│ visited_at    │
└───────────────┘
```

---

## 🧪 Testing

```bash
# Backend tests con cobertura
cd backend
pip install pytest pytest-cov
pytest tests/ -v --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test

# Tests en modo watch
npm run test:watch
```

### Estructura de Tests

```
backend/tests/
├── conftest.py          # Fixtures compartidos
├── test_api.py          # Tests de endpoints
├── test_services.py     # Tests de lógica de negocio
└── test_repositories.py # Tests de acceso a datos

frontend/src/
├── components/**/*.test.jsx  # Tests de componentes
└── pages/**/*.test.jsx       # Tests de páginas
```

---

## 🏗️ Arquitectura

El proyecto sigue una **arquitectura en capas** con separación de responsabilidades:

```
memorial-qr/
├── backend/                    # 🐍 API FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py        # Dependencias (auth, db)
│   │   │   └── v1/
│   │   │       └── endpoints/ # Controladores REST
│   │   ├── core/              # Seguridad, rate limiting
│   │   ├── models/            # Modelos SQLAlchemy (ORM)
│   │   ├── schemas/           # Schemas Pydantic (validación)
│   │   ├── services/          # Lógica de negocio
│   │   ├── repositories/      # Acceso a datos (queries)
│   │   ├── config.py          # Configuración centralizada
│   │   └── main.py            # Punto de entrada
│   ├── tests/                 # Tests pytest
│   ├── uploaded_images/       # Archivos subidos
│   └── requirements.txt
│
├── frontend/                  # ⚛️ React + Vite
│   ├── src/
│   │   ├── api/              # Cliente API (axios)
│   │   ├── components/
│   │   │   ├── common/       # Spinner, ErrorMessage
│   │   │   ├── memorial/     # AnimatedCandle, PhotoGallery, etc.
│   │   │   └── analytics/    # VisitorMap
│   │   ├── pages/            # Login, Register, Dashboard, etc.
│   │   └── styles/           # CSS global
│   ├── public/
│   └── package.json
│
├── docker-compose.yml         # 🐳 Orquestación de servicios
├── traefik.yml               # 🔀 Configuración reverse proxy
└── .github/workflows/        # 🔄 CI/CD pipelines
```

### Flujo de Datos

```
                         ┌─────────────────────────────────────┐
                         │           TRAEFIK (:80)             │
                         │         Reverse Proxy               │
                         └──────────────┬──────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
            ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
            │   Frontend    │   │    Backend    │   │   PostgreSQL  │
            │  React/Vite   │   │    FastAPI    │   │      :5432    │
            │    :5173      │   │     :8000     │   └───────────────┘
            └───────────────┘   └───────┬───────┘           ▲
                                        │                   │
                                        └───────────────────┘
                                         Service → Repository
```

**Rutas de Traefik:**
- `localhost/` → Frontend (React)
- `localhost/api/*` → Backend (FastAPI)  
- `localhost/docs` → Swagger UI
- `localhost/static/*` → Archivos estáticos

---

## 🔧 Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password_seguro
POSTGRES_DB=memorial_qr
DATABASE_URL=postgresql://postgres:tu_password_seguro@db:5432/memorial_qr

# Seguridad JWT
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# URLs (con Traefik todo pasa por puerto 80)
BACKEND_URL=http://localhost
FRONTEND_URL=http://localhost

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `DATABASE_URL` | URL de conexión PostgreSQL | ✅ |
| `SECRET_KEY` | Clave secreta para JWT (mín. 32 caracteres) | ✅ |
| `ALGORITHM` | Algoritmo JWT | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos | ✅ |
| `BACKEND_URL` | URL base del backend | ✅ |
| `FRONTEND_URL` | URL base del frontend | ✅ |
| `PGADMIN_DEFAULT_EMAIL` | Email para pgAdmin | Opcional |
| `PGADMIN_DEFAULT_PASSWORD` | Password para pgAdmin | Opcional |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

<div align="center">

**Juan Ampuero**

[![GitHub](https://img.shields.io/badge/GitHub-@JuanAmpuero06-181717?style=flat-square&logo=github)](https://github.com/JuanAmpuero06)

</div>

---

<div align="center">

### 🕯️ Hecho con ❤️ para preservar los recuerdos de quienes amamos

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

*Memorial QR - Donde los recuerdos perduran para siempre*

</div>
