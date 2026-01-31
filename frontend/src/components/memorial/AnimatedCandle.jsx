import { useState, useEffect } from 'react';

/**
 * Componente de Vela Virtual Animada
 * Una vela realista con animaciones de llama y resplandor
 */
function AnimatedCandle({ isLit = true, size = 'medium', onClick }) {
  const [flameIntensity, setFlameIntensity] = useState(1);
  
  // Variación aleatoria de la llama
  useEffect(() => {
    if (!isLit) return;
    
    const interval = setInterval(() => {
      setFlameIntensity(0.8 + Math.random() * 0.4);
    }, 100);
    
    return () => clearInterval(interval);
  }, [isLit]);
  
  const sizes = {
    small: { candle: 'w-6 h-12', flame: 'w-2 h-4', glow: 'w-8 h-8' },
    medium: { candle: 'w-8 h-16', flame: 'w-3 h-6', glow: 'w-12 h-12' },
    large: { candle: 'w-10 h-20', flame: 'w-4 h-8', glow: 'w-16 h-16' }
  };
  
  const currentSize = sizes[size] || sizes.medium;
  
  return (
    <div 
      className="relative group cursor-pointer transition-transform hover:scale-105"
      onClick={onClick}
      role="button"
      aria-label={isLit ? "Vela encendida" : "Encender vela"}
    >
      {/* Resplandor exterior */}
      {isLit && (
        <div 
          className={`absolute -top-10 left-1/2 -translate-x-1/2 ${currentSize.glow} bg-gradient-radial from-amber-400/40 via-amber-500/20 to-transparent rounded-full blur-xl animate-pulse`}
          style={{ opacity: flameIntensity * 0.6 }}
        />
      )}
      
      {/* Llama exterior (resplandor) */}
      {isLit && (
        <div 
          className={`absolute -top-8 left-1/2 -translate-x-1/2 ${currentSize.flame} bg-gradient-to-t from-amber-500 via-amber-400 to-yellow-300 rounded-full blur-sm`}
          style={{ 
            transform: `translateX(-50%) scale(${flameIntensity})`,
            opacity: 0.8 
          }}
        />
      )}
      
      {/* Llama interior */}
      {isLit && (
        <div 
          className={`absolute -top-7 left-1/2 -translate-x-1/2 w-2 h-5 bg-gradient-to-t from-amber-400 via-yellow-300 to-white rounded-full`}
          style={{ 
            transform: `translateX(-50%) scaleX(${0.8 + flameIntensity * 0.2}) scaleY(${flameIntensity})`,
          }}
        />
      )}
      
      {/* Mecha */}
      <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0.5 h-2 bg-gray-800 rounded-full" />
      
      {/* Vela (cuerpo) */}
      <div className={`${currentSize.candle} bg-gradient-to-b from-amber-50 via-amber-100 to-amber-200 rounded-lg shadow-lg relative overflow-hidden`}>
        {/* Efecto de cera derretida */}
        <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-b from-amber-200 to-transparent" />
        
        {/* Textura de la vela */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent" />
        
        {/* Gotas de cera */}
        {isLit && (
          <>
            <div className="absolute top-1 left-1 w-1 h-2 bg-amber-200/80 rounded-full animate-drip" />
            <div className="absolute top-2 right-1 w-0.5 h-1.5 bg-amber-100/60 rounded-full animate-drip-slow" />
          </>
        )}
      </div>
      
      {/* Base de la vela */}
      <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-10 h-2 bg-amber-800 rounded-full shadow-md" />
      
      {/* Reflejo de luz en la superficie */}
      {isLit && (
        <div 
          className="absolute -bottom-3 left-1/2 -translate-x-1/2 w-16 h-4 bg-gradient-to-t from-amber-400/20 to-transparent rounded-full blur-md"
          style={{ opacity: flameIntensity * 0.4 }}
        />
      )}
      
      {/* Animaciones CSS personalizadas */}
      <style>{`
        @keyframes drip {
          0%, 100% { transform: translateY(0); opacity: 0.8; }
          50% { transform: translateY(2px); opacity: 0.6; }
        }
        
        @keyframes drip-slow {
          0%, 100% { transform: translateY(0); opacity: 0.6; }
          50% { transform: translateY(3px); opacity: 0.4; }
        }
        
        .animate-drip {
          animation: drip 3s ease-in-out infinite;
        }
        
        .animate-drip-slow {
          animation: drip-slow 4s ease-in-out infinite 0.5s;
        }
      `}</style>
    </div>
  );
}

export default AnimatedCandle;
