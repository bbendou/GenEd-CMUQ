/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import AnalyticsPage from '../components/Analytics';
import '@testing-library/jest-dom';

jest.mock('../components/CategoryCoverage', () => () => (
  <div data-testid="category-coverage">Category Coverage Component</div>
));

jest.mock('../components/EnrollmentAnalytics', () => () => (
  <div data-testid="enrollment-analytics">Enrollment Analytics Component</div>
));

describe('AnalyticsPage', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('renders the page title and subtitle', () => {
    render(<AnalyticsPage />);
    expect(screen.getByText('Analyze Courses')).toBeInTheDocument();
    expect(screen.getByText(/Visualize requirement coverage/i)).toBeInTheDocument();
  });

  it('saves selectedMajor to localStorage', () => {
    render(<AnalyticsPage />);
    expect(localStorage.getItem('analyticsMajor')).toBe('bio');
  });

  it('renders CategoryCoverage and EnrollmentAnalytics components', () => {
    render(<AnalyticsPage />);
    expect(screen.getByTestId('category-coverage')).toBeInTheDocument();
    expect(screen.getByTestId('enrollment-analytics')).toBeInTheDocument();
  });
});
