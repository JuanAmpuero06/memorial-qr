import axios from 'axios';

// Usamos la variable de entorno que definimos en docker-compose, 
// o localhost por defecto si corremos fuera de docker.
// Con Traefik, todo pasa por el puerto 80
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost'; 

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- INTERCEPTOR (Truco Pro) ---
// Esto inyecta el Token automáticamente en cada petición si existe.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;