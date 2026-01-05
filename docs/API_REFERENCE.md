# 🔌 API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

El MVP no requiere autenticación. Los perfiles se identifican por UUID.

---

## Endpoints

### Health Check

#### `GET /health`

Verifica el estado de la API.

**Response 200:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-01-05T12:00:00Z"
}
```

---

### Profiles

#### `POST /api/v1/profiles`

Crea un nuevo perfil de estudiante.

**Request Body:**
```json
{
  "province": "Buenos Aires",
  "locality": "La Plata",
  "works_while_studying": "maybe",
  "preferred_modality": "hybrid",
  "max_weekly_hours": 25,
  "has_technical_degree": false,
  "interest_areas": ["technology", "business"]
}
```

**Response 201:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-05T12:00:00Z",
  "province": "Buenos Aires",
  "locality": "La Plata",
  "works_while_studying": "maybe",
  "preferred_modality": "hybrid",
  "max_weekly_hours": 25,
  "has_technical_degree": false,
  "interest_areas": ["technology", "business"]
}
```

#### `GET /api/v1/profiles/{id}`

Obtiene un perfil por ID.

**Response 200:** (mismo formato que POST)

**Response 404:**
```json
{
  "detail": "Profile not found"
}
```

#### `PATCH /api/v1/profiles/{id}`

Actualiza parcialmente un perfil.

**Request Body:**
```json
{
  "max_weekly_hours": 30,
  "interest_areas": ["technology", "engineering"]
}
```

**Response 200:** Perfil actualizado completo.

---

### Programs

#### `GET /api/v1/programs`

Lista programas con filtros opcionales.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `area` | string | Filtrar por área (ej: `technology`) |
| `type` | string | `degree`, `technical`, `course` |
| `modality` | string | `in_person`, `remote`, `hybrid` |
| `province` | string | Provincia de la institución |
| `work_compatible` | boolean | Compatible con trabajo |
| `max_duration` | number | Duración máxima en años |
| `page` | integer | Página (default: 1) |
| `per_page` | integer | Items por página (default: 20, max: 100) |

**Response 200:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Licenciatura en Sistemas",
      "type": "degree",
      "duration_years": 5,
      "modality": "in_person",
      "weekly_hours": 25,
      "shift": "evening",
      "area": "technology",
      "work_compatible": true,
      "institution": {
        "id": "...",
        "name": "Universidad de Buenos Aires",
        "short_name": "UBA"
      }
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8
}
```

#### `GET /api/v1/programs/{id}`

Obtiene detalle de un programa.

**Response 200:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "name": "Licenciatura en Sistemas",
  "type": "degree",
  "duration_years": 5,
  "modality": "in_person",
  "weekly_hours": 25,
  "shift": "evening",
  "area": "technology",
  "work_compatible": true,
  "description": "Carrera orientada a...",
  "requirements": "Título secundario completo",
  "institution": {
    "id": "...",
    "name": "Universidad de Buenos Aires",
    "short_name": "UBA",
    "province": "Buenos Aires",
    "city": "Ciudad Autónoma de Buenos Aires",
    "website": "https://www.uba.ar",
    "is_public": true
  }
}
```

---

### Trajectories

#### `GET /api/v1/trajectories`

Lista trayectorias con filtros.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `tags` | string[] | Filtrar por tags (comma-separated) |
| `outcome` | string | `completed`, `switched`, `dropped`, `in_progress` |
| `area` | string | Área del programa relacionado |
| `page` | integer | Página |
| `per_page` | integer | Items por página |

**Response 200:**
```json
{
  "items": [
    {
      "id": "...",
      "title": "De querer medicina a encontrar mi lugar en enfermería",
      "summary": "Empecé medicina pero...",
      "outcome": "switched",
      "tags": ["career_change", "first_generation"],
      "program": {
        "id": "...",
        "name": "Licenciatura en Enfermería"
      }
    }
  ],
  "total": 30,
  "page": 1,
  "per_page": 20,
  "pages": 2
}
```

#### `GET /api/v1/trajectories/{id}`

Obtiene detalle completo de una trayectoria.

**Response 200:**
```json
{
  "id": "...",
  "title": "De querer medicina a encontrar mi lugar en enfermería",
  "summary": "Empecé medicina pero el ritmo y la carga horaria...",
  "story": "Historia completa...",
  "challenges": "El mayor desafío fue aceptar que...",
  "alternatives": "Consideré kinesiología y...",
  "outcome": "switched",
  "tags": ["career_change", "first_generation"],
  "context": {
    "worked_while_studying": true,
    "province": "Córdoba",
    "modality": "in_person"
  },
  "year_started": 2022,
  "program": {
    "id": "...",
    "name": "Licenciatura en Enfermería",
    "institution": {
      "name": "Universidad Nacional de Córdoba"
    }
  }
}
```

---

### Recommendations

#### `POST /api/v1/recommendations`

Genera recomendaciones para un perfil.

**Request Body:**
```json
{
  "profile_id": "550e8400-e29b-41d4-a716-446655440000",
  "limit": 10
}
```

**Response 201:**
```json
{
  "id": "...",
  "profile_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-05T12:00:00Z",
  "programs": [
    {
      "program_id": "...",
      "program": {
        "name": "Tecnicatura en Programación",
        "institution": {"short_name": "UTN"}
      },
      "score": 0.92,
      "reasons": [
        {
          "factor": "interest_match",
          "description": "Coincide con tu interés en Tecnología",
          "weight": 0.4,
          "contribution": 0.368
        },
        {
          "factor": "work_compatible",
          "description": "Turno noche, compatible con trabajo",
          "weight": 0.25,
          "contribution": 0.23
        },
        {
          "factor": "modality_match",
          "description": "Modalidad híbrida como preferís",
          "weight": 0.15,
          "contribution": 0.138
        },
        {
          "factor": "location",
          "description": "Disponible en tu provincia",
          "weight": 0.1,
          "contribution": 0.092
        },
        {
          "factor": "duration",
          "description": "Duración corta (2 años)",
          "weight": 0.1,
          "contribution": 0.092
        }
      ],
      "matched_trajectories": [
        {
          "id": "...",
          "title": "Trabajé de día y estudié de noche",
          "match_reason": "También trabajaba mientras estudiaba"
        }
      ]
    }
  ]
}
```

#### `GET /api/v1/recommendations/{id}`

Obtiene una recomendación guardada.

---

### Feedback

#### `POST /api/v1/feedback`

Envía feedback sobre una recomendación, trayectoria o programa.

**Request Body:**
```json
{
  "profile_id": "550e8400-e29b-41d4-a716-446655440000",
  "target_type": "recommendation",
  "target_id": "...",
  "rating": 4,
  "comment": "Me sirvió para descubrir opciones que no conocía"
}
```

**Response 201:**
```json
{
  "id": "...",
  "created_at": "2026-01-05T12:00:00Z",
  "message": "¡Gracias por tu feedback!"
}
```

---

## Códigos de Error

| Code | Description |
|------|-------------|
| 400 | Bad Request - Datos inválidos |
| 404 | Not Found - Recurso no existe |
| 422 | Unprocessable Entity - Validación fallida |
| 500 | Internal Server Error |

**Formato de error:**
```json
{
  "detail": "Mensaje descriptivo del error",
  "errors": [
    {
      "field": "interest_areas",
      "message": "Debe seleccionar al menos un área de interés"
    }
  ]
}
```
