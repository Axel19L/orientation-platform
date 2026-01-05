# 📊 Modelo de Datos

## Diagrama de Entidades

```
┌─────────────────┐       ┌─────────────────┐
│    profiles     │       │  institutions   │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ created_at      │       │ name            │
│ updated_at      │       │ short_name      │
│ province        │       │ type            │
│ locality        │       │ province        │
│ works_while_    │       │ city            │
│   studying      │       │ website         │
│ preferred_      │       │ is_public       │
│   modality      │       └────────┬────────┘
│ max_weekly_     │                │
│   hours         │                │ 1:N
│ has_technical_  │                │
│   degree        │       ┌────────▼────────┐
│ interest_areas  │       │    programs     │
└────────┬────────┘       ├─────────────────┤
         │                │ id (PK)         │
         │                │ institution_id  │
         │                │   (FK)          │
         │                │ name            │
         │                │ type            │
         │                │ duration_years  │
         │                │ modality        │
         │                │ weekly_hours    │
         │                │ shift           │
         │                │ area            │
         │                │ work_compatible │
         │                │ description     │
         │                └────────┬────────┘
         │                         │
         │    ┌────────────────────┼────────────────────┐
         │    │                    │                    │
         │    │ N:M                │ 1:N                │ 1:N
         │    │                    │                    │
┌────────▼────▼───┐    ┌──────────▼─────────┐  ┌──────▼───────┐
│ recommendations │    │    trajectories    │  │   feedback   │
├─────────────────┤    ├────────────────────┤  ├──────────────┤
│ id (PK)         │    │ id (PK)            │  │ id (PK)      │
│ profile_id (FK) │    │ program_id (FK)    │  │ profile_id   │
│ created_at      │    │ title              │  │ target_type  │
│ programs (JSON) │    │ summary            │  │ target_id    │
│ - program_id    │    │ story              │  │ rating       │
│ - score         │    │ challenges        │  │ comment      │
│ - reasons[]     │    │ alternatives       │  │ created_at   │
│ - matched_      │    │ outcome            │  └──────────────┘
│   trajectories  │    │ tags               │
└─────────────────┘    │ context            │
                       │ year_started       │
                       │ is_verified        │
                       └────────────────────┘
```

---

## Definición de Tablas

### `profiles`

Perfil del estudiante (sin datos personales identificables).

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `created_at` | TIMESTAMP | No | Fecha de creación |
| `updated_at` | TIMESTAMP | No | Última actualización |
| `province` | VARCHAR(100) | Sí | Provincia de residencia |
| `locality` | VARCHAR(200) | Sí | Localidad/ciudad |
| `works_while_studying` | ENUM | Sí | 'yes', 'no', 'maybe' |
| `preferred_modality` | ENUM | Sí | 'in_person', 'remote', 'hybrid', 'no_preference' |
| `max_weekly_hours` | INTEGER | Sí | Horas semanales disponibles para estudio |
| `has_technical_degree` | BOOLEAN | Sí | Si tiene título técnico secundario |
| `interest_areas` | VARCHAR[] | Sí | Array de áreas de interés |

**Áreas de interés predefinidas:**
- `technology` - Tecnología e Informática
- `health` - Salud y Medicina
- `social_sciences` - Ciencias Sociales
- `exact_sciences` - Ciencias Exactas y Naturales
- `arts` - Arte y Diseño
- `business` - Negocios y Administración
- `education` - Educación
- `engineering` - Ingeniería
- `law` - Derecho y Ciencias Jurídicas
- `communication` - Comunicación y Medios
- `agriculture` - Agro y Medio Ambiente
- `trades` - Oficios y Técnicas

---

### `institutions`

Instituciones educativas (universidades, institutos).

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `name` | VARCHAR(300) | No | Nombre completo |
| `short_name` | VARCHAR(50) | Sí | Siglas (UBA, UTN, etc.) |
| `type` | ENUM | No | 'university', 'institute', 'other' |
| `province` | VARCHAR(100) | No | Provincia |
| `city` | VARCHAR(200) | Sí | Ciudad |
| `website` | VARCHAR(500) | Sí | Sitio web oficial |
| `is_public` | BOOLEAN | No | Si es pública (gratuita) |

---

### `programs`

