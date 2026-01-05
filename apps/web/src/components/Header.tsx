import { Link } from 'react-router-dom';

export const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">O</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">
                Orientation Platform
              </span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-8">
            <Link 
              to="/programs" 
              className="text-gray-700 hover:text-primary font-medium transition-colors"
            >
              Programas
            </Link>
            <Link 
              to="/trajectories" 
              className="text-gray-700 hover:text-primary font-medium transition-colors"
            >
              Historias
            </Link>
            <Link 
              to="/profile" 
              className="btn-primary"
            >
              Mi Perfil
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
};
