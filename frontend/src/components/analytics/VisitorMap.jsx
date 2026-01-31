import { useState, useEffect } from 'react';

/**
 * Componente de Mapa de Visitantes
 * Muestra estadísticas de ubicación de los visitantes
 */
function VisitorMap({ locations = [] }) {
  // Mapeo de códigos de país a banderas emoji
  const countryFlags = {
    'Argentina': '🇦🇷', 'Bolivia': '🇧🇴', 'Brasil': '🇧🇷', 'Chile': '🇨🇱',
    'Colombia': '🇨🇴', 'Costa Rica': '🇨🇷', 'Cuba': '🇨🇺', 'Ecuador': '🇪🇨',
    'El Salvador': '🇸🇻', 'España': '🇪🇸', 'Estados Unidos': '🇺🇸',
    'Guatemala': '🇬🇹', 'Honduras': '🇭🇳', 'México': '🇲🇽', 'Nicaragua': '🇳🇮',
    'Panamá': '🇵🇦', 'Paraguay': '🇵🇾', 'Perú': '🇵🇪', 'Puerto Rico': '🇵🇷',
    'República Dominicana': '🇩🇴', 'Uruguay': '🇺🇾', 'Venezuela': '🇻🇪',
    'United States': '🇺🇸', 'Spain': '🇪🇸', 'Mexico': '🇲🇽', 'Brazil': '🇧🇷',
    'France': '🇫🇷', 'Germany': '🇩🇪', 'Italy': '🇮🇹', 'United Kingdom': '🇬🇧',
    'Canada': '🇨🇦', 'Australia': '🇦🇺', 'Japan': '🇯🇵', 'China': '🇨🇳'
  };

  const getFlag = (country) => countryFlags[country] || '🌍';

  // Agrupar por país
  const countryStats = locations.reduce((acc, loc) => {
    if (!loc.country) return acc;
    if (!acc[loc.country]) {
      acc[loc.country] = { count: 0, cities: {} };
    }
    acc[loc.country].count += loc.count;
    if (loc.city) {
      acc[loc.country].cities[loc.city] = (acc[loc.country].cities[loc.city] || 0) + loc.count;
    }
    return acc;
  }, {});

  const sortedCountries = Object.entries(countryStats)
    .sort(([, a], [, b]) => b.count - a.count);

  const totalVisits = locations.reduce((sum, loc) => sum + loc.count, 0);

  if (locations.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <span className="text-xl">🌍</span>
          Visitantes por Ubicación
        </h3>
        <div className="text-center py-8 text-gray-500">
          <p>Aún no hay datos de ubicación disponibles</p>
          <p className="text-sm mt-2">La geolocalización se activa con visitantes reales</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">
      <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
        <span className="text-xl">🌍</span>
        Visitantes por Ubicación
        <span className="text-sm font-normal text-gray-500">
          ({totalVisits} visitas geolocalizadas)
        </span>
      </h3>

      {/* Mapa visual simplificado (barras) */}
      <div className="space-y-3">
        {sortedCountries.map(([country, data], index) => {
          const percentage = (data.count / totalVisits) * 100;
          const topCities = Object.entries(data.cities)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3);

          return (
            <div key={country} className="group">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{getFlag(country)}</span>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-800">{country}</span>
                    <span className="text-sm text-gray-600">{data.count} visitas</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-500"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              </div>
              
              {/* Ciudades (expandible) */}
              {topCities.length > 0 && (
                <div className="ml-10 mt-2 text-xs text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity">
                  {topCities.map(([city, count]) => (
                    <span key={city} className="inline-block mr-3">
                      📍 {city}: {count}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Resumen */}
      <div className="mt-6 pt-4 border-t border-gray-100 flex items-center justify-between text-sm text-gray-500">
        <span>{sortedCountries.length} países</span>
        <span>{Object.values(countryStats).reduce((sum, c) => sum + Object.keys(c.cities).length, 0)} ciudades</span>
      </div>
    </div>
  );
}

export default VisitorMap;
