export const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Orientation Platform
            </h3>
            <p className="text-gray-600 text-sm">
              Plataforma de orientación vocacional para estudiantes secundarios de Argentina.
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3">Enlaces</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>
                <a href="/programs" className="hover:text-primary transition-colors">
                  Programas
                </a>
              </li>
              <li>
                <a href="/trajectories" className="hover:text-primary transition-colors">
                  Historias
                </a>
              </li>
              <li>
                <a href="/about" className="hover:text-primary transition-colors">
                  Acerca de
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3">Proyecto</h4>
            <p className="text-gray-600 text-sm">
              Código abierto bajo licencia MIT.
            </p>
            <a 
              href="https://github.com/Axel19L/orientation-platform" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary hover:text-primary-dark text-sm font-medium inline-block mt-2"
            >
              Ver en GitHub →
            </a>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-gray-200 text-center text-sm text-gray-600">
          <p>© 2026 Orientation Platform. Código abierto para la comunidad.</p>
        </div>
      </div>
    </footer>
  );
};
