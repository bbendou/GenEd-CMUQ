/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import MultiSelectDropdown from '../components/MultiSelectDropdown.js';

describe('MultiSelectDropdown', () => {
  const mockHandleChange = jest.fn();
  const mockClear = jest.fn();
  const options = ['core---humanities'];

  beforeEach(() => {
    mockHandleChange.mockClear();
    mockClear.mockClear();
  });

  test('renders button and toggles dropdown', () => {
    render(
      <MultiSelectDropdown
        major="BA"
        allRequirements={options}
        selectedFilters={{ BA: [] }}
        handleFilterChange={mockHandleChange}
        clearFilters={mockClear}
      />
    );

    const button = screen.getByText(/select/i);
    expect(button).toBeInTheDocument();

    fireEvent.click(button);
    expect(screen.getByText(/clear all/i)).toBeInTheDocument();
  });

  test('calls clearFilters when "CLEAR ALL" is clicked', () => {
    render(
      <MultiSelectDropdown
        major="BA"
        allRequirements={["core---humanities"]}
        selectedFilters={{ BA: ["core---humanities"] }}
        handleFilterChange={mockHandleChange}
        clearFilters={mockClear}
      />
    );
  
    fireEvent.click(screen.getByText(/select/i));
  
    const clearButton = screen.getByText(/clear all/i);
    fireEvent.click(clearButton);
  
    expect(mockClear).toHaveBeenCalledWith("BA");
  });

  test('calls handleFilterChange with all options when "SELECT ALL" is clicked', () => {
    const options = ['core---humanities', 'core---natural-sciences'];
  
    render(
      <MultiSelectDropdown
        major="BA"
        allRequirements={options}
        selectedFilters={{ BA: [] }}
        handleFilterChange={mockHandleChange}
        clearFilters={mockClear}
      />
    );
  
    fireEvent.click(screen.getByText(/select/i)); 
  
    const selectAllButton = screen.getByText(/select all/i);
    fireEvent.click(selectAllButton);
  
    expect(mockHandleChange).toHaveBeenCalledWith("BA", options);
  });

    test('calls handleFilterChange with empty array when "SELECT ALL" is clicked again', () => {
        const options = ['core---humanities', 'core---natural-sciences'];
    
        render(
        <MultiSelectDropdown
            major="BA"
            allRequirements={options}
            selectedFilters={{ BA: options }}
            handleFilterChange={mockHandleChange}
            clearFilters={mockClear}
        />
        );
    
        fireEvent.click(screen.getByText(/select/i)); 
    
        const selectAllButton = screen.getByText(/select all/i);
        fireEvent.click(selectAllButton);
    
        expect(mockHandleChange).toHaveBeenCalledWith("BA", []);
    });
  
});
