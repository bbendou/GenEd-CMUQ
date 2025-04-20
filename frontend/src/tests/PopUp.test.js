/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Popup from '../components/PopUp.js';

const mockCourse = {
  course_code: '76-101',
  course_name: 'Interpretation and Argument',
  units: 9,
  description: 'Introductory writing course.',
  prerequisites: 'None',
  offered: ['F22', 'S23', 'F23'],
  requirements: {
    IS: [
      { requirement: 'IS---core---interpretation', type: false },
      { requirement: 'IS---gened---communication---writing', type: true }
    ]
  }
};

const mockRequirement = {
  requirement: ['IS---gened---communication---writing'],
  courses: [
    {
      course_code: '76-101',
      course_name: 'Interpretation and Argument',
      requirements: {
        IS: [{ requirement: 'IS---gened---communication---writing', type: true }]
      }
    },
    {
      course_code: '76-150',
      course_name: 'Science Writing',
      requirements: {
        IS: [{ requirement: 'IS---gened---communication---writing', type: true }]
      }
    }
  ]
};

describe('Popup component', () => {
  const mockOnClose = jest.fn();
  const mockOpenPopup = jest.fn();

  test('renders course details when type is "course"', () => {
    render(
      <Popup
        isOpen={true}
        onClose={mockOnClose}
        type="course"
        content={mockCourse}
        openPopup={mockOpenPopup}
      />
    );

    expect(screen.getByText(/Course Code:/)).toBeInTheDocument();
    expect(screen.getByText(/76-101/)).toBeInTheDocument();
    expect(screen.getByText(/Interpretation and Argument/)).toBeInTheDocument();
    expect(screen.getByText(/Semesters Offered:/)).toBeInTheDocument();
    expect(screen.getByText(/IS/)).toBeInTheDocument();
  });

  test('renders requirement details when type is "requirement"', () => {
    render(
      <Popup
        isOpen={true}
        onClose={mockOnClose}
        type="requirement"
        content={mockRequirement}
        openPopup={mockOpenPopup}
      />
    );

    expect(screen.getByText(/Requirement Details/)).toBeInTheDocument();
    expect(screen.getByText(/communication → writing/)).toBeInTheDocument();
    expect(screen.getByText(/Courses Fulfilling This Requirement/)).toBeInTheDocument();
    expect(screen.getByText(/76-101 - Interpretation and Argument/)).toBeInTheDocument();
    expect(screen.getByText(/76-150 - Science Writing/)).toBeInTheDocument();
  });

  test('calls onClose when the ✖ button is clicked', () => {
    render(
      <Popup
        isOpen={true}
        onClose={mockOnClose}
        type="course"
        content={mockCourse}
        openPopup={mockOpenPopup}
      />
    );

    const closeButton = screen.getByText(/✖/);
    fireEvent.click(closeButton);
    expect(mockOnClose).toHaveBeenCalled();
  });

  test('returns null when isOpen is false', () => {
    render(
      <Popup
        isOpen={false}
        onClose={mockOnClose}
        type="course"
        content={mockCourse}
        openPopup={mockOpenPopup}
      />
    );
    expect(screen.queryByText(/Course Code:/)).not.toBeInTheDocument();
  });

  test('calls openPopup when clicking course link inside requirement popup', () => {
    render(
      <Popup
        isOpen={true}
        onClose={mockOnClose}
        type="requirement"
        content={mockRequirement}
        openPopup={mockOpenPopup}
      />
    );
  
    const courseLink = screen.getByText(/76-101 - Interpretation and Argument/);
    fireEvent.click(courseLink);
  
    expect(mockOpenPopup).toHaveBeenCalledWith(
      'course',
      expect.objectContaining({
        course_code: '76-101',
        course_name: 'Interpretation and Argument'
      })
    );
  });

});
