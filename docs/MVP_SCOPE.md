# 📋 Alcance del MVP

## Objetivo del MVP

Validar que el concepto de "recomendaciones explicables + trayectorias reales" aporta valor a estudiantes que terminan el secundario.

**Tiempo estimado**: 4-6 semanas de desarrollo

---

## ✅ QUÉ ENTRA en el MVP

### Funcionalidades

| Feature | Descripción | Prioridad |
|---------|-------------|-----------|
| **Perfil básico** | Crear y editar perfil sin datos sensibles | P0 |
| **Explorar programas** | Listar y filtrar carreras/tecnicaturas/cursos | P0 |
| **Explorar trayectorias** | Ver historias reales categorizadas | P0 |
| **Recomendaciones v1** | Motor basado en reglas con explicación | P0 |
| **Feedback** | Marcar utilidad de recomendaciones | P0 |
| **Comparador básico** | Comparar 2-3 opciones lado a lado | P1 |

### Datos

| Dataset | Cantidad mínima | Fuente |
|---------|-----------------|--------|
| Programas (carreras/tecnicaturas) | 50-100 | Curado manualmente |
| Instituciones | 20-30 | Universidades públicas principales |
| Trayectorias | 15-30 | Anonimizadas y curadas |
| Áreas de interés | 10-15 | Predefinidas |

### Entidades del Perfil (sin datos sensibles)

```
- Áreas de interés (múltiple selección)
- ¿Necesita trabajar mientras estudia? (sí/no/no sé)
- Modalidad preferida (presencial/virtual/híbrido/sin preferencia)
- Provincia/localidad (para opciones cercanas)
- Máxima carga horaria semanal disponible
- ¿Tiene título secundario técnico? (sí/no)
```

### Endpoints API

```
POST   /api/v1/profiles          # Crear perfil
GET    /api/v1/profiles/{id}     # Obtener perfil
PATCH  /api/v1/profiles/{id}     # Actualizar perfil

GET    /api/v1/programs          # Listar programas (con filtros)
GET    /api/v1/programs/{id}     # Detalle de programa

GET    /api/v1/trajectories      # Listar trayectorias
GET    /api/v1/trajectories/{id} # Detalle de trayectoria

POST   /api/v1/recommendations   # Generar recomendaciones para perfil
GET    /api/v1/recommendations/{id}  # Obtener recomendación guardada

POST   /api/v1/feedback          # Enviar feedback
```

### Stack Técnico MVP

**Backend**:
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Pytest
- Ruff + Pyright

**Frontend**:
- React + Vite
- TypeScript
- TailwindCSS
- React Query

**Infra**:
- Docker Compose (desarrollo)
- GitHub Actions (CI)

---

## ❌ QUÉ NO ENTRA en el MVP

### Funcionalidades Diferidas

| Feature | Razón para diferir |
|---------|-------------------|
| **Autenticación** | Usar UUID anónimo, sin login |
| **Cuentas de usuario** | Complejidad innecesaria para validar |
| **Búsqueda full-text** | Filtros básicos son suficientes |
| **Chat/IA conversacional** | Fuera de scope inicial |
| **App mobile** | Web responsive primero |
| **Panel de admin** | Gestión manual de datos |
| **Notificaciones** | Sin necesidad en MVP |
| **Múltiples idiomas** | Solo español argentino |
| **Mentorías** | Requiere usuarios registrados |
| **Integración becas** | Complejidad de datos externos |

### Datos Diferidos

| Dataset | Razón |
|---------|-------|
| Todas las universidades privadas | Empezar con públicas |
| Cursos cortos/bootcamps | Foco en educación formal |
| Salarios por carrera | Datos difíciles de validar |
| Estadísticas de inserción laboral | Requiere fuentes oficiales |

### Características Técnicas Diferidas

| Característica | Razón |
|----------------|-------|
| Cache distribuido | Overkill para MVP |
| Rate limiting avanzado | Tráfico bajo inicial |
| Monitoreo/observabilidad | Logs básicos suficientes |
| Deployment automatizado | Deploy manual inicial |
| Tests E2E | Unit + integration primero |

---

## 📊 Criterios de Éxito del MVP

### Cuantitativos
- [ ] API responde en < 500ms (p95)
- [ ] 0 errores críticos en producción
- [ ] Cobertura de tests > 70%

### Cualitativos
- [ ] 10 usuarios reales completan el flujo
- [ ] Feedback promedio ≥ 3.5/5 en utilidad
- [ ] Usuarios entienden "por qué" de recomendaciones

---

## 🚦 Decisiones de Scope

### ¿Por qué sin autenticación?
- Reduce fricción para probar
- Evita gestión de contraseñas/emails
- UUID en localStorage es suficiente para MVP
- Si el usuario borra datos, no perdemos nada crítico

### ¿Por qué solo universidades públicas?
- Datos más accesibles
- Evita conflictos de interés
- Representa la mayoría de estudiantes target

### ¿Por qué reglas en vez de ML?
- Explicabilidad total
- No requiere datos de entrenamiento
- Fácil de iterar y debuggear
- ML puede venir después con datos reales

---

## 📅 Milestones

| Semana | Objetivo |
|--------|----------|
| 1 | Estructura + docs + API skeleton |
| 2 | Modelo de datos + seed data |
| 3 | Motor de recomendaciones v1 |
| 4 | Frontend básico funcional |
| 5 | Integración + testing |
| 6 | Beta con usuarios reales |
