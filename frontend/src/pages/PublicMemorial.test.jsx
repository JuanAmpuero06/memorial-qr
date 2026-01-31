import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { server } from '../test/mocks/server';
import PublicMemorial from './PublicMemorial';

// Configurar MSW
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Wrapper con Router y parámetros
const renderWithRouter = (slug = 'juan-perez-abc123') => {
  return render(
    <MemoryRouter initialEntries={[`/memorial/${slug}`]}>
      <Routes>
        <Route path="/memorial/:slug" element={<PublicMemorial />} />
      </Routes>
    </MemoryRouter>
  );
};

describe('PublicMemorial Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem.mockReturnValue('test_visitor_id');
  });

  it('shows loading spinner initially', () => {
    renderWithRouter();
    
    const spinner = document.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it('displays memorial information', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    });
    
    expect(screen.getByText(/siempre en nuestros corazones/i)).toBeInTheDocument();
  });

  it('displays birth and death dates', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    });
    
    // Las fechas deben mostrarse
    expect(screen.getByText(/1950/)).toBeInTheDocument();
    expect(screen.getByText(/2024/)).toBeInTheDocument();
  });

  it('displays calculated age', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    });
    
    // La edad calculada (73 años)
    expect(screen.getByText(/73 años/i)).toBeInTheDocument();
  });

  it('shows error message for non-existent memorial', async () => {
    renderWithRouter('no-existe');
    
    await waitFor(() => {
      expect(screen.getByText(/memorial no encontrado/i)).toBeInTheDocument();
    });
  });

  it('displays reaction buttons', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    });
    
    // Los botones de reacción deben estar presentes
    expect(screen.getByText('🕯️')).toBeInTheDocument();
    expect(screen.getByText('🌸')).toBeInTheDocument();
    expect(screen.getByText('❤️')).toBeInTheDocument();
    expect(screen.getByText('🙏')).toBeInTheDocument();
    expect(screen.getByText('🕊️')).toBeInTheDocument();
  });

  it('displays reaction counts', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      expect(screen.getByText('Juan Pérez')).toBeInTheDocument();
    });
    
    // Los conteos de reacciones
    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument(); // candles
      expect(screen.getByText('10')).toBeInTheDocument(); // hearts
    });
  });
});
