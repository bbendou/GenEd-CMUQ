/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen} from '@testing-library/react';
import CategoryCoverage from '../components/CategoryCoverage';
import '@testing-library/jest-dom';

// Mock Plotly
jest.mock('react-plotly.js', () => () => <div data-testid="mock-plot" />);

const mockMajors = {
  is: 'Information Systems',
  ba: 'Business Administration',
  cs: 'Computer Science',
  bio: 'Biological Sciences'
};

describe('CategoryCoverage', () => {
  beforeEach(() => {
    global.fetch = jest.fn((url) => {
      if (url.includes('/courses/semesters')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ semesters: ['F23', 'S23'] }),
        });
      }
      if (url.includes('/analytics/course-coverage')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            coverage: [
              { requirement: 'GenEd---Science---Lab', num_courses: 2 },
              { requirement: 'GenEd---Math---Calculus', num_courses: 3 }
            ]
          }),
        });
      }
      return Promise.reject(new Error('Unknown API'));
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders Plotly graph if data is available', async () => {
    render(
      <CategoryCoverage
        selectedMajor="cs"
        setSelectedMajor={() => {}}
        majors={mockMajors}
      />
    );

    const plot = await screen.findByTestId('mock-plot');
    expect(plot).toBeInTheDocument();
  });
});
