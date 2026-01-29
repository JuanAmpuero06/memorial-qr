import { useState, useEffect } from 'react'
import Login from './Login'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Al cargar la página, revisamos si ya hay un token guardado
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  }

  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>
      <nav style={{ padding: '10px', backgroundColor: '#f0f0f0', marginBottom: '20px' }}>
        <strong>Memorial QR</strong>
        {isAuthenticated && (
          <button onClick={handleLogout} style={{ float: 'right', cursor: 'pointer' }}>
            Cerrar Sesión
          </button>
        )}
      </nav>

      {isAuthenticated ? (
        <div style={{ padding: '20px' }}>
          <h1>¡Bienvenido al Panel! 👋</h1>
          <p>Aquí verás tus memoriales pronto.</p>
        </div>
      ) : (
        <Login onLoginSuccess={() => setIsAuthenticated(true)} />
      )}
    </div>
  )
}

export default App