# Orientation Platform - Frontend

Frontend React + Vite para la plataforma de orientación vocacional.

## Setup (por implementar)

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Build de producción
npm run build
```

## Stack

- **React 18** - UI library
- **Vite** - Build tool
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **React Router** - Routing
- **TanStack Query** - Server state management
- **Axios** - HTTP client

## Estructura propuesta

```
apps/web/
├── src/
│   ├── components/      # Componentes reutilizables
│   ├── pages/           # Páginas/rutas
│   ├── hooks/           # Custom hooks
│   ├── services/        # API calls
│   ├── types/           # TypeScript types
│   ├── utils/           # Utilidades
│   └── App.tsx
├── public/
└── package.json
```

## Flujo del MVP

1. **Onboarding**: Pantalla de bienvenida
2. **Perfil**: Formulario de intereses y contexto
3. **Recomendaciones**: Lista de programas recomendados con razones
4. **Explorar**: Navegar trayectorias y programas
5. **Feedback**: Evaluar utilidad de las recomendaciones

## Por implementar

- [ ] Inicializar proyecto con Vite
- [ ] Configurar TailwindCSS
- [ ] Crear componentes base
- [ ] Implementar flujo de onboarding
- [ ] Conectar con API
- [ ] Testing
