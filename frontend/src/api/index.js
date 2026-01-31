import axios from 'axios';

// Usamos la variable de entorno que definimos en docker-compose, 
// o localhost por defecto si corremos fuera de docker.
const API_URL = 'http://localhost:8000'; 

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