const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface Profile {
  id: string;
  province: string;
  locality?: string;
  works_while_studying: 'yes' | 'no' | 'maybe';
  preferred_modality: 'in_person' | 'remote' | 'hybrid' | 'no_preference';
  max_weekly_hours?: number;
  has_technical_degree: boolean;
  interest_areas: string[];
  created_at: string;
  updated_at?: string;
}

export interface Institution {
  id: string;
  name: string;
  short_name?: string;
  type: string;
  province: string;
  city: string;
  website?: string;
  is_public: boolean;
}

export interface Program {
  id: string;
  institution_id: string;
  name: string;
  type: string;
  duration_years: number;
  modality: string;
  weekly_hours?: number;
  shift: string;
  area: string;
  work_compatible: boolean;
  description?: string;
  requirements?: string;
  institution?: Institution;
}

export interface Trajectory {
  id: string;
  program_id?: string;
  title: string;
  summary: string;
  story: string;
  challenges?: string;
  alternatives?: string;
  outcome?: string;
  tags: string[];
  context: Record<string, unknown>;
  year_started: number;
  is_verified: boolean;
  program?: Program;
}

export interface RecommendationReason {
  factor: string;
  description: string;
  weight: number;
  contribution: number;
}

export interface RecommendedProgram {
  program_id: string;
  score: number;
  reasons: RecommendationReason[];
  matched_trajectories: string[];
}

export interface Recommendation {
  id: string;
  profile_id: string;
  programs: RecommendedProgram[];
  created_at: string;
}

export const api = {
  // Health check
  async health(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`);
    if (!response.ok) throw new Error('Health check failed');
    return response.json();
  },

  // Programs
  async getPrograms(params?: {
    skip?: number;
    limit?: number;
    area?: string;
    modality?: string;
  }): Promise<{ items: Program[]; total: number; skip: number; limit: number }> {
    const query = new URLSearchParams();
    if (params?.skip !== undefined) query.set('skip', params.skip.toString());
    if (params?.limit !== undefined) query.set('limit', params.limit.toString());
    if (params?.area) query.set('area', params.area);
    if (params?.modality) query.set('modality', params.modality);

    const response = await fetch(`${API_BASE_URL}/programs?${query}`);
    if (!response.ok) throw new Error('Failed to fetch programs');
    return response.json();
  },

  async getProgram(id: string): Promise<Program> {
    const response = await fetch(`${API_BASE_URL}/programs/${id}`);
    if (!response.ok) throw new Error('Failed to fetch program');
    return response.json();
  },

  // Trajectories
  async getTrajectories(params?: {
    skip?: number;
    limit?: number;
  }): Promise<{ items: Trajectory[]; total: number; skip: number; limit: number }> {
    const query = new URLSearchParams();
    if (params?.skip !== undefined) query.set('skip', params.skip.toString());
    if (params?.limit !== undefined) query.set('limit', params.limit.toString());

    const response = await fetch(`${API_BASE_URL}/trajectories?${query}`);
    if (!response.ok) throw new Error('Failed to fetch trajectories');
    return response.json();
  },

  async getTrajectory(id: string): Promise<Trajectory> {
    const response = await fetch(`${API_BASE_URL}/trajectories/${id}`);
    if (!response.ok) throw new Error('Failed to fetch trajectory');
    return response.json();
  },

  // Profiles
  async createProfile(data: Omit<Profile, 'id' | 'created_at' | 'updated_at'>): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create profile');
    return response.json();
  },

  async getProfile(id: string): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles/${id}`);
    if (!response.ok) throw new Error('Failed to fetch profile');
    return response.json();
  },

  async updateProfile(id: string, data: Partial<Omit<Profile, 'id' | 'created_at' | 'updated_at'>>): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update profile');
    return response.json();
  },

  // Recommendations
  async createRecommendation(data: {
    profile_id: string;
    limit?: number;
  }): Promise<Recommendation> {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create recommendation');
    return response.json();
  },

  async getRecommendation(id: string): Promise<Recommendation> {
    const response = await fetch(`${API_BASE_URL}/recommendations/${id}`);
    if (!response.ok) throw new Error('Failed to fetch recommendation');
    return response.json();
  },
};
