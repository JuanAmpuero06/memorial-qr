import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import PublicMemorial from './pages/PublicMemorial.jsx';

// Componente "Protegido" (Panel de Admin)
function AdminLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loadingAuth, setLoadingAuth] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) setIsAuthenticated(true);
    setLoadingAuth(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    navigate('/login');
  };

  if (loadingAuth) return null;

  // Si no está autenticado, redirigir a login
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="font-sans bg-gray-50 min-h-screen">
      <nav className="px-5 py-4 bg-gray-800 text-white flex justify-between items-center">
        <strong className="text-xl">🕊️ Memorial QR (Admin)</strong>
        <button 
          onClick={handleLogout} 
          className="bg-transparent border border-white text-white px-3 py-1 rounded hover:bg-white hover:text-gray-800 transition-colors cursor-pointer"
        >
          Cerrar Sesión
        </button>
      </nav>

      <div className="max-w-5xl mx-auto my-5 px-5">
        <Dashboard />
      </div>
    </div>
  );
}

// Componente Principal con Rutas
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta Pública: Lo que se ve al escanear el QR */}
        <Route path="/view/:slug" element={<PublicMemorial />} />

        {/* Rutas de Autenticación */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Ruta Privada: El panel de administración */}
        <Route path="/" element={<AdminLayout />} />
        
        {/* Cualquier otra cosa redirige al admin */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;