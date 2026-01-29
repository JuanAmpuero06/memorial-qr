import { useState } from 'react';
import api from './api';

function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // 1. Enviamos los datos al endpoint que creamos en FastAPI
      // Nota: OAuth2 espera datos en formato form-data, no JSON puro a veces,
      // pero FastAPI acepta x-www-form-urlencoded. Axios lo maneja así:
      const formData = new URLSearchParams();
      formData.append('username', email); // FastAPI usa 'username' para el email
      formData.append('password', password);

      const response = await api.post('/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      // 2. Si todo sale bien, guardamos el token
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      
      // 3. Avisamos a App.jsx que ya entramos
      onLoginSuccess();
      
    } catch (err) {
      console.error(err);
      setError('Credenciales incorrectas. Intenta de nuevo.');
    }
  };

  return (
    <div style={{ maxWidth: '300px', margin: '50px auto', border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Contraseña:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Entrar
        </button>
      </form>
    </div>
  );
}

export default Login;