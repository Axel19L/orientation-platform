import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Trajectory } from '../services/api';
import { translate } from '../utils/translations';

export const TrajectoriesPage = () => {
  const [trajectories, setTrajectories] = useState<Trajectory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTrajectory, setSelectedTrajectory] = useState<Trajectory | null>(null);

  useEffect(() => {
    loadTrajectories();
  }, []);

  const loadTrajectories = async () => {
    try {
      setLoading(true);
      const response = await api.getTrajectories({ limit: 20 });
      setTrajectories(response.items);
      setError(null);
    } catch (err) {
      setError('Error al cargar historias');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-secondary min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Historias de Estudiantes
          </h1>
          <p className="text-lg text-gray-600">
            Conocé experiencias reales de quienes ya transitaron estos caminos
          </p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary"></div>
            <p className="mt-4 text-gray-600">Cargando historias...</p>
          </div>
        ) : error ? (
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-600">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {trajectories.map((trajectory) => (
              <div key={trajectory.id} className="card">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex gap-2 flex-wrap">
                    {trajectory.tags.slice(0, 3).map((tag, index) => (
                      <span
                        key={index}
                        className="inline-block px-2 py-1 bg-accent-pink-soft text-white text-xs font-medium rounded"
                      >
                        {translate(tag)}
                      </span>
                    ))}
                  </div>
                  {trajectory.is_verified && (
                    <span className="inline-block px-2 py-1 bg-primary text-white text-xs font-medium rounded">
                      ✓ Verificada
                    </span>
                  )}
                </div>

                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {trajectory.title}
                </h3>

                {trajectory.program && (
                  <p className="text-sm text-primary font-medium mb-3">
                    {trajectory.program.name}
                  </p>
                )}

                <p className="text-gray-600 mb-4 line-clamp-3">
                  {trajectory.summary}
                </p>

                <button
                  onClick={() => setSelectedTrajectory(trajectory)}
                  className="text-primary hover:text-primary-dark font-medium text-sm"
                >
                  Leer historia completa →
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Modal */}
        {selectedTrajectory && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedTrajectory(null)}
          >
            <div
              className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-8">
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-3xl font-bold text-gray-900">
                    {selectedTrajectory.title}
                  </h2>
                  <button
                    onClick={() => setSelectedTrajectory(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {selectedTrajectory.program && (
                  <p className="text-primary font-medium mb-4">
                    {selectedTrajectory.program.name}
                  </p>
                )}

                <div className="flex gap-2 flex-wrap mb-6">
                  {selectedTrajectory.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="inline-block px-3 py-1 bg-secondary text-gray-700 text-sm rounded"
                    >
                      {translate(tag)}
                    </span>
                  ))}
                </div>

                <div className="space-y-6 text-gray-700">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Historia</h3>
                    <p className="whitespace-pre-line">{selectedTrajectory.story}</p>
                  </div>

                  {selectedTrajectory.challenges && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Desafíos</h3>
                      <p className="whitespace-pre-line">{selectedTrajectory.challenges}</p>
                    </div>
                  )}

                  {selectedTrajectory.alternatives && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Alternativas consideradas</h3>
                      <p className="whitespace-pre-line">{selectedTrajectory.alternatives}</p>
                    </div>
                  )}

                  {selectedTrajectory.outcome && (
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Resultado</h3>
                      <p className="whitespace-pre-line">{selectedTrajectory.outcome}</p>
                    </div>
                  )}
                </div>

                <div className="mt-8 pt-6 border-t border-gray-200 text-sm text-gray-600">
                  <p>Año de inicio: {selectedTrajectory.year_started}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
