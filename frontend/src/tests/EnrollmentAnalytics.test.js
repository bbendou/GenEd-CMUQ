/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import EnrollmentAnalytics from '../components/Analytics';
import '@testing-library/jest-dom';

// Patch for process.env
const API_BASE_URL = 'http://localhost';

jest.mock('react-plotly.js', () => (props) => (
  <div data-testid="mock-plot">
    Plotly Graph: {props.layout?.title}
  </div>
));

beforeAll(() => {
  global.fetch = jest.fn((url) => {
    const expectedUrl = `${API_BASE_URL}/analytics/enrollment-data?course_code=76-101`;

    if (url === expectedUrl) {
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            enrollment_data: [
              { semester: 'F22', enrollment_count: 25, class_: 1 },
              { semester: 'S23', enrollment_count: 30, class_: 2 },
            ],
          }),
      });
    }

    return Promise.reject(new Error(`Unexpected URL: ${url}`));
  });
});

afterAll(() => {
  global.fetch.mockRestore();
});

describe('EnrollmentAnalytics', () => {
  test('renders input fields and buttons', () => {
    render(<EnrollmentAnalytics />);
    expect(screen.getAllByPlaceholderText(/enter course code/i)).toHaveLength(2);
    expect(screen.getByText(/add course/i)).toBeInTheDocument();
    expect(screen.getByText(/load course/i)).toBeInTheDocument();
  });
});
