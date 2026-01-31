import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ErrorMessage from './ErrorMessage';

describe('ErrorMessage', () => {
  it('renders with provided message', () => {
    render(<ErrorMessage message="Test error message" />);
    
    expect(screen.getByText(/Test error message/i)).toBeInTheDocument();
    expect(screen.getByText(/Error:/i)).toBeInTheDocument();
  });

  it('renders default message when no message provided', () => {
    render(<ErrorMessage />);
    
    expect(screen.getByText(/Ha ocurrido un error inesperado/i)).toBeInTheDocument();
  });

  it('has correct error styling', () => {
    render(<ErrorMessage message="Error" />);
    
    const container = document.querySelector('.text-red-600');
    expect(container).toBeInTheDocument();
    expect(container).toHaveClass('bg-red-100');
    expect(container).toHaveClass('border-red-300');
  });

  it('has strong label for error', () => {
    render(<ErrorMessage message="Test" />);
    
    const strongElement = screen.getByText('Error:');
    expect(strongElement.tagName).toBe('STRONG');
  });
});
