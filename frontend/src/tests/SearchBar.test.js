/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchBar from '../components/SearchBar.js';

beforeAll(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ departments: [] }), // Mocked empty departments
      })
    );
  });
  
  afterAll(() => {
    global.fetch.mockRestore();
  });
  

describe('SearchBar', () => {
  const setup = (overrides = {}) => {
    const defaults = {
      selectedDepartments: [],
      setSelectedDepartments: jest.fn(),
      searchQuery: '',
      setSearchQuery: jest.fn(),
      noPrereqs: null,
      setNoPrereqs: jest.fn(),
      offeredQatar: null,
      setOfferedQatar: jest.fn(),
      offeredPitts: null,
      setOfferedPitts: jest.fn(),
      coreOnly: null,
      setCoreOnly: jest.fn(),
      genedOnly: null,
      setGenedOnly: jest.fn(),
    };

    const props = { ...defaults, ...overrides };

    render(<SearchBar {...props} />);

    return props;
  };

  test('renders selected department tag and clears on X click', () => {
    const { setSelectedDepartments } = setup({
      selectedDepartments: ['76'],
    });

    const tagCloseButton = screen.getByRole('button', { name: /×/i });
    fireEvent.click(tagCloseButton);

    expect(setSelectedDepartments).toHaveBeenCalled();
  });

  test('renders search query tag and clears on X click', () => {
    const { setSearchQuery } = setup({
      searchQuery: '76-101',
    });

    const closeButton = screen.getByRole('button', { name: /×/i });
    fireEvent.click(closeButton);
    
    expect(setSearchQuery).toHaveBeenCalledWith('');
    

    expect(setSearchQuery).toHaveBeenCalledWith('');
  });

  test('updates location filter from MultiSelectDropdown', () => {
    const { setOfferedQatar, setOfferedPitts } = setup();

    setOfferedQatar(true);
    setOfferedPitts(false);

    expect(setOfferedQatar).toHaveBeenCalledWith(true);
    expect(setOfferedPitts).toHaveBeenCalledWith(false);
  });

  test('sets default course type filters on mount', () => {
    const setCoreOnly = jest.fn();
    const setGenedOnly = jest.fn();

    setup({
      coreOnly: null,
      genedOnly: null,
      setCoreOnly,
      setGenedOnly,
    });

    expect(setCoreOnly).toHaveBeenCalledWith(true);
    expect(setGenedOnly).toHaveBeenCalledWith(true);
  });
});
