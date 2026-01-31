import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import Spinner from '../components/common/Spinner.jsx'; // Importar el componente Spinner
import ErrorMessage from '../components/common/ErrorMessage.jsx'; // Importar el componente ErrorMessage

function PublicMemorial() {
  const { slug } = useParams(); // Capturamos el slug de la URL
  const [memorial, setMemorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        // Usamos el endpoint PÚBLICO que creamos en el backend
        const response = await api.get(`/public/memorials/${slug}`);
        setMemorial(response.data);
      } catch (err) {
        console.error("Error cargando memorial:", err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchPublicData();
  }, [slug]);

  if (loading) return <Spinner />; // Usar el componente Spinner
  if (error) return <ErrorMessage message="Memorial no encontrado." />; // Usar el componente ErrorMessage

  return (
    <div className="max-w-2xl mx-auto my-10 p-10 text-center font-serif bg-amber-50 border border-gray-300 rounded-lg shadow-lg">
      
      {/* --- NUEVO: FOTO DEL DIFUNTO --- */}
      {memorial.image_filename && (
        <img 
          src={memorial.image_filename} 
          alt={memorial.name}
          className="w-36 h-36 object-cover rounded-full border-4 border-white shadow-md mb-5 mx-auto"
        />
      )}

      <h1 className="text-4xl text-gray-800 mb-2 mt-0">
        {memorial.name}
      </h1>
      
      {/* Fechas (Si las tuvieras en el futuro) */}
      {/* <p className="text-gray-600">1950 - 2023</p> */}

      <hr className="w-1/2 border-0 border-t border-gray-400 my-5 mx-auto" />

      <p className="text-xl italic text-gray-700 mb-8">
        "{memorial.epitaph}"
      </p>

      {memorial.bio && (
        <div className="text-justify leading-7 text-gray-600">
          <p>{memorial.bio}</p>
        </div>
      )}

      <div className="mt-12 text-xs text-gray-400">
        🕊️ Memorial QR
      </div>
    </div>
  );
}

export default PublicMemorial;