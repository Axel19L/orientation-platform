import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import type { Profile } from '../services/api';

const PROVINCES = [
  'Buenos Aires', 'CABA', 'Catamarca', 'Chaco', 'Chubut', 'Córdoba',
  'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja',
  'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta', 'San Juan',
  'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero',
  'Tierra del Fuego', 'Tucumán'
];

const INTEREST_AREAS = [
  { value: 'technology', label: 'Tecnología' },
  { value: 'health', label: 'Salud' },
  { value: 'social_sciences', label: 'Ciencias Sociales' },
  { value: 'arts', label: 'Arte y Diseño' },
  { value: 'engineering', label: 'Ingeniería' },
  { value: 'business', label: 'Negocios' },
  { value: 'education', label: 'Educación' },
  { value: 'exact_sciences', label: 'Ciencias Exactas' },
];

const MODALITIES = [
  { value: 'in_person', label: 'Presencial' },
  { value: 'remote', label: 'Virtual' },
  { value: 'hybrid', label: 'Híbrida' },
  { value: 'no_preference', label: 'Sin preferencia' },
];

export const ProfilePage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profileId, setProfileId] = useState<string | null>(
    localStorage.getItem('profileId')
  );

  const [formData, setFormData] = useState({
    province: '',
    locality: '',
    works_while_studying: false,
    preferred_modality: 'in_person',
    max_weekly_hours: 20,
    has_technical_degree: false,
    interest_areas: [] as string[],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.interest_areas.length === 0) {
      setError('Seleccioná al menos un área de interés');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      let profile: Profile;
      const profileData = {
        ...formData,
        works_while_studying: formData.works_while_studying ? 'yes' : 'no',
      };
      
      if (profileId) {
        profile = await api.updateProfile(profileId, profileData);
      } else {
        profile = await api.createProfile(profileData);
        localStorage.setItem('profileId', profile.id);
        setProfileId(profile.id);
      }

      // Generate recommendations
      const recommendation = await api.createRecommendation({
        profile_id: profile.id,
        limit: 10,
      });

      navigate(`/recommendations/${recommendation.id}`);
    } catch (err) {
      setError('Error al guardar el perfil');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleInterestArea = (area: string) => {
    setFormData((prev) => ({
      ...prev,
      interest_areas: prev.interest_areas.includes(area)
        ? prev.interest_areas.filter((a) => a !== area)
        : [...prev.interest_areas, area],
    }));
  };

  return (
    <div className="bg-secondary min-h-screen py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="card">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {profileId ? 'Actualizar mi perfil' : 'Crear mi perfil'}
          </h1>
          <p className="text-gray-600 mb-8">
            Contanos sobre vos para recibir recomendaciones personalizadas
          </p>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Province */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provincia *
              </label>
              <select
                required
                value={formData.province}
                onChange={(e) => setFormData({ ...formData, province: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="">Seleccionar provincia</option>
                {PROVINCES.map((province) => (
                  <option key={province} value={province}>
                    {province}
                  </option>
                ))}
              </select>
            </div>

            {/* Locality */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Localidad
              </label>
              <input
                type="text"
                value={formData.locality}
                onChange={(e) => setFormData({ ...formData, locality: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="Ej: Rosario"
              />
            </div>

            {/* Interest Areas */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Áreas de interés * (seleccioná una o más)
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {INTEREST_AREAS.map((area) => (
                  <button
                    key={area.value}
                    type="button"
                    onClick={() => toggleInterestArea(area.value)}
                    className={`px-4 py-2 rounded font-medium text-sm transition-colors ${
                      formData.interest_areas.includes(area.value)
                        ? 'bg-primary text-white'
                        : 'bg-white border border-gray-300 text-gray-700 hover:border-primary'
                    }`}
                  >
                    {area.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Preferred Modality */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Modalidad preferida *
              </label>
              <select
                required
                value={formData.preferred_modality}
                onChange={(e) => setFormData({ ...formData, preferred_modality: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                {MODALITIES.map((modality) => (
                  <option key={modality.value} value={modality.value}>
                    {modality.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Works while studying */}
            <div className="flex items-start">
              <input
                type="checkbox"
                id="works"
                checked={formData.works_while_studying}
                onChange={(e) =>
                  setFormData({ ...formData, works_while_studying: e.target.checked })
                }
                className="mt-1 h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label htmlFor="works" className="ml-3 text-sm text-gray-700">
                Trabajo o planeo trabajar mientras estudio
              </label>
            </div>

            {/* Max weekly hours */}
            {formData.works_while_studying && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Máximo de horas semanales disponibles para estudiar
                </label>
                <input
                  type="number"
                  min="5"
                  max="40"
                  value={formData.max_weekly_hours}
                  onChange={(e) =>
                    setFormData({ ...formData, max_weekly_hours: parseInt(e.target.value) })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
            )}

            {/* Technical degree */}
            <div className="flex items-start">
              <input
                type="checkbox"
                id="technical"
                checked={formData.has_technical_degree}
                onChange={(e) =>
                  setFormData({ ...formData, has_technical_degree: e.target.checked })
                }
                className="mt-1 h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label htmlFor="technical" className="ml-3 text-sm text-gray-700">
                Tengo o estoy cursando una escuela técnica
              </label>
            </div>

            {/* Submit */}
            <div className="flex gap-4 pt-4">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Procesando...' : profileId ? 'Actualizar y ver recomendaciones' : 'Crear perfil y ver recomendaciones'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
