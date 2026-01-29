import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from './api';

function PublicMemorial() {
  const { slug } = useParams(); // Capturamos el slug de la URL
  const [memorial, setMemorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        // Usamos el endpoint PÚBLICO que creamos en el backend (sin candado)
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

  if (loading) return <div style={{textAlign: 'center', marginTop: '50px'}}>Cargando memoria...</div>;
  if (error) return <div style={{textAlign: 'center', marginTop: '50px', color: 'red'}}>Memorial no encontrado.</div>;

  return (
    <div style={{ 
      maxWidth: '600px', 
      margin: '40px auto', 
      padding: '40px', 
      textAlign: 'center', 
      fontFamily: "'Georgia', serif", // Fuente más clásica/seria
      backgroundColor: '#fffcf5', // Un tono crema suave
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      boxShadow: '0 4px 10px rgba(0,0,0,0.05)'
    }}>
      <h1 style={{ fontSize: '2.5em', color: '#333', marginBottom: '10px' }}>
        {memorial.name}
      </h1>
      
      {/* Fechas (Si las tuvieras en el futuro) */}
      {/* <p style={{ color: '#666' }}>1950 - 2023</p> */}

      <hr style={{ width: '50%', border: '0', borderTop: '1px solid #ccc', margin: '20px auto' }} />

      <p style={{ 
        fontSize: '1.2em', 
        fontStyle: 'italic', 
        color: '#555', 
        marginBottom: '30px' 
      }}>
        "{memorial.epitaph}"
      </p>

      {memorial.bio && (
        <div style={{ textAlign: 'justify', lineHeight: '1.6', color: '#444' }}>
          <p>{memorial.bio}</p>
        </div>
      )}

      <div style={{ marginTop: '50px', fontSize: '0.8em', color: '#999' }}>
        🕊️ Memorial QR
      </div>
    </div>
  );
}

export default PublicMemorial;