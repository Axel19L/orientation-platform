# 🎓 Orientation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB.svg)](https://react.dev/)

**Plataforma open-source de orientación vocacional para estudiantes que terminan el secundario en Argentina.**

## 🎯 ¿Qué es Orientation Platform?

Es un sistema de apoyo a decisiones que ayuda a estudiantes a tomar decisiones informadas sobre su camino académico/laboral mediante:

- **Perfil simple del estudiante**: intereses, contexto y preferencias
- **Trayectorias reales**: historias curadas y anonimizadas de otros estudiantes
- **Recomendaciones explicables**: reglas claras con "por qué te lo sugiero"
- **Comparador básico de opciones**: carreras, tecnicaturas y cursos con criterios prácticos

> ⚠️ **No es un test vocacional psicológico ni "un oráculo"**. Es una herramienta para explorar opciones con información real.

## 🏗️ Estructura del Proyecto

```
orientation-platform/
├── apps/
│   ├── api/          # Backend FastAPI
│   └── web/          # Frontend React (Vite)
├── docs/             # Documentación del proyecto
├── infra/
│   └── docker/       # Configuración Docker
└── .github/
    └── workflows/    # CI/CD GitHub Actions
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11+
- Node.js 20+
- Docker y Docker Compose
- Git

### Levantar el entorno de desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/orientation-platform.git
cd orientation-platform

# Levantar PostgreSQL con Docker
docker compose -f infra/docker/docker-compose.yml up -d

# Configurar el backend
cd apps/api
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor de desarrollo
uvicorn src.main:app --reload

# En otra terminal, configurar el frontend
cd apps/web
npm install
npm run dev
```

### URLs de desarrollo

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## 📚 Documentación

- [Visión del Proyecto](docs/VISION.md)
- [Alcance del MVP](docs/MVP_SCOPE.md)
- [Modelo de Datos](docs/DATA_MODEL.md)
- [Guía de Contribución](docs/CONTRIBUTING.md)

## 🧪 Testing

```bash
# Backend
cd apps/api
pytest

# Frontend
cd apps/web
npm test
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee nuestra [Guía de Contribución](docs/CONTRIBUTING.md) antes de enviar un PR.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- A todos los estudiantes que comparten sus trayectorias
- A las instituciones educativas argentinas que colaboran con información
- A la comunidad open-source

---

