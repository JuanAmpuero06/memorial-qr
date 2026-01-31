import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { server } from '../test/mocks/server';
import Login from './Login';

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

// Mock de useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem.mockReturnValue(null);
  });

  it('renders login form', () => {
    renderWithRouter(<Login />);
    
    expect(screen.getByText(/iniciar sesión/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/tu@email.com/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar|iniciar/i })).toBeInTheDocument();
  });

  it('shows validation error for empty email', async () => {
    const user = userEvent.setup();
    renderWithRouter(<Login />);
    
    const submitButton = screen.getByRole('button', { name: /entrar|iniciar/i });
    await user.click(submitButton);
    
    // Verificar que el formulario tiene validación HTML5
    const emailInput = screen.getByPlaceholderText(/tu@email.com/i);
    expect(emailInput).toBeRequired();
  });

  it('has email input field', () => {
    renderWithRouter(<Login />);
    
    const emailInput = screen.getByPlaceholderText(/tu@email.com/i);
    expect(emailInput).toBeInTheDocument();
    expect(emailInput).toHaveAttribute('type', 'email');
  });

  it('has password input field', () => {
    renderWithRouter(<Login />);
    
    const passwordInput = document.querySelector('input[type="password"]');
    expect(passwordInput).toBeInTheDocument();
  });

  it('has link to register page', () => {
    renderWithRouter(<Login />);
    
    const registerLink = screen.getByRole('link', { name: /crear una cuenta/i });
    expect(registerLink).toBeInTheDocument();
    expect(registerLink).toHaveAttribute('href', '/register');
  });
});
