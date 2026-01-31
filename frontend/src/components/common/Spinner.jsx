import React from 'react';

function Spinner() {
  return (
    <div className="flex justify-center items-center min-h-[100px] my-5">
      <div className="border-4 border-gray-200 border-t-blue-500 rounded-full w-10 h-10 animate-spin"></div>
    </div>
  );
}

export default Spinner;