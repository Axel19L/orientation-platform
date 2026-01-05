# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a Orientation Platform! Este documento te guiará en el proceso.

## 📋 Antes de Empezar

1. **Lee la documentación**: Familiarízate con [VISION.md](VISION.md) y [MVP_SCOPE.md](MVP_SCOPE.md)
2. **Revisa issues abiertos**: Puede que alguien ya esté trabajando en lo mismo
3. **Pregunta antes de empezar**: Para features grandes, abre un issue de discusión primero

## 🔧 Configuración del Entorno

### Prerrequisitos

- Python 3.11+
- Node.js 20+
- Docker y Docker Compose
- Git

### Setup

```bash
# Clonar el repo
git clone https://github.com/tu-usuario/orientation-platform.git
cd orientation-platform

# Backend
cd apps/api
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"

# Frontend
cd ../web
npm install

# Base de datos
cd ../../infra/docker
docker compose up -d
```

## 🌿 Flujo de Trabajo con Git

### Branches

- `main`: Producción, siempre estable
- `develop`: Desarrollo activo
- `feature/*`: Nuevas funcionalidades
- `fix/*`: Corrección de bugs
- `docs/*`: Documentación

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato (no afecta código)
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Mantenimiento

**Ejemplos:**
```
feat(api): add recommendations endpoint
fix(web): correct profile form validation
docs: update installation instructions
chore(api): upgrade fastapi to 0.110
```

## 🧪 Testing

### Backend

```bash
cd apps/api

# Todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/test_recommendations.py -v
```

### Frontend

```bash
cd apps/web

# Tests
npm test

# Con coverage
npm run test:coverage
```

## 📝 Estilo de Código

### Python

- **Formatter**: Ruff
- **Linter**: Ruff
- **Type checker**: Pyright

```bash
cd apps/api

# Format
ruff format .

# Lint
ruff check .

# Type check
pyright
```

### TypeScript/JavaScript

- **Formatter**: Prettier
- **Linter**: ESLint

```bash
cd apps/web

# Format + lint
npm run lint
npm run format
```

## 📬 Pull Requests

### Checklist

- [ ] El código sigue las guías de estilo
- [ ] Los tests pasan localmente
- [ ] Se agregaron tests para nuevas funcionalidades
- [ ] La documentación está actualizada
- [ ] El PR tiene una descripción clara

### Template de PR

```markdown
## Descripción
[Qué hace este PR]

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva feature
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo probarlo?
[Pasos para probar los cambios]

## Screenshots (si aplica)
[Capturas de pantalla]

## Checklist
- [ ] Tests pasan
- [ ] Lint pasa
- [ ] Documentación actualizada
```

## 🐛 Reportar Bugs

Usa el template de issues e incluye:

1. **Descripción clara** del problema
2. **Pasos para reproducir**
3. **Comportamiento esperado** vs actual
4. **Screenshots** si aplica
5. **Entorno**: OS, versión de navegador, etc.

## 💡 Proponer Features

1. **Abre un issue** de tipo "Feature Request"
2. **Describe el problema** que resuelve
3. **Propone una solución** (puede ser informal)
4. **Espera feedback** antes de implementar

## 🏷️ Labels de Issues

- `good first issue`: Ideal para empezar
- `help wanted`: Se necesita ayuda
- `bug`: Algo no funciona
- `enhancement`: Mejora
- `documentation`: Relacionado a docs
- `question`: Pregunta o discusión

## 📜 Código de Conducta

- Sé respetuoso y constructivo
- Acepta feedback con apertura
- Ayuda a otros contribuidores
- Prioriza la claridad sobre la brevedad

## ❓ ¿Preguntas?

- Abre un issue con el label `question`
- Únete a nuestro Discord [próximamente]

---

¡Gracias por contribuir! 🎉
