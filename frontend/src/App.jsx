import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'; // <--- Importamos Router
import Login from './pages/Login.jsx';
import Dashboard from './pages/Dashboard.jsx';
import PublicMemorial from './pages/PublicMemorial.jsx'; // <--- Importamos el nuevo componente

// Componente "Protegido" (El antiguo App)
function AdminLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) setIsAuthenticated(true);
    setLoadingAuth(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (loadingAuth) return null; // Evita parpadeos

  return (
    <div className="font-sans bg-gray-50 min-h-screen">
      <nav className="px-5 py-4 bg-gray-800 text-white flex justify-between items-center">
        <strong className="text-xl">🕊️ Memorial QR (Admin)</strong>
        {isAuthenticated && (
          <button 
            onClick={handleLogout} 
            className="bg-transparent border border-white text-white px-3 py-1 rounded hover:bg-white hover:text-gray-800 transition-colors cursor-pointer"
          >
            Cerrar Sesión
          </button>
        )}
      </nav>

      <div className="max-w-5xl mx-auto my-5 px-5">
        {isAuthenticated ? (
          <Dashboard />
        ) : (
          <Login onLoginSuccess={() => setIsAuthenticated(true)} />
        )}
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

        {/* Ruta Privada: El panel de administración */}
        <Route path="/" element={<AdminLayout />} />
        
        {/* Cualquier otra cosa redirige al admin */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;