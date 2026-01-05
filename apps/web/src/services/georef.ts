/**
 * Servicio para interactuar con la API de GeoRef (Servicio de Normalización de Datos Geográficos de Argentina)
 * Documentación: https://datosgobabierto.github.io/georef-ar-api/
 */

interface GeoRefProvince {
  id: string;
  nombre: string;
}

interface GeoRefLocality {
  id: string;
  nombre: string;
  provincia: {
    id: string;
    nombre: string;
  };
  municipio: {
    id: string;
    nombre: string;
  };
}

interface GeoRefResponse<T> {
  cantidad: number;
  total: number;
  inicio: number;
  parametros: any;
  localidades?: T[];
  provincias?: T[];
}

const GEOREF_API_BASE = 'https://apis.datos.gob.ar/georef/api';

export const georefService = {
  /**
   * Obtiene todas las provincias de Argentina
   */
  async getProvinces(): Promise<string[]> {
    try {
      const response = await fetch(`${GEOREF_API_BASE}/provincias`);
      const data: GeoRefResponse<GeoRefProvince> = await response.json();
      return data.provincias?.map(p => p.nombre).sort() || [];
    } catch (error) {
      console.error('Error fetching provinces:', error);
      // Fallback a lista estática
      return [
        'Buenos Aires', 'CABA', 'Catamarca', 'Chaco', 'Chubut', 'Córdoba',
        'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja',
        'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta', 'San Juan',
        'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero',
        'Tierra del Fuego, Antártida e Islas del Atlántico Sur', 'Tucumán'
      ];
    }
  },

  /**
   * Obtiene todas las localidades de una provincia
   * @param provinceName Nombre de la provincia
   * @param max Cantidad máxima de resultados (default: 1000)
   */
  async getLocalitiesByProvince(provinceName: string, max: number = 1000): Promise<string[]> {
    try {
      // Normalizar nombre de la provincia para la API
      let provinceQuery = provinceName;
      if (provinceName === 'CABA') {
        provinceQuery = 'Ciudad Autónoma de Buenos Aires';
      }
      
      const response = await fetch(
        `${GEOREF_API_BASE}/localidades?provincia=${encodeURIComponent(provinceQuery)}&max=${max}&campos=nombre`
      );
      const data: GeoRefResponse<GeoRefLocality> = await response.json();
      
      // Obtener nombres únicos y ordenarlos
      const uniqueLocalities = Array.from(
        new Set(data.localidades?.map(l => l.nombre) || [])
      ).sort();
      
      return uniqueLocalities;
    } catch (error) {
      console.error(`Error fetching localities for ${provinceName}:`, error);
      return [];
    }
  },

  /**
   * Busca localidades por nombre en toda Argentina
   * @param searchTerm Término de búsqueda
   * @param max Cantidad máxima de resultados
   */
  async searchLocalities(searchTerm: string, max: number = 50): Promise<Array<{name: string, province: string}>> {
    try {
      const response = await fetch(
        `${GEOREF_API_BASE}/localidades?nombre=${encodeURIComponent(searchTerm)}&max=${max}&campos=nombre,provincia.nombre`
      );
      const data: GeoRefResponse<GeoRefLocality> = await response.json();
      
      return data.localidades?.map(l => ({
        name: l.nombre,
        province: l.provincia.nombre
      })) || [];
    } catch (error) {
      console.error('Error searching localities:', error);
      return [];
    }
  }
};
