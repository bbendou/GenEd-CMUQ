/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import CourseTablePage from '../components/CourseTablePage';
import '@testing-library/jest-dom';

// Mock localStorage
beforeEach(() => {
  const store = {};
  jest.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => store[key] || null);
  jest.spyOn(Storage.prototype, 'setItem').mockImplementation((key, value) => {
    store[key] = value;
  });
});

afterEach(() => {
  localStorage.clear();
  jest.clearAllMocks();
  cleanup();
});

// Mock fetch
beforeAll(() => {
  global.fetch = jest.fn((url) => {
    if (url.includes('/departments')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ departments: [] }),
      });
    }

    if (url.includes('/requirements')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          requirements: [
            {
              requirement: 'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
              type: false,
              major: 'is'
            },
            {
              requirement: 'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
              type: true,
              major: 'cs'
            },
          ]
        }),
      });
    }

    if (url.includes('/courses/search')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          courses: [
            {
              course_code: '76-101',
              course_name: 'Interpretation & Argument',
              offered: ['F23'],
              prerequisites: '[76-100]',
              requirements: {
                IS: [{
                  requirement: 'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
                  type: false
                }],
                CS: [{
                  requirement: 'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
                  type: true
                }]
              }
            }
          ]
        }),
      });
    }

    if (url.includes('/courses/semesters')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ semesters: ['F23', 'S24'] }),
      });
    }

    return Promise.reject(new Error('Unknown endpoint: ' + url));
  });
});

afterAll(() => {
  global.fetch.mockRestore();
});

describe('CourseTablePage', () => {
  test('renders title and loading spinner initially', async () => {
    render(<CourseTablePage />);
    expect(screen.getByText(/CMU-Q Curriculum Requirements/i)).toBeInTheDocument();
    expect(screen.getByText(/Visualize, plan/i)).toBeInTheDocument();
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  test('loads course table after data is fetched', async () => {
    render(<CourseTablePage />);
    await waitFor(() => {
      expect(screen.getByText(/76-101/)).toBeInTheDocument();
    });

    expect(screen.getByText(/Interpretation & Argument/)).toBeInTheDocument();
  });

  test('adds course to plan and shows toast', async () => {
    render(<CourseTablePage />);
    await screen.findByText(/76-101/);

    const addAllBtn = screen.getByText(/Add All to Plan/);
    fireEvent.click(addAllBtn);

    await waitFor(() => {
      expect(screen.getByText(/added to Plan/i)).toBeInTheDocument();
    });
  });

  test('opens and cancels Clear All Filters popup', async () => {
    render(<CourseTablePage />);
    await screen.findByText(/76-101/);

    // Simulate filter input to enable the button
    const input = screen.getByPlaceholderText(/specific course number/i);
    fireEvent.change(input, { target: { value: '76-101' } });

    const clearBtn = screen.getByText(/Clear All Filters/i);
    fireEvent.click(clearBtn);

    expect(
      screen.getByText(/are you sure you want to clear all filters/i)
    ).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Cancel/i));
    expect(screen.getByText(/Clear All Filters/i)).toBeInTheDocument();
  });
});
