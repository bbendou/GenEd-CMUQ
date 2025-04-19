/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import MainTabs from '../components/MainTabs';
import '@testing-library/jest-dom';

jest.mock('../components/CourseTablePage', () => () => <div data-testid="general-tab">Course Table Page</div>);
jest.mock('../components/PlanCourseTab', () => () => <div data-testid="plan-tab">Plan Course Tab</div>);
jest.mock('../components/Analytics', () => () => <div data-testid="analytics-tab">Analytics Page</div>);

describe('MainTabs', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('renders the general tab by default', () => {
    render(<MainTabs />);
    expect(screen.getByText('View')).toHaveClass('tab active');
    expect(screen.getByTestId('general-tab')).toBeInTheDocument();
  });

  test('switches to Plan tab on click', () => {
    render(<MainTabs />);
    const planButton = screen.getByText('Plan');
    fireEvent.click(planButton);

    expect(planButton).toHaveClass('tab active');
    expect(screen.getByTestId('plan-tab')).toBeInTheDocument();
  });

  test('switches to Analytics tab on click', () => {
    render(<MainTabs />);
    const analyticsButton = screen.getByText('Analytics');
    fireEvent.click(analyticsButton);

    expect(analyticsButton).toHaveClass('tab active');
    expect(screen.getByTestId('analytics-tab')).toBeInTheDocument();
  });

  test('remembers last selected tab using localStorage', async () => {
    localStorage.setItem('activeTab', 'plan');
    render(<MainTabs />);

    await waitFor(() => {
      expect(screen.getByTestId('plan-tab')).toBeInTheDocument();
    });
    expect(screen.getByText('Plan')).toHaveClass('tab active');
  });
});
