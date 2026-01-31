import { useState, useEffect } from 'react';
import api from '../../api';

/**
 * Componente de Libro de Condolencias
 * Permite a visitantes dejar mensajes y al propietario moderarlos
 */
function Condolences({ slug, isOwner = false }) {
  const [condolences, setCondolences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [pendingCount, setPendingCount] = useState(0);
  const [showPending, setShowPending] = useState(false);
  
  const [newCondolence, setNewCondolence] = useState({
    author_name: '',
    author_relationship: '',
    message: ''
  });

  useEffect(() => {
    fetchCondolences();
  }, [slug, showPending]);

  const fetchCondolences = async () => {
    try {
      const endpoint = isOwner && showPending 
        ? `/api/v1/condolences/manage/${slug}` 
        : `/api/v1/condolences/${slug}`;
      
      const response = await api.get(endpoint);
      setCondolences(response.data.items || []);
      setPendingCount(response.data.pending_count || 0);
    } catch (error) {
      console.error('Error cargando condolencias:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      const visitorId = localStorage.getItem('visitor_id');
      await api.post(`/api/v1/condolences/${slug}`, {
        ...newCondolence,
        visitor_id: visitorId
      });
      
      setNewCondolence({ author_name: '', author_relationship: '', message: '' });
      setShowForm(false);
      alert('Tu mensaje ha sido enviado y será revisado por la familia. ¡Gracias!');
    } catch (error) {
      console.error('Error enviando condolencia:', error);
      alert('Error al enviar el mensaje');
    } finally {
      setSubmitting(false);
    }
  };

  const handleModerate = async (condolenceId, action) => {
    try {
      if (action === 'approve') {
        await api.patch(`/api/v1/condolences/${condolenceId}`, { is_approved: true });
      } else if (action === 'feature') {
        await api.patch(`/api/v1/condolences/${condolenceId}`, { is_featured: true });
      } else if (action === 'unfeature') {
        await api.patch(`/api/v1/condolences/${condolenceId}`, { is_featured: false });
      } else if (action === 'delete') {
        if (!window.confirm('¿Eliminar este mensaje?')) return;
        await api.delete(`/api/v1/condolences/${condolenceId}`);
      }
      fetchCondolences();
    } catch (error) {
      console.error('Error moderando:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  return (
    <div className="mt-8 p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-amber-400 font-semibold text-sm uppercase tracking-wider flex items-center gap-2">
          <span>📖</span> Libro de Condolencias
          {condolences.length > 0 && (
            <span className="bg-amber-500/20 px-2 py-0.5 rounded-full text-xs">
              {condolences.length}
            </span>
          )}
        </h3>
        
        <div className="flex gap-2">
          {isOwner && pendingCount > 0 && (
            <button
              onClick={() => setShowPending(!showPending)}
              className={`text-xs px-3 py-1 rounded-full transition-colors ${
                showPending 
                  ? 'bg-amber-500 text-white' 
                  : 'bg-amber-500/20 text-amber-400 hover:bg-amber-500/30'
              }`}
            >
              {pendingCount} pendientes
            </button>
          )}
          
          {!isOwner && (
            <button
              onClick={() => setShowForm(!showForm)}
              className="text-xs bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full hover:bg-amber-500/30 transition-colors"
            >
              {showForm ? '✕ Cancelar' : '✍️ Dejar mensaje'}
            </button>
          )}
        </div>
      </div>

      {/* Formulario para visitantes */}
      {showForm && !isOwner && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 bg-slate-700/30 rounded-xl space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Tu nombre *"
              value={newCondolence.author_name}
              onChange={(e) => setNewCondolence({ ...newCondolence, author_name: e.target.value })}
              className="bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              required
              minLength={2}
            />
            <input
              type="text"
              placeholder="Relación (familiar, amigo...)"
              value={newCondolence.author_relationship}
              onChange={(e) => setNewCondolence({ ...newCondolence, author_relationship: e.target.value })}
              className="bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>
          <textarea
            placeholder="Escribe tu mensaje de condolencia... *"
            value={newCondolence.message}
            onChange={(e) => setNewCondolence({ ...newCondolence, message: e.target.value })}
            className="w-full bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
            rows={4}
            required
            minLength={10}
          />
          <p className="text-slate-500 text-xs">
            * Tu mensaje será revisado por la familia antes de publicarse.
          </p>
          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-amber-500 text-white py-2 rounded-lg hover:bg-amber-600 transition-colors disabled:opacity-50"
          >
            {submitting ? 'Enviando...' : 'Enviar Condolencia'}
          </button>
        </form>
      )}

      {/* Lista de condolencias */}
      {condolences.length > 0 ? (
        <div className="space-y-4">
          {condolences.map((condolence) => (
            <div 
              key={condolence.id} 
              className={`p-4 rounded-xl transition-colors ${
                condolence.is_featured 
                  ? 'bg-amber-500/10 border border-amber-500/30' 
                  : 'bg-slate-700/30 hover:bg-slate-700/50'
              } ${!condolence.is_approved ? 'opacity-60 border-l-4 border-l-yellow-500' : ''}`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-amber-400 to-amber-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {condolence.author_name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <p className="text-white font-medium text-sm flex items-center gap-2">
                      {condolence.author_name}
                      {condolence.is_featured && (
                        <span className="text-amber-400 text-xs">⭐ Destacado</span>
                      )}
                      {!condolence.is_approved && (
                        <span className="text-yellow-400 text-xs bg-yellow-400/20 px-2 py-0.5 rounded-full">
                          Pendiente
                        </span>
                      )}
                    </p>
                    {condolence.author_relationship && (
                      <p className="text-slate-500 text-xs">{condolence.author_relationship}</p>
                    )}
                  </div>
                </div>
                
                {/* Botones de moderación */}
                {isOwner && (
                  <div className="flex gap-1">
                    {!condolence.is_approved && (
                      <button
                        onClick={() => handleModerate(condolence.id, 'approve')}
                        className="text-green-400 hover:text-green-300 p-1 text-sm"
                        title="Aprobar"
                      >
                        ✓
                      </button>
                    )}
                    <button
                      onClick={() => handleModerate(
                        condolence.id, 
                        condolence.is_featured ? 'unfeature' : 'feature'
                      )}
                      className="text-amber-400 hover:text-amber-300 p-1 text-sm"
                      title={condolence.is_featured ? 'Quitar destacado' : 'Destacar'}
                    >
                      {condolence.is_featured ? '★' : '☆'}
                    </button>
                    <button
                      onClick={() => handleModerate(condolence.id, 'delete')}
                      className="text-red-400 hover:text-red-300 p-1 text-sm"
                      title="Eliminar"
                    >
                      🗑️
                    </button>
                  </div>
                )}
              </div>
              
              <p className="text-slate-300 text-sm mt-3 leading-relaxed whitespace-pre-line">
                "{condolence.message}"
              </p>
              
              <p className="text-slate-500 text-xs mt-2">
                {new Date(condolence.created_at).toLocaleDateString('es-ES', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-slate-500 text-sm">
            {showPending 
              ? 'No hay mensajes pendientes de aprobación' 
              : 'Sé el primero en dejar un mensaje de condolencia'}
          </p>
        </div>
      )}
    </div>
  );
}

export default Condolences;
