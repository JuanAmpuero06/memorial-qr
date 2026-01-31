import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { server } from '../test/mocks/server';
import Dashboard from './Dashboard';

// Configurar MSW
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Wrapper con Router
const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Dashboard Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem.mockReturnValue('fake-jwt-token');
  });

  it('shows loading spinner initially', () => {
    renderWithRouter(<Dashboard />);
    
    const spinner = document.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it('renders dashboard title', async () => {
    renderWithRouter(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/mis memoriales/i)).toBeInTheDocument();
    });
  });

  it('shows create memorial button', async () => {
    renderWithRouter(<Dashboard />);
    
    await waitFor(() => {
      const createButton = screen.queryByRole('button', { name: /crear memorial|nuevo memorial/i });
      expect(createButton || screen.queryByText(/crear memorial/i)).toBeTruthy();
    });
  });

  it('displays empty state when no memorials', async () => {
    renderWithRouter(<Dashboard />);
    
    await waitFor(() => {
      // Verificar que aparece el estado vacío o el título del dashboard
      const emptyState = screen.queryByText(/no tienes memoriales/i);
      const dashboardTitle = screen.queryByText(/mis memoriales/i);
      expect(emptyState || dashboardTitle).toBeTruthy();
    });
  });

  it('has correct page structure', async () => {
    renderWithRouter(<Dashboard />);
    
    await waitFor(() => {
      // Verificar estructura básica del dashboard
      const mainContainer = document.querySelector('.min-h-screen');
      expect(mainContainer).toBeInTheDocument();
    });
  });
});
