# 🕯️ Memorial QR

<div align="center">

![Memorial QR Logo](https://img.shields.io/badge/Memorial-QR-amber?style=for-the-badge&logo=qrcode&logoColor=white)

**Memoriales digitales accesibles mediante códigos QR**

[![Backend CI](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/backend.yml/badge.svg)](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/frontend.yml/badge.svg)](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/frontend.yml)
[![Docker](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/docker.yml/badge.svg)](https://github.com/JuanAmpuero06/memorial-qr/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Demo](#-demo) • [Características](#-características) • [Instalación](#-instalación) • [Documentación](#-documentación) • [Contribuir](#-contribuir)

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
| 🪦 **Memoriales Digitales** | Crea tributos con foto, biografía, fechas y epitafio |
| 📱 **Códigos QR Personalizados** | QR con foto integrada y diseño decorativo |
| 🕯️ **Vela Virtual Animada** | Vela realista con animaciones de llama |
| 💐 **Sistema de Reacciones** | Velas, flores, corazones, oraciones y palomas |
| 📖 **Libro de Condolencias** | Visitantes pueden dejar mensajes (con moderación) |
| 📅 **Línea de Tiempo** | Eventos importantes de la vida del fallecido |
| 📸 **Galería Multimedia** | Múltiples fotos y videos por memorial |
| 📊 **Analytics Avanzado** | Estadísticas de visitas y reacciones |
| 🌍 **Geolocalización** | Mapa de visitantes por país y ciudad |

### 🛠️ Características Técnicas

- ✅ API REST completa con FastAPI
- ✅ Autenticación JWT segura
- ✅ Base de datos PostgreSQL
- ✅ Frontend React moderno con Vite
- ✅ Diseño responsive con TailwindCSS
- ✅ Docker Compose para desarrollo
- ✅ CI/CD con GitHub Actions
- ✅ Tests automatizados (pytest + Vitest)

---

## 🖼️ Screenshots

<div align="center">

### Vista Pública del Memorial
*Memorial con vela animada, reacciones y condolencias*

### Dashboard de Administración
*Gestión de memoriales con estadísticas en tiempo real*

### Código QR Personalizado
*QR con foto integrada y diseño decorativo*

</div>

---

## 🚀 Instalación

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)
- O alternativamente: Python 3.11+, Node.js 20+, PostgreSQL 15+

### 🐳 Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/JuanAmpuero06/memorial-qr.git
cd memorial-qr

# Crear archivo de configuración
cp .env.example .env
# Editar .env con tus valores

# Levantar todos los servicios
docker compose up -d

# Ver logs
docker compose logs -f
```

**Servicios disponibles:**
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:8000
- 📚 Swagger Docs: http://localhost:8000/docs
- 🗄️ pgAdmin: http://localhost:5050

### 💻 Desarrollo Local

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

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build
```

</details>

---

## 📚 Documentación

### 🔌 API Endpoints

#### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login` | Iniciar sesión |
| `POST` | `/api/v1/auth/register` | Registrar usuario |

#### Memoriales
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/memorials/` | Listar mis memoriales |
| `POST` | `/api/v1/memorials/` | Crear memorial |
| `GET` | `/api/v1/memorials/public/{slug}` | Ver memorial público |
| `GET` | `/api/v1/memorials/{slug}/qr?with_photo=true` | Descargar QR con foto |

#### Condolencias
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/condolences/{slug}` | Obtener condolencias |
| `POST` | `/api/v1/condolences/{slug}` | Enviar condolencia |
| `PATCH` | `/api/v1/condolences/{id}` | Moderar (aprobar/destacar) |

#### Línea de Tiempo
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/timeline/public/{slug}` | Ver timeline |
| `POST` | `/api/v1/timeline/{memorial_id}` | Agregar evento |

#### Galería
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/gallery/public/{slug}` | Ver galería |
| `POST` | `/api/v1/gallery/{memorial_id}` | Subir foto/video |

> 📖 Documentación completa disponible en `/docs` (Swagger UI)

### 🗄️ Modelos de Datos

```
┌─────────────────┐       ┌──────────────────┐
│      User       │       │    Memorial      │
├─────────────────┤       ├──────────────────┤
│ id              │──────<│ id               │
│ email           │       │ slug             │
│ hashed_password │       │ name, bio        │
│ is_active       │       │ birth/death_date │
└─────────────────┘       │ image_filename   │
                          └────────┬─────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   Condolence  │        │  TimelineEvent  │        │    MediaItem    │
├───────────────┤        ├─────────────────┤        ├─────────────────┤
│ author_name   │        │ title           │        │ filename        │
│ message       │        │ event_date      │        │ media_type      │
│ is_approved   │        │ event_type      │        │ caption         │
│ is_featured   │        │ icon            │        │ is_featured     │
└───────────────┘        └─────────────────┘        └─────────────────┘
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test
```

---

## 🏗️ Arquitectura

```
memorial-qr/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── services/       # Lógica de negocio
│   │   └── repositories/   # Acceso a datos
│   └── tests/              # Tests pytest
│
├── frontend/               # React + Vite
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── pages/          # Páginas/rutas
│   │   └── api/            # Cliente API
│   └── tests/              # Tests Vitest
│
├── .github/workflows/      # CI/CD GitHub Actions
└── docker-compose.yml      # Orquestación Docker
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### 📝 Guidelines

- Seguir el estilo de código existente
- Agregar tests para nuevas funcionalidades
- Actualizar documentación si es necesario
- Usar commits descriptivos en español

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Juan Ampuero**

- GitHub: [@JuanAmpuero06](https://github.com/JuanAmpuero06)

---

<div align="center">

Hecho con ❤️ para preservar los recuerdos de quienes amamos

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

</div>
