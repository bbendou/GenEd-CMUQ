/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SelectedFilters from '../components/SelectedFilters.js';

describe('SelectedFilters', () => {
  const mockHandleFilterChange = jest.fn();
  const mockRemoveOfferedSemester = jest.fn();

  beforeEach(() => {
    mockHandleFilterChange.mockClear();
    mockRemoveOfferedSemester.mockClear();
  });

  test('renders offered semesters and calls removeOfferedSemester on click', () => {
    render(
      <SelectedFilters
        selectedFilters={{ BA: [], BS: [], CS: [], IS: [] }}
        selectedOfferedSemesters={['F23', 'S24']}
        handleFilterChange={mockHandleFilterChange}
        removeOfferedSemester={mockRemoveOfferedSemester}
      />
    );

    expect(screen.getByText('F23')).toBeInTheDocument();
    expect(screen.getByText('S24')).toBeInTheDocument();

    const closeBtn = screen.getAllByRole('button')[0];
    fireEvent.click(closeBtn);

    expect(mockRemoveOfferedSemester).toHaveBeenCalledWith('F23');
  });
  test('returns null when there are no selected filters or semesters', () => {
    render(
      <SelectedFilters
        selectedFilters={{ BA: [], BS: [], CS: [], IS: [] }}
        selectedOfferedSemesters={[]}
        handleFilterChange={mockHandleFilterChange}
        removeOfferedSemester={mockRemoveOfferedSemester}
      />
    );

    expect(screen.queryByTestId('selected-filters')).not.toBeInTheDocument();
  });
});
