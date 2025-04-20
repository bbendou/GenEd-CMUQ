/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PlanCourseTab from '../components/PlanCourseTab';
import '@testing-library/jest-dom';

beforeEach(() => {
  const store = {};
  jest.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => store[key] || null);
  jest.spyOn(Storage.prototype, 'setItem').mockImplementation((key, value) => {
    store[key] = value;
  });
});

beforeAll(() => {
  global.fetch = jest.fn((url) => {
    if (url.includes('/requirements')) {
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            requirements: [
              {
                requirement:
                  'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
                type: false,
                major: 'is',
              },
              {
                requirement:
                  'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
                type: true,
                major: 'cs',
              },
            ],
          }),
      });
    }

    if (url.includes('/courses/search?searchQuery=76-101')) {
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            courses: [
              {
                course_code: '76-101',
                course_name: 'Interpretation & Argument',
              },
            ],
          }),
      });
    }

    if (url.includes('/courses/76-101')) {
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            course_code: '76-101',
            course_name: 'Interpretation & Argument',
            offered: ['F23', 'S24'],
            prerequisites: '[76-100]',
            requirements: {
              IS: [
                {
                  requirement:
                    'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
                  type: false,
                },
              ],
              CS: [
                {
                  requirement:
                    'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
                  type: true,
                },
              ],
            },
          }),
      });
    }

    return Promise.reject(new Error('Unknown endpoint: ' + url));
  });
});

afterAll(() => {
  global.fetch.mockRestore();
});

describe('PlanCourseTab', () => {
  test('renders title and subtitle', () => {
    render(<PlanCourseTab />);
    expect(screen.getByText(/Plan Courses/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Add courses from the main table or search/i)
    ).toBeInTheDocument();
  });

  test('searches and adds a course to the plan', async () => {
    render(<PlanCourseTab />);
    const input = screen.getByPlaceholderText(/search by course code/i);
    const searchBtn = screen.getByRole('button', { name: /🔍/i });
  
    fireEvent.change(input, { target: { value: '76-101' } });
    fireEvent.click(searchBtn);
  
    await waitFor(() => {
      expect(
        screen.getByText((content, element) =>
          element?.textContent?.includes('76-101')
        )
      ).toBeInTheDocument();
    });
  
    const addBtn = screen.getByRole('button', { name: /\+ Add/i });
    fireEvent.click(addBtn);
  
    await waitFor(() => {
      expect(screen.getByText(/Course added! 🎉/i)).toBeInTheDocument();
    });
  });
  
  test('prevents duplicate addition', async () => {
    render(<PlanCourseTab />);
    const input = screen.getByPlaceholderText(/search by course code/i);
    const searchBtn = screen.getByRole('button', { name: /🔍/i });
  
    fireEvent.change(input, { target: { value: '76-101' } });
    fireEvent.click(searchBtn);
  
    await waitFor(() => {
      expect(
        screen.getByText((content, element) =>
          element?.textContent?.includes('76-101')
        )
      ).toBeInTheDocument();
    });
  
    const addBtn = screen.getByRole('button', { name: /\+ Add/i });
    fireEvent.click(addBtn);
  
    await waitFor(() => {
      expect(screen.getByText(/Course added!/i)).toBeInTheDocument();
    });
  
    fireEvent.click(screen.getByRole('button', { name: /Added/i }));
  
    await waitFor(() => {
      expect(screen.getByText(/Course already added!/i)).toBeInTheDocument();
    });
  });
  
  test('clears all courses when confirmed', async () => {
    window.confirm = jest.fn(() => true);
  
    render(<PlanCourseTab />);
    const input = screen.getByPlaceholderText(/search by course code/i);
    const searchBtn = screen.getByRole('button', { name: /🔍/i });
  
    fireEvent.change(input, { target: { value: '76-101' } });
    fireEvent.click(searchBtn);
  
    await waitFor(() => {
      expect(
        screen.getByText((content, element) =>
          element?.textContent?.includes('76-101')
        )
      ).toBeInTheDocument();
    });
  
    const addBtn = screen.getByRole('button', { name: /\+ Add/i });
    fireEvent.click(addBtn);
  
    await waitFor(() => {
      expect(screen.getByText(/Course added!/i)).toBeInTheDocument();
    });
  
    const table = await screen.findByRole('table');
    expect(table).toBeInTheDocument();
  
    fireEvent.click(screen.getByText(/Clear All/i));
  
    await waitFor(() => {
      expect(screen.getByText(/No planned courses yet/i)).toBeInTheDocument();
    });
  });
  

});