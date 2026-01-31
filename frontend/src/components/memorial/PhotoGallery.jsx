import { useState, useEffect } from 'react';
import api from '../../api';

/**
 * Componente de Galería de Fotos
 * Muestra múltiples fotos/videos del memorial
 */
function PhotoGallery({ slug, isOwner = false, memorialId = null }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchGallery();
  }, [slug]);

  const fetchGallery = async () => {
    try {
      const response = await api.get(`/api/v1/gallery/public/${slug}`);
      setItems(response.data.items || []);
    } catch (error) {
      console.error('Error cargando galería:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post(`/api/v1/gallery/${memorialId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchGallery();
    } catch (error) {
      console.error('Error subiendo archivo:', error);
      alert('Error al subir el archivo');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (itemId) => {
    if (!window.confirm('¿Eliminar esta foto?')) return;
    try {
      await api.delete(`/api/v1/gallery/${itemId}`);
      fetchGallery();
    } catch (error) {
      console.error('Error eliminando:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  if (items.length === 0 && !isOwner) {
    return null;
  }

  return (
    <div className="mt-8 p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-amber-400 font-semibold text-sm uppercase tracking-wider flex items-center gap-2">
          <span>📸</span> Galería de Recuerdos
        </h3>
        {isOwner && (
          <label className="text-xs bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full hover:bg-amber-500/30 transition-colors cursor-pointer">
            {uploading ? 'Subiendo...' : '+ Agregar foto'}
            <input
              type="file"
              accept="image/*,video/*"
              onChange={handleUpload}
              className="hidden"
              disabled={uploading}
            />
          </label>
        )}
      </div>

      {items.length > 0 ? (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {items.map((item) => (
            <div 
              key={item.id} 
              className="relative group aspect-square rounded-xl overflow-hidden cursor-pointer"
              onClick={() => setSelectedImage(item)}
            >
              {item.media_type === 'video' ? (
                <video 
                  src={item.filename}
                  className="w-full h-full object-cover"
                />
              ) : (
                <img 
                  src={item.filename}
                  alt={item.title || 'Foto de recuerdo'}
                  className="w-full h-full object-cover transition-transform group-hover:scale-110"
                />
              )}
              
              {/* Overlay con info */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="absolute bottom-2 left-2 right-2">
                  {item.title && (
                    <p className="text-white text-sm font-medium truncate">{item.title}</p>
                  )}
                  {item.taken_at && (
                    <p className="text-white/70 text-xs">{item.taken_at}</p>
                  )}
                </div>
              </div>
              
              {/* Botón eliminar (solo propietario) */}
              {isOwner && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(item.id);
                  }}
                  className="absolute top-2 right-2 bg-red-500/80 text-white w-6 h-6 rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-xs hover:bg-red-600"
                >
                  ✕
                </button>
              )}
              
              {/* Badge de video */}
              {item.media_type === 'video' && (
                <div className="absolute top-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-xs">
                  🎬 Video
                </div>
              )}
              
              {/* Badge destacado */}
              {item.is_featured && (
                <div className="absolute top-2 left-2 bg-amber-500/80 text-white px-2 py-1 rounded text-xs">
                  ⭐ Destacada
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-slate-500 text-sm text-center py-8">
          No hay fotos en la galería
        </p>
      )}

      {/* Modal de imagen ampliada */}
      {selectedImage && (
        <div 
          className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <button
            onClick={() => setSelectedImage(null)}
            className="absolute top-4 right-4 text-white text-2xl hover:text-amber-400 transition-colors"
          >
            ✕
          </button>
          
          <div className="max-w-4xl max-h-[90vh] relative" onClick={(e) => e.stopPropagation()}>
            {selectedImage.media_type === 'video' ? (
              <video 
                src={selectedImage.filename}
                controls
                autoPlay
                className="max-h-[80vh] rounded-lg"
              />
            ) : (
              <img 
                src={selectedImage.filename}
                alt={selectedImage.title || 'Foto ampliada'}
                className="max-h-[80vh] rounded-lg"
              />
            )}
            
            {(selectedImage.title || selectedImage.caption) && (
              <div className="mt-4 text-center">
                {selectedImage.title && (
                  <h4 className="text-white text-lg font-medium">{selectedImage.title}</h4>
                )}
                {selectedImage.caption && (
                  <p className="text-slate-400 mt-1">{selectedImage.caption}</p>
                )}
                {selectedImage.location && (
                  <p className="text-amber-400/70 text-sm mt-2">📍 {selectedImage.location}</p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default PhotoGallery;
