import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import Spinner from '../components/common/Spinner.jsx';
import ErrorMessage from '../components/common/ErrorMessage.jsx';

function PublicMemorial() {
  const { slug } = useParams();
  const [memorial, setMemorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
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

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message="Memorial no encontrado." />;

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 py-12 px-4">
      {/* Partículas decorativas */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-2 h-2 bg-amber-400 rounded-full animate-pulse opacity-60"></div>
        <div className="absolute top-40 right-20 w-1 h-1 bg-amber-300 rounded-full animate-pulse opacity-40"></div>
        <div className="absolute bottom-40 left-1/4 w-1.5 h-1.5 bg-amber-200 rounded-full animate-pulse opacity-50"></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-amber-400 rounded-full animate-pulse opacity-30"></div>
        <div className="absolute bottom-20 right-10 w-2 h-2 bg-amber-300 rounded-full animate-pulse opacity-40"></div>
      </div>

      <div className="max-w-2xl mx-auto relative">
        {/* Card principal */}
        <div className="bg-gradient-to-b from-slate-800/80 to-slate-900/80 backdrop-blur-sm rounded-3xl shadow-2xl overflow-hidden border border-slate-700/50">
          
          {/* Header con imagen */}
          <div className="relative">
            <div className="h-32 bg-gradient-to-r from-amber-600/20 via-amber-500/30 to-amber-600/20"></div>
            
            {/* Foto del difunto */}
            <div className="absolute -bottom-16 left-1/2 -translate-x-1/2">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-amber-400 to-amber-600 rounded-full blur-lg opacity-50 animate-pulse"></div>
                {memorial.image_filename ? (
                  <img 
                    src={memorial.image_filename} 
                    alt={memorial.name}
                    className="relative w-32 h-32 object-cover rounded-full border-4 border-slate-800 shadow-2xl"
                  />
                ) : (
                  <div className="relative w-32 h-32 bg-gradient-to-br from-slate-700 to-slate-800 rounded-full border-4 border-slate-700 shadow-2xl flex items-center justify-center">
                    <svg className="w-16 h-16 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Contenido */}
          <div className="pt-20 pb-10 px-8 text-center">
            {/* Nombre */}
            <h1 className="text-3xl sm:text-4xl font-serif text-amber-100 mb-2">
              {memorial.name}
            </h1>

            {/* Fechas */}
            {(memorial.birth_date || memorial.death_date) && (
              <p className="text-amber-400/80 text-sm font-medium tracking-wider mb-4">
                {memorial.birth_date && new Date(memorial.birth_date).getFullYear()}
                {memorial.birth_date && memorial.death_date && ' — '}
                {memorial.death_date && new Date(memorial.death_date).getFullYear()}
              </p>
            )}

            {/* Decorador */}
            <div className="flex items-center justify-center gap-4 my-6">
              <div className="h-px w-16 bg-gradient-to-r from-transparent to-amber-500/50"></div>
              <svg className="w-5 h-5 text-amber-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L9.19 8.63L2 9.24L7.46 13.97L5.82 21L12 17.27L18.18 21L16.54 13.97L22 9.24L14.81 8.63L12 2Z"/>
              </svg>
              <div className="h-px w-16 bg-gradient-to-l from-transparent to-amber-500/50"></div>
            </div>

            {/* Epitafio */}
            {memorial.epitaph && (
              <blockquote className="text-xl sm:text-2xl font-serif italic text-slate-300 mb-8 leading-relaxed">
                "{memorial.epitaph}"
              </blockquote>
            )}

            {/* Biografía */}
            {memorial.bio && (
              <div className="mt-8 p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
                <h3 className="text-amber-400 font-semibold text-sm uppercase tracking-wider mb-4">
                  En su memoria
                </h3>
                <p className="text-slate-300 leading-relaxed text-justify whitespace-pre-line">
                  {memorial.bio}
                </p>
              </div>
            )}

            {/* Vela animada */}
            <div className="mt-10 flex justify-center">
              <div className="relative group cursor-pointer">
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-3 h-6 bg-gradient-to-t from-amber-500 via-amber-400 to-yellow-300 rounded-full blur-sm animate-flicker"></div>
                <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-2 h-5 bg-gradient-to-t from-amber-400 to-yellow-200 rounded-full animate-flicker"></div>
                <div className="w-8 h-16 bg-gradient-to-b from-amber-100 to-amber-200 rounded-lg shadow-lg"></div>
                <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-10 h-2 bg-amber-800 rounded-full"></div>
              </div>
            </div>

            {/* Mensaje de condolencia */}
            <p className="mt-8 text-slate-500 text-sm">
              Encendemos esta vela en su memoria
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-full border border-slate-700/50">
            <svg className="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L9.19 8.63L2 9.24L7.46 13.97L5.82 21L12 17.27L18.18 21L16.54 13.97L22 9.24L14.81 8.63L12 2Z"/>
            </svg>
            <span className="text-slate-400 text-xs font-medium">Memorial QR</span>
          </div>
        </div>
      </div>

      {/* Estilos CSS para animaciones */}
      <style>{`
        @keyframes flicker {
          0%, 100% {
            opacity: 1;
            transform: translateX(-50%) scale(1);
          }
          25% {
            opacity: 0.9;
            transform: translateX(-50%) scale(1.02) rotate(-1deg);
          }
          50% {
            opacity: 1;
            transform: translateX(-50%) scale(0.98);
          }
          75% {
            opacity: 0.95;
            transform: translateX(-50%) scale(1.01) rotate(1deg);
          }
        }
        
        .animate-flicker {
          animation: flicker 2s infinite ease-in-out;
        }
      `}</style>
    </div>
  );
}

export default PublicMemorial;