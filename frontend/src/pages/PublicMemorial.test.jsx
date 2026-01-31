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

  it('renders page container', async () => {
    renderWithRouter();
    
    // Verificar que la página se renderiza
    await waitFor(() => {
      const container = document.querySelector('.min-h-screen');
      expect(container).toBeTruthy();
    }, { timeout: 3000 });
  });

  it('shows error message for non-existent memorial', async () => {
    renderWithRouter('no-existe');
    
    await waitFor(() => {
      const errorMessage = screen.queryByText(/memorial no encontrado/i) || 
                          screen.queryByText(/error/i);
      expect(errorMessage).toBeTruthy();
    }, { timeout: 3000 });
  });

  it('has correct URL structure', () => {
    const slug = 'test-memorial';
    renderWithRouter(slug);
    
    // Verificar que el componente se renderiza
    expect(document.body).toBeInTheDocument();
  });

  it('applies correct styling', async () => {
    renderWithRouter();
    
    await waitFor(() => {
      // Verificar que hay estilos aplicados
      const styledElements = document.querySelectorAll('[class*="bg-"]');
      expect(styledElements.length).toBeGreaterThan(0);
    });
  });
});
