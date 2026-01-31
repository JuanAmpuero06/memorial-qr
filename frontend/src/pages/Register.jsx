import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validar que las contraseñas coincidan
    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    // Validar longitud mínima de contraseña
    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);

    try {
      // Enviar datos de registro al backend
      await api.post('/users/', {
        email: email,
        password: password
      });

      // Si el registro es exitoso, redirigir al login
      alert('¡Registro exitoso! Ahora puedes iniciar sesión.');
      navigate('/login');
      
    } catch (err) {
      console.error(err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Error al registrar el usuario. Intenta de nuevo.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-sm mx-auto my-12 border border-gray-300 p-6 rounded-lg shadow-md bg-white">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Crear Cuenta</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1 font-medium">Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="tu@email.com"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1 font-medium">Contraseña:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            minLength={6}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Mínimo 6 caracteres"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 mb-1 font-medium">Confirmar Contraseña:</label>
          <input 
            type="password" 
            value={confirmPassword} 
            onChange={(e) => setConfirmPassword(e.target.value)} 
            required 
            minLength={6}
            className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Repite tu contraseña"
          />
        </div>
        {error && <p className="text-red-600 mb-3 text-sm">{error}</p>}
        <button 
          type="submit" 
          disabled={loading}
          className="w-full py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors cursor-pointer font-medium disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Registrando...' : 'Registrarse'}
        </button>
      </form>
      
      <div className="mt-4 text-center text-sm text-gray-600">
        ¿Ya tienes cuenta?{' '}
        <Link to="/login" className="text-blue-600 hover:text-blue-700 font-medium">
          Inicia sesión aquí
        </Link>
      </div>
    </div>
  );
}

export default Register;
