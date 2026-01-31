import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import Spinner from '../components/common/Spinner.jsx';
import VisitorMap from '../components/analytics/VisitorMap.jsx';

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMemorial, setSelectedMemorial] = useState(null);
  const [locationStats, setLocationStats] = useState([]);
  
  // Estados para filtros
  const [filters, setFilters] = useState({
    period: 'all',
    startDate: '',
    endDate: ''
  });
  const [showCustomDates, setShowCustomDates] = useState(false);

  // Períodos predefinidos
  const periods = [
    { value: 'all', label: 'Todo', icon: '📊' },
    { value: 'today', label: 'Hoy', icon: '📅' },
    { value: 'week', label: '7 días', icon: '📆' },
    { value: 'month', label: '30 días', icon: '🗓️' },
    { value: 'year', label: '1 año', icon: '📈' },
    { value: 'custom', label: 'Personalizado', icon: '⚙️' }
  ];

  useEffect(() => {
    fetchAnalytics();
  }, [filters]);

  useEffect(() => {
    if (selectedMemorial) {
      fetchLocationStats(selectedMemorial.memorial_slug);
    }
  }, [selectedMemorial]);

  const fetchLocationStats = async (slug) => {
    try {
      const response = await api.get(`/analytics/locations/${slug}`);
      setLocationStats(response.data.locations || []);
    } catch (error) {
      console.error('Error cargando ubicaciones:', error);
      setLocationStats([]);
    }
  };

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      
      // Construir parámetros de query
      const params = new URLSearchParams();
      
      if (filters.period === 'custom' && filters.startDate && filters.endDate) {
        params.append('start_date', filters.startDate);
        params.append('end_date', filters.endDate);
      } else if (filters.period !== 'all') {
        params.append('period', filters.period);
      }
      
      const url = `/analytics/dashboard${params.toString() ? '?' + params.toString() : ''}`;
      const response = await api.get(url);
      setAnalytics(response.data);
      
      if (response.data.memorials_analytics.length > 0) {
        // Mantener selección actual si existe, sino seleccionar el primero
        const currentId = selectedMemorial?.memorial_id;
        const found = response.data.memorials_analytics.find(m => m.memorial_id === currentId);
        setSelectedMemorial(found || response.data.memorials_analytics[0]);
      }
    } catch (error) {
      console.error('Error cargando analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePeriodChange = (period) => {
    if (period === 'custom') {
      setShowCustomDates(true);
      setFilters(prev => ({ ...prev, period: 'custom' }));
    } else {
      setShowCustomDates(false);
      setFilters({ period, startDate: '', endDate: '' });
    }
  };

  const handleCustomDateApply = () => {
    if (filters.startDate && filters.endDate) {
      fetchAnalytics();
    }
  };

  const getFilterDescription = () => {
    if (filters.period === 'custom' && filters.startDate && filters.endDate) {
      return `${filters.startDate} - ${filters.endDate}`;
    }
    const period = periods.find(p => p.value === filters.period);
    return period?.label || 'Todo el tiempo';
  };

  // Función para generar datos completos del gráfico (rellena días sin datos con 0)
  const getChartData = () => {
    if (!selectedMemorial?.daily_visits) return [];
    
    const visits = selectedMemorial.daily_visits;
    if (visits.length === 0) return [];
    
    // Determinar el rango de fechas según el filtro
    let days = 30;
    if (filters.period === 'today') days = 1;
    else if (filters.period === 'week') days = 7;
    else if (filters.period === 'month') days = 30;
    else if (filters.period === 'year') days = 365;
    else if (filters.period === 'custom' && filters.startDate && filters.endDate) {
      const start = new Date(filters.startDate);
      const end = new Date(filters.endDate);
      days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    }
    
    // Para períodos muy largos, limitar las barras
    const maxBars = Math.min(days, 60);
    
    // Crear mapa de visitas por fecha
    const visitMap = {};
    visits.forEach(v => { visitMap[v.date] = v.count; });
    
    // Generar array completo de días
    const result = [];
    const today = new Date();
    
    for (let i = maxBars - 1; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      result.push({
        date: dateStr,
        count: visitMap[dateStr] || 0,
        label: date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
      });
    }
    
    return result;
  };

  const chartData = getChartData();
  const maxVisits = chartData.length > 0 
    ? Math.max(...chartData.map(d => d.count), 1)
    : 1;

  const getChartTitle = () => {
    if (filters.period === 'today') return 'Visitas de hoy';
    if (filters.period === 'week') return 'Visitas últimos 7 días';
    if (filters.period === 'month') return 'Visitas últimos 30 días';
    if (filters.period === 'year') return 'Visitas último año';
    if (filters.period === 'custom') return `Visitas del período`;
    return 'Visitas últimos 30 días';
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

      {/* Barra de Filtros */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            {/* Filtros de Período */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-sm font-medium text-gray-600 mr-2">📅 Período:</span>
              {periods.map((period) => (
                <button
                  key={period.value}
                  onClick={() => handlePeriodChange(period.value)}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
                    filters.period === period.value
                      ? 'bg-indigo-600 text-white shadow-md'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <span className="mr-1">{period.icon}</span>
                  {period.label}
                </button>
              ))}
            </div>

            {/* Fechas Personalizadas */}
            {showCustomDates && (
              <div className="flex flex-wrap items-center gap-3 bg-gray-50 p-3 rounded-lg">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-gray-600">Desde:</label>
                  <input
                    type="date"
                    value={filters.startDate}
                    onChange={(e) => setFilters(prev => ({ ...prev, startDate: e.target.value }))}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <label className="text-sm text-gray-600">Hasta:</label>
                  <input
                    type="date"
                    value={filters.endDate}
                    onChange={(e) => setFilters(prev => ({ ...prev, endDate: e.target.value }))}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
                <button
                  onClick={handleCustomDateApply}
                  disabled={!filters.startDate || !filters.endDate}
                  className="px-4 py-1.5 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  Aplicar
                </button>
              </div>
            )}

            {/* Indicador de Filtro Activo */}
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <span className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full">
                🔍 {getFilterDescription()}
              </span>
            </div>
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
                    {getChartTitle()}
                  </h3>
                  
                  {chartData.length > 0 ? (
                    <div className="space-y-2">
                      {/* Gráfico de Líneas SVG */}
                      <div className="relative h-48">
                        <svg className="w-full h-full" viewBox="0 0 100 50" preserveAspectRatio="none">
                          {/* Líneas de cuadrícula horizontales */}
                          <line x1="0" y1="12.5" x2="100" y2="12.5" stroke="#e5e7eb" strokeWidth="0.2" />
                          <line x1="0" y1="25" x2="100" y2="25" stroke="#e5e7eb" strokeWidth="0.2" />
                          <line x1="0" y1="37.5" x2="100" y2="37.5" stroke="#e5e7eb" strokeWidth="0.2" />
                          
                          {/* Área bajo la línea */}
                          <defs>
                            <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                              <stop offset="0%" stopColor="#818cf8" stopOpacity="0.3" />
                              <stop offset="100%" stopColor="#818cf8" stopOpacity="0.05" />
                            </linearGradient>
                          </defs>
                          <path
                            d={`M 0,50 ${chartData.map((d, i) => {
                              const x = (i / (chartData.length - 1)) * 100;
                              const y = 50 - (d.count / maxVisits) * 45;
                              return `L ${x},${y}`;
                            }).join(' ')} L 100,50 Z`}
                            fill="url(#areaGradient)"
                          />
                          
                          {/* Línea principal */}
                          <path
                            d={chartData.map((d, i) => {
                              const x = (i / (chartData.length - 1)) * 100;
                              const y = 50 - (d.count / maxVisits) * 45;
                              return `${i === 0 ? 'M' : 'L'} ${x},${y}`;
                            }).join(' ')}
                            fill="none"
                            stroke="url(#lineGradient)"
                            strokeWidth="0.8"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          />
                          <defs>
                            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stopColor="#6366f1" />
                              <stop offset="100%" stopColor="#a855f7" />
                            </linearGradient>
                          </defs>
                        </svg>
                        
                        {/* Puntos interactivos */}
                        <div className="absolute inset-0 flex items-end">
                          {chartData.map((day, index) => {
                            const left = (index / (chartData.length - 1)) * 100;
                            const bottom = (day.count / maxVisits) * 90;
                            return (
                              <div
                                key={index}
                                className="absolute group"
                                style={{ 
                                  left: `${left}%`, 
                                  bottom: `${Math.max(bottom, 5)}%`,
                                  transform: 'translateX(-50%)'
                                }}
                              >
                                {day.count > 0 && (
                                  <div className="w-2.5 h-2.5 bg-indigo-500 rounded-full border-2 border-white shadow-md hover:scale-150 transition-transform cursor-pointer" />
                                )}
                                <div className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-20 pointer-events-none">
                                  <div className="font-medium">{day.label}</div>
                                  <div>{day.count} {day.count === 1 ? 'visita' : 'visitas'}</div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                        
                        {/* Eje Y - valores */}
                        <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400 -ml-8 py-1">
                          <span>{maxVisits}</span>
                          <span>{Math.round(maxVisits / 2)}</span>
                          <span>0</span>
                        </div>
                      </div>
                      
                      {/* Leyenda del eje X */}
                      <div className="flex justify-between text-xs text-gray-400 px-1 ml-0">
                        <span>{chartData[0]?.label}</span>
                        <span>{chartData[Math.floor(chartData.length / 2)]?.label}</span>
                        <span>{chartData[chartData.length - 1]?.label}</span>
                      </div>
                      
                      {/* Resumen de datos */}
                      <div className="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between text-sm">
                        <span className="text-gray-500">
                          📈 Total en período: <span className="font-semibold text-indigo-600">{chartData.reduce((sum, d) => sum + d.count, 0)} visitas</span>
                        </span>
                        <span className="text-gray-400">
                          Días con actividad: {chartData.filter(d => d.count > 0).length}/{chartData.length}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="h-48 flex items-center justify-center text-gray-400">
                      <div className="text-center">
                        <div className="text-4xl mb-2">📭</div>
                        <p>Sin datos de visitas en este período</p>
                      </div>
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

                {/* Mapa de Visitantes */}
                <VisitorMap locations={locationStats} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Analytics;
