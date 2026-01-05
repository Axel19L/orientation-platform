import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import type { Profile } from '../services/api';
import { georefService } from '../services/georef';

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
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
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

  const [localitySearch, setLocalitySearch] = useState('');
  const [availableLocalities, setAvailableLocalities] = useState<string[]>([]);
  const [loadingLocalities, setLoadingLocalities] = useState(false);

  // Cargar perfil existente
  useEffect(() => {
    if (profileId) {
      loadProfile();
    }
  }, [profileId]);

  // Cargar localidades cuando cambia la provincia
  useEffect(() => {
    if (formData.province) {
      loadLocalities();
    } else {
      setAvailableLocalities([]);
    }
  }, [formData.province]);

  const loadLocalities = async () => {
    if (!formData.province) return;
    
    try {
      setLoadingLocalities(true);
      const localities = await georefService.getLocalitiesByProvince(formData.province, 2000);
      setAvailableLocalities(localities);
    } catch (error) {
      console.error('Error al cargar localidades:', error);
      setAvailableLocalities([]);
    } finally {
      setLoadingLocalities(false);
    }
  };

  const loadProfile = async () => {
    if (!profileId) return;

    try {
      setLoadingProfile(true);
      const profile = await api.getProfile(profileId);
      setFormData({
        province: profile.province,
        locality: profile.locality || '',
        works_while_studying: profile.works_while_studying === 'yes',
        preferred_modality: profile.preferred_modality,
        max_weekly_hours: profile.max_weekly_hours,
        has_technical_degree: profile.has_technical_degree,
        interest_areas: profile.interest_areas,
      });
    } catch (err) {
      console.error('Error al cargar perfil:', err);
      // Si el perfil no existe, limpiar localStorage
      localStorage.removeItem('profileId');
      setProfileId(null);
    } finally {
      setLoadingProfile(false);
    }
  };

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
      setSuccess('¡Perfil guardado! Generando recomendaciones...');
      const recommendation = await api.createRecommendation({
        profile_id: profile.id,
        limit: 10,
      });

      // Wait a bit to show success message
      setTimeout(() => {
        navigate(`/recommendations/${recommendation.id}`);
      }, 1000);
    } catch (err) {
      setError('Error al guardar el perfil. Revisá los datos e intentá nuevamente.');
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

          {loadingProfile ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-primary"></div>
              <p className="mt-4 text-gray-600">Cargando perfil...</p>
            </div>
          ) : (
            <>
              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded">
                  <p className="text-red-600">{error}</p>
                </div>
              )}

              {success && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded">
                  <p className="text-green-600">{success}</p>
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
                onChange={(e) => {
                  setFormData({ 
                    ...formData, 
                    province: e.target.value,
                    locality: '' // Reset locality when province changes
                  });
                }}
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
            {formData.province && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Localidad *
                </label>
                
                {loadingLocalities ? (
                  <div className="flex items-center justify-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-gray-300 border-t-primary"></div>
                    <span className="ml-2 text-gray-600">Cargando localidades...</span>
                  </div>
                ) : (
                  <>
                    {/* Campo de búsqueda */}
                    <input
                      type="text"
                      placeholder="Buscar localidad..."
                      value={localitySearch}
                      onChange={(e) => setLocalitySearch(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent mb-2"
                    />
                    
                    {/* Select con resultados filtrados */}
                    <select
                      required
                      value={formData.locality}
                      onChange={(e) => {
                        setFormData({ ...formData, locality: e.target.value });
                        setLocalitySearch('');
                      }}
                      className="w-full px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary focus:border-transparent"
                      size={8}
                      disabled={availableLocalities.length === 0}
                    >
                      <option value="">Seleccionar localidad</option>
                      {availableLocalities
                        .filter((locality) =>
                          locality.toLowerCase().includes(localitySearch.toLowerCase())
                        )
                        .map((locality) => (
                          <option key={locality} value={locality}>
                            {locality}
                          </option>
                        ))}
                    </select>
                    <p className="mt-2 text-sm text-gray-500">
                      {availableLocalities.length} localidades disponibles. Usá el buscador para encontrar la tuya.
                    </p>
                  </>
                )}
              </div>
            )}

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
            </>
          )}
        </div>
      </div>
    </div>
  );
};
