# Orientation Platform API

Backend API para la plataforma de orientación vocacional.

## Setup

```bash
# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -e ".[dev]"

# Copiar variables de entorno
copy .env.example .env

# Levantar base de datos
docker compose -f ../../infra/docker/docker-compose.yml up -d

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn src.main:app --reload
```

## Comandos útiles

```bash
# Tests
pytest

# Tests con coverage
pytest --cov=src --cov-report=html

# Linting
ruff check .

# Formateo
ruff format .

# Type checking
pyright

# Crear nueva migración
alembic revision --autogenerate -m "descripción"
```

## Estructura

```
apps/api/
├── src/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión a DB
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic
│   ├── routers/             # Endpoints
│   └── services/            # Lógica de negocio
├── tests/
├── alembic/                 # Migraciones
└── pyproject.toml
```
