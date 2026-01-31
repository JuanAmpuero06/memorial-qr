# Testing - Memorial QR

## Backend (Python/FastAPI)

### Ejecutar todos los tests
```bash
cd backend
pytest
```

### Ejecutar con coverage
```bash
pytest --cov=app --cov-report=html
```

### Ejecutar solo tests unitarios
```bash
pytest -m unit
```

### Ejecutar solo tests de integración
```bash
pytest -m integration
```

### Ejecutar tests específicos
```bash
pytest tests/test_repositories.py -v
pytest tests/test_services.py -v
pytest tests/test_api.py -v
```

### Ejecutar en Docker
```bash
docker-compose exec backend pytest
```

---

## Frontend (React/Vitest)

### Ejecutar todos los tests
```bash
cd frontend
npm test
```

### Ejecutar con UI interactiva
```bash
npm run test:ui
```

### Ejecutar con coverage
```bash
npm run test:coverage
```

### Ejecutar tests específicos
```bash
npm test -- src/components/
npm test -- src/pages/Login.test.jsx
```

### Watch mode (desarrollo)
```bash
npm test -- --watch
```

---

## Estructura de Tests

### Backend
```
backend/
├── pytest.ini              # Configuración de pytest
└── tests/
    ├── __init__.py
    ├── conftest.py         # Fixtures compartidos
    ├── test_repositories.py # Tests de repositorios
    ├── test_services.py    # Tests de servicios
    └── test_api.py         # Tests de endpoints
```

### Frontend
```
frontend/
├── vite.config.js          # Configuración de Vitest
└── src/
    ├── test/
    │   ├── setup.js        # Setup global
    │   └── mocks/
    │       ├── handlers.js # Handlers de MSW
    │       └── server.js   # Servidor MSW
    ├── components/
    │   └── common/
    │       ├── Spinner.test.jsx
    │       └── ErrorMessage.test.jsx
    └── pages/
        ├── Login.test.jsx
        ├── Register.test.jsx
        └── PublicMemorial.test.jsx
```

---

## Markers de Tests (Backend)

- `@pytest.mark.unit` - Tests unitarios rápidos
- `@pytest.mark.integration` - Tests de integración con BD
- `@pytest.mark.slow` - Tests lentos

## Cobertura Mínima Recomendada

- **Backend**: 80%+ de cobertura
- **Frontend**: 70%+ de cobertura
