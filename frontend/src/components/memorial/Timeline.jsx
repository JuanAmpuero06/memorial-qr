import { useState, useEffect } from 'react';
import api from '../../api';

/**
 * Componente de Línea de Tiempo
 * Muestra eventos importantes de la vida del fallecido
 */
function Timeline({ slug, isOwner = false, memorialId = null }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newEvent, setNewEvent] = useState({
    title: '',
    description: '',
    event_date: '',
    event_type: 'general',
    icon: ''
  });

  const eventTypes = {
    birth: { icon: '👶', label: 'Nacimiento', color: 'bg-pink-500' },
    education: { icon: '🎓', label: 'Educación', color: 'bg-blue-500' },
    career: { icon: '💼', label: 'Carrera', color: 'bg-green-500' },
    family: { icon: '💒', label: 'Familia', color: 'bg-purple-500' },
    achievement: { icon: '🏆', label: 'Logro', color: 'bg-yellow-500' },
    travel: { icon: '✈️', label: 'Viaje', color: 'bg-cyan-500' },
    hobby: { icon: '🎨', label: 'Hobby', color: 'bg-orange-500' },
    general: { icon: '📌', label: 'General', color: 'bg-slate-500' },
    other: { icon: '✨', label: 'Otro', color: 'bg-indigo-500' }
  };

  useEffect(() => {
    fetchTimeline();
  }, [slug]);

  const fetchTimeline = async () => {
    try {
      const response = await api.get(`/api/v1/timeline/public/${slug}`);
      setEvents(response.data.events || []);
    } catch (error) {
      console.error('Error cargando timeline:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddEvent = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/api/v1/timeline/${memorialId}`, newEvent);
      setNewEvent({ title: '', description: '', event_date: '', event_type: 'general', icon: '' });
      setShowForm(false);
      fetchTimeline();
    } catch (error) {
      console.error('Error agregando evento:', error);
    }
  };

  const handleDeleteEvent = async (eventId) => {
    if (!window.confirm('¿Eliminar este evento?')) return;
    try {
      await api.delete(`/api/v1/timeline/${eventId}`);
      fetchTimeline();
    } catch (error) {
      console.error('Error eliminando evento:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  if (events.length === 0 && !isOwner) {
    return null;
  }

  return (
    <div className="mt-8 p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-amber-400 font-semibold text-sm uppercase tracking-wider flex items-center gap-2">
          <span>📅</span> Línea de Tiempo
        </h3>
        {isOwner && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="text-xs bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full hover:bg-amber-500/30 transition-colors"
          >
            {showForm ? '✕ Cancelar' : '+ Agregar'}
          </button>
        )}
      </div>

      {/* Formulario para agregar evento */}
      {showForm && isOwner && (
        <form onSubmit={handleAddEvent} className="mb-6 p-4 bg-slate-700/30 rounded-xl space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Título del evento"
              value={newEvent.title}
              onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
              className="bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              required
            />
            <input
              type="date"
              value={newEvent.event_date}
              onChange={(e) => setNewEvent({ ...newEvent, event_date: e.target.value })}
              className="bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
              required
            />
          </div>
          <textarea
            placeholder="Descripción (opcional)"
            value={newEvent.description}
            onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
            className="w-full bg-slate-700/50 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
            rows={2}
          />
          <div className="flex gap-2 flex-wrap">
            {Object.entries(eventTypes).map(([key, { icon, label }]) => (
              <button
                type="button"
                key={key}
                onClick={() => setNewEvent({ ...newEvent, event_type: key, icon })}
                className={`px-3 py-1 rounded-full text-xs transition-all ${
                  newEvent.event_type === key 
                    ? 'bg-amber-500 text-white' 
                    : 'bg-slate-600/50 text-slate-300 hover:bg-slate-600'
                }`}
              >
                {icon} {label}
              </button>
            ))}
          </div>
          <button
            type="submit"
            className="w-full bg-amber-500 text-white py-2 rounded-lg hover:bg-amber-600 transition-colors"
          >
            Guardar Evento
          </button>
        </form>
      )}

      {/* Timeline */}
      {events.length > 0 ? (
        <div className="relative">
          {/* Línea vertical */}
          <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-amber-500/50 via-amber-400/30 to-transparent"></div>
          
          <div className="space-y-6">
            {events.map((event, index) => {
              const typeInfo = eventTypes[event.event_type] || eventTypes.general;
              return (
                <div key={event.id} className="relative pl-12 group">
                  {/* Punto en la línea */}
                  <div className={`absolute left-2 top-1 w-5 h-5 rounded-full ${typeInfo.color} flex items-center justify-center text-xs shadow-lg`}>
                    {event.icon || typeInfo.icon}
                  </div>
                  
                  {/* Contenido */}
                  <div className="bg-slate-700/30 rounded-xl p-4 hover:bg-slate-700/50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-white font-medium">{event.title}</h4>
                        <p className="text-amber-400/80 text-xs mt-1">
                          {new Date(event.event_date).toLocaleDateString('es-ES', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </p>
                      </div>
                      {isOwner && (
                        <button
                          onClick={() => handleDeleteEvent(event.id)}
                          className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-300 text-sm transition-opacity"
                        >
                          🗑️
                        </button>
                      )}
                    </div>
                    {event.description && (
                      <p className="text-slate-400 text-sm mt-2">{event.description}</p>
                    )}
                    {event.image_filename && (
                      <img 
                        src={event.image_filename} 
                        alt={event.title}
                        className="mt-3 rounded-lg max-h-40 object-cover"
                      />
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <p className="text-slate-500 text-sm text-center py-4">
          No hay eventos en la línea de tiempo
        </p>
      )}
    </div>
  );
}

export default Timeline;
