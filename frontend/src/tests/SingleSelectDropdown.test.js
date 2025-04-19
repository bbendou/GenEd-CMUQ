/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SingleSelectDropdown from '../components/SingleSelectDropdown.js';

describe('SingleSelectDropdown', () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    mockOnChange.mockClear();
  });

  const options = ['all', 'with', 'without'];

  test('renders dropdown and toggles open', () => {
    render(
      <SingleSelectDropdown options={options} selected={null} onChange={mockOnChange} />
    );

    const button = screen.getByText(/select/i);
    expect(button).toBeInTheDocument();

    fireEvent.click(button);
    expect(screen.getByText(/All Courses/)).toBeInTheDocument();
    expect(screen.getByText(/Has Pre-reqs/)).toBeInTheDocument();
    expect(screen.getByText(/No Pre-reqs/)).toBeInTheDocument();
  });

  test('checkbox reflects the selected option', () => {
    render(
      <SingleSelectDropdown options={options} selected={'with'} onChange={mockOnChange} />
    );

    fireEvent.click(screen.getByText(/select/i));

    const checkedBox = screen.getByLabelText(/Has Pre-reqs/);
    expect(checkedBox).toBeChecked();

    const uncheckedBox = screen.getByLabelText(/No Pre-reqs/);
    expect(uncheckedBox).not.toBeChecked();
  });

  test('calls onChange and closes dropdown when option is selected', () => {
    render(
      <SingleSelectDropdown options={options} selected={null} onChange={mockOnChange} />
    );
  
    fireEvent.click(screen.getByText(/select/i)); 
    const option = screen.getByLabelText(/No Pre-reqs/);
    fireEvent.click(option);
  
    expect(mockOnChange).toHaveBeenCalledWith('without');
  
    expect(screen.queryByText(/No Pre-reqs/)).toBeNull();
  });
  

  test('closes dropdown when clicking outside', () => {
    render(
      <>
        <SingleSelectDropdown options={options} selected={null} onChange={mockOnChange} />
        <div data-testid="outside-element">Outside</div>
      </>
    );
  
    fireEvent.click(screen.getByText(/select/i)); // open dropdown
    expect(screen.getByText(/All Courses/)).toBeInTheDocument();
  
    fireEvent.mouseDown(screen.getByTestId('outside-element'));
  
    expect(screen.queryByText(/All Courses/)).toBeNull();
  });
  
});
