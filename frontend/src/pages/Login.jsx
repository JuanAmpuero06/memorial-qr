import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // 1. Enviamos los datos al endpoint que creamos en FastAPI
      const formData = new URLSearchParams();
      formData.append('username', email); // FastAPI usa 'username' para el email
      formData.append('password', password);

      const response = await api.post('/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      // 2. Si todo sale bien, guardamos el token
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      
      // 3. Redirigir al dashboard
      navigate('/');
      
    } catch (err) {
      console.error(err);
      setError('Credenciales incorrectas. Intenta de nuevo.');
    }
  };

  return (
    <div className="max-w-sm mx-auto my-12 border border-gray-300 p-6 rounded-lg shadow-md bg-white">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1 font-medium">Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1 font-medium">Contraseña:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        {error && <p className="text-red-600 mb-3">{error}</p>}
        <button type="submit" className="w-full py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors cursor-pointer font-medium">
          Entrar
        </button>
      </form>
      
      <div className="mt-4 text-center text-sm text-gray-600">
        ¿No tienes cuenta?{' '}
        <Link to="/register" className="text-blue-600 hover:text-blue-700 font-medium">
          Regístrate aquí
        </Link>
      </div>
    </div>
  );
}

export default Login;