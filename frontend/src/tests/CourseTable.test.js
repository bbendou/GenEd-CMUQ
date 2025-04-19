/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CourseTable from '../components/CourseTable.js';

const mockCourses = [
  {
    course_code: '76-101',
    course_name: 'Interpretation & Argument',
    prerequisites: '[76-100, 15-121, 15-122, 15-150, 21-127, 36-200, 36-201]',
    offered: ['F23', 'S24'],
    requirements: {
      IS: [
        {
          requirement:
            'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
          type: false
        }
      ],
      CS: [
        {
          requirement:
            'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
          type: true
        }
      ]
    }
  }
];

const mockAllRequirements = {
  IS: [
    {
      requirement:
        'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core',
      type: false
    }
  ],
  CS: [
    {
      requirement:
        'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement',
      type: true
    }
  ]
};

describe('CourseTable', () => {
  const defaultProps = {
    courses: mockCourses,
    allRequirements: mockAllRequirements,
    selectedFilters: {
      IS: [
        'BS in Information Systems---Concentration---Information Security and Privacy---Regulatory and Behavioral Core'
      ],
      CS: [
        'GenEd---Science and Engineering---Science and Engineering (CB)---Lab Requirement'
      ]
    },
    handleFilterChange: jest.fn(),
    clearFilters: jest.fn(),
    offeredOptions: ['F23', 'S24'],
    selectedOfferedSemesters: [],
    setSelectedOfferedSemesters: jest.fn(),
    coreOnly: null,
    genedOnly: null,
    allowRemove: true,
    handleRemoveCourse: jest.fn(),
    noPrereqs: null,
    setNoPrereqs: jest.fn(),
    compactViewMode: null,
    hideDropdowns: true,
    isPlanTab: false
  };

  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockCourses[0])
      })
    );
  });

  afterAll(() => {
    global.fetch.mockRestore();
  });

  test('renders course code and name', () => {
    render(<CourseTable {...defaultProps} />);
    expect(screen.getByText(/76-101/)).toBeInTheDocument();
    expect(screen.getByText(/Interpretation & Argument/)).toBeInTheDocument();
  });

  test('clicking course code opens course popup with fetch', async () => {
    render(<CourseTable {...defaultProps} />);
    fireEvent.click(screen.getByText(/76-101/));
    await waitFor(() => {
      expect(screen.getByText(/Course Details/)).toBeInTheDocument();
    });
  });

  test('clicking requirement cell opens requirement popup', async () => {
    render(<CourseTable {...defaultProps} />);
    const reqCell = screen.getByText(/regulatory and behavioral core/i);
    fireEvent.click(reqCell);
    await waitFor(() => {
      expect(screen.getByText(/Requirement Details/)).toBeInTheDocument();
    });
  });

  test('renders formatted prereq preview and expands on click', () => {
    render(<CourseTable {...defaultProps} />);
    const expandBtn = screen.getByText(/show more/i);
    expect(expandBtn).toBeInTheDocument();
    fireEvent.click(expandBtn);
    expect(screen.getByText(/76-100/)).toBeInTheDocument();
  });

  test('calls handleRemoveCourse on ✖ click', () => {
    render(<CourseTable {...defaultProps} />);
    const removeBtn = screen.getByRole('button', { name: /✖/i });
    fireEvent.click(removeBtn);
    expect(defaultProps.handleRemoveCourse).toHaveBeenCalledWith('76-101');
  });

  test('renders no courses message when table is empty', () => {
    render(<CourseTable {...defaultProps} courses={[]} />);
    expect(screen.getByText(/No courses found/i)).toBeInTheDocument();
  });

  test('formats requirement path using compactViewMode=last1', () => {
    render(<CourseTable {...defaultProps} compactViewMode="last1" />);
    expect(screen.getByText(/regulatory and behavioral core/i)).toBeInTheDocument();
    expect(screen.getByText(/lab requirement/i)).toBeInTheDocument();
  });
});
