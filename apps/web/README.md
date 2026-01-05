# Orientation Platform - Frontend

Frontend web desarrollado con React, TypeScript, Vite y TailwindCSS para la plataforma de orientación vocacional.

## 🎨 Diseño

### Paleta de Colores Minimalista

- **Primary**: `#0B758C` - Azul verdoso principal
- **Secondary**: `#F2EBDC` - Beige claro de fondo
- **Accent Burgundy**: `#732231` - Borgoña oscuro
- **Accent Pink**: `#F24B6A` - Rosa vibrante
- **Accent Pink Soft**: `#D97789` - Rosa suave

Sin gradientes, diseño limpio y minimalista.

## 🚀 Desarrollo

### Requisitos Previos

- Node.js 20.19+ o 22.12+
- Backend API corriendo en `http://localhost:8000`

### Instalación

```bash
cd apps/web
npm install
```

### Variables de Entorno

Crear archivo `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Iniciar Desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### Build para Producción

```bash
npm run build
npm run preview
```

## 📁 Estructura

```
src/
├── components/       # Componentes reutilizables
│   ├── Header.tsx
│   └── Footer.tsx
├── layouts/          # Layouts de página
│   └── Layout.tsx
├── pages/            # Vistas principales
│   ├── HomePage.tsx
│   ├── ProgramsPage.tsx
│   ├── TrajectoriesPage.tsx
│   ├── ProfilePage.tsx
│   └── RecommendationsPage.tsx
├── services/         # Cliente API
│   └── api.ts
├── App.tsx           # Router principal
└── main.tsx          # Entry point
```

## 🧭 Rutas

- `/` - Landing page con información general
- `/programs` - Exploración de programas educativos con filtros
- `/trajectories` - Historias de estudiantes
- `/profile` - Creación/edición de perfil
- `/recommendations/:id` - Vista de recomendaciones personalizadas

## 🔧 Tecnologías

- **React 18** - Framework UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool y dev server
- **TailwindCSS** - Estilos utility-first
- **React Router** - Navegación SPA
- **Fetch API** - Comunicación con backend

## 📱 Features

### Página de Inicio
- Hero section con CTAs
- Cards de features principales
- Call to action para crear perfil

### Programas
- Listado con paginación
- Filtros por área y modalidad
- Cards con información resumida
- Indicadores visuales (compatible con trabajo, modalidad, etc.)

### Historias (Trajectories)
- Grid de historias verificadas
- Modal con historia completa
- Tags y metadata
- Información del programa asociado

### Perfil
- Formulario multi-campo
- Selección de provincia y localidad
- Áreas de interés (multi-select)
- Preferencias de modalidad
- Compatible con trabajo y estudio
- Persistencia en localStorage

### Recomendaciones
- Scoring visual con porcentajes
- Breakdown de factores explicado
- Barras de progreso por factor
- Colores distintivos por tipo de match
- Links a detalles de programas

## 🎯 Próximos Pasos

- [ ] Página de detalle de programa individual
- [ ] Sistema de feedback para recomendaciones
- [ ] Búsqueda y filtros avanzados
- [ ] Comparación de programas
- [ ] Exportar recomendaciones a PDF
- [ ] Dark mode
- [ ] Responsive optimizations
- [ ] Accesibilidad (ARIA labels, keyboard navigation)

## 📄 Licencia

MIT - Ver LICENSE en el root del proyecto
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
