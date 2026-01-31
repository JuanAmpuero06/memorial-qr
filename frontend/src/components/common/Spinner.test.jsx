import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Spinner from './Spinner';

describe('Spinner', () => {
  it('renders correctly', () => {
    render(<Spinner />);
    
    // El spinner debe estar en el documento
    const spinner = document.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });

  it('has correct styling classes', () => {
    render(<Spinner />);
    
    const spinner = document.querySelector('.animate-spin');
    expect(spinner).toHaveClass('border-4');
    expect(spinner).toHaveClass('rounded-full');
  });

  it('is centered', () => {
    render(<Spinner />);
    
    const container = document.querySelector('.flex');
    expect(container).toHaveClass('justify-center');
    expect(container).toHaveClass('items-center');
  });
});
