import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api, Recommendation, Program } from '../services/api';

export const RecommendationsPage = () => {
  const { id } = useParams<{ id: string }>();
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [programs, setPrograms] = useState<Map<string, Program>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadRecommendation();
    }
  }, [id]);

  const loadRecommendation = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const rec = await api.getRecommendation(id);
      setRecommendation(rec);

      // Load program details
      const programMap = new Map<string, Program>();
      for (const item of rec.programs) {
        try {
          const program = await api.getProgram(item.program_id);
          programMap.set(item.program_id, program);
        } catch (err) {
          console.error(`Failed to load program ${item.program_id}`, err);
        }
      }
      setPrograms(programMap);
      setError(null);
    } catch (err) {
      setError('Error al cargar recomendaciones');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getFactorColor = (factor: string) => {
    const colors: Record<string, string> = {
      interest_match: 'bg-primary',
      work_compatible: 'bg-accent-pink',
      modality_match: 'bg-accent-burgundy',
      location: 'bg-accent-pink-soft',
      duration: 'bg-gray-500',
    };
    return colors[factor] || 'bg-gray-400';
  };

  const getFactorLabel = (factor: string) => {
    const labels: Record<string, string> = {
      interest_match: 'Intereses',
      work_compatible: 'Trabajo',
      modality_match: 'Modalidad',
      location: 'Ubicación',
      duration: 'Duración',
    };
    return labels[factor] || factor;
  };

  if (loading) {
    return (
      <div className="bg-secondary min-h-screen py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary"></div>
            <p className="mt-4 text-gray-600">Generando recomendaciones...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !recommendation) {
    return (
      <div className="bg-secondary min-h-screen py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-600">{error || 'Recomendación no encontrada'}</p>
            <Link to="/profile" className="btn-primary inline-block mt-4">
              Volver al perfil
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-secondary min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Tus Recomendaciones
          </h1>
          <p className="text-lg text-gray-600">
            Programas educativos seleccionados según tu perfil
          </p>
        </div>

        <div className="space-y-6">
          {recommendation.programs.map((item) => {
            const program = programs.get(item.program_id);
            const scorePercentage = Math.round(item.score * 100);

            return (
              <div key={item.program_id} className="card">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h2 className="text-2xl font-bold text-gray-900">
                        {program?.name || 'Cargando...'}
                      </h2>
                      <span
                        className={`px-3 py-1 rounded text-white font-bold text-sm ${
                          scorePercentage >= 90
                            ? 'bg-primary'
                            : scorePercentage >= 70
                            ? 'bg-accent-pink'
                            : 'bg-accent-burgundy'
                        }`}
                      >
                        {scorePercentage}% match
                      </span>
                    </div>

                    {program?.institution && (
                      <p className="text-gray-600 mb-2">
                        📍 {program.institution.short_name || program.institution.name} - {program.institution.city}, {program.institution.province}
                      </p>
                    )}

                    {program && (
                      <div className="flex gap-4 text-sm text-gray-600">
                        <span>📚 {program.type}</span>
                        <span>⏱️ {program.duration_years} años</span>
                        <span>🎓 {program.modality}</span>
                        {program.work_compatible && <span>💼 Compatible con trabajo</span>}
                      </div>
                    )}
                  </div>
                </div>

                {/* Score breakdown */}
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-gray-700 mb-3">
                    ¿Por qué este programa?
                  </h3>
                  <div className="space-y-2">
                    {item.reasons.map((reason, idx) => (
                      <div key={idx} className="flex items-start gap-3">
                        <div
                          className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${getFactorColor(
                            reason.factor
                          )}`}
                        ></div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-gray-700">
                              {getFactorLabel(reason.factor)}
                            </span>
                            <span className="text-xs text-gray-500">
                              {Math.round(reason.contribution * 100)}%
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{reason.description}</p>
                          <div className="mt-1 w-full bg-gray-200 rounded-full h-1.5">
                            <div
                              className={`h-1.5 rounded-full ${getFactorColor(reason.factor)}`}
                              style={{ width: `${reason.contribution * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {program && (
                  <div>
                    {program.description && (
                      <p className="text-gray-700 mb-4">{program.description}</p>
                    )}
                    <Link
                      to={`/programs/${program.id}`}
                      className="btn-primary inline-block"
                    >
                      Ver detalles del programa
                    </Link>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 card bg-white">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            ¿Querés cambiar tus preferencias?
          </h3>
          <p className="text-gray-600 mb-4">
            Actualizá tu perfil para recibir nuevas recomendaciones
          </p>
          <Link to="/profile" className="btn-secondary">
            Actualizar perfil
          </Link>
        </div>
      </div>
    </div>
  );
};
