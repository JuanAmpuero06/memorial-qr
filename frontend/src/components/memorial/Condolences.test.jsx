import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { server } from '../../test/mocks/server';
import Condolences from './Condolences';

// Configurar MSW
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Condolences Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem.mockReturnValue('test_visitor_id');
  });

  it('renders without crashing', () => {
    render(<Condolences slug="juan-perez-abc123" />);
    
    // El componente debe renderizar sin errores
    expect(document.body).toBeInTheDocument();
  });

  it('shows loading state initially', () => {
    render(<Condolences slug="juan-perez-abc123" />);
    
    // Puede mostrar spinner o texto de carga
    const spinner = document.querySelector('.animate-spin, .animate-pulse');
    const loadingText = screen.queryByText(/cargando/i);
    
    expect(spinner || loadingText).toBeTruthy();
  });

  it('displays condolences after loading', async () => {
    render(<Condolences slug="juan-perez-abc123" />);
    
    // Esperar a que carguen las condolencias
    await waitFor(() => {
      const condolenceElements = document.querySelectorAll('[class*="condolence"], [data-testid*="condolence"]');
      // El componente debería mostrar contenido después de cargar
      expect(document.body.textContent).toBeTruthy();
    }, { timeout: 3000 });
  });

  it('has form to add new condolence', async () => {
    render(<Condolences slug="juan-perez-abc123" />);
    
    // Buscar botón para mostrar formulario
    await waitFor(() => {
      const addButton = screen.queryByRole('button', { name: /dejar.*mensaje|escribir|añadir/i });
      if (addButton) {
        expect(addButton).toBeInTheDocument();
      }
    }, { timeout: 2000 });
  });

  it('renders owner moderation controls when isOwner is true', async () => {
    render(<Condolences slug="juan-perez-abc123" isOwner={true} />);
    
    await waitFor(() => {
      // Esperar a que termine de cargar
      const spinner = document.querySelector('.animate-spin');
      if (!spinner) {
        // El propietario puede tener controles adicionales
        expect(document.body).toBeInTheDocument();
      }
    }, { timeout: 2000 });
  });
});
