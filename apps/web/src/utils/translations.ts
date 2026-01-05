// Traducciones de enums del backend a español

export const translations = {
  // Interest Areas
  technology: 'Tecnología',
  health: 'Salud',
  social_sciences: 'Ciencias Sociales',
  exact_sciences: 'Ciencias Exactas',
  arts: 'Arte',
  business: 'Negocios',
  education: 'Educación',
  engineering: 'Ingeniería',
  law: 'Derecho',
  communication: 'Comunicación',
  agriculture: 'Agricultura',

  // Modalities
  in_person: 'Presencial',
  remote: 'Virtual',
  hybrid: 'Híbrida',
  no_preference: 'Sin preferencia',

  // Works While Studying
  yes: 'Sí',
  no: 'No',
  maybe: 'Tal vez',

  // Program Types
  degree: 'Carrera Universitaria',
  technical: 'Tecnicatura',
  course: 'Curso',

  // Institution Types
  university: 'Universidad',
  institute: 'Instituto',
  other: 'Otra',

  // Shifts
  morning: 'Mañana',
  afternoon: 'Tarde',
  evening: 'Noche',
  flexible: 'Flexible',

  // Trajectory Tags
  career_change: 'Cambio de carrera',
  first_generation: 'Primera generación',
  worked_full_time: 'Trabajó tiempo completo',
  single_parent: 'Padre/Madre soltero/a',
  rural_background: 'Origen rural',
  scholarship: 'Becado/a',
  part_time_studies: 'Estudio part-time',
  online_degree: 'Título online',
  technical_background: 'Con título técnico',
  mature_student: 'Estudiante adulto',

  // Trajectory Outcomes
  completed: 'Completado',
  switched: 'Cambió de carrera',
  dropped: 'Abandonó',
  in_progress: 'En curso',
};

export const translate = (key: string): string => {
  return translations[key as keyof typeof translations] || key;
};

export const translateArray = (keys: string[]): string[] => {
  return keys.map(translate);
};
