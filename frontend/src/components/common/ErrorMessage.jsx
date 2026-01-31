import React from 'react';

function ErrorMessage({ message }) {
  return (
    <div className="text-center mt-12 text-red-600 p-4 bg-red-100 border border-red-300 rounded-lg max-w-md mx-auto">
      <strong>Error:</strong> {message || 'Ha ocurrido un error inesperado.'}
    </div>
  );
}

export default ErrorMessage;