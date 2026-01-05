import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import type { Program } from '../services/api';
import { translate } from '../utils/translations';

export const ProgramsPage = () => {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    area: '',
    modality: '',
  });

  useEffect(() => {
    loadPrograms();
  }, [filters]);

  const loadPrograms = async () => {
    try {
      setLoading(true);
      const response = await api.getPrograms({
        limit: 30,
        ...(filters.area && { area: filters.area }),
        ...(filters.modality && { modality: filters.modality }),
      });
      setPrograms(response.items);
      setError(null);
    } catch (err) {
      setError('Error al cargar programas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const areas = ['Tecnología', 'Salud', 'Ciencias Sociales', 'Arte y Diseño', 'Ingeniería', 'Negocios'];
  const modalities = ['Presencial', 'Virtual', 'Híbrida'];

  return (
    <div className="bg-secondary min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Programas Educativos
          </h1>
          <p className="text-lg text-gray-600">
            Explorá carreras y tecnicaturas de instituciones argentinas
          </p>
        </div>

        {/* Filters */}
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filtros</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Área
              </label>
              <select
                value={filters.area}
                onChange={(e) => setFilters({ ...filters, area: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">Todas las áreas</option>
                {areas.map((area) => (
                  <option key={area} value={area}>
                    {area}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Modalidad
              </label>
              <select
                value={filters.modality}
                onChange={(e) => setFilters({ ...filters, modality: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">Todas las modalidades</option>
                {modalities.map((modality) => (
                  <option key={modality} value={modality}>
                    {modality}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Programs List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary"></div>
            <p className="mt-4 text-gray-600">Cargando programas...</p>
          </div>
        ) : error ? (
          <div className="card bg-red-50 border border-red-200">
            <p className="text-red-600">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {programs.map((program) => (
              <div key={program.id} className="card">
                <div className="flex items-start justify-between mb-3">
                  <span className="inline-block px-3 py-1 bg-primary text-white text-xs font-medium rounded">
                    {translate(program.area)}
                  </span>
                  {program.work_compatible && (
                    <span className="inline-block px-3 py-1 bg-accent-pink-soft text-white text-xs font-medium rounded">
                      Compatible con trabajo
                    </span>
                  )}
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {program.name}
                </h3>
                
                {program.institution && (
                  <p className="text-sm text-gray-600 mb-3">
                    {program.institution.short_name || program.institution.name}
                  </p>
                )}
                
                <div className="space-y-1 text-sm text-gray-600 mb-4">
                  <p>📚 {translate(program.type)} - {program.duration_years} años</p>
                  <p>📍 {translate(program.modality)}</p>
                  {program.weekly_hours && (
                    <p>⏰ {program.weekly_hours} hs/semana</p>
                  )}
                </div>
                
                {program.description && (
                  <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                    {program.description}
                  </p>
                )}
                
                <Link
                  to={`/programs/${program.id}`}
                  className="inline-block text-primary hover:text-primary-dark font-medium text-sm"
                >
                  Ver detalles →
                </Link>
              </div>
            ))}
          </div>
        )}

        {!loading && !error && programs.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-600 text-lg">
              No se encontraron programas con los filtros seleccionados
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
