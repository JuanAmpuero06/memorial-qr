import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import Spinner from '../components/common/Spinner.jsx';

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMemorial, setSelectedMemorial] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await api.get('/analytics/dashboard');
      setAnalytics(response.data);
      if (response.data.memorials_analytics.length > 0) {
        setSelectedMemorial(response.data.memorials_analytics[0]);
      }
    } catch (error) {
      console.error('Error cargando analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const getReactionIcon = (type) => {
    const icons = {
      candle: '🕯️',
      flower: '🌸',
      heart: '❤️',
      pray: '🙏',
      dove: '🕊️'
    };
    return icons[type] || '❓';
  };

  const getReactionName = (type) => {
    const names = {
      candle: 'Velas',
      flower: 'Flores',
      heart: 'Corazones',
      pray: 'Oraciones',
      dove: 'Palomas'
    };
    return names[type] || type;
  };

  if (loading) return <Spinner />;

  if (!analytics) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100 flex items-center justify-center">
        <p className="text-gray-600">Error cargando datos</p>
      </div>
    );
  }

  const maxVisits = selectedMemorial?.daily_visits?.length > 0 
    ? Math.max(...selectedMemorial.daily_visits.map(d => d.count), 1)
    : 1;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                📊 Analytics
              </h1>
              <p className="text-gray-600 mt-1">
                Estadísticas de visitas y reacciones
              </p>
            </div>
            <Link
              to="/"
              className="inline-flex items-center px-4 py-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors font-medium"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Volver al Dashboard
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Generales */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-md p-6 border-l-4 border-indigo-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">Total Memoriales</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{analytics.total_memorials}</p>
              </div>
              <div className="h-12 w-12 bg-indigo-100 rounded-xl flex items-center justify-center">
                <svg className="h-6 w-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-md p-6 border-l-4 border-emerald-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">Total Visitas</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{analytics.total_visits}</p>
              </div>
              <div className="h-12 w-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                <svg className="h-6 w-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-md p-6 border-l-4 border-pink-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm font-medium">Total Reacciones</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{analytics.total_reactions}</p>
              </div>
              <div className="h-12 w-12 bg-pink-100 rounded-xl flex items-center justify-center">
                <svg className="h-6 w-6 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {analytics.memorials_analytics.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-md">
            <div className="mx-auto h-20 w-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <svg className="h-10 w-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Sin datos todavía</h3>
            <p className="text-gray-600">Crea tu primer memorial para comenzar a ver estadísticas</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Lista de Memoriales */}
            <div className="bg-white rounded-2xl shadow-md overflow-hidden">
              <div className="p-4 border-b border-gray-100">
                <h3 className="font-semibold text-gray-900">Memoriales</h3>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                {analytics.memorials_analytics.map((mem) => (
                  <button
                    key={mem.memorial_id}
                    onClick={() => setSelectedMemorial(mem)}
                    className={`w-full p-4 text-left hover:bg-gray-50 transition-colors border-b border-gray-50 ${
                      selectedMemorial?.memorial_id === mem.memorial_id ? 'bg-indigo-50 border-l-4 border-l-indigo-500' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{mem.memorial_name}</p>
                        <p className="text-sm text-gray-500">{mem.stats.total_visits} visitas</p>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-gray-400">
                        {Object.entries(mem.reactions_count).map(([type, count]) => (
                          count > 0 && (
                            <span key={type} className="flex items-center">
                              {getReactionIcon(type)} {count}
                            </span>
                          )
                        ))}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Detalle del Memorial Seleccionado */}
            {selectedMemorial && (
              <div className="lg:col-span-2 space-y-6">
                {/* Stats del Memorial */}
                <div className="bg-white rounded-2xl shadow-md p-6">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-xl">📈</span>
                    Estadísticas de "{selectedMemorial.memorial_name}"
                  </h3>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 text-center">
                      <p className="text-2xl font-bold text-indigo-600">{selectedMemorial.stats.total_visits}</p>
                      <p className="text-xs text-gray-600 mt-1">Total</p>
                    </div>
                    <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 text-center">
                      <p className="text-2xl font-bold text-emerald-600">{selectedMemorial.stats.today_visits}</p>
                      <p className="text-xs text-gray-600 mt-1">Hoy</p>
                    </div>
                    <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-xl p-4 text-center">
                      <p className="text-2xl font-bold text-amber-600">{selectedMemorial.stats.week_visits}</p>
                      <p className="text-xs text-gray-600 mt-1">Esta semana</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 text-center">
                      <p className="text-2xl font-bold text-purple-600">{selectedMemorial.stats.month_visits}</p>
                      <p className="text-xs text-gray-600 mt-1">Este mes</p>
                    </div>
                  </div>
                </div>

                {/* Gráfico de Visitas */}
                <div className="bg-white rounded-2xl shadow-md p-6">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-xl">📊</span>
                    Visitas últimos 30 días
                  </h3>
                  
                  {selectedMemorial.daily_visits.length > 0 ? (
                    <div className="h-48 flex items-end gap-1">
                      {selectedMemorial.daily_visits.map((day, index) => {
                        const height = (day.count / maxVisits) * 100;
                        return (
                          <div
                            key={index}
                            className="flex-1 group relative"
                          >
                            <div
                              className="bg-gradient-to-t from-indigo-500 to-purple-500 rounded-t transition-all hover:from-indigo-600 hover:to-purple-600"
                              style={{ height: `${Math.max(height, 4)}%` }}
                            ></div>
                            <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                              {day.date}: {day.count} visitas
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  ) : (
                    <div className="h-48 flex items-center justify-center text-gray-400">
                      Sin datos de visitas aún
                    </div>
                  )}
                </div>

                {/* Reacciones */}
                <div className="bg-white rounded-2xl shadow-md p-6">
                  <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <span className="text-xl">💝</span>
                    Reacciones recibidas
                  </h3>
                  
                  <div className="grid grid-cols-5 gap-3">
                    {Object.entries(selectedMemorial.reactions_count).map(([type, count]) => (
                      <div
                        key={type}
                        className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4 text-center hover:shadow-md transition-shadow"
                      >
                        <div className="text-3xl mb-2">{getReactionIcon(type)}</div>
                        <p className="text-xl font-bold text-gray-800">{count}</p>
                        <p className="text-xs text-gray-500">{getReactionName(type)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Analytics;
