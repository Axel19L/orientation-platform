-- Script de inicialización de PostgreSQL
-- Este script se ejecuta automáticamente al crear el contenedor

-- Crear extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Base de datos orientation_db inicializada correctamente';
END $$;
