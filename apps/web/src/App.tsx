import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './layouts/Layout';
import { HomePage } from './pages/HomePage';
import { ProgramsPage } from './pages/ProgramsPage';
import { ProgramDetailPage } from './pages/ProgramDetailPage';
import { TrajectoriesPage } from './pages/TrajectoriesPage';
import { ProfilePage } from './pages/ProfilePage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="programs" element={<ProgramsPage />} />
          <Route path="programs/:id" element={<ProgramDetailPage />} />
          <Route path="trajectories" element={<TrajectoriesPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="recommendations/:id" element={<RecommendationsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
