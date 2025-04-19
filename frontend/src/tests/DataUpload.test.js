/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DataUpload from '../components/DataUpload';
import '@testing-library/jest-dom';

// Mock global fetch
beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ message: 'Success' }),
    })
  );
});

afterEach(() => {
  jest.clearAllMocks();
});

describe('DataUpload Component', () => {
  test('renders key elements and upload button disabled initially', () => {
    render(<DataUpload />);

    expect(screen.getByText(/Database Data Upload/i)).toBeInTheDocument();
    expect(screen.getByText(/Select Course ZIP Files/i)).toBeInTheDocument();
    expect(screen.getByText(/Upload Data/i)).toBeDisabled();
  });

  test('shows error when uploading invalid department file', async () => {
    render(<DataUpload />);
    const file = new File(['bad content'], 'departments.txt', { type: 'text/plain' });

    const input = screen.getByLabelText(/Select Department CSV File/i);
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/Department file must be a CSV file/i)).toBeInTheDocument();
    });
  });
});