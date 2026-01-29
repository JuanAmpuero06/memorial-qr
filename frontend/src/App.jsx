import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'; // <--- Importamos Router
import Login from './Login';
import Dashboard from './Dashboard';
import PublicMemorial from './PublicMemorial'; // <--- Importamos el nuevo componente

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
    <div style={{ fontFamily: 'Arial, sans-serif', backgroundColor: '#f4f4f9', minHeight: '100vh' }}>
      <nav style={{ padding: '15px 20px', backgroundColor: '#333', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong style={{ fontSize: '1.2em' }}>🕊️ Memorial QR (Admin)</strong>
        {isAuthenticated && (
          <button 
            onClick={handleLogout} 
            style={{ background: 'transparent', border: '1px solid white', color: 'white', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }}
          >
            Cerrar Sesión
          </button>
        )}
      </nav>

      <div style={{ maxWidth: '1000px', margin: '20px auto', padding: '0 20px' }}>
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