Carreras, tecnicaturas y cursos.

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `institution_id` | UUID (FK) | No | Referencia a institución |
| `name` | VARCHAR(300) | No | Nombre del programa |
| `type` | ENUM | No | 'degree', 'technical', 'course' |
| `duration_years` | DECIMAL(3,1) | Sí | Duración en años |
| `modality` | ENUM | No | 'in_person', 'remote', 'hybrid' |
| `weekly_hours` | INTEGER | Sí | Carga horaria semanal estimada |
| `shift` | ENUM | Sí | 'morning', 'afternoon', 'evening', 'flexible' |
| `area` | VARCHAR(50) | No | Área de conocimiento (match con interest_areas) |
| `work_compatible` | BOOLEAN | Sí | Si es compatible con trabajo |
| `description` | TEXT | Sí | Descripción breve |
| `requirements` | TEXT | Sí | Requisitos de ingreso |
| `created_at` | TIMESTAMP | No | Fecha de creación |
| `updated_at` | TIMESTAMP | No | Última actualización |

**Tipos de programa:**
- `degree` - Carrera universitaria (4-6 años)
- `technical` - Tecnicatura (2-3 años)
- `course` - Curso/diplomatura (< 2 años)

---

### `trajectories`

Historias reales de estudiantes (anonimizadas).

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `program_id` | UUID (FK) | Sí | Programa relacionado (puede ser null si cambió) |
| `title` | VARCHAR(200) | No | Título descriptivo |
| `summary` | VARCHAR(500) | No | Resumen corto |
| `story` | TEXT | No | Historia completa |
| `challenges` | TEXT | Sí | Desafíos enfrentados |
| `alternatives` | TEXT | Sí | Alternativas consideradas o tomadas |
| `outcome` | ENUM | No | 'completed', 'switched', 'dropped', 'in_progress' |
| `tags` | VARCHAR[] | Sí | Tags para categorizar |
| `context` | JSONB | Sí | Contexto adicional estructurado |
| `year_started` | INTEGER | Sí | Año en que comenzó |
| `is_verified` | BOOLEAN | No | Si fue verificada por moderadores |
| `created_at` | TIMESTAMP | No | Fecha de creación |

**Estructura de `context` (JSONB):**
```json
{
  "worked_while_studying": true,
  "province": "Buenos Aires",
  "modality": "hybrid",
  "had_technical_degree": false,
  "interest_areas": ["technology", "business"]
}
```

**Tags sugeridos:**
- `first_generation` - Primera generación universitaria
- `career_change` - Cambió de carrera
- `worked_full_time` - Trabajó tiempo completo
- `moved_cities` - Se mudó para estudiar
- `scholarship` - Tuvo beca
- `remote_learning` - Estudió mayormente virtual
- `night_shift` - Turno noche

---

### `recommendations`

Recomendaciones generadas para un perfil.

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `profile_id` | UUID (FK) | No | Perfil que solicitó |
| `created_at` | TIMESTAMP | No | Fecha de generación |
| `programs` | JSONB | No | Lista de programas recomendados |

**Estructura de `programs` (JSONB):**
```json
[
  {
    "program_id": "uuid",
    "score": 0.85,
    "reasons": [
      {
        "factor": "interest_match",
        "description": "Coincide con tu interés en Tecnología",
        "weight": 0.4
      },
      {
        "factor": "work_compatible",
        "description": "Compatible con trabajo (turno noche)",
        "weight": 0.3
      }
    ],
    "matched_trajectories": ["uuid1", "uuid2"]
  }
]
```

---

### `feedback`

Feedback de usuarios sobre recomendaciones/trayectorias.

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | UUID | No | Identificador único |
| `profile_id` | UUID (FK) | Sí | Perfil que da feedback (opcional) |
| `target_type` | ENUM | No | 'recommendation', 'trajectory', 'program' |
| `target_id` | UUID | No | ID del elemento evaluado |
| `rating` | INTEGER | No | 1-5 estrellas |
| `comment` | TEXT | Sí | Comentario opcional |
| `created_at` | TIMESTAMP | No | Fecha |

---

## Índices Recomendados

```sql
-- Búsquedas frecuentes
CREATE INDEX idx_programs_area ON programs(area);
CREATE INDEX idx_programs_type ON programs(type);
CREATE INDEX idx_programs_institution ON programs(institution_id);
CREATE INDEX idx_programs_modality ON programs(modality);

CREATE INDEX idx_trajectories_program ON trajectories(program_id);
CREATE INDEX idx_trajectories_tags ON trajectories USING GIN(tags);
CREATE INDEX idx_trajectories_outcome ON trajectories(outcome);

CREATE INDEX idx_recommendations_profile ON recommendations(profile_id);
CREATE INDEX idx_feedback_target ON feedback(target_type, target_id);
```

---

## Migraciones Iniciales

1. `001_create_institutions.py`
2. `002_create_programs.py`
3. `003_create_profiles.py`
4. `004_create_trajectories.py`
5. `005_create_recommendations.py`
6. `006_create_feedback.py`
7. `007_seed_initial_data.py`
