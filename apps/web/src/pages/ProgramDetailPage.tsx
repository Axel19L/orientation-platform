import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import type { Program } from '../services/api';
import { translate } from '../utils/translations';

export const ProgramDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const [program, setProgram] = useState<Program | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadProgram();
    }
  }, [id]);

  const loadProgram = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const data = await api.getProgram(id);
      setProgram(data);
      setError(null);
    } catch (err) {
      setError('Error al cargar el programa');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-secondary min-h-screen py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary"></div>
            <p className="mt-4 text-gray-600">Cargando programa...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !program) {
    return (
      <div className="bg-secondary min-h-screen py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-600">{error || 'Carrera no encontrada'}</p>
            <Link to="/programs" className="btn-primary inline-block mt-4">
              Volver a carreras
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-secondary min-h-screen py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="mb-6">
          <Link to="/programs" className="text-primary hover:text-primary-dark">
            ← Volver a carreras
          </Link>
        </nav>

        {/* Main Card */}
        <div className="card">
          {/* Header */}
          <div className="flex items-start justify-between mb-6">
            <div>
              <span className="inline-block px-3 py-1 bg-primary text-white text-sm font-medium rounded mb-3">
                {translate(program.area)}
              </span>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                {program.name}
              </h1>
              {program.institution && (
                <div className="text-lg text-gray-600">
                  <p className="font-semibold">{program.institution.name}</p>
                  <p>{program.institution.city}, {program.institution.province}</p>
                  {program.institution.website && (
                    <a
                      href={program.institution.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:text-primary-dark"
                    >
                      Sitio web →
                    </a>
                  )}
                </div>
              )}
            </div>
            {program.work_compatible && (
              <span className="px-4 py-2 bg-accent-pink text-white text-sm font-medium rounded">
                💼 Compatible con trabajo
              </span>
            )}
          </div>

          {/* Quick Info */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 p-4 bg-secondary rounded-lg">
            <div>
              <p className="text-sm text-gray-600 mb-1">Tipo</p>
              <p className="font-semibold text-gray-900">{translate(program.type)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Duración</p>
              <p className="font-semibold text-gray-900">{program.duration_years} años</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Modalidad</p>
              <p className="font-semibold text-gray-900">{translate(program.modality)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Turno</p>
              <p className="font-semibold text-gray-900">{translate(program.shift)}</p>
            </div>
          </div>

          {/* Description */}
          {program.description && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Descripción</h2>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {program.description}
              </p>
            </div>
          )}

          {/* Requirements */}
          {program.requirements && (
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Requisitos</h2>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {program.requirements}
              </p>
            </div>
          )}

          {/* Additional Details */}
          <div className="border-t border-gray-200 pt-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Detalles adicionales</h2>
            <div className="space-y-3">
              {program.weekly_hours && (
                <div className="flex items-start">
                  <span className="text-gray-600 font-medium w-48">Horas semanales:</span>
                  <span className="text-gray-900">{program.weekly_hours} horas</span>
                </div>
              )}
              {program.institution && (
                <>
                  <div className="flex items-start">
                    <span className="text-gray-600 font-medium w-48">Tipo de institución:</span>
                    <span className="text-gray-900">{translate(program.institution.type)}</span>
                  </div>
                  <div className="flex items-start">
                    <span className="text-gray-600 font-medium w-48">Institución:</span>
                    <span className="text-gray-900">
                      {program.institution.is_public ? 'Pública' : 'Privada'}
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="mt-8 pt-6 border-t border-gray-200 flex gap-4">
            <Link to="/profile" className="btn-primary flex-1 text-center">
              Crear perfil para recomendaciones
            </Link>
            <Link to="/programs" className="btn-secondary flex-1 text-center">
              Ver más carreras
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
