import { useState, useEffect } from 'react';
import api from './api';

function Dashboard() {
  const [memorials, setMemorials] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Estado para el formulario de crear nuevo
  const [newName, setNewName] = useState('');
  const [newEpitaph, setNewEpitaph] = useState('');

  // 1. Cargar memoriales al iniciar
  const fetchMemorials = async () => {
    console.log("1. 📡 Iniciando fetchMemorials (Pidiendo datos al backend)..."); 
    try {
      const response = await api.get('/memorials/');
      console.log("2. ✅ Respuesta recibida del Backend:", response.data); 
      setMemorials(response.data);
    } catch (error) {
      console.error("3. ❌ Error fatal cargando memoriales:", error);
      if (error.response) {
        console.error("   Datos del error:", error.response.status, error.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("0. 🏁 El componente Dashboard se montó en pantalla."); 
    fetchMemorials();
  }, []);

  // 2. Función para crear uno nuevo
  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newName) return;

    try {
      console.log("Intentando crear memorial:", newName);
      await api.post('/memorials/', {
        name: newName,
        epitaph: newEpitaph
      });
      // Limpiamos el formulario y recargamos la lista
      setNewName('');
      setNewEpitaph('');
      fetchMemorials(); 
    } catch (error) {
      console.error("Error al crear:", error);
      alert("Error al crear el memorial");
    }
  };

  // 3. Función para descargar el QR
  const downloadQR = async (memorial) => {
    try {
      console.log("Descargando QR para:", memorial.slug);
      const response = await api.get(`/memorials/${memorial.slug}/qr`, {
        responseType: 'blob' 
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `qr-${memorial.slug}.png`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error descargando QR", error);
    }
  };

  if (loading) return <p style={{padding: '20px'}}>Cargando datos del servidor...</p>;

  return (
    <div>
      {/* --- FORMULARIO DE CREACIÓN --- */}
      <div style={{ background: '#fff', padding: '20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
        <h3 style={{ marginTop: 0 }}>🕯️ Crear Nuevo Memorial</h3>
        <form onSubmit={handleCreate} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input 
            type="text" 
            placeholder="Nombre del Difunto" 
            value={newName}
            onChange={e => setNewName(e.target.value)}
            required
            style={{ padding: '8px', flex: '1', minWidth: '200px' }}
          />
          <input 
            type="text" 
            placeholder="Epitafio (Ej: Siempre en nuestros corazones)" 
            value={newEpitaph}
            onChange={e => setNewEpitaph(e.target.value)}
            style={{ padding: '8px', flex: '2', minWidth: '200px' }}
          />
          <button type="submit" style={{ padding: '8px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Crear
          </button>
        </form>
      </div>

      {/* --- LISTA DE MEMORIALES --- */}
      <h3>Mis Memoriales ({memorials.length})</h3>
      
      {memorials.length === 0 && (
        <div style={{ padding: '20px', background: '#ffeeba', color: '#856404', borderRadius: '5px' }}>
          ⚠️ La lista está vacía. Intenta crear un memorial nuevo arriba.
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
        {memorials.map(mem => (
          <div key={mem.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px', background: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#333' }}>{mem.name}</h4>
            <p style={{ fontStyle: 'italic', color: '#666' }}>"{mem.epitaph || 'Sin epitafio'}"</p>
            <p style={{ fontSize: '0.8em', color: '#999' }}>Slug: {mem.slug}</p>
            
            <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
              <button 
                onClick={() => downloadQR(mem)}
                style={{ flex: 1, padding: '8px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                📲 Descargar QR
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;