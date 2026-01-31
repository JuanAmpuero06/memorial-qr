import { useState, useEffect } from 'react';
import api from '../api';
import Spinner from '../components/common/Spinner.jsx'; // Importar el componente Spinner

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
  // 4. Función para subir foto
  const handleFileUpload = async (memorialId, file) => {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post(`/memorials/${memorialId}/upload-photo`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Importante para enviar archivos
        },
      });
      // Recargar la lista para ver la foto nueva
      fetchMemorials();
    } catch (error) {
      console.error("Error subiendo foto:", error);
      alert("Error al subir la imagen");
    }
  };

  if (loading) return <Spinner />; // Usar el componente Spinner

  return (
    <div>
      {/* --- FORMULARIO DE CREACIÓN --- */}
      <div className="bg-white p-5 rounded-lg mb-5 shadow-md">
        <h3 className="mt-0 mb-4 text-xl font-bold text-gray-800">🕯️ Crear Nuevo Memorial</h3>
        <form onSubmit={handleCreate} className="flex gap-3 flex-wrap">
          <input 
            type="text" 
            placeholder="Nombre del Difunto" 
            value={newName}
            onChange={e => setNewName(e.target.value)}
            required
            className="p-2 flex-1 min-w-[200px] border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <input 
            type="text" 
            placeholder="Epitafio (Ej: Siempre en nuestros corazones)" 
            value={newEpitaph}
            onChange={e => setNewEpitaph(e.target.value)}
            className="p-2 flex-[2] min-w-[200px] border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <button type="submit" className="px-5 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors cursor-pointer font-medium">
            Crear
          </button>
        </form>
      </div>

      {/* --- LISTA DE MEMORIALES --- */}
      <h3 className="text-xl font-bold text-gray-800 mb-4">Mis Memoriales ({memorials.length})</h3>
      
      {memorials.length === 0 && (
        <div className="p-5 bg-yellow-100 text-yellow-800 rounded-lg">
          ⚠️ La lista está vacía. Intenta crear un memorial nuevo arriba.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {memorials.map(mem => (
          <div key={mem.id} className="border border-gray-300 rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition-shadow">
            
            {/* --- SECCIÓN DE FOTO --- */}
            <div className="mb-4 text-center">
              {mem.image_filename ? (
                <img 
                  src={mem.image_filename} 
                  alt="Foto del difunto" 
                  className="w-24 h-24 object-cover rounded-full mx-auto border-2 border-gray-200"
                />
              ) : (
                <div className="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center mx-auto text-4xl">
                  👤
                </div>
              )}
            </div>

            <h4 className="m-0 mb-2 text-center text-lg font-semibold text-gray-800">{mem.name}</h4>
            <p className="italic text-gray-600 text-center text-sm">"{mem.epitaph || 'Sin epitafio'}"</p>
            
            <div className="mt-4 flex flex-col gap-2">
              
              {/* INPUT PARA SUBIR FOTO */}
              <label className="text-sm text-blue-600 cursor-pointer text-center hover:text-blue-700 transition-colors">
                📷 Cambiar Foto
                <input 
                  type="file" 
                  accept="image/*" 
                  className="hidden" 
                  onChange={(e) => handleFileUpload(mem.id, e.target.files[0])}
                />
              </label>

              <button 
                onClick={() => downloadQR(mem)}
                className="p-2 bg-gray-800 text-white rounded hover:bg-gray-700 transition-colors cursor-pointer"
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