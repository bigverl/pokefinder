import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CoverageAnalyzerResults } from './CoverageAnalyzerResults';
import type { CoverageAnalyzerResponse } from '../../api/types';

const mockData: CoverageAnalyzerResponse = {
  team_strengths_table: {
    rows: [{ effectiveness: '2x', enemy_type: 'grass', friendly_type: 'fire' }],
  },
  team_weaknesses_table: {
    rows: [{ effectiveness: '2x', enemy_type: 'water', friendly_type: 'fire' }],
  },
};

describe('CoverageAnalyzerResults', () => {
  it('renders strengths tab with columns', () => {
    render(<CoverageAnalyzerResults data={mockData} />);
    expect(screen.getByText('effectiveness')).toBeInTheDocument();
    expect(screen.getByText('enemy type')).toBeInTheDocument();
    expect(screen.getByText('your type')).toBeInTheDocument();
  });

  it('renders strengths data', () => {
    render(<CoverageAnalyzerResults data={mockData} />);
    expect(screen.getByText('grass')).toBeInTheDocument();
    expect(screen.getByText('2x')).toBeInTheDocument();
  });

  it('renders with null data without crashing', () => {
    render(<CoverageAnalyzerResults data={null} />);
    expect(screen.getByText('effectiveness')).toBeInTheDocument();
  });
});
